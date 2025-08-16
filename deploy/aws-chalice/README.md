# AWS Chalice Deployment for AlphaVantage MCP Server

This directory contains an **automated AWS Chalice deployment** for the AlphaVantage MCP Server, providing serverless deployment to AWS Lambda with API Gateway integration.

## Overview

The Chalice deployment wraps the existing MCP HTTP server functionality without modifying the core server code. It provides:

- **🚀 Serverless deployment** on AWS Lambda
- **🌐 API Gateway integration** for HTTP endpoints  
- **🔐 OAuth 2.0/2.1 support** with AWS Cognito integration
- **🌍 CORS handling** for browser compatibility
- **⚙️ Environment-based configuration** (dev/prod stages)
- **📜 Automated setup scripts** for easy deployment

## Prerequisites

1. **AWS CLI** configured with appropriate permissions
2. **Python 3.12+** (matches the main project)
3. **AlphaVantage API key**
4. **jq** (for Cognito setup script)

## Quick Start

### 🚀 Option 1: Deploy without Authentication

```bash
# Navigate to deployment directory
cd deploy/aws-chalice

# Deploy to development (no OAuth)
./deploy.sh dev --setup
```

### 🔐 Option 2: Deploy with AWS Cognito Authentication

```bash
# Navigate to deployment directory
cd deploy/aws-chalice

# Setup AWS Cognito (one-time)
./setup-cognito.sh us-east-1 alphavantage-mcp-users

# Deploy to production (with OAuth)
./deploy.sh prod --setup
```

**That's it!** 🎉 The scripts handle everything automatically.

## Automated Scripts

### 📜 `deploy.sh` - Main Deployment Script

```bash
./deploy.sh [dev|prod] [--setup]
```

**Options:**
- `dev` or `prod` - Deployment stage (default: dev)
- `--setup` - First-time setup (copies source files to vendor/ directory, installs dependencies)

**Examples:**
```bash
./deploy.sh dev --setup     # First-time dev deployment
./deploy.sh prod            # Production deployment
./deploy.sh dev             # Update existing dev deployment
```

### 🔐 `setup-cognito.sh` - AWS Cognito Setup

```bash
./setup-cognito.sh [region] [pool-name]
```

**Parameters:**
- `region` - AWS region (default: us-east-1)
- `pool-name` - Cognito User Pool name (default: alphavantage-mcp-users)

**What it does:**
- ✅ Creates Cognito User Pool with security policies
- ✅ Sets up custom resource server with MCP scopes (`mcp-server/read`, `mcp-server/write`)
- ✅ Creates app client with OAuth 2.0 flows
- ✅ Configures domain for OAuth endpoints
- ✅ Optionally updates `.chalice/config.json` automatically

## Configuration

### Environment Variables

The scripts automatically handle configuration, but you can manually edit `.chalice/config.json`:

#### Required Variables
- `ALPHAVANTAGE_API_KEY`: Your AlphaVantage API key

#### OAuth Variables (for Cognito integration)
- `OAUTH_ENABLED`: Set to "true" to enable OAuth authentication
- `OAUTH_AUTHORIZATION_SERVER_URL`: Cognito discovery endpoint
- `OAUTH_CLIENT_ID`: Cognito app client ID
- `OAUTH_CLIENT_SECRET`: Cognito app client secret
- `OAUTH_REQUIRED_SCOPES`: Required scopes (e.g., "mcp-server/read mcp-server/write")

### Deployment Stages

- **dev**: Development stage with OAuth disabled by default
- **prod**: Production stage with OAuth enabled by default

## Manual Commands (if needed)

If you prefer manual deployment:

```bash
# Deploy to development
chalice deploy --stage dev

# Deploy to production  
chalice deploy --stage prod

# Update environment variables
chalice deploy --stage prod --env-var ALPHAVANTAGE_API_KEY=your-new-key
```

## API Endpoints

After deployment, your API will be available at the provided API Gateway URL:

### Health Check
- `GET /` - Returns service status and version

### MCP Endpoints
- `POST /mcp` - Main MCP endpoint for tool calls
- `GET /mcp/{proxy+}` - Handle MCP sub-paths

### OAuth Endpoints (if enabled)
- `GET /.well-known/oauth-protected-resource` - OAuth metadata endpoint

## Usage Examples

### Basic MCP Request

```bash
curl -X POST https://your-api-id.execute-api.region.amazonaws.com/api/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "stock_quote",
      "arguments": {
        "symbol": "AAPL"
      }
    }
  }'
```

### With OAuth Authentication

```bash
curl -X POST https://your-api-id.execute-api.region.amazonaws.com/v1/mcp \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-jwt-token" \
  -H "X-Session-ID: your-session-id" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "stock_quote",
      "arguments": {
        "symbol": "AAPL"
      }
    }
  }'
```

## Monitoring and Logs

### View Logs

```bash
chalice logs --stage prod
```

### Real-time Logs

```bash
chalice logs --stage prod --follow
```

### CloudWatch Integration

The deployment automatically integrates with AWS CloudWatch for:
- Lambda function metrics
- API Gateway metrics
- Custom application logs

## Cost Considerations

### Lambda Pricing
- **Free Tier**: 1M requests/month + 400,000 GB-seconds
- **Pay-per-use**: $0.20 per 1M requests + $0.0000166667 per GB-second

### API Gateway Pricing
- **Free Tier**: 1M API calls/month (first 12 months)
- **Pay-per-use**: $3.50 per million API calls

### Estimated Monthly Cost
For moderate usage (100K requests/month):
- Lambda: ~$1-2
- API Gateway: ~$0.35
- **Total**: ~$1.50-2.50/month

## Security Best Practices

1. **Environment Variables**: Store sensitive data in environment variables, not in code
2. **OAuth Authentication**: Enable OAuth for production deployments
3. **API Keys**: Rotate AlphaVantage API keys regularly
4. **CORS**: Configure CORS appropriately for your use case
5. **Monitoring**: Set up CloudWatch alarms for unusual activity

## Troubleshooting

### Common Issues

1. **Import Errors**:
   - Ensure all dependencies are in `requirements.txt`
   - Check Python version compatibility

2. **Permission Errors**:
   - Verify AWS CLI configuration
   - Ensure IAM user has necessary permissions

3. **Timeout Issues**:
   - Increase `lambda_timeout` in config.json
   - Consider using async patterns for long-running operations

4. **Memory Issues**:
   - Increase `lambda_memory_size` in config.json
   - Monitor CloudWatch metrics

### Debug Mode

Enable debug logging by setting environment variable:
```json
{
  "environment_variables": {
    "CHALICE_DEBUG": "true"
  }
}
```

## Cleanup

To remove the deployment:

```bash
chalice delete --stage dev
chalice delete --stage prod
```

## Limitations

1. **Cold Starts**: Lambda functions may experience cold start latency
2. **Execution Time**: Maximum 15-minute execution time per request
3. **Memory**: Maximum 10GB memory per function
4. **Payload Size**: 6MB request/response limit

## Support

For issues specific to the Chalice deployment:
1. Check the [Chalice documentation](https://chalice.readthedocs.io/)
2. Review AWS Lambda and API Gateway documentation
3. Check CloudWatch logs for detailed error information

For AlphaVantage MCP Server issues, refer to the main project documentation.
