#include <Arduino.h>
#include <esp_log.h>
#include "ble_task.h"
#include "mqtt_task.h"

// static variables
const char* ssid = "Nyan Note 11 Pro";
const char* password = "thekillingjoke";
const char* mqtt_broker = "broker.hivemq.com";
const int mqtt_port = 1883;
const char* pub_topic = "ict720/khaing/data"; //nyan change this to your name
const char* sub_topic = "ict720/khaing/cmd"; //nyan this too
WiFiClient espClient;
PubSubClient mqttClient(espClient);

// static functions

// constant definitions
#define TAG             "MQTT TASK"

void mqtt_callback(char* topic, byte* payload, unsigned int length) {
    char buf[256];
    memcpy(buf, payload, length);
    buf[length] = 0;
    ESP_LOGW(TAG, "MQTT received: %s", buf);
}

// MQTT task handler
void mqtt_task_handler(void *pvParameters) {
    // setup:
    // - connect to wifi
    WiFi.mode(WIFI_OFF);
    vTaskDelay(100/portTICK_PERIOD_MS);
    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        vTaskDelay(500/portTICK_PERIOD_MS);
    }
    // - connect to mqtt broker
    mqttClient.setServer(mqtt_broker, mqtt_port);
    mqttClient.setCallback(mqtt_callback);
    mqttClient.connect("Khaing"); //NYAN change this to anything

    // - subscribe to topics
    mqttClient.subscribe(sub_topic);
    // loop: 
    while(1) {
        // wait for message from BLE task
        // - if message received, publish to mqtt broker
        ble_msg_t ble_msg;
        char msg_buff[256];
        if(xQueueReceive(bleQueue, &ble_msg, 1000/portTICK_PERIOD_MS) == pdTRUE) {
            ESP_LOGW(TAG, "MQTT task running");
            ESP_LOGW(TAG, "Queue received %s: %d", ble_msg.addr.toString().c_str(), ble_msg.rssi);
            if(ble_msg.rssi > -60) {
                sprintf(msg_buff, "Found %s %d", ble_msg.addr.toString().c_str(), ble_msg.rssi);
                mqttClient.publish(pub_topic, msg_buff);
            }
        }
        mqttClient.loop();
    }
}