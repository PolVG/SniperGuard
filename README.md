```text
####################################################################################################
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

## 1) Descripció del projecte

## ¿Què és SniperGuard?

**SniperGuard** és una eina escrita en **Python** amb llicència 'open-source' de tipus 'MIT' que permet executar funcionalitats de **hardening (bastionatge de PCs)** i **cleaning (neteja/manteniment)** en el nostre PC a través de la consola de comandes (Terminal), i fins i tot: a través d'un entorn gràfic (GUI).

El motiu per el qual es bona idea combinar ambes funcionalits, 
es perquè un dels processos vitals del **hardening** d'un PC
es basa en descobrir quins serveis i software instal·lat 
al equip ja no es pas necessari. De fet, aquesta acció va molt lligat
al **cleaning**, on aquest consisteix en netejar tots aquells arxius 
residuals que ocupen massa emmagatzematge al nostre disc dur.

Per tant, aquest software ens ajuda a automatizar un conjunt
de tasques que requereixen d'alta intervenció manual,
amb l'objectiu que l'usuari aprengui i apliqui aquestes funcionalitats
en el menor temps possible.

## 2) Problemes que resol

  **Cleaning**

- **Netejar unitat de disc en pocs clics** 
  Les eines com el 'cleanmgr.exe' de Windows, i el 'SpaceMonguer' (eina que 
  fa un diagrama explicant quines carpetes al PC pesen més) son desconegudes
  pels usuaris no experts en el sector de l'informàtica.
  Per tant, l'objectiu ens ajuda a netejar tota serie d'arxius residuals
  perquè en pocs clics la unitat de disc quedi més buida.

- **Excés manual de 'inputs' del usuari per revisar l'estat d'un PC**
  Els procesos de **Hardening** requereix d'una alta intervenció manual
  i de coneixement per esbrinar quins processos sobren, quins usuaris administradors
  tenen contrasenyes dèbils, com actualizar Windows i Windows Defender, i en si:
  esbrinar quines configuracions dèbils o manques de privacitat posseix l'usuari
  (Ex: La 'calculadora' fa servir la geolocalització del usuari en temps real).

- **Manca d'auditoria del procés de Hardening i/o Cleaing**
SniperGuard disposa d'un sistema de logs complet amb diferents nivells de detall que registra totes les operacions realitzades. Això permet permet als usuaris comprimir, descomprimir o esborrar aquests registres segons les necessitats, i sobretot: coneixer en tot a la carpeta
"/logs" cada una de les acciones que ha fet el programa.
---

## 2) Requisits de sistema i dependències

### Sistema operatiu
- **Només compatible amb Windows 10 i 11**.

### Python
- **Python 3.8 o superior**
- Recomanat: `python` disponible al **PATH**.

### Privilegis
- Es obligatori executar-lo com **Administrador** per arrancar el programari.
- Això es deu a que SniperGuard necessita accés i manipulació de carpetes
  de Windows que només els administradors poden interactuar-hi.

### Dependències Python
 `requirements.txt`:
- `rich==14.2.0`   ( Llibreria que permet crear interficies de terminal amb un toc més elegant).- `Pillow==12.0.0` ( Llibreria que permet a Python tractar amb imatges)

**IMPORTANT!** 'rich' es obligatori per executar la Terminal, 
                mentre que Pillow es obligatori per la GUI.
---


## 3) Passos d’instal·lació (dev)

<<<<<<< HEAD
### 1 — Verificar que tenim els 'PIPs' necessaris
Malgrat que amb "pip list" coneixem els PIPs instal·lats a Python,
simplement executant la comanda: `python -m pip install -r requirements.txt`
ens assegurem de tenir els PIPs necessaris per arrencar SniperGuard.
=======

### 3.1.1 Instal·lar els requeriments si no ho han descarregat prèviament a partir de requirements.txt
`python -m pip install -r requirements.txt`

### 3.1.2 Instal·lar els requeriments manualment
`pip install rich`
`pip install Pillow`


>>>>>>> origin/develop

### Opció A (terminal) i Opció B (GUI)
Tenim a dipossició dos arxius ".py" que ens ajuden a arrencar quina versió volem:
- Terminal: main.py
- GUI: GUI.py


## 4) Instruccions detallades d’ús i exemples

<<<<<<< HEAD
Un cop arrenquem la nostre versió favorita de SniperGuard,
procedim a aprendre que podem fer en cada una d'elles.

### Opció A (terminal) -> main.py
Quan executem `main.py` un cop instal·lats els PIPs: es mostra al
usuari quines opcions tenim.
Per seleccionar cada opció en tots els menús de SniperGuard:
simplement escribim el número del "ID" d'aquella acció,
i premem la tecla "Enter/Intro".
=======
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
>>>>>>> origin/develop

**Exemple recomanat (segur)**
Es recomanable sempre primer inspeccionar que hi ha (BAR),
i un cop estem segurs de l'abast de neteja (DEL) 
o bastionatge (HARD): executar-la.


### 4.1 Menú principal 

Escolleix una opció:
┏━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ ID ┃          Títol          ┃            Descripció            ┃
┡━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ 1. │ Hardening (Bastionatge) │   Permet actualitzar el seu PC   │
├────┼─────────────────────────┼──────────────────────────────────┤
│ 2. │  Neteja i manteniment   │ Permet netejar arxius residuals  │
│    │                         │           del seu PC.            │
├────┼─────────────────────────┼──────────────────────────────────┤
│ 3. │     Gestió de logs      │ Permet comprimir, descomprimir i │
│    │                         │   esborrar logs de SniperGuard   │
├────┼─────────────────────────┼──────────────────────────────────┤
│ 4. │         Sons FX         │   Permet activar el sons FX de   │
│    │                         │           SniperGuard            │
├────┼─────────────────────────┼──────────────────────────────────┤
│ 5. │         Sortir          │ Atura l'execució de SniperGuard  │
└────┴─────────────────────────┴──────────────────────────────────┘

### 4.2 Hardening o Cleaning

Dintre de les opciones de **Hardening** i **Cleaning**, l'usuari pot fer el següent:
- **Mode BAR**: Només inspecciona l'estat actual de l'opció escollida per oferir-nos un informe de la situació.
- **Mode DEL/HARD**: S'executa el **Mode BAR** i aplica al nostre PC la funcionalitat de **Hardening (HARD)** o **Cleaning (DEL)** escollida.

### 4.3 Exemple de Hardening (Bastionatge)

A continuació, es mostren les opcions disponibles en "Hardening".

- **BAR (Identificar / comprovar)**  

┏━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  ID  ┃                         Opció                          ┃
┡━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│  1   │        Comprovar si Windows Defender està actiu        │
├──────┼────────────────────────────────────────────────────────┤
│  2   │ Comprovar si falten actualitzacions a Windows Defender │
├──────┼────────────────────────────────────────────────────────┤
│  3   │  Comprovar si falten actualitzacions a Windows Update  │
├──────┼────────────────────────────────────────────────────────┤
│  4   │                     Tornar al menú                     │
└──────┴────────────────────────────────────────────────────────┘

- **HARD (Aplicar / executar)**  
Si volem executar una acció de "Hardening", aquestes son les opcions.
┏━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  ID  ┃                      Opció                       ┃
┡━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│  1   │      Actualitzar Windows Defender (-30 sec)      │
├──────┼──────────────────────────────────────────────────┤
│  2   │ Actualitzar Windows amb Windows Update (+10 min) │
├──────┼──────────────────────────────────────────────────┤
│  3   │                  Tornar al menú                  │
└──────┴──────────────────────────────────────────────────┘

- **Resultat Hardening** 
Es mostrarà durant l'execució quin script de Python ha executat
el codi PowerShell necessari per dur a terme aquella acció.
De fet, es mostrarà una icona d'status amb el temps trigat
a executar aquella acció per donar feedback al usuari
de quan s'inicia, i quan s'atura el procés.

Finalment, tota acció definitiva realitzada a SniperGuard:
es retorna al menú principal.
---

### 4.4 Exemple de Cleaning (Neteja i manteniment)
Dos modes principals:

- **BAR**: inspecció (no elimina res).
- **DEL**: inspecció + eliminació.

### 4.4 Exemple de Cleaning (Neteja i manteniment)
A continuació, es mostren les opcions disponibles de "Cleaning".
┏━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  ID  ┃                   Opció                    ┃
┡━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│  1   │           Estat arxius temporals           │
├──────┼────────────────────────────────────────────┤
│  2   │ Estat navegadors (historial/cookies/caché) │
├──────┼────────────────────────────────────────────┤
│  3   │        Estat paperera de reciclatge        │
├──────┼────────────────────────────────────────────┤
│  4   │ Estat carpeta 'C:\Windows\WinSxS' (+3 min) │
├──────┼────────────────────────────────────────────┤
│  5   │               Tornar al menú               │
└──────┴────────────────────────────────────────────┘

- **DEL (Aplicar / executar)**  
┏━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  ID  ┃                      Opció                      ┃
┡━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│  1   │            Netejar arxius temporals             │
├──────┼─────────────────────────────────────────────────┤
│  2   │  Netejar navegadors (historial/cookies/caché)   │
├──────┼─────────────────────────────────────────────────┤
│  3   │          Buidar paperera de reciclatge          │
├──────┼─────────────────────────────────────────────────┤
│  4   │ Realitzar una neteja ràpida amb 'cleanmgr.exe'  │
├──────┼─────────────────────────────────────────────────┤
│  5   │  Realitzar una neteja lenta amb 'cleanmgr.exe'  │
├──────┼─────────────────────────────────────────────────┤
│  6   │ Esborrar arxius residuals a 'C:\Windows\WinSxS' │
├──────┼─────────────────────────────────────────────────┤
│  7   │                 Tornar al menú                  │
└──────┴─────────────────────────────────────────────────┘

- **Resultat Cleaning** 
Es mostrarà durant l'execució quin script de Python ha executat
el codi PowerShell necessari per dur a terme aquella acció.
De fet, es mostrarà una icona d'status amb el temps trigat
a executar aquella acció per donar feedback al usuari
de quan s'inicia, i quan s'atura el procés.

Finalment, tota acció definitiva realitzada a SniperGuard:
es retorna al menú principal.

---
### 4.5 Gestió de logs

A SniperGuard volem donar feedback en tot moment del que està fent el nostre
programa quan s'executa al seu PC. Tot i així, pot existir un rang d'usuaris
que tots els logs no els interissi, es a dir: només vulgui veure logs
si cumpleix certa categoria: DEBUG, INFO, NOTICE, WARNING, ERROR.

┏━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ ID ┃        Títol         ┃                 Descripció                  ┃
┡━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ 1. │   Comprimir (ZIP)    │       Comprimeix els logs en un .ZIP        │
├────┼──────────────────────┼─────────────────────────────────────────────┤
│ 2. │ Descomprimir (UNZIP) │      Descomprimeix els logs d'un .ZIP       │
├────┼──────────────────────┼─────────────────────────────────────────────┤
│ 3. │    Esborrar logs     │    Esborra tots els logs de SpineGuard.     │
├────┼──────────────────────┼─────────────────────────────────────────────┤
│ 4. │    Baròmetre logs    │ Defineix quina categoria de logs a mostrar. │
├────┼──────────────────────┼─────────────────────────────────────────────┤
│ 5. │        Sortir        │          Tornar al menú principal           │
└────┴──────────────────────┴─────────────────────────────────────────────┘


-  Baròmetre logs : El canvi del **nivell mínim de logs** es guarda al fitxer `config/config.ini`
                    amb l'objectiu que SniperGuard carregui per defecte aquella configuració
                    de logs cada cop que s'inicií. 
---

### 4.6 Sons FX
Permet activar o desactivar sons mentre s'utilitza SniperGuard.

Els `.wav` estan a `sounds/` i s’executen amb la llibreria
`winsound` (no requereix PIP, només 'import').

RECORDA! Els sons estan desactivats per defecte, i requereixen
         activar-los manualment per cada cop que l'usuari els vulgui.

Els fitxers son:
- `reloading.mp3` -> L'usuari ha d'escollir una opció a executar a SniperGuard.
- `gun.mp3` -> L'usuari escolleix una opció a executar a SniperGuard.
- `shell.mp3` -> L'usuari vol tornar al menú principal.
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



