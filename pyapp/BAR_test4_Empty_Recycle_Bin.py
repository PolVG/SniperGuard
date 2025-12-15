import subprocess
from modules.LogRegister import log

# ------------------------------
# CONFIGURACIÓ BARÒMETRE (MB)
# ------------------------------
URGENT_MB = 1024      # 1 GB
RECOMMENDED_MB = 250  # 250 MB


def get_recycle_bin_size_mb():
    """
    Retorna la mida total de la paperera (MB) utilitzant PowerShell.
    Si no hi ha paperera o està buida, retorna 0.
    """
    log("Inici càlcul mida paperera de reciclatge (PowerShell)", 100)

    ps = r"""
    $total = 0
    Get-PSDrive -PSProvider FileSystem | ForEach-Object {
        $rb = Join-Path $_.Root '$Recycle.Bin'
        if (Test-Path $rb) {
            Get-ChildItem $rb -Recurse -Force -ErrorAction SilentlyContinue |
            Where-Object { -not $_.PSIsContainer } |
            ForEach-Object { $total += $_.Length }
        }
    }
    [math]::Round($total / 1MB, 2)
    """

    p = subprocess.run(
        ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps],
        capture_output=True,
        text=True
    )

    if p.returncode != 0:
        log(
            f"PowerShell ha retornat error ({p.returncode}): {p.stderr.strip()}",
            400
        )
        return 0.0

    try:
        size_mb = float(p.stdout.strip())
        log(f"Mida paperera calculada correctament: {size_mb} MB", 200)
        return size_mb
    except Exception as e:
        log(
            f"No s'ha pogut parsejar sortida PowerShell: '{p.stdout.strip()}' ({repr(e)})",
            400
        )
        return 0.0


def barometre(size_mb):
    log(f"Avaluant baròmetre paperera: {size_mb} MB", 100)

    if size_mb >= URGENT_MB:
        return "🔴", "URGENT — La paperera ocupa molt espai"
    elif size_mb >= RECOMMENDED_MB:
        return "🟡", "RECOMANABLE — Pots alliberar espai fàcilment"
    else:
        return "🟢", "NO CAL — Però no fa mal buidar-la"


def diagnosticar_papelera():
    log("==== Inici diagnòstic paperera de reciclatge ====", 200)

    print("===== DIAGNÒSTIC PAPERERA DE RECICLATGE =====")

    size_mb = get_recycle_bin_size_mb()
    color, msg = barometre(size_mb)

    print(f"Mida total paperera : {size_mb} MB")
    print(f"Baròmetre           : {color} {msg}")

    if size_mb == 0:
        log("Paperera buida detectada", 250)
        print("ℹ️ La paperera ja està buida.")
    else:
        log(
            f"Resultat diagnòstic paperera: {size_mb} MB | estat={color}",
            250
        )

    log("==== Fi diagnòstic paperera de reciclatge ====", 200)


if __name__ == "__main__":
    diagnosticar_papelera()
