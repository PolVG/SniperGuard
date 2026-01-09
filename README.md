```text
####################################################################################################
##................................................................................................##
##...........................................................%#########...........................##
##.........................................................##############.........................##
##........................................................################........................##
##.......................................................#################%.......................##
##.......................................................##################.......................##
##.......................................................##################.......................##
##.......................................................#::-::::=%-#######.......................##
##.......#########################################.......###################*.....................##
##.......##.....................................##........%##......#########=#....................##
##.......##.......................................%.#####..################=####+.................##
##.......##......----:--:-.......::..:-....+############*...+#############=#########..............##
##.......##....................:-:::-::...#:::###-##=......#############=####=%#######%...........##
##.......##.......--.:---.......:...::-...#::-##=######%########################======+#..........##
##.......##.......:-.-.--.....=-::::-:......:..####=##########################==-======*#.........##
##.......##........-.-.--......::..:::......###=*############################==##======-##........##
##.......##..............................###*###############################+##=========##=.......##
##.......##..............:--........#.%########=---=####-=###################==========###%.......##
##.......##.........::.:::.......+#################==#######################===========####.......##
##.......##.......::::.:::.....#-######..#########=====*###################+%%*=======####%.......##
##.......##.......--:-.-::::...#*#=.........###########=##==###############*=========######.......##
##.......##.........:-:......................@############==#+===############=======######-.......##
##.......##.....................................##.*#########============##==##===########........##
##.......##.....................................##...##########===-==-=====#+====#########........##
##.......#########################################......#########+##=====--=#====########%........##
##.........................................................############+=##===+##########.........##
##......###########################################%.........###%###########==###########.........##
##.....##############################################.........###########################.........##
##...:#################################################.......##########################=.........##
##....################################################=.......###########################.........##
##............................................................%##########################.........##
##................................................................................................##
##................................................................................................##
##.....#####............##@............................@####%................................%#%..##
##...###...+:........................................%##%...%................................%#%..##
##...###......=#*#####..##..##-####....#####...#####-##.........##...##..*######..##=##.:######%..##
##....%#####..:##...##..##..##%...##..##...##..##:..###...####..##...##.......##..###...##...%#%..##
##........%##.:##...##..##..##%...##*########..##...%##.....##..##...##..#######..##...###...%##..##
##...#....###.:##...##..##..##%...##..##.......##....###....##..##...##..##...##..##....##...%#%..##
##...######%..-##...##..##..##+####....######..##.....-######%..%###%##..#######..##.....######%..##
##..........................##%...................................................................##
##..........................##@...................................................................##
##................................................................................................##
####################################################################################################
```

# SniperGuard

## 1) Descripció del projecte i problema que resol

**SniperGuard** és una eina escrita en **Python** orientada a **Windows** que permet fer **hardening (bastionatge)** i **cleaning (neteja/manteniment)** del sistema mitjançant un menú per consola.

Problemes que resol:
- **Manteniment deficient** del PC (acumulació de temporals, residus, caché/historial de navegadors, paperera plena).
- **Desconeixement de l’estat de seguretat/actualització** (Windows Defender i Windows Update).
- Necessitat de tenir **traçabilitat**: l’eina registra accions i errors en **fitxers de log**.

L’eina funciona amb dos enfocaments:
- **Mode BAR**: inspecció/identificació (només comprovar estat).
- **Mode DEL/HARD**: comprovar + executar accions (neteja o actualització).

---

## 2) Requisits de sistema i dependències

### Sistema operatiu
- **Windows**.

### Python
- **Python 3.8 o superior**
- Recomanat: `python` disponible al **PATH**.

### Privilegis
- Cal executar com a **Administrador** per tenir funcionalitat completa (SniperGuard comprova permisos i pot aturar-se si no són suficients).

### Dependències Python
 `requirements.txt`:
- `rich==14.2.0` (interfície de terminal: taules, panells, progrés)
- `Pillow==12.0.0` (relacionat amb GUI/imatges si s’utilitza)

