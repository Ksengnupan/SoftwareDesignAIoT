# SoftwareDesignAIoT
#Title: ***IoT-enabled Smart Ordering System***

###Members
1. Seng Nu Pan (sengnupan.kumgyi@gmail.com)
2. Kaung Htet San (kaunghtetsan275@gmail.com)
3. Khaing Zar Mon (m6522040556@g.siit.tu.ac.th)
4. Ei Thandar Phyu (eithandar.p@live.ku.th
5. Hnyot Myet Wunn Shunn Le Maung (hnyotmyetwunnshunnle.m@live.ku.th)
6. Nang Aeindray Kyaw (nangaeindray.k@live.ku.th)

###Hardware
1. M5Stack Core2 (M5Stack Core2)
    *CP210x USB serial
    *LCD 320x240
    *6-axis IMU MPU6886
2. M5Stack Basic (M5Stack Core ESP32)
    *CP210x USB serial
    *LCD 320x240
3. M5 CoreInk (M5Stack Core Ink)
    *CP210x USB serial
    *E-ink 200x200
4. M5StickC (M5Stick-C)
    *FTDI USB serial
    *LCD 80x160
    *6-axis IMU MPU6886
5. ATOM Echo (M5Stack-ATOM)
    *FTDI USB serial
6. ATOM Matrix (M5Stack-ATOM)
    *FTDI USB serial
    *LED 5x5
    *6-axis IMU MPU6886

##Objectives
1. To facilitate remote management and tracking order data.
2. To make ordering process more convenient and achieve customer satisfaction.
3. To develop a novel recommendation system to increase customer traction.

***User stories and acceptance criteria***
1. As a **customer**, I want to ***order food easily*** so that ***I will be satisfied.***
    Scenario: ***customer arrives***, given ***customer is in the shop***, when ***customer scan the QR code***, then ***the menu  will be displayed.***
    Scenario: ***Customer orders***, given ***customer reads the menu***, when ***customer has chosen the menu***, then ***order list will be displayed to the kitchen.***
    Scenario: ***order notification***, given ***the customer is in the queue***, when ***the order is ready***, then ***the customer will be notified.***


3. As a **kitchen staff**, I want to ***receive the order*** so that ***I can prepare the food.***
    Scenario: ***receive the order***, given ***the order list***, when ***the kitchen staff receives the order***, then ***the order will be recorded.***
    Scenario: ***prepare the food***, given ***the order list***, when ***the kitchen staff prepares the food***, then ***the food will be ready.***

4. As a ***shop owner***, I want to ***see the statistics and modify the content*** so that ***I can overview and manage the shop.***
    Scenario: ***sales report*** given ***the records from database*** when ***the shop owner selects the query based on date and time,*** then ***the corresponding report will be displayed.***
    Scenario: ***modify the menu*** given ***the analysis result*** when ***the demand changes,*** then ***the menu will be updated.***
