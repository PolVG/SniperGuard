import subprocess
import sys
from pathlib import Path

import importlib.util


# Ruta del directori on es troba aquest start.py
PROJECT_ROOT = Path(__file__).resolve().parent

# Ruta absoluta al fitxer requirements.txt
REQUIREMENTS = PROJECT_ROOT / "requirements.txt"

# Ruta absoluta al programa principal
MAIN_SCRIPT = PROJECT_ROOT / "main.py"


def requirements_installed() -> bool:
    """
    Comprova si les llibreries crítiques del projecte estan instal·lades.

    Retorna:
        True  si estàn instalades
        False si no ho està
    """

    # Llista mínima de mòduls clau per arrencar SniperGuard
    required_modules = [
        "rich",   # llibreria essencial per la UI de SniperGuard
    ]

    # Recorrem cada mòdul clau
    for module in required_modules:

        # find_spec() retorna None si el mòdul NO existeix
        if importlib.util.find_spec(module) is None:
            return False  # falta alguna dependència

    # Si totes existeixen
    return True



def install_requirements():
    """
    Executa:
        python -m pip install -r requirements.txt

    """

    print("Falten dependencies. Instal·lant-les a través de 'requirements.txt' ...")

    subprocess.check_call([
        sys.executable, "-m", "pip", "install", "-r", 
        str(REQUIREMENTS) # Ruta absoluta a requirements.txt
    ])

    # check_call:
    # - Atura el programa si pip falla


if __name__ == "__main__":
    """
    Flux:
    1: Comprova si les dependències estan instal·lades
    2: Si no ho estan -> executa pip install
    3: Llança el main.py real
    """

    # Pas 1: comprovació ràpida
    if not requirements_installed():
        
        # Pas 2: instal·lació dels PIPs si es necessari.
        install_requirements()

    # Pas 3: executar el main.py de SniperGuard
    subprocess.check_call([
        sys.executable,
        str(MAIN_SCRIPT)
    ])
