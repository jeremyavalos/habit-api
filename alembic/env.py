from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # 🔹 Base de datos
    DATABASE_URL: str

    # 🔹 Seguridad JWT
    SECRET_KEY: str = "supersecret"
    ALGORITHM: str = "HS256"

    # 🔹 Expiración de tokens
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # 🔹 Configuración de entorno
    model_config = SettingsConfigDict(env_file=".env")


# 🔥 Instancia global
settings = Settings()