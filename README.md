# 🛡️ Industrial KYC Verification Gateway

An industrial-grade, AI-driven Know Your Customer (KYC) verification system built for security and high transparency.

## 🚀 Key Features
*   **AI-Powered Verification**: Fully automated OCR, Liveness detection, and Face Matching using `EasyOCR` and `OpenCV`.
*   **Security-First Architecture**: Implements the `DIV_SECRET_ID` primitive to bind results securely across distributed tasks.
*   **Industrial Object Storage**: Integrated with **MinIO** (S3-compatible) for persistent artifact storage with an automated "Local Fallback" mechanism.
*   **Full Traceability**: Specialized `audit.log` and `debug.log` trails for complete user-level auditing and security compliance.
*   **Real-time Transparency**: A modern, glassmorphic dashboard providing live AI scores and detailed failure reasons.
*   **CI/CD Integrated**: Pre-configured with **GitHub Actions** for automated testing and deployment validation.

## 🛠️ Tech Stack
- **Backend**: FastAPI (Python), SQLAlchemy (SQLite)
- **Frontend**: React + Vite, MediaPipe
- **Storage**: MinIO / S3
- **DevOps**: GitHub Actions, Docker Compose

## 📦 Quick Start
1.  **Environment**: `python -m venv venv`
2.  **Install**: `pip install -r requirements.txt`
3.  **Launch**: `python run.py`
4.  **Dashboard**: Access `http://localhost:5173`
