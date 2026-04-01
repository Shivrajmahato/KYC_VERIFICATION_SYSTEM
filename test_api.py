import requests
import time
import subprocess
import os
import sys

print("Starting server...")
process = subprocess.Popen([sys.executable, "run.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
time.sleep(5) # Wait for server to start

try:
    print("1. Starting Session...")
    session_payload = {
        "tenant_id": "tenant_A",
        "client_id": "client_001",
        "user_id": "user_123"
    }
    res_start = requests.post("http://127.0.0.1:8005/gateway/session/start", json=session_payload)
    if res_start.status_code != 200:
        print("Error starting session:", res_start.text)
        exit(1)
        
    div_secret_id = res_start.json()["div_secret_id"]
    print(f"Session Started: {div_secret_id}")
    
    print("\n2. Uploading Document...")
    # Valid 1x1 base64 pixels for testing
    VALID_B64 = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
    doc_payload = {
        "document_front_image": VALID_B64,
        "document_back_image": VALID_B64
    }
    res_doc = requests.post(f"http://127.0.0.1:8005/gateway/session/{div_secret_id}/document", json=doc_payload)
    print("Doc upload response:", res_doc.json())
    
    print("\n3. Waiting 1 second, then Uploading Selfie...")
    time.sleep(1)
    live_payload = {
        "selfie_image": VALID_B64
    }
    res_live = requests.post(f"http://127.0.0.1:8005/gateway/session/{div_secret_id}/liveness", json=live_payload)
    print("Liveness upload response:", res_live.json())
    
    print("\n4. Polling status until completion...")
    for _ in range(15):
        time.sleep(1.5)
        res_status = requests.get(f"http://127.0.0.1:8005/gateway/status/{div_secret_id}")
        if res_status.status_code != 200:
            print("Error fetching status:", res_status.text)
            continue
            
        status_data = res_status.json()
        print(f"Overall Status: {status_data['overall_status']} (Score: {status_data.get('final_confidence')})")
        for mod in status_data['modules']:
            print(f"  - {mod['module']}: {mod['status']} (Conf: {mod.get('confidence_score')})")
            
        if status_data['overall_status'] in ["COMPLETED", "FAILED"]:
            print("Finished processing!")
            break
finally:
    print("\nShutting down server...")
    process.kill()