---

## 3) Passos d’instal·lació (dev)


### 3.1.1 Instal·lar els requeriments si no ho han descarregat prèviament a partir de requirements.txt
`python -m pip install -r requirements.txt`

### 3.1.2 Instal·lar els requeriments manualment
`pip install rich`
`pip install Pillow`





## 4) Instruccions detallades d’ús i exemples

### 4.1 Arrencada desde GUI
Executa (millor com a administrador):

```cmd 
python GUI.py
```

### 4.2 Arrencada desde consola
Executa (millor com a administrador):

```cmd 
python main.py
```

Això llança `main.py` després de verificar dependències.

### 4.2 Menú principal (consola)
Des de `main.py` apareix un menú amb:
1. **Hardening (Bastionatge)**
2. **Cleaning (Neteja i manteniment)**
3. **Gestió de logs**
4. **Sons FX**
5. **Sortir**

Les accions reals es duen a terme executant scripts de la carpeta `pyapp/`.



### 4.3 Hardening (Bastionatge)
Hi ha dos modes:

- **BAR (Identificar / comprovar)**  
  Exemples (segons el menú):
  - Comprovar si Windows Defender està actiu
  - Comprovar si falten actualitzacions de Windows Defender
  - Comprovar si falten actualitzacions de Windows Update

- **HARD/DEL (Aplicar / executar)**  
  Exemples (segons el menú):
  - Actualitzar Windows Defender
  - Actualitzar Windows amb Windows Update (pot trigar minuts)

**Exemple**
1) `python start.py`  
2) Tria `1` (Hardening)  
3) Tria mode (BAR o HARD)  
4) Tria una opció i prem Enter

---

### 4.4 Cleaning (Neteja i manteniment)
Dos modes principals:

- **BAR**: inspecció (no elimina res).
- **DEL**: inspecció + eliminació.

Opcions habituals (segons menú):
- Arxius temporals
- Navegadors (historial/cookies/caché)
- Paperera de reciclatge
- DISM (WinSxS) i `cleanmgr.exe` (neteja ràpida/lenta)

**Exemple recomanat (segur)**
1) Executa primer en mode **BAR** per veure què hi ha.
2) Després repeteix en mode **DEL** per fer la neteja.

---

### 4.5 Gestió de logs
Permet:
- **Comprimir** logs (ZIP)
- **Descomprimir** logs (UNZIP)
- **Esborrar** logs
- Canviar el **nivell mínim de logs** (“baròmetre”), guardat a `config/config.ini`

Els logs es guarden a `logs/`.

---

### 4.6 Sons FX
Permet activar/desactivar sons mentre s’utilitza SniperGuard.
Els `.wav` estan a `sounds/` i s’executen amb `winsound`.

---

## 5) Breu descripció de l’estructura del codi



- `main.py`  
  Lògica principal de l’aplicació per consola:
  - menús (Hardening/Cleaning/Logs/Sons)
  - comprovació de permisos d’administrador
  - executor de scripts (`run_script`) que llança scripts de `pyapp/`
  - interfície per consola amb Rich
  - integració amb logs

- `pyapp/`  
  Scripts de tasques (hardening i cleaning) executats des del menú.

- `modules/LogRegister.py`  
  Sistema de logs:
  - crea fitxer de log per execució
  - nivells (DEBUG/INFO/NOTICE/WARNING/ERROR)
  - lectura/escriptura del nivell mínim via `config/config.ini`

- `recursos.py`  
  Utilitats:
  - validació d’entrada (`check_input_user`)
  - comprovació d’admin
  - compressió/descompressió/esborrat de logs
  - reproducció de sons

- `config/`  
  Configuració (p. ex. `config.ini` per al nivell de logs).

- `logs/`  
  Emmagatzematge de logs.

- `sounds/`, `img/`, `GUI.py`  
  Recursos multimèdia i possible GUI.



