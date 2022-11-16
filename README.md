[![ForTheBadge winter-is-coming](http://ForTheBadge.com/images/badges/winter-is-coming.svg)](http://ForTheBadge.com)
[![ForTheBadge built-with-love](http://ForTheBadge.com/images/badges/built-with-love.svg)](https://GitHub.com/Naereen/)
[![ForTheBadge powered-by-electricity](http://ForTheBadge.com/images/badges/powered-by-electricity.svg)](http://ForTheBadge.com)
[![ForTheBadge uses-git](http://ForTheBadge.com/images/badges/uses-git.svg)](https://GitHub.com/)

![powered-by-francesc-arrufi](https://user-images.githubusercontent.com/55920937/200260447-dfed043a-6ff3-471d-b6b3-4e9601472b21.svg)

![chronology-this-is-a-diary-from-my-tfg-process](https://user-images.githubusercontent.com/55920937/201152650-08d420c4-5ad6-4d96-bb12-2a7dee1c6c52.svg)

NOTA
====
Aquest diari està recollit cronològicament, de forma que tot el més vell està a la part de dalt de la pàgina i es va baixant a mesura que ha avançat el procés.


Espero que aquest procés de documentació serveixi en un futur per fer la memòria, si més no per aprendre i tindre un "xuletari" on mirar de tant en tant.

APUNTS TFG
===========


[![Generic badge](https://img.shields.io/badge/License-Apache2-<COLOR>.svg)](https://github.com/6q4598/TFG/blob/main/LICENSE)
[![Generic badge](https://img.shields.io/badge/Web-cellerarrufi.com-<COLOR>.svg)](https://www.cellerarrufi.com)


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

He fet servir Debian 9 i Ubuntu 20.04, però podem usar qualsevol altra distribució soportada.

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

#### **1.** Instal·lació de SDK i l'entorn de treball de .NET a Debian

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

#### **2.** Instal·lació de SDK.

SDK permet desenvolupar aplicacions amb .NET.

Instal·lant SDK de .NET, no necessita instalar l'entorn d'execució corresponenet.

Per instalar-ho, executar:

```
 $ sudo apt update
 $ sudo apt install -y dotnet-sdk-6.0
```

Com podem veure, he instal·lat la última versió de SDK fins la data d'avui: la 6.

(ACTUALMENT AQUESTA TECNOLOGIA ESTÀ DESCONTINUADA)

#### **3.** Instal·lació del runtime

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

#### **5.** Execució d'una aplicació .NET en un entorn Linux

Un cop realitzats els pasos anteriors, podem fer correr una aplicació .NET amb la següent comanda (dins d'on tinguem el projecte .csproj).

```
# Aplicació .NET 6.0
$ dotnet run
```

#### **4.** Tenir en compte

Que abans s'ha de crear el projecte .NET amb Visual Studio.

#### **5.** Migrar el projecte a la màquina virtual Linux

Primer de tot, s'ha de compilar i executar l'aplicació amb el Visual Studio.

Després, hem de copiar la carpeta (carpeta arrel de l'aplicacio)/bin/Debug/netcoreapp3.1/publish a la nostra màquina Linux.

Un cop ho haguem fet, en la carpeta publish de la màquina virtual hem d'executar:

```
 $ dotnet nomAplicacio.dll
```

Hem de comprobar que el servidor està enviant quelcom (executar i mostrar captura).

#### **6.** Configuració del servidor Nginx

Anem a /etc/nginx/sites-available i modifiquem el _location_ que hi hagi dins del default per:

```
	proxy_pass http://localhost:5000;
	proxy_http_version 1.1;
	proxy_set_header Upgrade $http_upgrade;
	proxy_set_header Connection keep-alive;
	proxy_set_header Host $host;
	proxy_cache_bypass $http_upgrade;
```

Incís: per modificar aquest fitxer es necessiten els permisos adeqüats:

```
 $ sudo chomod 677
```

Reiniciem el servei i el tornem a executar.

```
 $ sudo service nginx restart
 $ sudo nginx -s reload
```

EXECUCIÓ DE DOCKERS EN QUALSEVOL SISTEMA
====================================

Si tenim una aplicació .NET (ja sigui en Linux o Windows) dockeritzada (això ho podem fer en un entorn de desenvolupament Windows i amb Visual Studio fàcilment) [*ENSENYAR A LA MEMÒRIA COM ES POT FER!!!!*], podem.

```
 $ docker build -t image_name .
 $ docker run -it --rm -p 5000:80 --name container_name image_name
```

La primera comanda compila l'aplicació Docker i crea una imatge de nom _image_name_. És *key sensitive*, pel qual el nom de la imatge ha d'anar en minúscules. La comanda busca _Dockerfile_ en el directori especificat (el punt vol dir directori actual), pel que es recomanable comprobar que existeixi abans d'executar qualsevol comanda.

La segona inicia l'aplicació. La comanda elimina automàticament el contenidor quan aquest es tanqui i li asigna el port 5000 de la màquina local al port 80 del contenidor, i li dóna a aquest el nom de _container_name_. El contenidor s'asigna a la imatge _image_name_.

EXECUCIÓ DEL PROJECTE 4246 EN UN ENTORN LINUX
========================================

- Antecedents
	- El projecte està preparat per funcionar en un entorn Windows.
	- El projecte usa la versió 5 del framwork .NET.
	- Volem provar de fer-ho funcionar en un entorn Linux.

- Al final hem aconseguit que funcioni en un entorn Linux.

Pasos a seguir per fer funcionar el projecte 4246 en un entorn Linux
--------------------------------------------------------------

- Només necessitem la versió 5 de .NET, no fa falta instal·lar la 6 ni la 7.
- Instal·lar la versio 5 de .NET: https://learn.microsoft.com/es-es/dotnet/core/install/linux-debian#debian-9-
- Executar-ho amb "dotnet run".

#### **1.** Problema 1

Hi han inconsistencia entre el format de temps en .NET Core dintre de servidors Linux i Windows, ja que en Linux els formats d'hora tenen un protocol diferent (diferent forma d'escrirue) que en Windows. Això provoca un error ja que el programa no pot llegir aquests formats.

- Enllaços d'interès:
	- https://www.programmerall.com/article/743392620/
	- https://dejanstojanovic.net/aspnet/2018/july/differences-in-time-zones-in-net-core-on-windows-and-linux-host-os/
	- https://www.stevejgordon.co.uk/timezonenotfoundexception-in-alpine-based-docker-images
	- *IMPORTANT* - https://stackoverflow.com/questions/41566395/timezoneinfo-in-net-core-when-hosting-on-unix-nginx

#### **2.** Sol·lució 1

Per sol·lucionar aquest error, podem canviar la variable que ens està causant el problema. Per trobar-la i no tindre que buscar fitxer per fitxer, podem fer servir la comanda grep:                                 |

```
 # Dins del folder on tinguem els fitxers del projecte 4246.
 $ grep -ri "TimeZoneInfo.FindSystemTimezoneById"
```

La podem canviar pel format que usa Linux usant vim. Substituim la línia:

```
string _spainTimeZoneId = "Romance Standard Time";
```

Per:

```
	string _spainTimeZoneId = "Europe/Madrid";
```

STANDARD SQL - Us dels mòduls SQL d'Ingimec
=======================================

Per fer servir bases de dades SQL usant els estàndards d'Ingimec hem de crear-nos primer un mòdul XML. Això ho podem fer manualment o a través de l'eina <<ING_SQL_XML_Configurator>>, que a través d'una interfície gràfica creada amb WinsForms ens genera un arxiu XML amb les dades necessàries per poder usar bases de dades SQL en els projectes de la empresa.

Un cop fet això, el primer que hem de fer és comprobar que aquest fitxer XML generat tingui les dades correctes. Podem compar-les amb les que hi ha a la base de dades fent:

```
string pathXML = "Path on haguem guardat el fitxer. Preferiblement, ha d'estar dins la carpeta del mateix projecte.";
string error;

int dbResult = ING_SQL_MANAGER.InitSQLDBConnection(pathXML, out error);

if (dbResult != 0) {

	Console.WriteLine("Control d'errors.");
	return;

}
```

Si això no ens retorna cap error, podem fer una consulta. Per fer un ```SELECT TOP (10) * FROM taula```, cridarem la funció _GetXRegisters_:

```
string selectError;
List<List<object>> _datamans = ING_SQL_Manager.GetXRegisters(table_info, 10, ( int ) SqlOrder.ASC, out selectError);

if (dbResult != 0) {

	MessageBox.Show("A type error \"" + error + "\" has been generated", "ERROR: " + dbResult.ToString(), MessageBoxButton.OK, MessageBoxImage.Error);
	return;

}
```

I podem comprobar que hem fet la consulta correctament llegint i imprimint per pantalla la matriu _datamans_.

```
string result = "";

for (int k = 0; k < 10; k++) {

	for (int l = 0; l < 13; l++) {

		result += _datamans[k][l] + " --- ";

	}

	result += "\n";

}

Console.WriteLine(result);
```

#### **1. ** Si volem incloure una taula sencera de la BD al nostre WPF gràfica

##### **1.1** Opció 1, fent servir .NET Framwork i LINQ

Hem d'instal·lar els següents paquets Nuget.

- Microsoft.EntityFrameworkCore.Design

- Microsoft.EntityFrameworkCore.SqlServer

- Microsoft.EntityFrameworkCore.Tools

I obrir la *consola del gestor de paquets Nuget* per escriure:

```
Scaffold-DbContext "Server=.\LOCAL_SERVER;User ID=YOUR_DB_USER;Password=YOUR_DB_PASSWORD;Database=YOUR_DATABASE;Trusted_Connection=False;" Microsoft.EntityFrameworkCore.SqlServer -OutputDir Models
```

I després crear un nou item al projecte de tipus _ADO.NET Entity Data Model_.

Si ens trobem amb algún error com:

> A connection was successfully established with the server, but then an error occurred during the login process. (provider: SSL Provider, error: 0 - La cadena de certificación fue emitida por una entidad en la que no se confía.)

Hem d'afegir ```TrustServerCertificate=True``` a la instrucció.

Amb això se'ns haurà agregat la BD ja creada al nostre projecte.

##### **1.2** Opció 2, fent servir .NET i els mòduls Stàndard d'Ingimec

Amb les instruccions que hem vist anteriorment hem obtingut una llista de llistes que conté les X primeres files d'una taula de la nostra base de dades. Si volem imprimir-ho en una interfície gràfica, podem fer el següent.

1. Primer hem de definir un <<DataGrid>>, que serà on mostrarem el contigunt de la taula.

2. Després, hem de recórrer la llista de llistes per tal formatejar les dades correctament.

	- Com que el contigut de la llista de llistes està format en base a "objectes", si no formatejem bé les dades aquestes no se'ns mostraràn, o bé ho faràn d'alguna forma incorrecta.

```
// Abans hem guardat el contingut de la taula en una variable de nom "_datamans".
// Ens creem una llista que contindrà el nom de cada columna de la nostra taula per a mostrar-ho en la
// Interfície gràfica final.
List<string> headers = new List<string> {

	"Aquí", "Posarem", "El", "Titol", "De", "Cada", "Columna", "Per", "Tal", "De", "Mostrar-ho", "Correctament", "En", "La", "Pantalla"

};

// Degut a que la quantitat de columnes de la taula pot variar, tranformarem les seves dades al format correcte.
// També farem servir DataTable per a que ens sigui més fàcil després insertar les dades en el DataGrid.
var dataTable = new DataTable();

// Crea les columnes del DataGrid.
int numberColumns = 13;

for (int k = 0; k < numberColumns; k++) {

	dataTable.Columns.Add(headers[k]);

}

// Copia les dades de la taula de la base de dades en el DataTable.
for (int k = 0; k < _datamans.Count; k++) {

	dt.Rows.Add(_datamans[k].Take(numberColumns).ToArray());

}

// I finalment mostrem el DataGrid en la nostra interfície.
showTable.ItemSource = dt.DefaultView;
```

