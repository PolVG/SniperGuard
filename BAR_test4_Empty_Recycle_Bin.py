import subprocess

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

    try:
        return float(p.stdout.strip())
    except Exception:
        return 0.0


def barometre(size_mb):
    if size_mb >= URGENT_MB:
        return "🔴", "URGENT — La paperera ocupa molt espai"
    elif size_mb >= RECOMMENDED_MB:
        return "🟡", "RECOMANABLE — Pots alliberar espai fàcilment"
    else:
        return "🟢", "NO CAL — Però no fa mal buidar-la"


def diagnosticar_papelera():
    print("===== DIAGNÒSTIC PAPERERA DE RECICLATGE =====")

    size_mb = get_recycle_bin_size_mb()
    color, msg = barometre(size_mb)

    print(f"Mida total paperera : {size_mb} MB")
    print(f"Baròmetre           : {color} {msg}")

    if size_mb == 0:
        print("ℹ️ La paperera ja està buida.")


if __name__ == "__main__":
    diagnosticar_papelera()

