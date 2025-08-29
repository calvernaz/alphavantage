"""
OAuth 2.1 implementation for AlphaVantage MCP Server.

This module provides OAuth 2.1 resource server functionality as required by the
Model Context Protocol specification (2025-06-18). It supports configuration-driven
OAuth that works with any compliant OAuth 2.1 authorization server.

Key features:
- OAuth 2.0 Protected Resource Metadata (RFC 9728)
- Access token validation (JWT and introspection)
- WWW-Authenticate header handling
- Configuration-driven authorization server discovery
- MCP Security Best Practices compliance

Security Features:
- Token audience validation (prevents token passthrough attacks)
- Secure session ID generation and binding
- User-specific session binding to prevent session hijacking
- Proper error handling with OAuth-compliant responses
"""

import logging
import secrets
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Union
from urllib.parse import urljoin

import httpx
import jwt
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

logger = logging.getLogger(__name__)


@dataclass
class OAuthConfig:
    """Configuration for OAuth 2.1 resource server functionality."""

    # Authorization server configuration
    authorization_server_url: str
    """URL of the OAuth 2.1 authorization server (e.g., https://auth.example.com)"""

    # Resource server identity
    resource_server_uri: str
    """Canonical URI of this MCP server (e.g., https://mcp.example.com)"""

    # Token validation settings
    token_validation_method: str = "jwt"
    """Method for token validation: 'jwt' or 'introspection'"""

    jwt_public_key: Optional[str] = None
    """Public key for JWT validation (PEM format)"""

    jwt_algorithm: str = "RS256"
    """JWT signing algorithm"""

    introspection_endpoint: Optional[str] = None
    """Token introspection endpoint URL (RFC 7662)"""

    introspection_client_id: Optional[str] = None
    """Client ID for introspection requests"""

    introspection_client_secret: Optional[str] = None
    """Client secret for introspection requests"""

    # Metadata configuration
    resource_metadata_path: str = "/.well-known/oauth-protected-resource"
    """Path for OAuth 2.0 Protected Resource Metadata endpoint"""

    # Optional scopes
    required_scopes: List[str] = None
    """List of required scopes for accessing this resource"""

    # Security settings
    session_binding_enabled: bool = True
    """Enable user-specific session binding for security"""

    def __post_init__(self):
        """Validate configuration after initialization."""
        if not self.authorization_server_url:
            raise ValueError("authorization_server_url is required")
        if not self.resource_server_uri:
            raise ValueError("resource_server_uri is required")

        if self.token_validation_method == "jwt" and not self.jwt_public_key:
            logger.warning("JWT validation selected but no public key provided")
        elif (
            self.token_validation_method == "introspection"
            and not self.introspection_endpoint
        ):
            raise ValueError(
                "introspection_endpoint required for introspection validation"
            )

        if self.required_scopes is None:
            self.required_scopes = []


class OAuthError(Exception):
    """Base exception for OAuth-related errors."""

    def __init__(self, error: str, description: str = None, status_code: int = 401):
        self.error = error
        self.description = description
        self.status_code = status_code
        super().__init__(f"{error}: {description}" if description else error)


class TokenValidationResult:
    """Result of token validation."""

    def __init__(self, valid: bool, claims: Dict = None, error: str = None):
        self.valid = valid
        self.claims = claims or {}
        self.error = error

    @property
    def subject(self) -> Optional[str]:
        """Get the subject (user) from token claims."""
        return self.claims.get("sub")

    @property
    def audience(self) -> Optional[Union[str, List[str]]]:
        """Get the audience from token claims."""
        return self.claims.get("aud")

    @property
    def scopes(self) -> List[str]:
        """Get the scopes from token claims."""
        scope_claim = self.claims.get("scope", "")
        if isinstance(scope_claim, str):
            return scope_claim.split() if scope_claim else []
        elif isinstance(scope_claim, list):
            return scope_claim
        return []

    @property
    def user_id(self) -> Optional[str]:
        """Get a unique user identifier for session binding."""
        # Use subject as the primary user identifier
        return self.subject


class SecureSessionManager:
    """
    Secure session management following MCP security best practices.

    Implements:
    - Secure, non-deterministic session IDs
    - User-specific session binding
    - Session validation
    """

    def __init__(self):
        self._sessions: Dict[str, Dict] = {}

    def generate_session_id(self, user_id: str) -> str:
        """
        Generate a secure session ID bound to a user.

        Format: <user_id_hash>:<secure_random_token>
        This prevents session hijacking by binding sessions to users.
        """
        # Generate cryptographically secure random token
        secure_token = secrets.token_urlsafe(32)

        # Create a hash of user_id for binding (not reversible)
        import hashlib

        user_hash = hashlib.sha256(user_id.encode()).hexdigest()[:16]

        session_id = f"{user_hash}:{secure_token}"

        # Store session metadata
        self._sessions[session_id] = {
            "user_id": user_id,
            "created_at": __import__("time").time(),
        }

        logger.debug(f"Generated secure session ID for user: {user_id}")
        return session_id

    def validate_session(self, session_id: str, user_id: str) -> bool:
        """
        Validate that a session ID belongs to the specified user.

        This prevents session hijacking attacks.
        """
        if not session_id or session_id not in self._sessions:
            return False

        session_data = self._sessions[session_id]
        return session_data.get("user_id") == user_id

    def cleanup_expired_sessions(self, max_age_seconds: int = 3600):
        """Clean up expired sessions."""
        current_time = __import__("time").time()
        expired_sessions = [
            sid
            for sid, data in self._sessions.items()
            if current_time - data.get("created_at", 0) > max_age_seconds
        ]

        for sid in expired_sessions:
            del self._sessions[sid]

        if expired_sessions:
            logger.info(f"Cleaned up {len(expired_sessions)} expired sessions")


