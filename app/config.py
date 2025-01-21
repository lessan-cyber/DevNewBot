from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    bot_token: str  # Clé attendue dans le fichier .env
    quiz_api: str
    gemini_api_key: str
    class Config:
        env_file = ".env"  # Chemin vers le fichier .env
        env_file_encoding = "utf-8"  # Encodage du fichier .env

# Charger les paramètres
settings = Settings()

# Vérification
