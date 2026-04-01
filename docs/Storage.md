# 💾 Storage Engine Guide

The Industrial KYC system uses a **Dual-Mode Storage Engine** for high availability.

## 🗄️ MinIO (Object Storage)
The primary storage engine is an S3-compatible **MinIO** cluster.
- **Bucket**: `kyc-verification-docs`
- **Pathing**: `/{div_secret_id}/{image_type}.jpg`
- **Persistence**: Images are stored permanently for auditing and compliance.

## 🔄 Local Fallback Mode
In development or during localized outages, the system automatically switches to the **`local_storage/`** directory.
- **Behavior**: If the MinIO server is unreachable, the Gateway will create a local folder for the session.
- **Benefit**: Ensures zero-downtime testing during CI/CD runs and local development.

## 🧪 Database Persistence
*   **Engine**: SQLite (Internal) / SQLAlchemy
*   **Key Tables**:
    -   `verification_sessions`: Master session record with final scores.
    -   `module_status`: Per-module (OCR, Liveness) metadata and results.
