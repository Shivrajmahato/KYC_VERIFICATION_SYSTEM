import { useState, useEffect } from 'react';
import './index.css';
import CameraView from './components/CameraView';

const API_BASE = "http://127.0.0.1:8005/gateway";

function App() {
  const [session, setSession] = useState(null);
  const [status, setStatus] = useState(null);
  const [step, setStep] = useState('landing');
  const [loading, setLoading] = useState(false);

  // Camera Integration State
  const [cameraMode, setCameraMode] = useState(null); // 'document' or 'liveness'
  const [captureStep, setCaptureStep] = useState(null); // 'front', 'back', 'selfie'
  const [frontImage, setFrontImage] = useState(null);

  const startSession = async () => {
    setLoading(true);
    try {
      const resp = await fetch(`${API_BASE}/session/start`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ tenant_id: "tenant_A", client_id: "client_1", user_id: "user_777" })
      });
      const data = await resp.json();
      setSession(data.div_secret_id);
      setStep('hub');
    } catch (e) {
      alert("Failed to start session. Is backend running?");
    }
    setLoading(false);
  };

  useEffect(() => {
    if (!session) return;
    const interval = setInterval(async () => {
      const resp = await fetch(`${API_BASE}/status/${session}`);
      if (resp.ok) {
        const data = await resp.json();
        setStatus(data);
        if (data.overall_status === 'COMPLETED' || data.overall_status === 'FAILED') {
          clearInterval(interval);
        }
      }
    }, 2000);
    return () => clearInterval(interval);
  }, [session]);

  const onCapture = async (dataUrl) => {
    if (cameraMode === 'document') {
      if (!frontImage) {
        setFrontImage(dataUrl);
        setCaptureStep('back');
      } else {
        // We have both now
        setLoading(true);
        await fetch(`${API_BASE}/session/${session}/document`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ document_front_image: frontImage, document_back_image: dataUrl })
        });
        setLoading(false);
        setCameraMode(null);
        setFrontImage(null);
        alert("Documents Scan Complete!");
      }
    } else if (cameraMode === 'liveness') {
      setLoading(true);
      await fetch(`${API_BASE}/session/${session}/liveness`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ selfie_image: dataUrl })
      });
      setLoading(false);
      setCameraMode(null);
      alert("Liveness Verification Captured & Uploading! Check MinIO in a few seconds.");
    }
  };

  const uploadDocsMock = async () => {
    setLoading(true);
    await fetch(`${API_BASE}/session/${session}/document`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ document_front_image: "mock_data", document_back_image: "mock_data" })
    });
    setLoading(false);
    alert("Mock Documents Uploaded!");
  };

  const uploadLivenessMock = async () => {
    setLoading(true);
    await fetch(`${API_BASE}/session/${session}/liveness`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ selfie_image: "mock_selfie" })
    });
    setLoading(false);
    alert("Mock Liveness Uploaded!");
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', padding: '50px' }}>
      <img src="/logo.png" style={{ height: '100px', marginBottom: '20px' }} alt="SR Logo" />
      
      {cameraMode && (
        <CameraView 
          mode={cameraMode} 
          onCapture={onCapture} 
          onCancel={() => setCameraMode(null)} 
        />
      )}

      {step === 'landing' && (
        <div className="glass-card" style={{ textAlign: 'center' }}>
          <h1>AI KYC Verification</h1>
          <p>Secure, fast, and automated.</p>
          <button className="btn-primary" onClick={startSession} disabled={loading}>
            {loading ? "Starting..." : "Start Verification"}
          </button>
        </div>
      )}

      {step === 'hub' && (
        <div className="glass-card" style={{ minWidth: '400px' }}>
          <div style={{ float: 'right' }} className={`status-badge status-${status?.overall_status || 'PENDING'}`}>
            {status?.overall_status || 'PENDING'}
          </div>
          <h3>Verification Session</h3>
          <p style={{ fontSize: '0.8rem', opacity: 0.7 }}>ID: {session}</p>
          
          <div style={{ margin: '30px 0' }}>
            <div className="module-item" style={{ background: 'rgba(255,255,255,0.05)', padding: '15px', borderRadius: '10px', marginBottom: '10px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '5px' }}>
                <strong>ID Documents (OCR)</strong>
                <span className={`status-badge status-${status?.modules?.find(m=>m.module==='OCR')?.status || 'PENDING'}`}>
                  {status?.modules?.find(m=>m.module==='OCR')?.status || 'PENDING'}
                </span>
              </div>
              {status?.modules?.find(m=>m.module==='OCR')?.confidence_score && (
                <div style={{ fontSize: '0.7rem', color: '#888', marginBottom: '5px' }}>
                  Confidence: {Math.round(status.modules.find(m=>m.module==='OCR').confidence_score * 100)}%
                </div>
              )}
              {status?.modules?.find(m=>m.module==='OCR')?.failure_reason && (
                <div style={{ fontSize: '0.7rem', color: '#ff4b2b', marginBottom: '10px' }}>
                  Error: {status.modules.find(m=>m.module==='OCR').failure_reason}
                </div>
              )}
              <div style={{ display: 'flex', gap: '10px' }}>
                <button className="btn-primary" style={{ padding: '8px 15px', fontSize: '0.7rem' }} onClick={() => { setCameraMode('document'); setCaptureStep('front'); }}>
                   Scan Document
                </button>
                <button title="Mock Upload" style={{ background: 'transparent', border: '1px solid #444', color: '#888', padding: '5px' }} onClick={uploadDocsMock}>
                   Upload
                </button>
              </div>
            </div>

            <div className="module-item" style={{ background: 'rgba(255,255,255,0.05)', padding: '15px', borderRadius: '10px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '5px' }}>
                <strong>Liveness Check</strong>
                <span className={`status-badge status-${status?.modules?.find(m=>m.module==='LIVENESS')?.status || 'PENDING'}`}>
                  {status?.modules?.find(m=>m.module==='LIVENESS')?.status || 'PENDING'}
                </span>
              </div>
              {status?.modules?.find(m=>m.module==='LIVENESS')?.confidence_score && (
                <div style={{ fontSize: '0.7rem', color: '#888', marginBottom: '5px' }}>
                  Confidence: {Math.round(status.modules.find(m=>m.module==='LIVENESS').confidence_score * 100)}%
                </div>
              )}
              {status?.modules?.find(m=>m.module==='LIVENESS')?.failure_reason && (
                <div style={{ fontSize: '0.7rem', color: '#ff4b2b', marginBottom: '10px' }}>
                  Error: {status.modules.find(m=>m.module==='LIVENESS').failure_reason}
                </div>
              )}
              <div style={{ display: 'flex', gap: '10px' }}>
                <button className="btn-primary" style={{ padding: '8px 15px', fontSize: '0.7rem', background: 'linear-gradient(90deg, #240b36, #c31432)' }} onClick={() => setCameraMode('liveness')}>
                   Live Verification
                </button>
                <button title="Mock Liveness" style={{ background: 'transparent', border: '1px solid #444', color: '#888', padding: '5px' }} onClick={uploadLivenessMock}>
                   Skip
                </button>
              </div>
            </div>
          </div>

          {status?.overall_status === 'IN_PROGRESS' && status?.modules?.find(m => m.module === 'FACE_COMPARE') && (
            <div style={{ textAlign: 'center', padding: '10px', border: '1px dashed #00d2ff', borderRadius: '10px', color: '#00d2ff' }}>
               AI Analysis in Progress...
            </div>
          )}

          {status?.overall_status === 'COMPLETED' && (
            <div style={{ marginTop: '30px', textAlign: 'center', borderTop: '1px solid rgba(255,255,255,0.1)', paddingTop: '20px' }}>
              <h2 style={{ color: '#00d2ff', marginBottom: '5px' }}>VERIFIED</h2>
              <p style={{ opacity: 0.8 }}>Identity match confidence: {Math.round(status.final_confidence * 100)}%</p>
            </div>
          )}
          
          {status?.overall_status === 'FAILED' && (
            <div style={{ marginTop: '30px', textAlign: 'center', borderTop: '1px solid rgba(255,255,255,0.1)', paddingTop: '20px' }}>
              <h2 style={{ color: '#c31432', marginBottom: '5px' }}>REJECTED</h2>
              <p style={{ opacity: 0.8 }}>Verification threshold not met.</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
