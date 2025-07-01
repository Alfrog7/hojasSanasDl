from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Clase para gestionar la configuración de la aplicación.
    Lee automáticamente las variables del archivo .env.
    """
    DATABASE_URL: str


    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()