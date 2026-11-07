#include <ESP8266WiFi.h>  // Use #include <WiFi.h> if running an ESP32
#include <ESP8266WebServer.h>

// Initialize the SRT-Diner Web Server on standard port 80
ESP8266WebServer server(80);

// Hardware pin mapping configuration
const int MOSFET_GATE_PIN = 5;  // GPIO5 (D1) links to the MOSFET gate
const int RED_LED_PIN = 4;      // GPIO4 (D2) switches the Red pulse channel
const int IR_LED_PIN = 0;       // GPIO0 (D3) switches the Infrared channel
const int PHOTO_DIODE_PIN = A0; // Analog sensor acquisition line

// In-flight structural metrics tracking states
long rawRedValue = 0;
long rawIRValue = 0;
String currentGateState = "IDLE";

void handleDataRequest() {
  // Execute a rapid charge exchange sequence phase
  currentGateState = "ACTIVE_DISCHARGE";
  digitalWrite(MOSFET_GATE_PIN, HIGH);
  delayMicroseconds(50); // Transient charge settlement window
  
  // 1. Sample the Red Light Transmission Phase
  digitalWrite(RED_LED_PIN, HIGH);
  delayMicroseconds(20);
  rawRedValue = analogRead(PHOTO_DIODE_PIN) * 8; // Scale factor simulation
  digitalWrite(RED_LED_PIN, LOW);
  
  // 2. Sample the Near-Infrared Transmission Phase
  digitalWrite(IR_LED_PIN, HIGH);
  delayMicroseconds(20);
  rawIRValue = analogRead(PHOTO_DIODE_PIN) * 8;
  digitalWrite(IR_LED_PIN, LOW);
  
  // Reset gate controls back to standard monitoring state
  digitalWrite(MOSFET_GATE_PIN, LOW);
  currentGateState = "IDLE";
  
  // Construct the exact clean JSON response payload required by your Python script
  String jsonPayload = "{";
  jsonPayload += "\"red\":" + String(rawRedValue) + ",";
  jsonPayload += "\"ir\":" + String(rawIRValue) + ",";
  jsonPayload += "\"mosfet_gate\":\"" + currentGateState + "\"";
  jsonPayload += "}";
  
  server.send(200, "application/json", jsonPayload);
}

void setup() {
  Serial.begin(115200);
  
  // Pin mode registration
  pinMode(MOSFET_GATE_PIN, OUTPUT);
  pinMode(RED_LED_PIN, OUTPUT);
  pinMode(IR_LED_PIN, OUTPUT);
  digitalWrite(MOSFET_GATE_PIN, LOW);
  
  // Broadcast local network access point: "SRT-Diner-Node"
  WiFi.softAP("SRT-Diner-Node", "auhx1234");
  Serial.println("SRT-Diner Network access point broadcasting active.");
  Serial.print("Node IP Address: ");
  Serial.println(WiFi.softAPIP());
  
  // Route matching endpoints
  server.on("/data", handleDataRequest);
  server.begin();
  Serial.println("HTTP server listening framework ready.");
}

void loop() {
  server.handleClient(); // Constantly process incoming network poll requests
}

