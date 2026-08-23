import yaml
from pathlib import Path
from domain.server import Server
from config.paths import diretorio_base

class ConfigServers:
    def __init__(self):
        self._path = diretorio_base() / "servers.yaml"
        self._servers = self._load()

    def _load(self) -> list[Server]:
        if not self._path.exists():
            raise FileNotFoundError(f"Arquivo de config não encontrado: {self._path}")

        with open(self._path) as f:
            dados = yaml.safe_load(f)

        return [Server(**s) for s in dados]

    def list(self) -> list[Server]:
        return self._servers

    def search_by_name(self, name: str) -> Server:
        for servidor in self._servers:
            if servidor.name == name:
                return servidor
        raise ValueError(f"Servidor '{name}' não encontrado na configuração")

config_servers = ConfigServers()