---
title: "Authentication Endpoints"
dimension: api
type: endpoint-group
source_refs: ["raw/api-reference.md#authentication"]
tags: [auth, jwt, login, session]
methods: [POST]
base_path: "/api/v1/auth"
auth_required: false
graph_edges:
  - target: "pages/business/login-flow"
    relation: "implements"
  - target: "pages/data/user-entity"
    relation: "accepts"
  - target: "pages/data/session-entity"
    relation: "returns"
  - target: "pages/database/sessions-table"
    relation: "persisted-by"
  - target: "pages/integration/redis-session-store"
    relation: "delegates-to"
  - target: "pages/architecture/middleware-chain"
    relation: "part-of"
created: 2026-04-14
updated: 2026-04-14
---

# Authentication Endpoints

The auth endpoints handle user login, token refresh, and logout. They are
the only unauthenticated endpoints in the service — all other routes require
a valid JWT in the `Authorization` header.

## POST /api/v1/auth/login

Authenticates a user with email and password, returns a JWT access token
and a refresh token.

**Request:**
```json
{
  "email": "string (required)",
  "password": "string (required)"
}
```

**Response (200):**
```json
{
  "access_token": "string (JWT, 15min expiry)",
  "refresh_token": "string (opaque, 7d expiry)",
  "user": {
    "id": "uuid",
    "email": "string",
    "role": "admin | member | viewer"
  }
}
```

**Flow:**
1. Validate input against [[pages/data/login-dto|LoginDTO]]
2. Look up user by email → [[pages/data/user-entity]]
3. Verify password hash (bcrypt)
4. Generate JWT with user ID and role claims
5. Create session record → [[pages/database/sessions-table]]
6. Store session in Redis → [[pages/integration/redis-session-store]]
7. Return tokens

**Error Codes:**
| Status | Code | When |
|--------|------|------|
| 400 | INVALID_INPUT | Missing or malformed email/password |
| 401 | INVALID_CREDENTIALS | Email not found or password mismatch |
| 429 | RATE_LIMITED | More than 5 failed attempts in 15 minutes |

**Business rules:** Rate limiting is per-IP + per-email combination.
After 5 failed attempts, the account is soft-locked for 15 minutes.
See [[pages/business/login-flow#rate-limiting]] for details.

## POST /api/v1/auth/refresh

Exchanges a valid refresh token for a new access token.

**Request:**
```json
{
  "refresh_token": "string (required)"
}
```

**Response (200):**
```json
{
  "access_token": "string (JWT, 15min expiry)"
}
```

**Flow:**
1. Look up refresh token in sessions → [[pages/database/sessions-table]]
2. Validate not expired and not revoked
3. Generate new JWT
4. Return new access token (refresh token unchanged)

**Error Codes:**
| Status | Code | When |
|--------|------|------|
| 401 | INVALID_TOKEN | Token not found, expired, or revoked |

## POST /api/v1/auth/logout

Revokes the current session's refresh token.

**Request:** Empty body. Requires `Authorization: Bearer <access_token>` header.

**Response (204):** No content.

**Flow:**
1. Extract user ID from JWT
2. Revoke refresh token in [[pages/database/sessions-table]]
3. Remove session from [[pages/integration/redis-session-store]]

## Cross-Repo Interactions

This auth system is consumed by:
- [[order-service::pages/integration/auth-client]] — validates JWTs on incoming requests
- [[payment-service::pages/integration/auth-client]] — validates JWTs for payment authorization

The JWT signing key is shared via environment variable `JWT_SECRET`.
See [[raw/env-and-flags#jwt-secret]] for configuration.
<!-- cross-repo: order-service and payment-service may not be bootstrapped yet -->