class OAuthResourceServer:
    """OAuth 2.1 Resource Server implementation for MCP."""

    def __init__(self, config: OAuthConfig):
        self.config = config
        self.session_manager = SecureSessionManager()
        self._http_client = httpx.AsyncClient()
        logger.info(
            f"Initialized OAuth resource server for {config.resource_server_uri}"
        )

    async def get_protected_resource_metadata(self) -> Dict:
        """
        Generate OAuth 2.0 Protected Resource Metadata (RFC 9728).

        Returns metadata that clients use to discover the authorization server.
        """
        metadata = {
            "resource": self.config.resource_server_uri,
            "authorization_servers": [self.config.authorization_server_url],
        }

        if self.config.required_scopes:
            metadata["scopes_supported"] = self.config.required_scopes

        logger.debug(f"Generated resource metadata: {metadata}")
        return metadata

    async def handle_resource_metadata_request(self, request: Request) -> JSONResponse:
        """Handle requests to the protected resource metadata endpoint."""
        try:
            metadata = await self.get_protected_resource_metadata()
            return JSONResponse(
                content=metadata, headers={"Content-Type": "application/json"}
            )
        except Exception as e:
            logger.error(f"Error serving resource metadata: {e}")
            return JSONResponse(
                content={
                    "error": "server_error",
                    "error_description": "Failed to generate metadata",
                },
                status_code=500,
            )

    def extract_bearer_token(self, request: Request) -> Optional[str]:
        """Extract Bearer token from Authorization header."""
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return None
        return auth_header[7:]  # Remove "Bearer " prefix

    async def validate_jwt_token(self, token: str) -> TokenValidationResult:
        """Validate JWT access token with audience validation."""
        if not self.config.jwt_public_key:
            return TokenValidationResult(False, error="JWT public key not configured")

        try:
            # Decode and verify JWT with strict audience validation
            # This prevents token passthrough attacks (MCP Security Best Practice)
            claims = jwt.decode(
                token,
                self.config.jwt_public_key,
                algorithms=[self.config.jwt_algorithm],
                audience=self.config.resource_server_uri,  # Strict audience validation
                options={"verify_aud": True},  # Ensure audience is verified
            )

            logger.debug(f"JWT validation successful for subject: {claims.get('sub')}")
            return TokenValidationResult(True, claims)

        except jwt.ExpiredSignatureError:
            logger.warning("Token validation failed: Token expired")
            return TokenValidationResult(False, error="Token expired")
        except jwt.InvalidAudienceError:
            logger.warning(
                f"Token validation failed: Invalid audience. Expected: {self.config.resource_server_uri}"
            )
            return TokenValidationResult(False, error="Invalid audience")
        except jwt.InvalidTokenError as e:
            logger.warning(f"Token validation failed: {str(e)}")
            return TokenValidationResult(False, error=f"Invalid token: {str(e)}")
        except Exception as e:
            logger.error(f"JWT validation error: {e}")
            return TokenValidationResult(False, error="Token validation failed")

    async def validate_token_introspection(self, token: str) -> TokenValidationResult:
        """Validate token using OAuth 2.0 Token Introspection (RFC 7662)."""
        if not self.config.introspection_endpoint:
            return TokenValidationResult(
                False, error="Introspection endpoint not configured"
            )

        try:
            # Prepare introspection request
            auth = None
            if (
                self.config.introspection_client_id
                and self.config.introspection_client_secret
            ):
                auth = (
                    self.config.introspection_client_id,
                    self.config.introspection_client_secret,
                )

            response = await self._http_client.post(
                self.config.introspection_endpoint,
                data={"token": token},
                auth=auth,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )

            if response.status_code != 200:
                logger.warning(
                    f"Introspection failed with status: {response.status_code}"
                )
                return TokenValidationResult(False, error="Introspection failed")

            introspection_result = response.json()

            # Check if token is active
            if not introspection_result.get("active", False):
                return TokenValidationResult(False, error="Token inactive")

            # Validate audience (prevents token passthrough attacks)
            token_audience = introspection_result.get("aud")
            if token_audience:
                if isinstance(token_audience, list):
                    if self.config.resource_server_uri not in token_audience:
                        logger.warning(
                            f"Token audience mismatch. Expected: {self.config.resource_server_uri}, Got: {token_audience}"
                        )
                        return TokenValidationResult(False, error="Invalid audience")
                elif token_audience != self.config.resource_server_uri:
                    logger.warning(
                        f"Token audience mismatch. Expected: {self.config.resource_server_uri}, Got: {token_audience}"
                    )
                    return TokenValidationResult(False, error="Invalid audience")

            logger.debug(
                f"Token introspection successful for subject: {introspection_result.get('sub')}"
            )
            return TokenValidationResult(True, introspection_result)

        except Exception as e:
            logger.error(f"Token introspection error: {e}")
            return TokenValidationResult(False, error="Introspection failed")

    async def validate_access_token(self, token: str) -> TokenValidationResult:
        """Validate access token using configured method."""
        if self.config.token_validation_method == "jwt":
            result = await self.validate_jwt_token(token)
        elif self.config.token_validation_method == "introspection":
            result = await self.validate_token_introspection(token)
        else:
            return TokenValidationResult(False, error="Unknown validation method")

        # Check required scopes if token is valid
        if result.valid and self.config.required_scopes:
            token_scopes = result.scopes
            missing_scopes = set(self.config.required_scopes) - set(token_scopes)
            if missing_scopes:
                logger.warning(f"Token missing required scopes: {missing_scopes}")
                return TokenValidationResult(False, error="Insufficient scopes")

        return result

    async def authenticate_request(
        self, request: Request, session_id: str = None
    ) -> Tuple[bool, Optional[TokenValidationResult]]:
        """
        Authenticate an incoming request with session validation.

        Implements MCP security best practices:
        - Verifies all inbound requests when OAuth is enabled
        - Validates session binding to prevent hijacking

        Returns:
            Tuple of (is_authenticated, validation_result)
        """
        token = self.extract_bearer_token(request)
        if not token:
            logger.debug("No Bearer token found in request")
            return False, None

        result = await self.validate_access_token(token)
        if not result.valid:
            logger.warning(f"Token validation failed: {result.error}")
            return False, result

        # Additional session validation if session binding is enabled
        if self.config.session_binding_enabled and session_id and result.user_id:
            if not self.session_manager.validate_session(session_id, result.user_id):
                logger.warning(f"Session validation failed for user: {result.user_id}")
                return False, TokenValidationResult(False, error="Invalid session")

        logger.debug(f"Request authenticated for subject: {result.subject}")
        return True, result

    def create_www_authenticate_header(self) -> str:
        """Create WWW-Authenticate header for 401 responses."""
        metadata_url = urljoin(
            self.config.resource_server_uri, self.config.resource_metadata_path
        )
        return f'Bearer resource="{metadata_url}"'

    async def create_unauthorized_response(
        self, error: str = "invalid_token", description: str = None
    ) -> Response:
        """Create a 401 Unauthorized response with proper headers."""
        www_auth = self.create_www_authenticate_header()

        error_response = {"error": error}
        if description:
            error_response["error_description"] = description

        return JSONResponse(
            content=error_response,
            status_code=401,
            headers={"WWW-Authenticate": www_auth},
        )

    async def create_forbidden_response(
        self, error: str = "insufficient_scope", description: str = None
    ) -> Response:
        """Create a 403 Forbidden response."""
        error_response = {"error": error}
        if description:
            error_response["error_description"] = description

        return JSONResponse(content=error_response, status_code=403)

    def generate_secure_session(self, user_id: str) -> str:
        """Generate a secure session ID for a user."""
        return self.session_manager.generate_session_id(user_id)

    async def cleanup(self):
        """Cleanup resources."""
        await self._http_client.aclose()
        self.session_manager.cleanup_expired_sessions()


