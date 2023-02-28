# SoftwareDesignAIoT
#Title: ***IoT-enabled Smart Ordering System***

***Members***
1. Seng Nu Pan (sengnupan.kumgyi@gmail.com)
2. Kaung Htet San (kaunghtetsan275@gmail.com)
3. Khaing Zar Mon (m6522040556@g.siit.tu.ac.th)
4. Ei Thandar Phyu (eithandar.p@live.ku.th
5. Hnyot Myet Wun Shunn Le Maung (hnyotmyetwunnshunnle.m@live.ku.th)
6. Nang Aeindray Kyaw (nangaeindray.k@live.ku.th)

***Hardware***
1. M5Stack Core2 (M5Stack Core2)
    CP210x USB serial
    LCD 320x240
    6-axis IMU MPU6886
2. M5Stack Basic (M5Stack Core ESP32)
    CP210x USB serial
    LCD 320x240
3. M5 CoreInk (M5Stack Core Ink)
    CP210x USB serial
    E-ink 200x200
4. M5StickC (M5Stick-C)
    FTDI USB serial
    LCD 80x160
    6-axis IMU MPU6886
5. ATOM Echo (M5Stack-ATOM)
    FTDI USB serial
6. ATOM Matrix (M5Stack-ATOM)
    FTDI USB serial
    LED 5x5
    6-axis IMU MPU6886

***Objectives***
1. To facilitate remote management and tracking order data.
2. To make ordering process more convenient and achieve customer satisfaction.
3. To develop a novel recommendation system to promote customer traction.

***User stories and acceptance criteria***
1. As a **shop owner**, I want to **provide better ordering service** so that **customer satisfaction can be provided.**

    Scenario: ***customer arrives***, given ***customer is in the shop***, when ***customer presses the button***, then ***menu  will be displayed***.
    Scenario: ***Customer orders***, given ***customer reads the menu***, when ***customer has chosen the menu***, then ***order list will be displayed to the kitchen.***
2. As a ***customer***, I want to ***know order queues,*** so that ***I can want comfortably.***
    Scenario: ***order notification***, given ***the device is in customer hand*** when ***the order is ready,*** then ***I want to be notified.***
    Scenario: ***Queue Reduction,*** given ***the device is out of customer hand,*** when ***the customer get the order,*** then ***the number of queues from all devices will be updated.***
3. As a ***shop owner***, I want to ***track the order history,*** so that ***I can have more customer traction.***
    Scenario: ***Customer Recommendation,*** given ***the recommendation system is activated,*** when ***the user chooses a specific menu,*** then ***the complementary items will be displayed.***
    Scenario: ***Order Tracking*** given ***the records of daily orders,*** when ***date is selected, then order list is presented.***
