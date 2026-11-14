import datetime
from ..config import OSS_BUCKET, OSS_REGION, OSS_EXPIRE_SECONDS, REDIS_TTL_SECONDS
import alibabacloud_oss_v2 as oss
from uuid import uuid4
import redis

cfg = oss.config.load_default()
cfg.region = OSS_REGION
cfg.credentials_provider = oss.credentials.EnvironmentVariableCredentialsProvider()
client = oss.Client(cfg)

redis_client = redis.Redis(host='redis', port=6379,
                           db=0, decode_responses=True)


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

    @staticmethod
    def get_cached_url(key: str):
        cache_key = f"oss_url:{key}"

        try:
            cached_url = redis_client.get(cache_key)
            if cached_url:
                print(f"命中 Redis 缓存: {key}")
                return cached_url
        except Exception as e:
            pass

        fresh_url = StorageService.create_presign(key)

        if fresh_url:
            try:
                redis_client.set(cache_key, fresh_url, ex=REDIS_TTL_SECONDS)
            except Exception as e:
                print(f"Redis 写入失败: {e}")

        return fresh_url
