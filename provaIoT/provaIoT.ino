// #include <dummy.h>
// #include <PubSubClient.h>
// #include <WiFi.h>
// #include "AzureIotHub.h"

#define COUNTERS 10
#define INTERVAL 100
#define DEVICE_ID "Prova_pilot"
#define MESSAGE_MAX_LEN 256

static const char* connectionString = "HostName=IoTIngimec.azure-devices.net;DeviceId=proa_pilot;SharedAccessKey=9Pr+4pD5SE9P3F28XsyuYs71i/3nGYQmwJK+lsp5TUI=";

static bool messageSending = true;

static int target_lectura = 1000;

const char *messageData = "{\"DI1\":\"%d\", \"temps_DI1\":\"%lu\",\"DI2\":\"%d\", \"temps_DI2\":\"%lu\",\"DI3\":\"%d\", \"temps_DI3\":\"%lu\",\"DI4\":\"%d\", \"temps_DI4\":\"%lu\",\"DI5\":\"%d\", \"temps_DI5\":\"%lu\", \"DI6\":\"%d\", \"temps_DI6\":\"%lu\",\"DI7\":\"%d\", \"temps_DI7\":\"%lu\",\"DI8\":\"%d\", \"temps_DI8\":\"%lu\",\"DI9\":\"%d\", \"temps_DI9\":\"%lu\",\"DI10\":\"%d\", \"temps_DI10\":\"%lu\"}";

char mesagePayload[500];
char myinfo[10][500];

int indIn = 0;
int indOut = 0;

unsigned int temps_establert_mqtt = 3000;
unsigned int temps_enviar = 0;
unsigned int temps_llegir = 0;

unsigned long temps_anterior = 0;
unsigned long temps_actual = 0;
unsigned long temps_transcorregut = 0;
unsigned long temps_HIGH[COUNTERS] = {};
unsigned long temps_enviament = 0;

bool flanc_on[COUNTERS] = {LOW, LOW, LOW, LOW, LOW, LOW, LOW, LOW, LOW, LOW};
word CNT_flanc[COUNTERS] = {};

unsigned char DIs[] = {4, 2, 15, 32, 25, 26, 27, 14, 12, 13};
byte PINMODE[] = {INPUT, INPUT, INPUT, INPUT, INPUT, INPUT, INPUT, INPUT, INPUT, INPUT};

void setup() {

  // put your setup code here, to run once:
  Serial.begin(115200);
  Serial.println("Hello world.");

}

void loop() {

  // put your main code here, to run repeatedly:

}
