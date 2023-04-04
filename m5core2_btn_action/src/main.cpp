#include <M5Core2.h>
#include <WiFi.h>
#include <ArduinoJson.h>
#include "mqtt_task.h"

/*
#include <ArduinoJson.h>
#include <WiFiUdp.h>
#include <WiFiClient.h>

Button myButton(10, 10, 200, 100, false, "I'm a button !",
                    {BLACK, WHITE, WHITE});

M5.Lcd.setTextDatum(MC_DATUM);*/

// static variables
const char* ssid     = "ET_Phyu";
const char* password = "12345678";
const char* mqtt_broker = "broker.hivemq.com";
const int mqtt_port = 1883;
const char* pub_topic = "thekitchen/table";
const char* sub_topic = "thekitchen/server";
WiFiClient espClient;
PubSubClient mqttClient(espClient);
static DynamicJsonDocument sent_doc(1024);
static DynamicJsonDocument receive_doc(1024);

void threebtn() {

  M5.Lcd.setTextSize(2);
  M5.Lcd.fillRect(15, 205, 80, 40, RED);
  M5.Lcd.setTextColor(WHITE, RED);
  M5.Lcd.setCursor(25, 215);
  M5.Lcd.print("Order");

  M5.Lcd.fillRect(125, 205, 80, 40, GREEN);
  M5.Lcd.setTextColor(WHITE, GREEN);
  M5.Lcd.setCursor(147, 215);
  M5.Lcd.print("Pay");

  M5.Lcd.fillRect(230, 205, 80, 40, BLUE);
  M5.Lcd.setTextColor(WHITE, BLUE);
  M5.Lcd.setCursor(255, 215);
  M5.Lcd.print("Bot");
}

void callback(char* topic, byte* payload, unsigned int length) {
  // Handle MQTT message received
  Serial.print("Message received: ");
  /*for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();*/

  // convert byte payload to json
  // Deserialize the byte array into the JsonDocument
  DeserializationError error = deserializeJson(receive_doc, payload);

  // Check for errors during deserialization
  /*if (error) {
    Serial.print("deserializeJson() failed: ");
    Serial.println(error.f_str());
    return;
  }*/

  if (int(receive_doc["table_no"]) == 1){
    if (receive_doc["status"] == "payment"){
      if (receive_doc["msg"] == "OK"){
        Serial.println("Payment - ok");
        M5.Lcd.clear();
        M5.Lcd.fillScreen(BLACK);
        M5.Lcd.setTextColor(WHITE, BLACK);
        M5.Lcd.setTextSize(2);
        M5.Lcd.setCursor(0, 0);
        M5.Lcd.println("Thank you!");
        M5.Lcd.qrcode("https://030f-182-232-196-3.ngrok.io", 75, 23, 170, 6);
        threebtn();
      }
      else{
        Serial.println("Payment - err");
        M5.Lcd.clear();
        M5.Lcd.fillScreen(BLACK);
        M5.Lcd.setTextColor(WHITE, BLACK);
        M5.Lcd.setTextSize(2);
        M5.Lcd.setCursor(18, 100);
        M5.Lcd.print("Place your order first!");
        threebtn();
      }
    }
    else if (receive_doc["status"] == "order_ready"){
      Serial.println("Order ready");
      M5.Lcd.clear();
      M5.Lcd.fillScreen(BLACK);
      M5.Lcd.setTextColor(WHITE, BLACK);
      M5.Lcd.setTextSize(3);
      M5.Lcd.setCursor(20, 80);
      M5.Lcd.print("     Yay!!!    ");
      M5.Lcd.setCursor(20, 105);
      M5.Lcd.print("Order is ready.");
      threebtn();
    }

  }

  delay(200);
}

void reconnect() {
  // Loop until we're reconnected
  while (!mqttClient.connected()) {
    Serial.print("Connecting to MQTT broker...");
    if (mqttClient.connect("table1")) {
      Serial.println("connected");
      mqttClient.subscribe(sub_topic);
    } else {
      Serial.print("failed, rc=");
      Serial.print(mqttClient.state());
      Serial.println(" retrying in 5 seconds");
      delay(200);
    }
  }
}

void setup() {
  M5.begin();
  M5.Lcd.setTextSize(3);
  M5.Lcd.fillScreen(BLACK);
  M5.Lcd.setTextColor(WHITE);

  Serial.begin(115200);

  //connect to Wi-Fi
  WiFi.begin(ssid, password);
  Serial.println("Connecting");
  while(WiFi.status() != WL_CONNECTED) {
    delay(100);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to WiFi network");

  if (WiFi.status() == WL_CONNECTED) {
    // connect to mqtt broker
    mqttClient.setServer(mqtt_broker, mqtt_port);
    mqttClient.setCallback(callback);
    mqttClient.connect("table1");

    // subscribe to topics
    mqttClient.subscribe(sub_topic);
  }

}

void loop() {

  if (!mqttClient.connected()){
    reconnect();
  }

  M5.update();
  if (M5.BtnA.wasPressed()) {
    Serial.println("btnA");
    M5.Lcd.clear();
    M5.Lcd.fillScreen(BLACK);
    M5.Lcd.setTextColor(WHITE, BLACK);
    M5.Lcd.setTextSize(2);
    M5.Lcd.setCursor(0, 0);
    M5.Lcd.println("Place your order!");
    M5.Lcd.qrcode("https://030f-182-232-196-3.ngrok.io", 75, 23, 170, 6);
    threebtn();
  }
  else if (M5.BtnB.wasPressed()) {
    Serial.println("btnB");
    
    // request payment
    char pub_msg[256];
    sent_doc["status"] = "payment";
    sent_doc["table_no"] = 1;
    serializeJson(sent_doc, pub_msg);
    mqttClient.publish(pub_topic,pub_msg);  

  }
  else if (M5.BtnC.wasPressed()) {
    Serial.println("btnC");
    M5.Lcd.clear();
    M5.Lcd.fillScreen(BLACK);
    M5.Lcd.setTextColor(WHITE, BLACK);
    M5.Lcd.setTextSize(2);
    M5.Lcd.setCursor(0, 0);
    M5.Lcd.println("Subscribe & Get Promo Code");
    M5.Lcd.qrcode("https://line.me/R/ti/p/%40365tqywl", 75, 23, 170, 6);
    threebtn();
  }
  
  mqttClient.loop();

  delay(100);
}
