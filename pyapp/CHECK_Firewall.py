import subprocess
from modules.LogRegister import log

'''
Aquesta funció psesta feta per IA per comprovar si el Firewall de Windows està activat.
'''
ps = "Get-NetFirewallProfile | Select-Object Name, Enabled"


resultat = subprocess.run(
    ["powershell", "-Command", ps],
    capture_output=True,
    text=True
)

text = resultat.stdout #Nomes s'agafa l'output de la comanda sense errors
print(text)


if "False" in text:
    log("El Firewall esta desactivat.", 200)
else:
    log("El Firewall esta activat.", 200)

