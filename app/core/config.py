from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Clase para gestionar la configuración de la aplicación.
    Lee automáticamente las variables del archivo .env.
    """
    DATABASE_URL: str

    # Carga la configuración desde un archivo .env
    model_config = SettingsConfigDict(env_file=".env")


# Creamos una única instancia de la configuración para ser usada en toda la aplicación.
settings = Settings()