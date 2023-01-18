#include <SPI.h>
#include <Ethernet.h>

// Set the data connection: MAC, IP.
byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };
IPAddress ip{ 192, 168, 1, 100 };

// Initialize Ethernet library.
EthernetClient client;

// IP server (Linux).
char server[] = "192.168.1.107";

// Global variables.
String codigo;
String nombre;
bool fin = false;
bool pregunta = true;

// This function create the server connection.
int httpRequest(int identificador) {

  if (client.connect(server, 80)) {

    Serial.println("Conectado.");

    /***********************************************************************/
    client.print("GET /ingenieros/comunicaciones/valormysql.php?id=");
    client.print(identificador);
    client.println("HTTP/1.0");
    client.println("Host: 192.168.1.252");
    client.println("User-Agent: arduino-ethernet");
    client.println("Connection: close");
    client.println();
     /***********************************************************************/

  }

  else {

    Serial.println("Conexio fallida.");
    Serial.println("Desconectant.");
    client.stop();

  }

  delay(500);

  while (client.available()) {

    char c = client.read();
    codigo += c;
    fin = true;

  }

  if (fin) {

    int longitud = codigo.length();
    int posicion = codigo.indexOf("valor = ");
    nombre = "";

    for (int k = posicion + 6; k < longitud; k++) {

      if (codigo[k] == ';') {

        k = longitud;

      }

      else {

        nombre += codigo[k];

      }

    }

    fin = false;
    Serial.println("Valor de la variable nombre: " + nombre);
    Serial.println("Desconetarnos.");
    client.stop();
    
  }

  codigo = "";
  return 1;

}

void setup() {

  Serial.begin(9600);
  delay(1000);
  Ethernet.begin(mac, ip);
  Serial.print("IP: ");
  Serial.println(Ethernet.localIP());

}

void loop() {

  // Checks if have data in the serial port.
  if (pregunta == true) {

    Serial.print("Escriu el ID de la persona: ");

  }

  pregunta = false;

  // Reads the ID.
  if (Serial.available() > 0) {

    int identificador = Serial.read() - 48;
    Serial.println("ID persona:");
    Serial.println(identificador);
    Serial.println("===");
    httpRequest(identificador);
    pregunta = true;

  }

}