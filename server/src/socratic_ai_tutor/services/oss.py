import datetime
from ..config import OSS_BUCKET, OSS_REGION, OSS_EXPIRE_SECONDS
import alibabacloud_oss_v2 as oss
from uuid import uuid4

cfg = oss.config.load_default()
cfg.region = OSS_REGION
cfg.credentials_provider = oss.credentials.EnvironmentVariableCredentialsProvider()
client = oss.Client(cfg)


class StorageService:
    @staticmethod
    def upload_image(image_bytes: bytes, image_ext: str):
        try:
            key = f"{uuid4().hex}{image_ext}"
            client.put_object(
                oss.PutObjectRequest(
                    bucket=OSS_BUCKET,
                    key=key,
                    body=image_bytes
                )
            )
            return key
        except Exception as e:
            raise Exception(f"上传失败: {e}")

    @staticmethod
    def create_presign(key: str):
        try:
            print(f'Key: {key}')
            presign_result = client.presign(
                oss.GetObjectRequest(bucket=OSS_BUCKET, key=key),
                expires=datetime.timedelta(seconds=OSS_EXPIRE_SECONDS)
            )
            print(presign_result)
            return presign_result.url
        except Exception as e:
            raise Exception(f"签名失败: {e}")
