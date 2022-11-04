[![ForTheBadge winter-is-coming](http://ForTheBadge.com/images/badges/winter-is-coming.svg)](http://ForTheBadge.com)
[![ForTheBadge built-with-love](http://ForTheBadge.com/images/badges/built-with-love.svg)](https://GitHub.com/Naereen/)
[![ForTheBadge powered-by-electricity](http://ForTheBadge.com/images/badges/powered-by-electricity.svg)](http://ForTheBadge.com)
[![ForTheBadge uses-git](http://ForTheBadge.com/images/badges/uses-git.svg)](https://GitHub.com/)

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


INSTALL DOCKER
=============

- Primer, instalem i configurem la màquina virtual / màquina Linux que ens farà de servidor.
- Después, fem un "apt get" i un "apt upgrade" per acutalizar repositoris i paquets.
- Un cop fet això, podem configurar docker a la màquina virtual, al linux container o a la màquina Linux que farem servir de servidor.

Pasos
-----

#### **1.** Instalar i actualizar.

He fet servir Debian 9, però podem usar qualsevol altra distribució soportada.

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
