#!/bin/bash

# AWS Chalice Deployment Script for AlphaVantage MCP Server
# Usage: ./deploy.sh [dev|prod] [--setup]

set -e

STAGE=${1:-dev}
SETUP_FLAG=${2}

echo "🚀 AlphaVantage MCP Server - AWS Chalice Deployment"
echo "=================================================="

# Validate stage
if [[ "$STAGE" != "dev" && "$STAGE" != "prod" ]]; then
    echo "❌ Error: Stage must be 'dev' or 'prod'"
    echo "Usage: ./deploy.sh [dev|prod] [--setup]"
    exit 1
fi

echo "📋 Deploying to stage: $STAGE"

# Setup mode - copy source files to vendor directory and install dependencies
if [[ "$SETUP_FLAG" == "--setup" ]]; then
    echo "🔧 Setting up deployment environment..."
    
    # Create vendor directory and copy source files from main project
    if [[ -d "../../src/alphavantage_mcp_server" ]]; then
        echo "📂 Setting up vendor directory with source files..."
        mkdir -p vendor
        cp -r ../../src/alphavantage_mcp_server vendor/
        echo "✅ Source files copied to vendor/ directory"
        
        # Ensure dependencies are properly installed for Chalice's automatic layer
        echo "📦 Installing dependencies for Chalice automatic layer..."
        # Chalice will automatically detect and package dependencies from requirements.txt
        echo "✅ Dependencies configured for automatic layer"
    else
        echo "❌ Error: Source directory not found. Run from deploy/aws-chalice/"
        exit 1
    fi
    
    # Install Chalice if not already installed
    if ! command -v chalice &> /dev/null; then
        echo "📦 Installing Chalice..."
        pip install chalice
        echo "✅ Chalice installed"
    fi
    
    # Install dependencies locally so Chalice can validate imports
    echo "📦 Installing dependencies locally for Chalice validation..."
    pip install -r requirements.txt
    echo "✅ Dependencies installed locally"
fi

# Validate required files
if [[ ! -f "app.py" ]]; then
    echo "❌ Error: app.py not found. Run with --setup flag first."
    exit 1
fi

if [[ ! -d "vendor/alphavantage_mcp_server" ]]; then
    echo "❌ Error: vendor/alphavantage_mcp_server directory not found. Run with --setup flag first."
    exit 1
fi

# Check for required environment variables
echo "🔍 Checking configuration..."

CONFIG_FILE=".chalice/config.json"
if [[ ! -f "$CONFIG_FILE" ]]; then
    echo "❌ Error: Configuration file not found: $CONFIG_FILE"
    exit 1
fi

# Extract API key from config to check if it's set
API_KEY=$(python3 -c "
import json
with open('$CONFIG_FILE') as f:
    config = json.load(f)
    print(config['stages']['$STAGE']['environment_variables'].get('ALPHAVANTAGE_API_KEY', ''))
")

if [[ -z "$API_KEY" ]]; then
    echo "⚠️  Warning: ALPHAVANTAGE_API_KEY not set in configuration"
    echo "   Please update .chalice/config.json before deployment"
fi

# Deploy
echo "🚀 Deploying to AWS..."
chalice deploy --stage "$STAGE"

if [[ $? -eq 0 ]]; then
    echo ""
    echo "✅ Deployment successful!"
    echo ""
    echo "📊 Getting deployment info..."
    chalice url --stage "$STAGE" 2>/dev/null || echo "Run 'chalice url --stage $STAGE' to get the API URL"
    
    echo ""
    echo "🔗 Quick test commands:"
    echo "Health check:"
    echo "  curl \$(chalice url --stage $STAGE)"
    echo ""
    echo "MCP request example:"
    echo "  curl -X POST \$(chalice url --stage $STAGE)/mcp \\"
    echo "    -H 'Content-Type: application/json' \\"
    echo "    -d '{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"tools/list\"}'"
    echo ""
    echo "📝 View logs:"
    echo "  chalice logs --stage $STAGE"
    echo ""
    echo "🗑️  To delete deployment:"
    echo "  chalice delete --stage $STAGE"
else
    echo "❌ Deployment failed!"
    exit 1
fi
