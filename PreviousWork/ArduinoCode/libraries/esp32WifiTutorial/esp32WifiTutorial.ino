#include <dummy.h>

#include <WiFi.h>

// Constants.
const char* ssid = "TP-LINK_POCKET_3020_6CEA72"; // "INGIMEC";
const char* password = "02531090"; // "\I453.P126\?EWRfartdescriure";
const char* host = "www.google.es";
const char* streamId = "... ";
const char* privateKey = "--- ";

// Configuration.
void setup() {

  Serial.begin(9600);
  delay(10);

  // We start by connecting to a WiFi network.
  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {

    delay(500);
    Serial.print(".");

  }

  Serial.println("");
  Serial.println("WiFi connected.");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

}

int value = 0;

// Main Loop.
void loop() {

  delay(500);
  ++value;
  Serial.print("Connecting to: ");
  Serial.println(host);

  // Use WiFi client class to create TCP connections.
  WiFiClient client;
  const int httpPort = 80;

  if (!client.connect(host, httpPort)) {

    Serial.println("Connection failed.");
    return;

  }

  // We now create a URI for the request.
  String url = "/input/";
  url += streamId;
  url += "?private_key=";
  url += privateKey;
  url += "&value=";
  url += value;
  Serial.print("Requesting URL: ");
  Serial.println(url);

  // This will send the request to the server.
  client.print(String("GET ") + url + " HTTP/1.1\r\n" + "Host: " + host + "\r\n" + "Connection: close\r\n\r\n");

  unsigned long timeout = millis();

  while (client.available() == 0) {

    if (millis() - timeout > 5000) {

      Serial.println(">>> Client timeout :(");
      client.stop();
      return;

    }

  }

  // Read all the lines of the reply from server and print them to Serial Port.
  while (client.available()) {

    String line = client.readStringUntil('\r');
    Serial.print(line);

  }

  Serial.println();
  Serial.println("Closing connection.");

}
