# AWS Stateless MCP Lambda Deployment

This deployment uses the **stateless MCP pattern** from [aws-samples/sample-serverless-mcp-servers](https://github.com/aws-samples/sample-serverless-mcp-servers/tree/main/stateless-mcp-on-lambda-python) to deploy the AlphaVantage MCP Server on AWS Lambda.

## 🎯 Why Stateless MCP?

Unlike our previous attempts with Chalice and Lambda Web Adapter, this approach is specifically designed for **stateless MCP servers** that work perfectly with Lambda's execution model:

- ✅ **No session state management** - Each request is independent
- ✅ **Perfect for Lambda** - Stateless execution model matches Lambda
- ✅ **Horizontal scaling** - Seamless elasticity and load distribution
- ✅ **AWS-recommended pattern** - Based on official AWS samples

## 🏗️ Architecture

```
Internet → API Gateway → Lambda Function → AlphaVantage MCP Server → AlphaVantage API
```

Each Lambda invocation:
1. Receives MCP JSON-RPC request via API Gateway
2. Calls appropriate AlphaVantage MCP server function directly
3. Returns MCP-compliant JSON response
4. No persistent connections or session state required

## 🚀 Quick Start

### Prerequisites

```bash
# Install AWS CLI
pip install awscli

# Install AWS SAM CLI
pip install aws-sam-cli

# Configure AWS credentials
aws configure
```

### Deploy

```bash
# Set your AlphaVantage API key
export ALPHAVANTAGE_API_KEY=your_api_key_here

# Optional: Enable OAuth 2.1
export OAUTH_ENABLED=true
export OAUTH_AUTHORIZATION_SERVER_URL=https://your-oauth-server.com

# Deploy
cd deploy/aws-stateless-mcp-lambda
chmod +x deploy.sh
./deploy.sh
```

## 🧪 Testing

After deployment, test with these commands:

### 1. Initialize MCP Session
```bash
curl -X POST 'https://your-api-id.execute-api.region.amazonaws.com/prod/mcp' \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json' \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
      "protocolVersion": "2024-11-05",
      "capabilities": {},
      "clientInfo": {"name": "test-client", "version": "1.0.0"}
    }
  }'
```

### 2. List Available Tools
```bash
curl -X POST 'https://your-api-id.execute-api.region.amazonaws.com/prod/mcp' \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json' \
  -d '{
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/list"
  }'
```

### 3. Call a Tool
```bash
curl -X POST 'https://your-api-id.execute-api.region.amazonaws.com/prod/mcp' \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json' \
  -d '{
    "jsonrpc": "2.0",
    "id": 3,
    "method": "tools/call",
    "params": {
      "name": "stock_quote",
      "arguments": {"symbol": "AAPL"}
    }
  }'
```

## 🔐 OAuth 2.1 Support

Enable OAuth authentication by setting environment variables:

```bash
export OAUTH_ENABLED=true
export OAUTH_AUTHORIZATION_SERVER_URL=https://your-oauth-server.com
export OAUTH_CLIENT_ID=your_client_id
export OAUTH_CLIENT_SECRET=your_client_secret
```

When OAuth is enabled, include Bearer token in requests:

```bash
curl -X POST 'https://your-api-id.execute-api.region.amazonaws.com/prod/mcp' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer your_access_token' \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/list"}'
```

## 📊 Available Tools

The AlphaVantage MCP Server provides 50+ financial data tools:

### Stock Data
- `get_stock_quote` - Real-time stock quotes
- `get_intraday_data` - Intraday time series
- `get_daily_data` - Daily time series
- `get_weekly_data` - Weekly time series
- `get_monthly_data` - Monthly time series

### Technical Indicators
- `get_sma` - Simple Moving Average
- `get_ema` - Exponential Moving Average
- `get_rsi` - Relative Strength Index
- `get_macd` - MACD indicator
- And 30+ more technical indicators

### Fundamental Data
- `get_company_overview` - Company fundamentals
- `get_income_statement` - Income statements
- `get_balance_sheet` - Balance sheets
- `get_cash_flow` - Cash flow statements

### Economic Data
- `get_gdp` - GDP data
- `get_inflation` - Inflation rates
- `get_unemployment` - Unemployment rates
- And more economic indicators

## 🔍 Monitoring

### CloudWatch Logs
```bash
# Follow Lambda logs
aws logs tail /aws/lambda/alphavantage-stateless-mcp-alphavantage-mcp --follow

# Get function metrics
aws lambda get-function --function-name alphavantage-stateless-mcp-alphavantage-mcp
```

### API Gateway Metrics
- Monitor request count, latency, and errors in CloudWatch
- Set up alarms for high error rates or latency

## 🛠️ Troubleshooting

### Common Issues

**1. Import Errors**
```
ModuleNotFoundError: No module named 'alphavantage_mcp_server'
```
- **Solution**: Ensure the Lambda layer is properly built with source code

**2. API Key Errors**
```
{"error": "API key required"}
```
- **Solution**: Verify `ALPHAVANTAGE_API_KEY` environment variable is set

**3. Tool Not Found**
```
{"error": {"code": -32601, "message": "Method not found"}}
```
- **Solution**: Check tool name spelling and availability with `tools/list`

### Debug Mode

Enable debug logging by setting environment variable:
```bash
export DEBUG=true
```

## 💰 Cost Estimation

### Lambda Costs
- **Requests**: $0.20 per 1M requests
- **Duration**: $0.0000166667 per GB-second
- **Example**: 10,000 requests/month ≈ $2-5/month

### API Gateway Costs
- **REST API**: $3.50 per million API calls
- **Data transfer**: $0.09 per GB

### Total Estimated Cost
- **Light usage** (1K requests/month): ~$1/month
- **Moderate usage** (10K requests/month): ~$5/month
- **Heavy usage** (100K requests/month): ~$40/month

## 🧹 Cleanup

Remove all AWS resources:

```bash
aws cloudformation delete-stack --stack-name alphavantage-stateless-mcp
```


## 📚 References

- [AWS Sample Serverless MCP Servers](https://github.com/aws-samples/sample-serverless-mcp-servers)
- [MCP Specification](https://modelcontextprotocol.io/specification/2025-03-26/basic/transports)
- [AlphaVantage API Documentation](https://www.alphavantage.co/documentation/)
- [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/)

## 🤝 Contributing

This deployment is based on the official AWS sample pattern. For improvements:

1. Test changes locally with SAM
2. Update the Lambda function code
3. Redeploy with `./deploy.sh`
4. Verify with test commands

## 📄 License

This deployment follows the same MIT-0 license as the AWS sample repository.
