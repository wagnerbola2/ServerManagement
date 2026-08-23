from dataclasses import dataclass
import win32service


@dataclass
class Service:
    nome: str
    status: win32service
    tentativas_reinicio: int = 0

    def pode_reiniciar(self) -> bool:
        # regra de negócio: não deixa reiniciar mais que 3x seguidas
        return self.tentativas_reinicio < 3

    def registrar_tentativa(self):
        self.tentativas_reinicio += 1