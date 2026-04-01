# 🛡️ Security & Traceability Model

Security in this Industrial KYC system is built on **Cryptographic Session Binding** and **E2E Auditing**.

## 🔑 DIV_SECRET_ID
The `DIV_SECRET_ID` is a short-lived, HMAC-signed token that binds all artifacts (images, database rows, results) to a specific user session.
*   **Security Threat Mitigation**: Prevents "Session Hijacking" by ensuring that only the holder of the signed ID can upload artifacts.
*   **Result Binding**: All AI results (OCR, Liveness) are linked via this ID, preventing data cross-leakage.

## 📋 Audit Logging
The system maintains a high-fidelity **Security Audit Trail** for compliance.
*   **`audit.log`**: Strictly tracks high-level user events (Session Start, Decision Outcomes).
*   **`debug.log`**: Captures granular technical execution details for industrial troubleshooting.

## 🔒 Storage Security
All images are salted and stored in private MinIO buckets (or encrypted local storage), accessible only via the Gateway's internal storage manager.
