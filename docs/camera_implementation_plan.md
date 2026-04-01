# Camera Capture & Liveness Video Implementation

This plan details the addition of real-time camera interaction for document scanning and liveness verification within the React KYC Dashboard.

## User Review Required

> [!IMPORTANT]
> **Mock vs. Real Processing**: The current backend is a mock system. For the "Live Video Capture," we will show the live camera feed with the 60s TTL, but we will transmit a captured frame (selfie) to our existing `/liveness` endpoint for the final evaluation, as streaming video processing requires heavy AI infrastructure (e.g., WebRTC/WebSockets) not yet present in the core.

## Proposed Changes

---

### Step 1: UI Enhancement for Choice (Upload vs. Capture)

#### [MODIFY] frontend/src/App.jsx
- Update the "Status Hub" to show a selection modal or button group when "Upload Document" is clicked.
- Options: "Upload from Device" or "Scan with Camera".

---

### Step 2: Camera & Video Capture Logic

#### [NEW] frontend/src/components/CameraView.jsx
- Create a reusable component using `navigator.mediaDevices.getUserMedia`.
- Features:
  - Live `<video>` preview.
  - "Capture" button for document scanning (grabs current frame to a hidden `<canvas>` and exports as Base64).
  - "Liveness Start" button with a **60s Countdown Timer (TTL)**.
  - Automatic timeout logic if 60s expires.

---

### Step 3: Integration with KYC Pipeline

#### [MODIFY] frontend/src/App.jsx
- Integrate the `CameraView` into the main state machine.
- Ensure that after "Scanning" or "Liveness Session", the resulting Base64 images are sent to:
  - `POST /gateway/session/{id}/document` (for document)
  - `POST /gateway/session/{id}/liveness` (for liveness)
- Status Hub should then correctly reflect the transition to "Smart Waiting" and then "Evaluation".

---

### Step 4: Styling & Visual Polish

#### [MODIFY] frontend/src/index.css
- Add a "Scanning" overlay effect (e.g., a moving red horizontal line) to the camera preview for a premium "AI Document Detection" look.
- Add a circular progress or numeric countdown for the 60s Liveness TTL.

## Verification Plan

### Automated Tests
- Verification using the browser subagent to ensure the "Capture" buttons appear and the timer starts correctly when Liveness is triggered.

### Manual Verification
1. Open the dashboard.
2. Click "Upload Document" -> Select "Scan with Camera".
3. Verify camera permissions request and live feed.
4. Capture front and back.
5. Trigger Liveness -> Verify 60s countdown.
6. Verify status updates to "COMPLETED" after both are done.
