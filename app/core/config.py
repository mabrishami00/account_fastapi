from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MONGO_DB: str
    REDIS_URL: str
    SECRET_KEY: str

    ACCESS_KEY_EXPIRE_TIME: int = 3
    REFRESH_KEY_EXPIRE_TIME: int = 10

    SEND_OTP_URL: str = "http://podcast_fastapi:8003/notification/send_otp"

    class Config:
        env_file = "/home/mahdi/Documents/rss_project/account_fastapi/.env"


settings = Settings()
