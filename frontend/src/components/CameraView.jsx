import React, { useRef, useState, useEffect } from 'react';

const CameraView = ({ mode, onCapture, onCancel }) => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [stream, setStream] = useState(null);
  const [timeLeft, setTimeLeft] = useState(60);
  const [isLivenessActive, setIsLivenessActive] = useState(false);

  useEffect(() => {
    startCamera();
    return () => stopCamera();
  }, []);

  const [gesture, setGesture] = useState('Wait...');
  const [snapshots, setSnapshots] = useState([]);

  useEffect(() => {
    let timer;
    if (isLivenessActive && timeLeft > 0) {
      timer = setInterval(() => {
        setTimeLeft(prev => prev - 1);
        // Simulate Gesture Prompts
        if (timeLeft % 15 === 0) setGesture("Blink 3 Times");
        if (timeLeft % 15 === 8) setGesture("Turn Head Left");
        if (timeLeft % 15 === 4) {
            setGesture("Capturing Snapshot...");
            const snap = captureFrame();
            if (snap) setSnapshots(prev => [...prev, snap]);
        }
      }, 1000);
    } else if (timeLeft === 0 && isLivenessActive) {
      handleLivenessComplete();
    }
    return () => clearInterval(timer);
  }, [isLivenessActive, timeLeft]);

  const startCamera = async () => {
    try {
      const mediaStream = await navigator.mediaDevices.getUserMedia({ 
        video: { facingMode: "user" }, 
        audio: false 
      });
      setStream(mediaStream);
      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream;
      }
    } catch (err) {
      console.error("Error accessing camera:", err);
      alert("Could not access camera. Please check permissions.");
      onCancel();
    }
  };

  const stopCamera = () => {
    if (stream) {
      stream.getTracks().forEach(track => track.stop());
    }
  };

  const captureFrame = () => {
    const video = videoRef.current;
    const canvas = canvasRef.current;
    if (video && canvas) {
      const context = canvas.getContext('2d');
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      context.drawImage(video, 0, 0, canvas.width, canvas.height);
      return canvas.toDataURL('image/jpeg');
    }
    return null;
  };

  const handleCaptureDoc = () => {
    const dataUrl = captureFrame();
    if (dataUrl) {
      onCapture(dataUrl);
    }
  };

  const startLiveness = () => {
    setIsLivenessActive(true);
  };

  const handleLivenessComplete = () => {
    const dataUrl = captureFrame();
    setIsLivenessActive(false);
    if (dataUrl) {
      onCapture(dataUrl);
    }
  };

  return (
    <div className="camera-container" style={{
      position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
      background: 'rgba(0,0,0,0.9)', zIndex: 1000,
      display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center'
    }}>
      <div className="glass-card" style={{ position: 'relative', width: '90%', maxWidth: '600px', padding: '10px' }}>
        <h3 style={{ textAlign: 'center' }}>
          {mode === 'document' ? 'Scan Document' : 'Liveness Verification'}
        </h3>
        
        <div style={{ position: 'relative', overflow: 'hidden', borderRadius: '10px', background: '#000' }}>
          <video 
            ref={videoRef} 
            autoPlay 
            playsInline 
            style={{ width: '100%', display: 'block', transform: 'scaleX(-1)' }} 
          />
          
          {mode === 'document' && (
            <div className="scanning-line" style={{
              position: 'absolute', top: 0, left: 0, right: 0, height: '2px',
              background: 'rgba(255, 0, 0, 0.5)', boxShadow: '0 0 10px red',
              animation: 'scan 3s linear infinite'
            }} />
          )}

          {isLivenessActive && (
            <div style={{
              position: 'absolute', bottom: '20px', left: '50%', transform: 'translateX(-50%)',
              background: 'rgba(195, 20, 50, 0.8)', padding: '10px 20px', borderRadius: '10px',
              color: '#fff', fontWeight: 'bold', fontSize: '1.2rem', boxShadow: '0 0 15px rgba(0,0,0,0.5)'
            }}>
              {gesture}
            </div>
          )}

          {isLivenessActive && (
            <div style={{
              position: 'absolute', top: '10px', right: '10px',
              background: 'rgba(0,0,0,0.6)', padding: '5px 15px', borderRadius: '20px',
              border: '1px solid #c31432', color: '#fff', fontWeight: 'bold'
            }}>
              TTL: {timeLeft}s
            </div>
          )}
        </div>

        <canvas ref={canvasRef} style={{ display: 'none' }} />

        <div style={{ display: 'flex', justifyContent: 'center', gap: '20px', marginTop: '20px' }}>
          <button className="btn-primary" style={{ background: '#777' }} onClick={onCancel}>Cancel</button>
          
          {mode === 'document' && (
            <button className="btn-primary" onClick={handleCaptureDoc}>Capture Snapshot</button>
          )}

          {mode === 'liveness' && !isLivenessActive && (
            <button className="btn-primary" onClick={startLiveness}>Start Liveness Session</button>
          )}
          
          {isLivenessActive && (
            <button className="btn-primary" onClick={handleLivenessComplete}>Finish Now</button>
          )}
        </div>
      </div>

      <style dangerouslySetInnerHTML={{ __html: `
        @keyframes scan {
          0% { top: 0; }
          50% { top: 100%; }
          100% { top: 0; }
        }
      `}} />
    </div>
  );
};

export default CameraView;
