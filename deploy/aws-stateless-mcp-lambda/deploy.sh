#!/bin/bash

# AWS Stateless MCP Lambda Deployment Script
# Based on aws-samples/sample-serverless-mcp-servers pattern

set -e

echo "🚀 AlphaVantage Stateless MCP Server Deployment"
echo "=============================================="

# Check prerequisites
echo "📋 Checking prerequisites..."

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI is not installed. Please install it first."
    exit 1
fi

# Check if SAM CLI is installed
if ! command -v sam &> /dev/null; then
    echo "❌ AWS SAM CLI is not installed. Please install it first."
    echo "   Install with: pip install aws-sam-cli"
    exit 1
fi

# Check AWS credentials
if ! aws sts get-caller-identity &> /dev/null; then
    echo "❌ AWS credentials not configured. Please run 'aws configure' first."
    exit 1
fi

# Check required environment variables
if [ -z "$ALPHAVANTAGE_API_KEY" ]; then
    echo "❌ ALPHAVANTAGE_API_KEY environment variable is required."
    echo "   Set it with: export ALPHAVANTAGE_API_KEY=your_api_key_here"
    exit 1
fi

echo "✅ Prerequisites check passed"

# Set deployment parameters
STACK_NAME="alphavantage-stateless-mcp"
OAUTH_ENABLED="${OAUTH_ENABLED:-false}"
OAUTH_AUTHORIZATION_SERVER_URL="${OAUTH_AUTHORIZATION_SERVER_URL:-}"

echo ""
echo "📦 Deployment Configuration:"
echo "   Stack Name: $STACK_NAME"
echo "   OAuth Enabled: $OAUTH_ENABLED"
echo "   OAuth Server URL: ${OAUTH_AUTHORIZATION_SERVER_URL:-'(not set)'}"
echo ""

# Confirm deployment
read -p "🤔 Do you want to proceed with deployment? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Deployment cancelled."
    exit 1
fi

# Build the SAM application
echo ""
echo "🔨 Building SAM application..."
sam build --use-container

if [ $? -ne 0 ]; then
    echo "❌ SAM build failed."
    exit 1
fi

echo "✅ Build completed successfully"

# Deploy the SAM application
echo ""
echo "🚀 Deploying to AWS..."

# Deploy with conditional parameter handling
if [ -n "$OAUTH_AUTHORIZATION_SERVER_URL" ]; then
    # Deploy with OAuth URL
    sam deploy \
        --stack-name "$STACK_NAME" \
        --capabilities CAPABILITY_IAM \
        --resolve-s3 \
        --parameter-overrides \
            "AlphaVantageApiKey=$ALPHAVANTAGE_API_KEY" \
            "OAuthEnabled=$OAUTH_ENABLED" \
            "OAuthAuthorizationServerUrl=$OAUTH_AUTHORIZATION_SERVER_URL" \
        --no-confirm-changeset \
        --no-fail-on-empty-changeset
else
    # Deploy without OAuth URL (use default empty value)
    sam deploy \
        --stack-name "$STACK_NAME" \
        --capabilities CAPABILITY_IAM \
        --resolve-s3 \
        --parameter-overrides \
            "AlphaVantageApiKey=$ALPHAVANTAGE_API_KEY" \
            "OAuthEnabled=$OAUTH_ENABLED" \
        --no-confirm-changeset \
        --no-fail-on-empty-changeset
fi

if [ $? -ne 0 ]; then
    echo "❌ Deployment failed."
    exit 1
fi

echo "✅ Deployment completed successfully!"

# Get the API endpoint
echo ""
echo "📡 Getting deployment information..."
API_URL=$(aws cloudformation describe-stacks \
    --stack-name "$STACK_NAME" \
    --query 'Stacks[0].Outputs[?OutputKey==`McpApiUrl`].OutputValue' \
    --output text)

FUNCTION_NAME=$(aws cloudformation describe-stacks \
    --stack-name "$STACK_NAME" \
    --query 'Stacks[0].Outputs[?OutputKey==`FunctionName`].OutputValue' \
    --output text)

echo ""
echo "🎉 Deployment Summary:"
echo "======================"
echo "   API Endpoint: $API_URL"
echo "   Function Name: $FUNCTION_NAME"
echo "   Stack Name: $STACK_NAME"
echo ""

# Test the deployment
echo "🧪 Testing the deployment..."
echo ""

echo "1️⃣ Testing MCP Initialize..."
INIT_RESPONSE=$(curl -s -X POST "$API_URL" \
    -H 'Content-Type: application/json' \
    -H 'Accept: application/json' \
    -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test-client","version":"1.0.0"}}}')

if echo "$INIT_RESPONSE" | grep -q '"result"'; then
    echo "✅ Initialize test passed"
else
    echo "❌ Initialize test failed"
    echo "Response: $INIT_RESPONSE"
fi

echo ""
echo "2️⃣ Testing Tools List..."
TOOLS_RESPONSE=$(curl -s -X POST "$API_URL" \
    -H 'Content-Type: application/json' \
    -H 'Accept: application/json' \
    -d '{"jsonrpc":"2.0","id":2,"method":"tools/list"}')

if echo "$TOOLS_RESPONSE" | grep -q '"tools"'; then
    TOOL_COUNT=$(echo "$TOOLS_RESPONSE" | grep -o '"name"' | wc -l)
    echo "✅ Tools list test passed - Found $TOOL_COUNT tools"
else
    echo "❌ Tools list test failed"
    echo "Response: $TOOLS_RESPONSE"
fi

echo ""
echo "🎯 Manual Test Commands:"
echo "========================"
echo ""
echo "# Initialize MCP session:"
echo "curl -X POST '$API_URL' \\"
echo "  -H 'Content-Type: application/json' \\"
echo "  -H 'Accept: application/json' \\"
echo "  -d '{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"initialize\",\"params\":{\"protocolVersion\":\"2024-11-05\",\"capabilities\":{},\"clientInfo\":{\"name\":\"test-client\",\"version\":\"1.0.0\"}}}'"
echo ""
echo "# List available tools:"
echo "curl -X POST '$API_URL' \\"
echo "  -H 'Content-Type: application/json' \\"
echo "  -H 'Accept: application/json' \\"
echo "  -d '{\"jsonrpc\":\"2.0\",\"id\":2,\"method\":\"tools/list\"}'"
echo ""
echo "# Call a tool (get stock quote for AAPL):"
echo "curl -X POST '$API_URL' \\"
echo "  -H 'Content-Type: application/json' \\"
echo "  -H 'Accept: application/json' \\"
echo "  -d '{\"jsonrpc\":\"2.0\",\"id\":3,\"method\":\"tools/call\",\"params\":{\"name\":\"get_stock_quote\",\"arguments\":{\"symbol\":\"AAPL\"}}}'"
echo ""

echo "📊 Monitoring:"
echo "=============="
echo "   CloudWatch Logs: aws logs tail /aws/lambda/$FUNCTION_NAME --follow"
echo "   Function Metrics: aws lambda get-function --function-name $FUNCTION_NAME"
echo ""

echo "🧹 Cleanup (when done testing):"
echo "================================"
echo "   aws cloudformation delete-stack --stack-name $STACK_NAME"
echo ""

echo "✅ Stateless MCP deployment completed successfully!"
echo "   Your AlphaVantage MCP server is now running serverlessly on AWS Lambda!"
