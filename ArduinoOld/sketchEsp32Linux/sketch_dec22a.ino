#include <WiFi.h>

/****************************************************
 * FOR DEBUGGING                                    *
 * ------------------------------------------------ *
 * Global constant for debugging purpose. If is     *
 * set to True, debugging messages are printed,     *
 * else debugging messages are ignored.             *
 ****************************************************/
const bool debug = true;

// Set WiFi data connection.
const char* ssid = "INGIMEC";
const char* password = "\\I453.P126\\?EWRfartdescriure";

// Set Socket Server data connection.
const uint16_t port = 4554;
const char* host = "192.168.1.107";

// Define the client to connect to the Python Socket Server.
WiFiClient client;

// Define msg MQTT to send to Python Socket Server.
#define INTERVAL 100
#define DEVICE_ID "ProvaPythonServer"
#define MESSAGE_MAX_LEN 256
const char* messageData = "{\"DI1\":\"%d\", \"tempsDI1\":\"%lu\",\"DI2\":\"%d\", \"tempsDI2\":\"%lu\",\"DI3\":\"%d\", \"tempsDI3\":\"%lu\",\"DI4\":\"%d\", \"tempsDI4\":\"%lu\",\"DI5\":\"%d\", \"tempsDI5\":\"%lu\", \"DI6\":\"%d\", \"tempsDI6\":\"%lu\",\"DI7\":\"%d\", \"tempsDI7\":\"%lu\",\"DI8\":\"%d\", \"tempsDI8\":\"%lu\",\"DI9\":\"%d\", \"tempsDI9\":\"%lu\",\"DI10\":\"%d\", \"tempsDI10\":\"%lu\"}";
char messagePayload[500];
// static bool messageSending = true;
static int readTarget = 1000;

// Msg array.
char myInfo[10][500];
int indIn = 0;
int indOut = 0;
unsigned int timeStablishedMqtt = 6; // TODO: 60;
unsigned int timeSending = 0;
unsigned int timeReading = 0;

// Time variables.
unsigned long timeBefore = 0;
unsigned long timeActual = 0;
unsigned long timePassed = 0;

// Define digital inputs/outputs.
unsigned char DIs[] = { 4, 2, 15, 32, 25, 26, 27, 14, 12, 13 };
byte PINMODE[] = { INPUT, INPUT, INPUT, INPUT, INPUT, INPUT, INPUT, INPUT, INPUT, INPUT };

// Program variables.
#define COUNTERS 10
unsigned long timeHight[COUNTERS] = {};
bool flancOn[COUNTERS] = { LOW, LOW, LOW, LOW, LOW, LOW, LOW, LOW, LOW, LOW };
word flancCnt[COUNTERS] = {};
unsigned long timeSend = 0;

void setup() {

  // Set the Baudrate ESP32.
  Serial.begin(115200);
  Serial.print("ESP32 baudrate configured.\nStarting program.");

  // Start WiFi connection.
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {

    delay(500);
    Serial.print(" ... ");

  }

  // Check if the ESP32 has connected to the WiFi.
  if (WiFi.status() == WL_CONNECTED) { Serial.println("ESP32 connected to Internet succesful."); }
  else { Serial.println("ESP32 not connected to Internet. Program aborted. SETUP function."); return;}

  // Check correct connection with the Python Socket Server.
  for (int k = 0; k < 3; k++) { 
    
    if (!client.connect(host, port)) {
      
      Serial.println("Connection to socket failed.");
      delay(1000);

    }

    else {

      Serial.print("Connected to socket succesful.\n");
      break;

    }

  }

}

void loop() {

  delay(1000);

  if (!client.connect(host, port)) {

    Serial.println("Exit the program because the ESP32 has not connected to the Socket server.");
    client.stop();
    while (true) ;

  }

  // Read INPUTS/OUTPUTS and format the JSON to send the data readed to Python Server Socket.
  for (int k = 0; k < COUNTERS; k++) {

    if (digitalRead(DIs[k]) == HIGH) {

      if (flancOn[k] == HIGH) {

        if (debug == true) {

          Serial.print("Canvi de flanc: ");
          Serial.print(DIs[k]);

        }

        flancOn[k] = LOW;
        flancCnt[k]++;

      }

    }

    else { flancOn[k] = HIGH; }

  }
  
  // Prepare the JSON and send it to the socket client.
  timeReading = timeReading + 100;

  if (timeReading >= readTarget) {

    timeReading = 0;

    for (int k = 0; k < COUNTERS; k++) {

      if (digitalRead(DIs[k]) == HIGH) {

        timeHight[k] = timeHight[k] + 1000;

        if (debug == true) {

          Serial.print("DIGITAL HIGH");
          Serial.println(DIs[k]);
          Serial.println(timeHight[k]);

        }

      }

    }

    timeSending = timeSending + 2; // TODO: + 1;

    if (timeSending >= timeStablishedMqtt) {

      Serial.println("Sending IoT message.");
      timeSending = 0;

      // Formating the JSON with the INPUT/OUTPUT data.
      int numBytes = sprintf(messagePayload, messageData, flancCnt[0], timeHight[0], flancCnt[1], timeHight[1], flancCnt[2], timeHight[2], flancCnt[3], timeHight[3], flancCnt[4], timeHight[4], flancCnt[6], timeHight[6], flancCnt[7], timeHight[7], flancCnt[8], timeHight[8], flancCnt[9], timeHight[9]);

      if (debug == true) {
        
        Serial.println(numBytes);
        Serial.println(messagePayload);

      }

      // If WiFi is connected, send the JSON formated. If it not, save the JSON.
      if (!client.connect(host, port)) {

        Serial.println("Client is not connected to socket. Save JSON.");
        memcpy(myInfo[indIn], messagePayload, 500);
        indIn++;
        indIn %= 100;
        if (indIn == indOut) { indOut = indIn + 1; }

      }

      else {
        
        client.print("JSON sended:");
        delay(500);
        client.print(messagePayload);

      }

      // Reset flancs and OUTPUTS/INPUTS.
      for (int k = 0; k < COUNTERS; k++) {

        flancCnt[k] = 0;
        timeHight[k] = 0;

      }

    }

  }

  delay(100);

  // Check if the WiFi is disconnected. If it's not, it reconnects
  // it to the WiFi.
  if (WiFi.status() != WL_CONNECTED) {

    WiFi.begin(ssid, password);
    Serial.println(WiFi.status());

  }

}
