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

# ¿Que es SniperGuard?

SniperGuard es un programa open-source (de código libre) que permite realizar una limpieza 
y bastionado del equipo mediante el uso de código Python.
De este modo, el usuario podrá conocer que programas desfasados, y procesos inservibles 
está consumiendo su PC con el objetivo de erradicarlos del equipo. 


# ¿Que es el hardening?

El hardening se basa en la aplicación de técnicas y proceso orientados a reducir la superficie de ataque, 
corrección de vulnerabilidades conocidas (CVE), mitigación de debilidades de diseño o configuración (CWE), 
eliminación de configuraciones inseguras, y finalmente: cierre de servicios y puertos innecesarios.

En muchos entornos, especialmente corporativos: este bastionado se sigue realizando de forma parcialmente manual,
o con herramientas genéricas del sistema operativo (Ej: cleanmgr.exe). Debido a esto, 
nos obliga a invertir muchas horas en revisar programas instalados, servicios activos
y bloatware preinstalado por fabricantes del equipo adquirido, o por defecto en Windows. 

Esta abundancia de procesos en segundo plano incrementa tanto el riesgo de explotación 
(más servicios potencialmente vulnerables) como el ruido de logs y eventos que debe gestionar
el SOC mediante SIEM, SOAR o XDR: dificultando de este modo la detección rápida de ciberincidentes. 


# ¿Por que debo usar SniperGuard frente a otras herramientas del mercado?

SniperGuard es la fusión de una herramienta de limpieza del equipo + una herramienta de bastionado,
incorporando estas dos utilidades en un solo software.

Con SnipeGuard obtenemos equipos más rápidos y seguros al erradicar todos aquellos 
programas y archivos que el usuario considera 'no esencial', aplicar
automataticamente nuevas actualizaciones de Windows Update y Windows Defender en el equipo, y finalmente:
encontrar vulnerabilidades en el PC debido a software desactualizado, o procesos maliciosos ejecutandose en su PC.

Además, SniperGuard ofrece una GUI y un modo Terminal visualmente agradable y fácil de usar para todo tipo de usuario,
incluyendo una gran cantidad de 'feedback' que se ofrece al usuario para que siempre note que hay un 'sniper' ayudandole a proteger su equipo.

# Como usar SniperGuard versión Alpha

La versión Alpha de SniperGuard contiene las siguientes 
funcionalidades mediante el uso de la Terminal.
De este modo, el usuario debe introducir los números y pulsar Enter
cuando se solicite en el menú.

-- Opciones del menú principal: --

    Cleaning (1):
        Identificar (1): -> Modo Inspección.
         (1)  --> Borrar archivos temporales.
         (2)  --> Borrar cookies, historial y caché de los navegadores web.
         (3)  --> Borrar la papelera de reciclage de Windows.
        
        Identificar + Borrar (2): -> Se inspeccionaran los archivos y se borraran.ds
         (1)  --> Borrar archivos temporales.
         (2)  --> Borrar cookies, historial y caché de los navegadores web.
         (3)  --> Borrar la papelera de reciclage de Windows.
        
    
    Hardening (2): 
        (1) --> Identificar si faltan actualizaciones de Windows Update en el equipo.
        (2) --> Instalar actualizaciones restantes de Windows Update en el equipo.




=======
