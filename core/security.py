import hmac
import hashlib
import uuid
import time
import secrets
import base64

GATEWAY_SECRET = b"dev-secret-gateway-key-replace-in-prod"

def generate_div_secret_id(tenant_id: str, client_id: str) -> dict:
    request_id = str(uuid.uuid4())
    timestamp = str(int(time.time()))
    nonce = secrets.token_hex(8)
    
    message = f"{tenant_id}{client_id}{request_id}{timestamp}{nonce}".encode('utf-8')
    signature = hmac.new(GATEWAY_SECRET, message, hashlib.sha256).digest()
    div_secret_id = base64.urlsafe_b64encode(signature).decode('utf-8')[:32]
    
    return {
        "div_secret_id": div_secret_id,
        "request_id": request_id,
        "timestamp": timestamp,
        "nonce": nonce
    }

def derive_module_session_id(div_secret_id: str, module_name: str) -> str:
    message = f"{div_secret_id}{module_name}".encode('utf-8')
    return hashlib.sha256(message).hexdigest()
