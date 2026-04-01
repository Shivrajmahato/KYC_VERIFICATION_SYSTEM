# 🏛️ KYC System Architecture

This Industrial KYC system utilizes a **State-Machine Orchestrator** to manage independent AI modules in a secure, non-blocking environment.

## 🔄 The Master Flow
1.  **Session Start**: A unique `DIV_SECRET_ID` is cryptographically generated.
2.  **Document Intake**: OCR and Liveness images are ingested and stored in MinIO.
3.  **Module Execution**: Background tasks trigger the AI Drivers (EasyOCR, OpenCV).
4.  **Terminal Decision**: Once prerequisites (OCR/Liveness) are met, the Face Compare module makes the final VERIFIED/REJECTED decision.

## 🧠 AI Drivers
The system follows a "Driver Pattern," allowing AI models to be swapped without changing the core gateway logic.
-   **OCR Driver**: Handles text extraction and biometric data verification.
-   **Liveness Driver**: Analyzes selfie frames for depth and spoofing indicators.
-   **Face Matcher**: Uses cosine similarity to compare ID photos against live selfies.
