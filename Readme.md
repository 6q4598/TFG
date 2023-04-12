[![ForTheBadge winter-is-coming](http://ForTheBadge.com/images/badges/winter-is-coming.svg)](http://ForTheBadge.com)
[![ForTheBadge built-with-love](http://ForTheBadge.com/images/badges/built-with-love.svg)](https://GitHub.com/Naereen/)
[![ForTheBadge powered-by-electricity](http://ForTheBadge.com/images/badges/powered-by-electricity.svg)](http://ForTheBadge.com)
[![ForTheBadge uses-git](http://ForTheBadge.com/images/badges/uses-git.svg)](https://GitHub.com/)

![powered-by-francesc-arrufi](https://user-images.githubusercontent.com/55920937/200260447-dfed043a-6ff3-471d-b6b3-4e9601472b21.svg)

![chronology-this-is-a-diary-from-my-tfg-process](https://user-images.githubusercontent.com/55920937/201152650-08d420c4-5ad6-4d96-bb12-2a7dee1c6c52.svg)

APUNTS TFG
===========
Repositori del meu treball de fi de grau.

Aquest repositori conté tota la informació, investigació i treball realitzat durant tan llarg viatge.

[![Generic badge](https://img.shields.io/badge/License-Apache2-<COLOR>.svg)](https://github.com/6q4598/TFG/blob/main/LICENSE)
[![Generic badge](https://img.shields.io/badge/Web-cellerarrufi.com-<COLOR>.svg)](https://www.cellerarrufi.com)

ESTRUCTURA
==========
- Flask: conté el servidor Flask i els fitxers necessàris per a la pàgina web.
- PreviousWork: conté tota la investigació prèvia i les diferents proves i testos que s'han realitzat fins que es va decidir de fer-ho amb Flask.
- RaspyCom: conté els fils de comunicació amb el PLC i d'escriptura a la base de dades, així com la clase que calcula l'OEE.

Flask
-----
Conté el servidor Flask, així com la pàgina web i tots els seus fitxers.

- Static
	- BD
	- css
	- img
	- js
- templates
- api.py
- requeriments.txt

PreviousWork
------------
Conté tota la investigació prèvie sobre .NET, MVC, Dockers, Cosmos DB etc. Al final es va decidir fer-ho tot amb Flask i Python, amb una Raspberry PI, pel que això es va rebutjar.

- ApiNet
		- IOT4246
		- IOT4246_mvc
		- Screenshots
- ArduinoCode
		- libraries
		- sketchEsp32Linux
- BackupsDatabase
- Documents
- Esp32LinuxSockets
- Apunts diversos.

RaspyCom
--------
Amb els fils de comunicació amb el PLC, i d'escriptura a la base de dades. També conté la classe que fa el càlcul de l'OEE i tots els seus paràmetres.

- util
- main.py
- oee.py
- main.py