def create_oauth_config_from_env() -> Optional[OAuthConfig]:
    """Create OAuth configuration from environment variables."""
    import os

    auth_server_url = os.getenv("OAUTH_AUTHORIZATION_SERVER_URL")
    resource_uri = os.getenv("OAUTH_RESOURCE_SERVER_URI")

    if not auth_server_url or not resource_uri:
        logger.info("OAuth environment variables not found, OAuth disabled")
        return None

    return OAuthConfig(
        authorization_server_url=auth_server_url,
        resource_server_uri=resource_uri,
        token_validation_method=os.getenv("OAUTH_TOKEN_VALIDATION_METHOD", "jwt"),
        jwt_public_key=os.getenv("OAUTH_JWT_PUBLIC_KEY"),
        jwt_algorithm=os.getenv("OAUTH_JWT_ALGORITHM", "RS256"),
        introspection_endpoint=os.getenv("OAUTH_INTROSPECTION_ENDPOINT"),
        introspection_client_id=os.getenv("OAUTH_INTROSPECTION_CLIENT_ID"),
        introspection_client_secret=os.getenv("OAUTH_INTROSPECTION_CLIENT_SECRET"),
        required_scopes=os.getenv("OAUTH_REQUIRED_SCOPES", "").split()
        if os.getenv("OAUTH_REQUIRED_SCOPES")
        else [],
        session_binding_enabled=os.getenv(
            "OAUTH_SESSION_BINDING_ENABLED", "true"
        ).lower()
        == "true",
    )
