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
    * CP210x USB serial
    * LCD 320x240
    * 6-axis IMU MPU6886
2. M5Stack Basic (M5Stack Core ESP32)
    * CP210x USB serial
    * LCD 320x240
3. M5 CoreInk (M5Stack Core Ink)
    * CP210x USB serial
    * E-ink 200x200
4. M5StickC (M5Stick-C)
    * FTDI USB serial
    * LCD 80x160
    * 6-axis IMU MPU6886
5. ATOM Echo (M5Stack-ATOM)
    * FTDI USB serial
6. ATOM Matrix (M5Stack-ATOM)
    * FTDI USB serial
    * LED 5x5
    * 6-axis IMU MPU6886

## Objectives
1. To facilitate remote management and tracking order data.
2. To make ordering process more convenient and achieve customer satisfaction.
3. To develop a novel recommendation system to increase customer traction.

***User stories and acceptance criteria***

1. As a **Customer**, I want to ***order food easily*** so that ***I will be satisfied.***
    * Scenario : ***Customer arrives***, given ***customer is in the shop with BLE Tag***, when ***customer scan the QR code***, then ***the menu will be displayed with beep beep sound.***
    * Scenario: ***Customer browses the menu***, given ***customer reads the menu***, when ***customer has chosen the menu***, then ***the order will be added to the shopping cart.***
    * Scenario: ***Customer comfirms the orders***, given ***the order list is in the shopping cart***, when ***the order is confirmed***, then ***updated order list will be displayed to the kitchen.***
    * Scenario: ***Receive the order***, given ***the order list***, when ***the kitchen staff receives the order***, then ***the order will be  prepared and recorded in the database.***
    * Scenario: ***Order notification***, given ***the customer is in the queue***, when ***the order is ready***, then ***the customer will be notified***.

2. As a ***Shop Owner***, I want to ***see the dashboard and statistics*** so that ***I can overview and manage the shop.***
    * Scenario: ***Sales Report*** given ***the records from database*** when ***the shop owner selects the query,*** then ***the corresponding report will be displayed.***
    

### System Architecture and Behavior

User Interface (UI) and Web Server
Software system consists of **user interface, web server and database**. The firmware is developed for M5 Atom Echo and M5StickC. The web server is developed using the **FLASK framework, Docker **. The database is developed using the **MongoDB database**.

![Overall System Design](/images/OverallArchitecture.jpg)

* Customer can access the menu by **scanning the QR code**.
![Ordering Sequence Design](/images/UserStories1_1.jpg)

* **For the customer side:** when a customer selects a menu and submits an order, the order list is added to the database and the consumer is notified that the order has been placed. <br>
**For the kitchen staff side:** the web page that the kitchen staff sees is refreshed every 10 seconds, and the order list is shown on the desktop screen of the kitchen staff. <br>
![Ordering Sequence and Order Display Design](/images/userstories_1_2&3.jpg)

* Once the kitchen staff finishes preparing an order, they will use the website to indicate that it is ready. This will trigger an update to the order status in the database and a message will be sent to the MQTT broker indicating that the order is ready. When this message is received by core2, it will notify the customer that their order is now ready to be served. <br>
![Notification Sequence Design](/images/userstories1_5_notifycustomer.png)

<!-- * The business owner can **review the sales record and update the menu** when the demand changes. -->
<!-- ![Statistic Sequence Design](/images/statistic_seq.jpg) -->


### Member's Contribution 
***The strength of the team is each individual member. The strength of each member is the team." – Phil Jackson***
* **Seng Nu Pan** (ID:6522040564) 


Hello there! I am a contributor who has the responsibility for creating **The Dashboard** of our system. <br>


![General Flow](/images/pan_1.png)

I have implemented **Four functions** to help owner see the insights.
<br>

* Function 1
<br>

1_a: The owner can see **the available menu list**.
<br>

![Function 1_1](/images/pan_fun1_1.png)
<br>

1_b: The owner can **select each menu id and check details**
<br>

![Function 1_2](/images/pan_fun1_2.png)
<br>

* Function 2
<br>

The owner can check **the number of orders for selected date**.
<br>

![Function 2](/images/pan_fun2.png)
<br>

* Function 3
<br>

***What will be the top most popular dish of my shop?*** Yes, the owner can check it out with this function.
<br>

![Function 3](/images/pan_fun3.png)
<br>

* Function 4
<br>

***By the way, how much money have I earned so far?*** Yes, the owner can check it out with this function.
<br>

![Function 4](/images/pan_fun4.png)
<br>

* Result

***The following figure is the Dashboard what the owner see.***
<br>
![result](/images/result_dash.png)
<br>

***The following figure is the flow behind it.***
<br>
![flow](/images/flow.png)

* **Khaing Zar Mon** (ID:6522040556) 


Hello there! I am a contributor who has the responsibility for creating **Shopping Cart and Display the order list to the Kitchen Staff** of our system. <br>

**Shopping Cart:** When a customer adds items to their shopping cart, they can update or remove items, and when they click "Order" the order is placed, the order list and table number are added to the **open order collection**. Then the order status is updated to "order processing".<br><br>
![Shopping Cart](/images/Khaing_ShoppingCart.jpg)

**Display the order list to the kitchen staff:** Every 10 seconds, the screen will refresh to show the list of orders that are currently being processed. If an order is ready, a staff member will click the "Order Ready" button to notify the client with sound via the M5Core2 device, and the order list will be dropped by table number from the kitchen staff's screen and the order status will be updated from "order processing" to "finished" in the **open order collection**. <br><br>
![Order Display](/images/Khaing_OrderDisplay.jpg)

#M5 Core 2 **BLE detector**

* Core 2 will work as BLE detector and will be detecting every BLE devices nearby. RSSI threshold is set. We can also change the ```RSSI_THRESHOLD``` for any desire values as this threshold will depend on the environment being noisy or not.

![Set RSSU threshold](rssi.png)
* We will make a list of registered BLE devices. Collected BLE tags will be added to the known BLE devices list.
![Known BLE Devices](registered_devices.png)
* Firstly, the Core 2 will check whether the detected BLE devices are included in the known BLE devices list. If yes, the BLE mac addresses will be compared and displayed on serial monitor as” Found Registered Device” with their respective received signal strength values.

![Found Registered Device in Proximity](found.png)
* If the value of registered BLE device is within our set RSSI value, beep beep alarm will be played with M5 core 2’s built in speaker and Menu QR code for that table will be displayed on LCD. 

![M5 Core 2](menu_qr.jpg)
![Testing Video](testingvideo.mp4)


