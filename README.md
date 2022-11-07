[![ForTheBadge winter-is-coming](http://ForTheBadge.com/images/badges/winter-is-coming.svg)](http://ForTheBadge.com)
[![ForTheBadge built-with-love](http://ForTheBadge.com/images/badges/built-with-love.svg)](https://GitHub.com/Naereen/)
[![ForTheBadge powered-by-electricity](http://ForTheBadge.com/images/badges/powered-by-electricity.svg)](http://ForTheBadge.com)
[![ForTheBadge uses-git](http://ForTheBadge.com/images/badges/uses-git.svg)](https://GitHub.com/)
![powered-by-francesc-arrufi](https://user-images.githubusercontent.com/55920937/200260447-dfed043a-6ff3-471d-b6b3-4e9601472b21.svg)


[![Generic badge](https://img.shields.io/badge/License-Apache2-<COLOR>.svg)](https://github.com/6q4598/TFG/blob/main/LICENSE)
[![Generic badge](https://img.shields.io/badge/Web-cellerarrufi.com-<COLOR>.svg)](https://www.cellerarrufi.com)

APUNTS TFG
===========

- Migrar AZURE
	- Cost imprevist i elevat.
	- No sabem com funciona (és una màquina virtual? qui sap :( ) 
	- Quina seria millor forma:
		- Màquina virtual hostatjada (Azure, AWS etc.).
		- Màquina física a les oficines de INGIMEC.
		- Canviar el dispositiu ESP32 actual per una Raspberry, i fer que aquesta actués directament de servidor.
		- Crear un Linux Container, amb un servidor LAMP, que podría estar hostatjat en un PC ubicat a les oficines d'ingimec.
			- Això permet crear tants containers com projectes es desenvolupin.
			- Qualsevol màquina de producció d'Ingimec aniria a parar al mateix lloc. Tot centralitzat.
		
- Canviar dispositiu que envia les dades.
	- Actualment es una ESP32 de 10 entrades/sortides de la marca Industrial Shields.
	- Això comporta algunes problemàtiques:
		- Aquest dispositiu, al tenir nomès 10 IOs, no pot implementar moltes de les funcionalitats especificades.
		- No sabem com crear una dualitat entre els seus dos núclis. Tot i que crec que és posible, en el seu moment no se sabia com fer-ho. Apunts:
			- Jordi d'Industrial Shield va aconseguir implementar una funcionalitat en l'Arduino IDE que permetia usar els dos nuclis al mateix temps.
			- Si això és pot fer, no se com podría afectar al nostre dispositiu.
			- Pot ser molt complex d'implementar, inclús podria afectar negativament en el rendiment.
		- Actualment, si es volen enviar dos o més dades al mateix temps aquestes es perden.
	- Una raspberry podria solucionar alguns d'aquests problemes, a més que podría actuar de micro-servidor cap a N altres màquines dispositius conectats a aquesta.
	- Una raspberry també pot comportar problemes:
		- No hi ha protecció contra apagat. Si la RPI es desconecta, el servidor petaria.
		- La seva potència pot ser limitada.
		
- Canviar BD
	- No se amb quina tecnologia està implementada actualment la BD.
	- Envia un format molt raro, similar a JSON:
		- No envia les hores directament, per exemple, si no que ho fa dígit a dígit.
		- Hi ha dades enviades que no sabem què són.
		
- MOLTES DE LES FUNCIONALITATS QUE ES VOLEN IMPLEMENTAR NO ESTAN CREADES ENCARA.
	- Veure Excel "Millores proto.xlsx"


CREACIÓ I CONFIGURACIÓ DE L'ENTORN DE TREBALL
=========================================

- Primer, instalem i configurem la màquina virtual / màquina Linux que ens farà de servidor.
- Después, fem un "apt get" i un "apt upgrade" per acutalizar repositoris i paquets.
- Un cop fet això, podem configurar docker a la màquina virtual, al linux container o a la màquina Linux que farem servir de servidor.

Pasos
-----

#### **1.** Instalar i actualizar.

He fet servir Debian 9, però podem usar qualsevol altra distribució soportada.

*Apuntar els pasos per crear una màquina virtual Linux o el que convingui.*

```
 $ sudo apt install apt-transport-https ca-certificates curl software-properties-common
 $ curl -fsSL https://download.docker.com/linux/debian/gbs | sudo apt-key add -
 $ sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian stretch stable"
 $ sudo apt update
```

#### **2.** Instalar "docker" engine.

```
 $ sudo apt install docker-ce
```

#### **3.** Iniciar docker.

```
 $ sudo dockerd
```

#### **4.** Instalar una imatge de docker.

He fet servir la version "nginx" estable més nova, la 1.22.1. Podem consultar el llistat de les diferents versions actuals de nginx aquí: https://nginx.org/en/download.html

```
 $ sudo docker pull nginx:1.22.1
```

#### **5.** Eliminar una imatge de docker.

```
 $ docker rmi <<IMAGE ID>>
```

#### **6.** See the images installed.

```
 $ sudo docker images
```

#### **7.** Iniciar la imatge de docker amb nginx web server.

```
 $ sudo docker run -name sampleapp -p 80:80 -d nginx:1.22.1
```

#### **8.** Consultar que això funciona.

Primer hem de veure ip pública desde la terminal i consultar-la desde un navegador.

Si estem en una màquina virtual d'Azure o AWS, segurament ens apareixerà en la pàgina de configuració d'aquest.

Si pel contrari estem en un Linux container o en un WLS, o en una altra màquina Linux, podem consultar la ip públic que tenim amb:
ip a # veure apartat eth0.

Si anem a un navegador qualsevol ubicat en la nostra màquina física i posem aquesta ip a la barra d'adreçes ens apareixerà quelcom com: Imatges/nignxWelcomStartPage

Si apaguem el contenidor de docker i al engegarlo ens surt un error com:

> docker: Error response from daemon: Conflict. The container name "/sampleapp" is already in use by container "55081d5847a5312c911d12f048e24f83c94382c009b9b1e8343429f15f4301d1". You have to remove (or rename) that container to be able to reuse that name.
 See 'docker run --help'.

Tindrem de borrar el container que està causant el problema:

```
 $ sudo docker rm 55081d5847a5312c911d12f048e24f83c94382c009b9b1e8343429f15f4301d1
```

#### **9.** Reiniciar una màquina Windows Subsistem Linux (WSL)

Si ens trobem amb algún problema amb la màquina virtual (si aquesta ha estat la nostra opció), sempre podem reiniciar-la fent el següent.

Executant una terminal PowerShell com a administrador, escriure les següents comandes:

```
 $ wsl --shutdown # Per apagar el servei.
 $ wsl --start nomMaquina # Per iniciar-lo.
```

DEPLOY D'UNA APLICACIÓ .NET CORE A LINUX
=====================================

### **1.** Instal·lació de SDK i l'entorn de treball de .NET a Debian

En el meu cas, he fet servir l'última versió de Debian 9.

Per fer-ho, he seguit el manual de microsoft https://learn.microsoft.com/es-es/dotnet/core/install/linux-debian.

Obrim un terminal i executem:

```
 $ wget -O - https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.asc.gpg
 $ sudo mv microsoft.asc.gpg /etc/apt/trusted.gpg.d/
 $ wget https://packages.microsoft.com/config/debian/9/prod.list
 $ sudo mv prod.list /etc/apt/sources.list.d/microsoft-prod.list
 $ sudo chown root:root /etc/apt/trusted.gpg.d/microsoft.asc.gpg
 $ sudo chown root:root /etc/apt/sources.list.d/microsoft-prod.list
```

Amb això hem afegit la clau de la firma del paquet de Microsoft a la llista de claus de confiança. També agreguem el repositori de paquets.

### **2.** Instal·lació de SDK.

SDK permet desenvolupar aplicacions amb .NET.

Instal·lant SDK de .NET, no necessita instalar l'entorn d'execució corresponenet.

Per instalar-ho, executar:

```
 $ sudo apt update
 $ sudo apt install -y dotnet-sdk-6.0
```

Com podem veure, he instal·lat la última versió de SDK fins la data d'avui: la 6.

(ACTUALMENT AQUESTA TECNOLOGIA ESTÀ DESCONTINUADA)

### **3. ** Instal·lació del runtime

L'entorn ASP.NET Core permet executar aplicacions .NET a les quals no s'ha proporcionat l'entorn d'execució.

ASP.NET Core és el més compatible amb .NET.

Es pot instal·lar amb:

```
 $ sudo apt update
 $ sudo apt install -y aspnetcore-runtime-6.0
```

Si hi ha agut el següent error:

> Unable to locate package aspnetcore-runtime-6.0

Es pot consultar la pàgina de manual de microsoft: https://learn.microsoft.com/es-es/dotnet/core/install/linux-debian#apt-troubleshooting

Si fa falta, també podem instalar l'entorn d'execució .NET, el qual no inclou compatibilitat amb ASP.NET:

```
 $ sudo apt install dotnet-runtime-6.0
```

### **4.** Tenir en compte

Que abans s'ha de crear el projecte .NET amb Visual Studio.

### **5.** Migrar el projecte a la màquina virtual Linux

Primer de tot, s'ha de compilar i executar l'aplicació amb el Visual Studio.

Després, hem de copiar la carpeta (carpeta arrel de l'aplicacio)/bin/Debug/netcoreapp3.1/publish a la nostra màquina Linux.

Un cop ho haguem fet, en la carpeta publish de la màquina virtual hem d'executar:

```
 $ dotnet nomAplicacio.dll
```

Hem de comprobar que el servidor està enviant quelcom (executar i mostrar captura).

### **6.** Configuració del servidor Nginx

Anem a /etc/nginx/sites-available i modifiquem el _location_ que hi hagi dins del default per:

Incis: per modificar aquest fitxer es necessiten els permisos adeqüats:

```
sudo chomod 677
```

```
	proxy_pass http://localhost:5000;
	proxy_http_version 1.1;
	proxy_set_header Upgrade $http_upgrade;
	proxy_set_header Connection keep-alive;
	proxy_set_header Host $host;
	proxy_cache_bypass $http_upgrade;
```

Reiniciem el servei i el tornem a executar.

```
 $ sudo service nginx restart
 $ sudo nginx -s reload
```

