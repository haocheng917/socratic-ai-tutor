import os
import sys

OSS_REGION = os.getenv("OSS_REGION")
OSS_BUCKET = os.getenv("OSS_BUCKET")
API_KEY = os.getenv('API_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')

if not OSS_REGION or not OSS_BUCKET:
    print("致命错误：缺少 OSS_REGION 或 OSS_BUCKET 环境变量，请检查 .env 文件！")
    sys.exit(1)

OSS_EXPIRE_DAYS = 7
REDIS_TTL_SECONDS = (OSS_EXPIRE_DAYS * 24 * 60 * 60) - 3600
OSS_EXPIRE_SECONDS = OSS_EXPIRE_DAYS * 24 * 60 * 60
