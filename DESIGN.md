# System Design: Multi-Tenant Usage Metering & Billing Engine

## 1. System Overview
A backend system built with FastAPI and Supabase/PostgreSQL that handles multi-tenant usage metering, quota enforcement, and Stripe subscription synchronization using a $0 stack.

---

## 2. Database Schema Design
The database consists of four core tables:

* **`plans`**: Stores subscription tiers and hard resource constraints.
  * `id` (PK, String/UUID) — e.g., `"free"`, `"pro"`
  * `name` (String) — e.g., `"Free Tier"`, `"Pro Tier"`
  * `api_call_limit` (Integer) — e.g., `2000`
  * `ai_token_limit` (Integer) — e.g., `2000000`
  * `price_in_cents` (Integer) — e.g., `0` or `2900`

* **`tenants`**: Stores customer organization profiles.
  * `id` (PK, UUID) — Unique tenant identifier
  * `name` (String) — Tenant/Organization name
  * `stripe_customer_id` (String, Nullable) — Populated upon Stripe checkout upgrade
  * `created_at` (Timestamp)

* **`subscriptions`**: Links tenants to their active plan and tracks billing state.
  * `id` (PK, UUID)
  * `tenant_id` (FK referencing `tenants.id`)
  * `plan_id` (FK referencing `plans.id`)
  * `status` (String) — `"active"`, `"canceled"`, or `"past_due"`
  * `stripe_subscription_id` (String, Nullable)

* **`usage_events`**: Immutable ledger tracking resource consumption.
  * `id` (PK, UUID)
  * `tenant_id` (FK referencing `tenants.id`)
  * `usage_type` (String) — `"api_call"` or `"ai_tokens"`
  * `quantity` (Integer) — `1` for API calls, or token count for AI usage
  * `idempotency_key` (String, **Unique Constraint**) — Prevents duplicate logging on retries
  * `created_at` (Timestamp)

---

## 3. Plan Quotas & Seeding
* **Free Tier:** 2,000 API calls / 2,000,000 AI tokens per billing cycle.
* **Pro Tier:** Higher/custom limits managed via Stripe webhook sync.
* **Boot Seeding:** Default plans (`free` and `pro`) are automatically seeded into the database upon application startup if they do not already exist.

---

## 4. Metering API Contract (`POST /generate`)
The primary billable endpoint simulating an AI generation request.

* **Headers:**
  * `X-Tenant-ID`: Identifies the making request.
  * `Idempotency-Key`: Unique client-provided string for deduplication.
* **Request Body:**
  * JSON payload containing the prompt string.
* **Response:**
  * `200 OK`: Returns the simulated AI response and token metrics on success.
  * `429 Too Many Requests`: Returned when the tenant has exhausted their monthly API call or token quota.
  * `402 Payment Required`: Returned if subscription status is delinquent/unpaid.

---

## 5. Idempotency & Quota Enforcement Logic
1. **Idempotency Check:** Incoming requests include an `Idempotency-Key`. The backend checks `usage_events` for an existing match before processing to ensure retries do not double-count usage.
2. **Quota Check:** The system aggregates current-month usage events per tenant and compares them against limits defined in the active plan. Requests exceeding limits are blocked with a `429` status code.
3. **Usage Logging:** Validated requests sequentially record an `api_call` event (quantity `1`) and an `ai_tokens` event (simulated token count), sharing the same idempotency key.