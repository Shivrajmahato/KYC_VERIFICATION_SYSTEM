import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

try:
    from core.storage import storage_manager
    print(f"Bucket: {storage_manager.bucket_name}")
    
    objects = storage_manager.client.list_objects(storage_manager.bucket_name, recursive=True)
    print("Objects found in MinIO:")
    found = False
    for obj in objects:
        print(f" - {obj.object_name}")
        found = True
    
    if not found:
        print(" (No objects found in MinIO bucket)")
        
except Exception as e:
    print(f"Error: {e}")
