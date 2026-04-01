# 🚀 Production Deployment Manual

## 📂 Pre-Deployment Checklist
- [ ] **MinIO Gateway**: High Availability storage configured.
- [ ] **Database Persistence**: SQLite (dev) or PostgreSQL (industrial-prod).
- [ ] **HMAC Secret**: Change `GATEWAY_SECRET` in `core/security.py`.

## 🐳 Dockerized Deployment
1.  **Clone**: `git clone https://github.com/Shivrajmahato/KYC_VERIFICATION_SYSTEM.git`
2.  **Config**: Update `.env` with your Production MinIO credentials.
3.  **Launch**: `docker-compose up -d --build`

## 🛡️ Security Hardening
*   **SSL/TLS**: Always run the Gateway behind an Nginx proxy with Let's Encrypt certificates.
*   **Audit Rotation**: Configure `logrotate` to manage `audit.log` and `debug.log`.
*   **Access Restricted**: Ensure the `kyc-verification-docs` bucket is Private.
