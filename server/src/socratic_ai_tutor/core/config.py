from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # OSS
    OSS_REGION: str
    OSS_BUCKET: str

    # Tutor AI
    TUTOR_API_KEY: str
    TUTOR_BASE_URL: str
    TUTOR_MODEL: str

    # TTS
    # TTS_API_KEY: str
    # TTS_BASE_URL: str
    # TTS_MODEL: str

    # Database
    DATABASE_URL: str

    # Security
    SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"

    # OSS expiration
    OSS_EXPIRE_DAYS: int = 7

    @property
    def OSS_EXPIRE_SECONDS(self) -> int:
        return self.OSS_EXPIRE_DAYS * 86400

    @property
    def REDIS_TTL_SECONDS(self) -> int:
        return self.OSS_EXPIRE_SECONDS - 3600

settings = Settings() # type: ignore
