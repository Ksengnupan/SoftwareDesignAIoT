#include <Arduino.h>
#include <esp_log.h>
#include "ble_task.h"
#include "mqtt_task.h"

#include <WiFi.h>
#include <WiFiClient.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

// static variables

const char* ssid = "4G-CPE-96CE";
const char* password = "12345678";
const char* mqtt_broker_server = "broker.hivemq.com";
const int mqtt_port = 1883; // standard mqtt port number
const char* pub_topic = "ict720/kevin/data";
const char* sub_topic = "ict720/kevin/cmd";

WiFiClient espClient; // wifi client
PubSubClient mqttClient(espClient); // mqtt client
DynamicJsonDocument doc(1024);
long lastMsg = 0;
char msg[100];
int value = 0;

// static functions

// constant definitions
#define TAG             "MQTT TASK"

// callback function
void mqtt_callback(char* topic, byte* message, unsigned int length) {
    char buf[256];
    memcpy(buf, message, length);
    buf[length] = 0; // if you send 'hello', it will be h+e+l+l+o+0. Thus, it needs 6 bytes
    deserializeJson(doc, buf);
    if (doc["led"]=="on"){
        ESP_LOGW(TAG, "Got LED ON command");    
    }
    ESP_LOGW(TAG, "MQTT received: %s", buf);
} 

// MQTT task handler
void mqtt_task_handler(void *pvParameters) {
    // setup:
    // - connect to wifi
    WiFi.mode(WIFI_OFF);
    vTaskDelay(100 / portTICK_PERIOD_MS);
    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        vTaskDelay(500 / portTICK_PERIOD_MS);
    }
    ESP_LOGW(TAG, "WiFi Connected: %s", WiFi.localIP().toString().c_str());

    // - connect to mqtt broker
    //// where
    //// which top to subscribe, which topic to publish (can have more than one topic, e.g. data and command topics)
    mqttClient.setServer(mqtt_broker_server, mqtt_port);
    mqttClient.setCallback(mqtt_callback); // callback when you receive message from the server
    // mqttClient.connect("supachai2983621");
    mqttClient.connect("kevin_cautessan");

    // - subscribe to topics
    mqttClient.subscribe(sub_topic);

    // loop: 
    while(1) {
        // wait for message from BLE task
        // - if message received, publish to mqtt broker
        ble_msg_t ble_msg;
        char msg_buf[256];
        //// xQueueReceive(bleQueue, &buf, portMAX_DELAY); // delay seconds 4 billion milliseconds
        ////  mqtt requires to connect within specified time, otherwise you will be disconnected
        //// so we will use timeout approach
        if (xQueueReceive(bleQueue, &ble_msg, 1000/portTICK_PERIOD_MS)==pdTRUE){
            ESP_LOGW(TAG, "MQTT task running");
            ESP_LOGW(TAG, "Queue received %s: %d", ble_msg.addr.toString().c_str(), ble_msg.rssi);
            if (ble_msg.rssi > -200){
                doc["addr"] = ble_msg.addr.toString().c_str();
                doc["rssi"] = ble_msg.rssi;
                serializeJson(doc, msg_buf);
                // sprintf(msg_buf, "Meow found %s: %d", ble_msg.addr.toString().c_str(), ble_msg.rssi);
                mqttClient.publish(pub_topic, msg_buf);
            }
        }
        mqttClient.loop();
    }
}