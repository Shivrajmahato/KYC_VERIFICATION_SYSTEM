import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

try:
    from core.storage import storage_manager
    print("Storage Manager initialized.")
    
    test_content = b"test data"
    res = storage_manager.upload_file(test_content, "diag/test.txt", "text/plain")
    print(f"Upload result: {res}")
    
    if os.path.exists("local_storage"):
        print(f"local_storage exists. Contents: {os.listdir('local_storage')}")
    else:
        print("local_storage does NOT exist.")
        
except Exception as e:
    print(f"Error: {e}")
