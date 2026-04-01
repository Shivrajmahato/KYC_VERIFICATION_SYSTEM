# 📡 KYC Gateway API Reference

The KYC Gateway provides a secure REST API for session management and AI task triggering.

## 🚀 Authentication
All requests must be signed or carry a valid `div_secret_id` in the URL path.

### 1. Start Session
**POST** `/gateway/session/start`
Starts a new KYC session for a user.
- **Request Body**:
  ```json
  {
    "user_id": "string",
    "tenant_id": "string",
    "client_id": "string"
  }
  ```
- **Response**: Returns a `div_secret_id` and `request_id`.

### 2. Upload Document
**POST** `/gateway/session/{div_secret_id}/document`
Uploads ID images and triggers OCR processing.
- **Request Body**: `DocumentUploadRequest` (Base64 strings for front/back).

### 3. Upload Liveness
**POST** `/gateway/session/{div_secret_id}/liveness`
Uploads a live selfie and triggers Liveness detection.

### 4. Check Status
**GET** `/gateway/status/{div_secret_id}`
Returns the real-time status of all modules and the final KYC decision.
