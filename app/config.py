import os
from typing import ClassVar

import pytz
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

EAT_TIMEZONE = pytz.timezone("Africa/Nairobi")


def get_cors_origins():
    origins_str = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173")
    return [origin.strip() for origin in origins_str.split(",") if origin.strip()]


GOOGLE_CREDENTIALS = {
    "type": os.getenv("TYPE", ""),
    "project_id": os.getenv("PROJECT_ID", ""),
    "private_key_id": os.getenv("PRIVATE_KEY_ID", ""),
    "private_key": os.getenv("PRIVATE_KEY", "").replace("\\n", "\n").replace('"', ""),
    "client_email": os.getenv("CLIENT_EMAIL", ""),
    "client_id": os.getenv("CLIENT_ID", ""),
    "auth_uri": os.getenv("AUTH_URI", ""),
    "token_uri": os.getenv("TOKEN_URI", ""),
    "auth_provider_x509_cert_url": os.getenv("AUTH_PROVIDER_X509_CERT_URL", ""),
    "client_x509_cert_url": os.getenv("CLIENT_X509_CERT_URL", ""),
    "universe_domain": os.getenv("UNIVERSE_DOMAIN", ""),
}


class Settings(BaseSettings):
    APP_NAME: str = "Feedback Forwarder API"
    DEBUG: bool = False
    TIMEZONE: ClassVar[pytz.tzinfo.BaseTzInfo] = EAT_TIMEZONE

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
cors_origins = get_cors_origins()
google_credentials = GOOGLE_CREDENTIALS
