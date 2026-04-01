import io
import os
import logging
logger = logging.getLogger("KYC_GATEWAY")
from minio import Minio
from minio.error import S3Error

class StorageManager:
    def __init__(self):
        self.client = Minio(
            os.getenv("MINIO_ENDPOINT", "localhost:9000"),
            access_key=os.getenv("MINIO_ROOT_USER", "minioadmin"),
            secret_key=os.getenv("MINIO_ROOT_PASSWORD", "minioadmin"),
            secure=False
        )
        self.bucket_name = "kyc-verification-docs"
        self._ensure_bucket()

    def _ensure_bucket(self):
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
        except Exception:
            # Fallback for when MinIO isn't running - use local folder
            os.makedirs("local_storage", exist_ok=True)

    def upload_file(self, content_bytes, object_name, content_type="image/jpeg"):
        try:
            data = io.BytesIO(content_bytes)
            self.client.put_object(
                self.bucket_name,
                object_name,
                data=data,
                length=len(content_bytes),
                content_type=content_type
            )
            res = f"s3://{self.bucket_name}/{object_name}"
            logger.info(f"Storage: Successfully uploaded {object_name} to {res}")
            return res
        except Exception as e:
            # Fallback to local file storage if S3 fails
            logger.error(f"Storage Error: MinIO upload failed for {object_name}. Reason: {e}")
            local_path = os.path.join("local_storage", object_name.replace("/", "_"))
            with open(local_path, "wb") as f:
                f.write(content_bytes)
            return f"local://{local_path}"

storage_manager = StorageManager()
