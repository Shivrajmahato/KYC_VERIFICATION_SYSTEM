# Industrial KYC: Real AI, Gesture Detection & MinIO Storage

This plan evolves the project from a mock prototype into a "Real-World" architecture by adding object storage, modular AI drivers, and client-side gesture analysis.

## User Review Required

> [!IMPORTANT]
> **Infrastructure Prerequisite**: To use the MinIO features, you will need a MinIO server running (typically via Docker: `docker run -p 9000:9000 -p 9001:9001 minio/minio server /data --console-address ":9001"`). If you don't have it, I will implement a **Local File Storage Fallback** that mimics S3 behavior. 

## Proposed Changes

---

### Backend: Storage & Modular AI

#### [NEW] core/storage.py
- Implement `S3StorageManager` using the `minio` library.
- Functions: `upload_image`, `upload_video`, `generate_presigned_url`.
- Path Structure: `kyc-data/{tenant_id}/{customer_id}/{timestamp}/{file_type}.jpg`.

#### [MODIFY] modules/*/processor.py
- Refactor processors to use an **AI Driver Pattern**.
- Create a `base_driver.py` and implement a `MockDriver` (default).
- Provision a `RealDriver` hook where you can plug in `deepface` (Face Compare) or `easyocr` (OCR).
- Update threshold logic to return multi-dimensional results (Confidence, Match Status, OCR Text).

#### [MODIFY] gateway/main.py
- Update endpoints to handle `UploadFile` (for liveness video) rather than just Base64 where appropriate.
- Integrate the storage manager to persist all transaction artifacts (Front ID, Back ID, Liveness Video, Snapshots).

---

### Frontend: Gesture-Based Liveness

#### [MODIFY] frontend/src/components/CameraView.jsx
- **Gesture Detection Engine**: Integrate `@mediapipe/face_mesh` for real-time facial landmark analysis.
- **Motion Verification**: 
  - Instructions will appear (e.g., "Blink 3 times", "Turn head left").
  - System captures snapshots only when the gesture is detected.
- **Automatic Snapping**: High-res images are captured during the 60s TTL session when "Motion Snapshot" events occur.

#### [MODIFY] frontend/src/App.jsx
- Update result display to show detailed AI metrics (Threshold vs Prediction).
- Add visual indicators for "Gesture Verification Successful".

---

### Cleanup & Setup

#### [MODIFY] requirements.txt
- Add `minio`, `opencv-python-headless` (for AI processing), and other ML dependencies.

#### [NEW] setup_minio.ps1
- A quick helper script to check for MinIO connectivity and create the initial bucket.

## Verification Plan

### Automated Tests
- Updated `test_api.py` to verify backend storage persistence (checking if files exist in MinIO/local storage after a run).

### Manual Verification
1. Start Backend + MinIO.
2. Start Frontend.
3. Perform Document Scan -> Verify file appears in MinIO console.
4. Perform Liveness -> Follow gesture prompts -> Verify snapshots and video appear in MinIO under the correct timestamped path.
5. Review final KYC result based on the AI threshold evaluation.
