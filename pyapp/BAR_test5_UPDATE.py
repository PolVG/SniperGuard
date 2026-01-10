"""
TOT EL CONTINGUT D'AQUEST SCRIPT ESTA FET AMB IA. EN LA SEGUENT ENTREGA ES SUBSTITUIRA PER CODI HUMÀ.
"""

import subprocess, json
from datetime import datetime, timezone

def run_ps(ps: str):
    return subprocess.run(
        ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps],
        capture_output=True, text=True
    )

def main():
    ps = r"""
    $ErrorActionPreference = 'SilentlyContinue'

    $pending = @()
    try {
        $session  = New-Object -ComObject Microsoft.Update.Session
        $searcher = $session.CreateUpdateSearcher()
        $result   = $searcher.Search("IsInstalled=0 and IsHidden=0")

        for ($i=0; $i -lt $result.Updates.Count; $i++) {
            $u = $result.Updates.Item($i)

            # KB IDs (si n'hi ha)
            $kbs = @()
            try { $kbs = @($u.KBArticleIDs) } catch {}

            $pending += [pscustomobject]@{
                title = $u.Title
                kb    = ($kbs -join ",")
                reboot_required = $u.RebootRequired
                is_downloaded   = $u.IsDownloaded
            }
        }
    } catch {}

    # "Restart pending" (sense instal·lar res)
    $rebootPending = $false
    if (Test-Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Component Based Servicing\RebootPending") { $rebootPending = $true }
    if (Test-Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update\RebootRequired") { $rebootPending = $true }

    [pscustomobject]@{
        pending_count = $pending.Count
        reboot_pending = $rebootPending
        pending = $pending
    } | ConvertTo-Json -Depth 5
    """

    p = run_ps(ps)
    data = json.loads((p.stdout or "{}") or "{}")

    pending_count = int(data.get("pending_count", 0) or 0)
    reboot_pending = bool(data.get("reboot_pending", False))
    pending = data.get("pending", []) or []

    print("===== WINDOWS UPDATE — BARÒMETRE (DIAGNÒSTIC) =====")
    print(f"Updates pendents   : {pending_count}")
    print(f"Reinici pendent    : {'SÍ' if reboot_pending else 'NO'}")

    if pending_count == 0:
        print("\nOK — No hi ha actualitzacions pendents.")
        return

    # Baròmetre simple: si hi ha pendents -> 🔴
    print("\nURGENT — Tens actualitzacions pendents per instal·lar.\n")
    for u in pending:
        title = u.get("title", "")
        kb = u.get("kb", "")
        reboot = u.get("reboot_required", False)
        downloaded = u.get("is_downloaded", False)
        extra = []
        if kb:
            extra.append(f"KB:{kb}")
        if downloaded:
            extra.append("downloaded")
        if reboot:
            extra.append("reboot-required")
        suffix = f" ({', '.join(extra)})" if extra else ""
        print(f" - {title}{suffix}")

if __name__ == "__main__":
    main()
