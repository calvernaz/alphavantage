#!/bin/bash

# AWS Cognito Setup Script for AlphaVantage MCP Server
# Usage: ./setup-cognito.sh [region] [pool-name]

set -e

REGION=${1:-us-east-1}
POOL_NAME=${2:-alphavantage-mcp-users}

echo "🔐 AWS Cognito Setup for AlphaVantage MCP Server"
echo "=============================================="
echo "Region: $REGION"
echo "User Pool Name: $POOL_NAME"
echo ""

# Check if AWS CLI is configured
if ! aws sts get-caller-identity &>/dev/null; then
    echo "❌ Error: AWS CLI not configured. Please run 'aws configure' first."
    exit 1
fi

echo "📋 Step 1: Creating Cognito User Pool..."

# Create User Pool
USER_POOL_OUTPUT=$(aws cognito-idp create-user-pool \
    --pool-name "$POOL_NAME" \
    --region "$REGION" \
    --policies '{
        "PasswordPolicy": {
            "MinimumLength": 8,
            "RequireUppercase": true,
            "RequireLowercase": true,
            "RequireNumbers": true,
            "RequireSymbols": false
        }
    }' \
    --auto-verified-attributes email \
    --username-attributes email \
    --mfa-configuration OFF \
    --account-recovery-setting '{
        "RecoveryMechanisms": [
            {
                "Priority": 1,
                "Name": "verified_email"
            }
        ]
    }' \
    --output json)

USER_POOL_ID=$(echo "$USER_POOL_OUTPUT" | jq -r '.UserPool.Id')
echo "✅ User Pool created: $USER_POOL_ID"

echo ""
echo "📋 Step 2: Creating Resource Server for MCP scopes..."

# Create Resource Server for custom scopes
aws cognito-idp create-resource-server \
    --user-pool-id "$USER_POOL_ID" \
    --region "$REGION" \
    --identifier "mcp-server" \
    --name "AlphaVantage MCP Server" \
    --scopes '[
        {
            "ScopeName": "read",
            "ScopeDescription": "Read access to MCP tools and data"
        },
        {
            "ScopeName": "write", 
            "ScopeDescription": "Write access to MCP tools and operations"
        }
    ]' \
    --output json > /dev/null

echo "✅ Resource server created with custom scopes"

echo ""
echo "📋 Step 3: Creating App Client..."

# Create App Client
CLIENT_OUTPUT=$(aws cognito-idp create-user-pool-client \
    --user-pool-id "$USER_POOL_ID" \
    --region "$REGION" \
    --client-name "alphavantage-mcp-client" \
    --generate-secret \
    --explicit-auth-flows "ADMIN_NO_SRP_AUTH" "ALLOW_USER_SRP_AUTH" "ALLOW_REFRESH_TOKEN_AUTH" \
    --supported-identity-providers "COGNITO" \
    --allowed-o-auth-flows "client_credentials" "authorization_code" \
    --allowed-o-auth-scopes "mcp-server/read" "mcp-server/write" \
    --allowed-o-auth-flows-user-pool-client \
    --token-validity-units '{
        "AccessToken": "hours",
        "IdToken": "hours", 
        "RefreshToken": "days"
    }' \
    --access-token-validity 1 \
    --id-token-validity 1 \
    --refresh-token-validity 30 \
    --output json)

CLIENT_ID=$(echo "$CLIENT_OUTPUT" | jq -r '.UserPoolClient.ClientId')
CLIENT_SECRET=$(echo "$CLIENT_OUTPUT" | jq -r '.UserPoolClient.ClientSecret')

echo "✅ App Client created: $CLIENT_ID"

echo ""
echo "📋 Step 4: Creating User Pool Domain..."

# Create a domain for the User Pool (needed for OAuth endpoints)
DOMAIN_NAME="alphavantage-mcp-$(date +%s)"
aws cognito-idp create-user-pool-domain \
    --user-pool-id "$USER_POOL_ID" \
    --region "$REGION" \
    --domain "$DOMAIN_NAME" \
    --output json > /dev/null

echo "✅ User Pool domain created: $DOMAIN_NAME"

echo ""
echo "📋 Step 5: Configuring Google OAuth provider..."

# Add Google OAuth provider configuration
echo "Do you want to configure Google OAuth provider? (y/n)"
read -r CONFIGURE_GOOGLE

