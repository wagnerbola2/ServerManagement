from pydantic_settings import BaseSettings
from config.paths import diretorio_base

class Settings(BaseSettings):
    server_user: str
    server_domain: str
    server_password: str
    services_filter: str

    class Config:
        env_file = str(diretorio_base() / ".env")

# instância única, importável em qualquer lugar
settings = Settings()