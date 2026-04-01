# 🛠️ Industrial Troubleshooting Guide

## ❌ OCR Failures
*   **Cause**: Blurry image or low resolution.
*   **Fix**: Ensure your camera is properly focused and use **`VALID_B64`** during tests to verify the OCR engine is initialized.
*   **Audit**: Check `debug.log` for **"OCR Task failed"** errors.

## 🔴 Liveness Spoofing Detected
*   **Cause**: Static image detected instead of a live feed, or high depth mismatch.
*   **Fix**: Ensure the user is in good lighting and moving slightly during verification.

## 💾 Database IntegrityError (UNIQUE constraint)
*   **Cause**: Colliding `session_id`.
*   **Fix**: This is resolved in the Industrial Suite by using **UUIDs** for result binding. Ensure you've run a `kyc_sessions.db` reset.

## 📦 MinIO Connection Errors
*   **Cause**: Docker container is down or `MINIO_ROOT_PASSWORD` mismatch.
*   **Fix**: Re-launch with `docker-compose up -d`. The Gateway will auto-switch to **Local Fallback** if MinIO remains unreachable.