if [[ "$CONFIGURE_GOOGLE" =~ ^[Yy]$ ]]; then
  echo ""
  echo "🔧 Google OAuth Configuration Required:"
  echo "1. Go to https://console.cloud.google.com/apis/credentials"
  echo "2. Create OAuth 2.0 Client ID (Web application)"
  echo "3. Add this redirect URI:"
  echo "   https://$DOMAIN_NAME.auth.$REGION.amazoncognito.com/oauth2/idpresponse"
  echo ""
  
  read -p "Enter Google OAuth Client ID: " GOOGLE_CLIENT_ID
  read -p "Enter Google OAuth Client Secret: " GOOGLE_CLIENT_SECRET
  
  if [[ -n "$GOOGLE_CLIENT_ID" && -n "$GOOGLE_CLIENT_SECRET" ]]; then
    echo "Adding Google as identity provider..."
    
    aws cognito-idp create-identity-provider \
      --user-pool-id "$USER_POOL_ID" \
      --provider-name "Google" \
      --provider-type "Google" \
      --provider-details '{
        "client_id": "'"$GOOGLE_CLIENT_ID"'",
        "client_secret": "'"$GOOGLE_CLIENT_SECRET"'",
        "authorize_scopes": "email openid profile"
      }' \
      --attribute-mapping '{
        "email": "email",
        "name": "name",
        "username": "sub"
      }' \
      --region "$REGION"
    
    echo "✅ Google OAuth provider configured"
    
    # Update app client to support Google
    aws cognito-idp update-user-pool-client \
      --user-pool-id "$USER_POOL_ID" \
      --client-id "$CLIENT_ID" \
      --supported-identity-providers "COGNITO" "Google" \
      --region "$REGION"
    
    echo "✅ App client updated to support Google OAuth"
    GOOGLE_CONFIGURED="true"
  else
    echo "⚠️  Skipping Google OAuth configuration (missing credentials)"
    GOOGLE_CONFIGURED="false"
  fi
else
  GOOGLE_CONFIGURED="false"
fi

echo ""
echo "🎉 Cognito setup complete!"
echo ""
echo "📝 Configuration Details:"
echo "========================"
echo "User Pool ID: $USER_POOL_ID"
echo "Client ID: $CLIENT_ID"
echo "Client Secret: $CLIENT_SECRET"
echo "Region: $REGION"
echo "Domain: $DOMAIN_NAME.auth.$REGION.amazoncognito.com"
echo "Authorization Server URL: https://cognito-idp.$REGION.amazonaws.com/$USER_POOL_ID"
echo ""

echo "🔧 Next Steps:"
echo "=============="
echo "1. Update your .chalice/config.json with these values:"
echo ""
echo "   \"AWS_COGNITO_USER_POOL_ID\": \"$USER_POOL_ID\","
echo "   \"AWS_COGNITO_CLIENT_ID\": \"$CLIENT_ID\","
echo "   \"AWS_COGNITO_REGION\": \"$REGION\","
echo "   \"OAUTH_AUTHORIZATION_SERVER_URL\": \"https://cognito-idp.$REGION.amazonaws.com/$USER_POOL_ID\","
echo "   \"OAUTH_CLIENT_ID\": \"$CLIENT_ID\","
echo "   \"OAUTH_CLIENT_SECRET\": \"$CLIENT_SECRET\""
echo ""
echo "2. Deploy your Chalice application:"
echo "   ./deploy.sh prod"
echo ""
echo "3. Test OAuth token endpoint:"
echo "   curl -X POST https://$DOMAIN_NAME.auth.$REGION.amazoncognito.com/oauth2/token \\"
echo "     -H 'Content-Type: application/x-www-form-urlencoded' \\"
echo "     -d 'grant_type=client_credentials&client_id=$CLIENT_ID&client_secret=$CLIENT_SECRET&scope=mcp-server/read mcp-server/write'"
echo ""
if [[ "$GOOGLE_CONFIGURED" == "true" ]]; then
echo "4. Test Google OAuth login:"
echo "   https://$DOMAIN_NAME.auth.$REGION.amazoncognito.com/oauth2/authorize?client_id=$CLIENT_ID&response_type=code&scope=mcp-server/read+mcp-server/write&redirect_uri=https://example.com/callback"
echo ""
echo "5. No user creation needed - users authenticate with Google accounts!"
else
echo "4. Create test users (optional):"
echo "   aws cognito-idp admin-create-user --user-pool-id $USER_POOL_ID --username testuser --temporary-password TempPass123! --message-action SUPPRESS"
fi
echo ""

# Optionally update the config file automatically
read -p "🤖 Would you like to automatically update .chalice/config.json? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "📝 Updating configuration file..."
    
    # Create a temporary file with updated config
    jq --arg user_pool_id "$USER_POOL_ID" \
       --arg client_id "$CLIENT_ID" \
       --arg client_secret "$CLIENT_SECRET" \
       --arg region "$REGION" \
       --arg auth_server_url "https://cognito-idp.$REGION.amazonaws.com/$USER_POOL_ID" \
       '.stages.prod.environment_variables.AWS_COGNITO_USER_POOL_ID = $user_pool_id |
        .stages.prod.environment_variables.AWS_COGNITO_CLIENT_ID = $client_id |
        .stages.prod.environment_variables.AWS_COGNITO_REGION = $region |
        .stages.prod.environment_variables.OAUTH_AUTHORIZATION_SERVER_URL = $auth_server_url |
        .stages.prod.environment_variables.OAUTH_CLIENT_ID = $client_id |
        .stages.prod.environment_variables.OAUTH_CLIENT_SECRET = $client_secret' \
       .chalice/config.json > .chalice/config.json.tmp
    
    mv .chalice/config.json.tmp .chalice/config.json
    echo "✅ Configuration updated!"
    echo ""
    echo "🚀 Ready to deploy! Run: ./deploy.sh prod"
else
    echo "⏭️  Skipping automatic configuration update."
    echo "   Please manually update .chalice/config.json with the values above."
fi

echo ""
echo "🗑️  To cleanup these resources later:"
echo "   aws cognito-idp delete-user-pool --user-pool-id $USER_POOL_ID --region $REGION"
