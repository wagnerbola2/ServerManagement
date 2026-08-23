import sys
from pathlib import Path

def diretorio_base() -> Path:
    if getattr(sys, "frozen", False):
        # Rodando como .exe empacotado pelo PyInstaller
        return Path(sys.executable).parent
    else:
        # Rodando como script Python normal
        return Path(__file__).resolve().parent.parent