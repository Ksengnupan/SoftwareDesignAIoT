# SoftwareDesignAIoT
# Title: ***IoT-enabled Smart Ordering System***

### Members
1. Seng Nu Pan (sengnupan.kumgyi@gmail.com)
2. Kaung Htet San (kaunghtetsan275@gmail.com)
3. Khaing Zar Mon (m6522040556@g.siit.tu.ac.th)
4. Ei Thandar Phyu (eithandar.p@live.ku.th)
5. Hnyot Myet Wunn Shunn Le Maung (hnyotmyetwunnshunnle.m@live.ku.th)
6. Nang Aeindray Kyaw (nangaeindray.k@live.ku.th)

### Hardware
1. M5Stack Core2 (M5Stack Core2)
2. M5Stack Basic (M5Stack Core ESP32)
3. M5 CoreInk (M5Stack Core Ink)
4. M5StickC (M5Stick-C)
5. ATOM Echo (M5Stack-ATOM)
6. ATOM Matrix (M5Stack-ATOM)

## Objectives
* To make ordering process more convenient and achieve customer satisfaction.

***User stories and acceptance criteria***
1. As a **Customer**, I want to ***order food easily*** so that ***I will be satisfied.***
    * Scenario: ***Order notification***, given ***the customer is in the queue***, when ***the order is ready***, then ***the customer will be notified***.

### Contribution

Ei Thandar Phyu (ID: 6514552480)
I am a contributor who has the responsibility for Order Notification and Button Actions on M5Stack Core2. <br>

**Order Notification**  
* On M5Stack Core2 device, the WiFi will be initialized and a topic will be subscribed. The program will then wait for a message from the kitchen staff informing that an order is ready. When the kitchen staff presses the "Order Ready" button, the order status in the database will be updated and a message will be sent to the MQTT broker. <br>
![Publish order ready message](/images/send_order_ready.png)

* When Core2 receives a message from the subscribed topic, it will check the table number and verify that the message is "Order Ready". If the valid table number and order ready message were received, the customer will be notified that his order is ready to serve. <br>
![Notify Customer](/images/order_notify.jpg)

**Button Actions**
* The button actions on Core2 will only be enabled once the BLE tag is detected. If the customer clicks the Order button (btnA) on Core2, a QR code will be displayed to order again. <br>

* The customer can also subscribe to our Kitchen Line Bot by clicking the Line Bot button (btnC) on Core2 and scanning a QR code. <br>
![Place Order QR - btnA and Line Bot QE - btnC](/images/btnA_C.jpg)

* To request an invoice, the customer can click the Payment button (btnB) on Core2. After doing so, Core2 will use MQTT protocol to request that the server check whether there are any orders for the table. If there are no orders, the customer will be notified to order first. If there are orders, a QR code for the invoice will be displayed, which the customer can obtain by scanning it. <br>
![Payment message on MQTT Broker](/images/request_payment.png)
![Payment Action - btnB](/images/pay_btnB.jpg)


* After the payment process is complete, Core2 will begin detecting BLE tags.
