# 🚀 Industrial-Grade Asynchronous KYC System

An end-to-end, industrial-grade KYC (Know Your Customer) verification system featuring an asynchronous processing pipeline, modular AI drivers, gesture-based liveness detection, and S3-compatible object storage (MinIO).

## 🌟 Key Features

- **Asynchronous Pipeline**: Decoupled session lifecycle. Document OCR and Liveness can be completed in any order.
- **Smart Orchestration**: Automatic "Face Comparison" trigger once prerequisites are met.
- **Modular AI Drivers**: Provisioned for integration with real ML models (DeepFace, EasyOCR, etc.) via a pluggable driver pattern.
- **Gesture Liveness**: Real-time camera interaction with motion-triggered snapshots and 60-second TTL.
- **Artifact Storage**: Automated persistence of all KYC artifacts (ID scans, selfies, videos) to MinIO (S3) with timestamped audit trails.
- **Glassmorphic UI**: Premium React dashboard with real-time status hubs and camera scanning overlays.

## 🛠 Project Structure

```bash
├── core/            # Database (SQLite), S3 Storage Manager, Security
├── gateway/         # FastAPI Orchestration Layer & Endpoints
├── modules/         # Modular AI Processors (OCR, Liveness, FaceMatch)
├── frontend/        # React + Vite Dashboard (Tailored CSS)
├── docs/            # Implementation plans & Walkthroughs
└── docker-compose.yml # One-click MinIO Infrastructure
```

## 🚀 Quick Start (Few Clicks)

### 1. Start Infrastructure (MinIO)
Ensure Docker is running and execute:
```bash
docker-compose up -d
```

### 2. Setup Backend
1. **Activate Environment**:
```powershell
.\venv\Scripts\Activate.ps1
```
2. **Install Dependencies**:
```bash
pip install -r requirements.txt
```
3. **Run Gateway**:
```bash
python run.py
```
*(Server runs on port **8005**)*

### 3. Setup Frontend
1. **Navigate & Install**:
```bash
cd frontend
npm install
```
2. **Launch Dashboard**:
```bash
npm run dev
```
*(Access at `http://localhost:5173`)*

## 🧪 Verification
Run the integrated test suite to verify the full async event flow:
```bash
python test_api.py
```

## 🔧 Architecture Notes
- **Storage Fallback**: If MinIO is not reachable, the system automatically falls back to secure `local_storage/`.
- **Thresholds**: AI results are evaluated against a configurable confidence threshold (default 80%).

---
Developed with ❤️ for high-security verification workloads.
