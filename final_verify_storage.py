import sys
import os
import base64

# Add project root to path
sys.path.append(os.getcwd())

from core.storage import storage_manager

div_secret_id = "final_test_folder"
VALID_B64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
content = base64.b64decode(VALID_B64)

print(f"Uploading to bucket: {storage_manager.bucket_name}")
res = storage_manager.upload_file(content, f"{div_secret_id}/test_image.jpg")
print(f"Result: {res}")

print("\nListing all objects:")
objects = storage_manager.client.list_objects(storage_manager.bucket_name, recursive=True)
for obj in objects:
    print(f" - {obj.object_name}")
