"""
TOT EL CONTINGUT D'AQUEST SCRIPT ESTA FET AMB IA. EN LA SEGUENT ENTREGA ES SUBSTITUIRA PER CODI HUMÀ.
"""

import subprocess
import json

def run_ps(ps: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps],
        capture_output=True,
        text=True
    )

def list_updates():
    ps = r"""
    $ErrorActionPreference = 'Stop'
    $session  = New-Object -ComObject Microsoft.Update.Session
    $searcher = $session.CreateUpdateSearcher()
    $result   = $searcher.Search("IsInstalled=0 and IsHidden=0")

    $items = @()
    for ($i=0; $i -lt $result.Updates.Count; $i++) {
        $u = $result.Updates.Item($i)
        $kbs = @()
        try { $kbs = @($u.KBArticleIDs) } catch {}
        $items += [pscustomobject]@{
            index = $i
            title = $u.Title
            kb = ($kbs -join ",")
            reboot_required = $u.RebootRequired
            is_downloaded = $u.IsDownloaded
            can_request_user_input = $u.InstallationBehavior.CanRequestUserInput
            requires_network = $u.InstallationBehavior.RequiresNetworkConnectivity
        }
    }

    [pscustomobject]@{
        count = $items.Count
        updates = $items
    } | ConvertTo-Json -Depth 5
    """
    p = run_ps(ps)
    if p.returncode != 0 or not p.stdout.strip():
        raise RuntimeError(p.stderr.strip() or "No s'ha pogut obtenir el llistat d'updates.")
    return json.loads(p.stdout)

def install_updates_one_by_one():
    ps = r"""
    $ErrorActionPreference = 'Stop'

    function HexHresult([int]$hr) {
        $u = [uint32]$hr
        return ('0x{0:X8}' -f $u)
    }

    $session  = New-Object -ComObject Microsoft.Update.Session
    $searcher = $session.CreateUpdateSearcher()
    $result   = $searcher.Search("IsInstalled=0 and IsHidden=0")

    if ($result.Updates.Count -eq 0) {
        Write-Host "No hi ha actualitzacions pendents."
        return
    }

    for ($i=0; $i -lt $result.Updates.Count; $i++) {
        $u = $result.Updates.Item($i)

        Write-Host ""
        Write-Host "====================================================="
        Write-Host ("Instal·lant: " + $u.Title) -ForegroundColor Cyan

        # Acceptar EULA si cal
        try {
            if (-not $u.EulaAccepted) { $u.AcceptEula() | Out-Null }
        } catch {}

        # Descarregar només aquesta update
        $coll = New-Object -ComObject Microsoft.Update.UpdateColl
        $coll.Add($u) | Out-Null

        Write-Host "-> Descarregant..."
        $downloader = $session.CreateUpdateDownloader()
        $downloader.Updates = $coll
        $dres = $downloader.Download()

        Write-Host ("   Download ResultCode: " + $dres.ResultCode)
        if ($dres.ResultCode -ne 2) {
            # 2 = Succeeded
            Write-Host "   ⚠️ Download no OK. Saltem a la següent." -ForegroundColor Yellow
            continue
        }

        Write-Host "-> Instal·lant..."
        $installer = $session.CreateUpdateInstaller()
        $installer.Updates = $coll
        $ires = $installer.Install()

        Write-Host ("   Install ResultCode: " + $ires.ResultCode)
        Write-Host ("   RebootRequired    : " + $ires.RebootRequired)

        # Resultat detallat per update
        $ur = $ires.GetUpdateResult(0)
        Write-Host ("   Update HResult    : " + (HexHresult $ur.HResult))
        Write-Host ("   Update ResultCode : " + $ur.ResultCode)

        if ($ur.HResult -ne 0) {
            Write-Host "   ❌ Aquesta update ha fallat (veus l'HRESULT a dalt)." -ForegroundColor Red
        } else {
            Write-Host "   ✅ Aquesta update OK." -ForegroundColor Green
        }
    }

    Write-Host ""
    Write-Host "===== FI PROCÉS ====="
    """
    p = run_ps(ps)
    print("\n[STDOUT]\n" + (p.stdout or ""))
    if p.stderr and p.stderr.strip():
        print("\n[STDERR]\n" + p.stderr)

def main():
    print("===== WINDOWS UPDATE — LLISTA + INSTAL·LACIÓ =====\n")

    data = list_updates()
    n = data.get("count", 0)
    updates = data.get("updates", [])

    if n == 0:
        print("OK: No hi ha actualitzacions pendents.")
        return

    print(f"Actualitzacions pendents: {n}\n")
    for u in updates:
        kb = f" (KB:{u['kb']})" if u.get("kb") else ""
        flags = []
        if u.get("is_downloaded"): flags.append("downloaded")
        if u.get("can_request_user_input"): flags.append("user-input")
        if u.get("reboot_required"): flags.append("reboot")
        extra = f" [{', '.join(flags)}]" if flags else ""
        print(f" - {u['title']}{kb}{extra}")

    ans = input("\nVols instal·lar-les ara? (s/N): ").strip().lower()
    if ans != "s":
        print("Operació cancel·lada.")
        return

    print("\nWARNING: Instal·laré UNA A UNA i imprimiré el resultat detallat.")
    install_updates_one_by_one()

if __name__ == "__main__":
    main()
    input("\nPrem ENTER per sortir...")
