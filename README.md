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
    * Scenario : ***Customer arrives***, given ***customer is in the shop***, when ***customer scan the QR code***, then ***the menu  will be displayed.***
    * Scenario: ***Customer orders***, given ***customer reads the menu***, when ***customer has chosen the menu***, then ***order list will be displayed to the kitchen.***
    * Scenario: ***Receive the order***, given ***the order list***, when ***the kitchen staff receives the order***, then ***the order will be  prepared and recorded in the database.***
    * Scenario: ***Order notification***, given ***the customer is in the queue***, when ***the order is ready***, then ***the customer will be notified***.

2. As a ***Shop Owner***, I want to ***see the statistics and modify the content*** so that ***I can overview and manage the shop.***
    * Scenario: ***Sales Report*** given ***the records from database*** when ***the shop owner selects the query based on date and time,*** then ***the corresponding report will be displayed.***
    

### System Architecture and Behavior

User Interface (UI) and Web Server
Software system consists of **user interface, web server and database**. The firmware is developed for M5 Atom Echo and M5StickC. The web server is developed using the **FLASK framework**. The database is developed using the **MongoDB database**.

![Overall System Design](/images/overall_.jpg)

* User can access the menu by **scanning the QR code**.
![Ordering Sequence Design](/images/ordering_sequence.jpg)

* When the order is ready, the kitchen staff will **press the M5 stick to signal the Atom echo** that the customer's order is ready to be served.
![Notification Sequence Design](/images/noti_seq.jpg)

* The business owner can **review the sales record and update the menu** when the demand changes.
![Statistic Sequence Design](/images/statistic_seq.jpg)

### DataBase Shema
The following is the database schema for the system. The database consists of **three tables**. The **order table, menu table and the device table**. 
![Statistic Sequence Design](/images/schema.jpg)
