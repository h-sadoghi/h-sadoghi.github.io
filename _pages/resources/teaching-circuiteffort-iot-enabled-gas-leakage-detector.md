---
layout: legacy_page
title: IoT-Enabled Gas Leakage Detector
permalink: /resources/teaching-circuiteffort-iot-enabled-gas-leakage-detector/
description: Archived teaching material
nav: false
math: true
mermaid:
  enabled: false
  zoomable: false
legacy_source: https://hadisadoghiyazdi1971.github.io/teaching/studenteffort/circuiteffort/iot_enabled_gas_leakage_detector/
legacy_group: Circuits and electronics
legacy_dir: ltr
lang: en
---

{% raw %}

## Mahdi Ahmadi

<div markdown="1">

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/mahdi-00ba8c7ba2-480.webp 480w, /assets/img/legacy/mahdi-00ba8c7ba2-800.webp 800w, /assets/img/legacy/mahdi-00ba8c7ba2-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/mahdi-00ba8c7ba2.jpg" alt="my picture"></picture>

</div>

</div>

## Table of Contents

<!-- prettier-ignore -->
* TOC
{:toc}

## Introduction

Welcome to this tutorial! In this guide, we'll learn how to create an IoT-based Gas Leakage Detection System using the NodeMCU board and the MQ-2 gas sensor. This project integrates IoT technology, allowing you to monitor and control the system remotely from your mobile phone using the Blynk app.

The primary goal of this project is to design a low-cost, home security solution that can detect dangerous gas leaks and send notifications to your phone. It is particularly useful for preventing accidents caused by gas leakage, providing a convenient way to stay informed and alert even when you are not at home.

The system works by using the MQ-2 sensor to detect gas leakage. Once the sensor detects a gas leak, the system triggers an alert mechanism including a buzzer and LEDs, while simultaneously sending a push notification to your smartphone. Additionally, the gas levels are displayed on an LCD screen and the Blynk app interface, making it easy to monitor the status of the system in real-time.

This project is an excellent example of how IoT can be applied in everyday life to improve safety and security.

## Components

To build the Gas Leakage Detection System, you will need the following components:
| **Component** | **Quantity** | **Description/Link** |
|-----------------------------|--------------|------------------------------|
| **NodeMCU (ESP8266)** | 1 | A Wi-Fi development board to connect the sensor and send data to the Blynk app. |
| **MQ-2 Gas Sensor** | 1 | A sensor for detecting gases like LPG, smoke, and carbon monoxide. |
| **16x2 LCD Display** | 1 | To display gas levels and system status. |
| **I2C Module** | 1 | For simplifying connections between the LCD and NodeMCU. |
| **Buzzer** | 1 | Provides an audible alert when a gas leak is detected. |
| **Red LED** | 1 | Indicates a gas leak (on when a leak is detected). |
| **Green LED** | 1 | Indicates normal operation (on when no leak is detected). |
| **180-ohm Resistor** | 2 | Used for limiting current to LEDs. |
| **Breadboard** | 1 | For building the circuit without soldering. |
| **Jumper Wires** | Several | For connecting components on the breadboard. |

The system is designed to be affordable and easy to assemble, making it a great project for anyone interested in learning about IoT and home automation.

here is the picture of some important components:

**NodeMCU (ESP8266)**

<div markdown="1">

<div markdown="1">

    <img loading="lazy" src="/assets/img/legacy/nodemcu-8f039ade52.webp" alt="NodeMCU (ESP8266)">

</div>

</div>

<div class="caption" markdown="1">

NodeMCU (ESP8266) with labels on all pins

</div>

**16x2 LCD Display** and **I2C Module**

<div markdown="1">

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/i2c-2d4ce1b459-480.webp 480w, /assets/img/legacy/i2c-2d4ce1b459-800.webp 800w, /assets/img/legacy/i2c-2d4ce1b459-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/i2c-2d4ce1b459.jpg" alt="I2C Module"></picture>

</div>

</div>

<div class="caption" markdown="1">

I2C Module with labels on all pins

</div>

<div markdown="1">

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/lcd-96692d5cca-480.webp 480w, /assets/img/legacy/lcd-96692d5cca-800.webp 800w, /assets/img/legacy/lcd-96692d5cca-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/lcd-96692d5cca.png" alt="16x2 LCD Display"></picture>

</div>

</div>

<div class="caption" markdown="1">

16x2 LCD Display details of all pins

</div>

**MQ-2 Gas Sensor**

<div markdown="1">

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/mq2-80aa69e461-480.webp 480w, /assets/img/legacy/mq2-80aa69e461-800.webp 800w, /assets/img/legacy/mq2-80aa69e461-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/mq2-80aa69e461.jpg" alt="MQ-2 Gas Sensor"></picture>

</div>

</div>

<div class="caption" markdown="1">

MQ-2 Gas Sensor labels

</div>

<div markdown="1">

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/mq2-back-bb32fe4f81-480.webp 480w, /assets/img/legacy/mq2-back-bb32fe4f81-800.webp 800w, /assets/img/legacy/mq2-back-bb32fe4f81-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/mq2-back-bb32fe4f81.jpg" alt="MQ-2 Gas Sensor back"></picture>

</div>

</div>

<div class="caption" markdown="1">

back of MQ-2 Gas Sensor details

</div>

## Circuit Diagram

<div markdown="1">

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/circuit-diagram-a93e23fc02-480.webp 480w, /assets/img/legacy/circuit-diagram-a93e23fc02-800.webp 800w, /assets/img/legacy/circuit-diagram-a93e23fc02-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/circuit-diagram-a93e23fc02.png" alt="Circuit Diagram"></picture>

</div>

</div>

<div class="caption" markdown="1">

Circuit Diagram designed by Proteus

</div>

> Always use a resistor in series with an LED to limit the current and protect the component from damage.

---

## How to Calculate the Resistor Value

Use **Ohm’s Law** to determine the appropriate resistor:

$$
Min Resistor = \frac{V_{\text{supply}} - V_f}{Max Current}
$$

Where:

- V_supply : Power supply voltage (Volts)
- V_f : LED forward voltage (Volts)
- I : Desired LED current (Amps, e.g. 20 mA = 0.02 A)

---

### LED Resistor Reference Table

| **Power Supply** | **LED Vf** | **Max Current** | **Min Resistor (Ω)** |
| ---------------- | ---------- | --------------- | -------------------- |
| 3V               | 2.0V       | 20 mA           | 50 Ω                 |
| 4.5V             | 2.0V       | 20 mA           | 125 Ω                |
| 5V               | 2.0V       | 20 mA           | 150 Ω                |
| 9V               | 2.0V       | 20 mA           | 350 Ω                |
| 3V               | 3.0V       | 20 mA           | LED OFF              |
| 4.5V             | 3.0V       | 20 mA           | 75 Ω                 |
| 5V               | 3.0V       | 20 mA           | 100 Ω                |
| 9V               | 3.0V       | 20 mA           | 300 Ω                |

---

> **Note:** If the supply voltage is equal to or less than the LED’s forward voltage, the LED will **not light up**.

## Set up Blynk IoT Cloud

First, go to the [Blynk Website](https://blynk.cloud/dashboard/login) and log in.

---

### Step 1: Log In

Click on **Log In** and enter your account credentials.

<div markdown="1">

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/login-df7c9717af-480.webp 480w, /assets/img/legacy/login-df7c9717af-800.webp 800w, /assets/img/legacy/login-df7c9717af-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/login-df7c9717af.png" alt="Login Image"></picture>

</div>

</div>

<div class="caption" markdown="1">

login screen

</div>

---

### Step 2: Create a New Template

Now we are going to create a new template for this project.

- In the **Dashboard**, click on the **Developer Zone** tab.
- Then select **My Templates**.
- Click on the **New Template** button.

You can also use the **Quickstart Template**, but it provides fewer configuration options.

<div markdown="1">

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/template-bd220f2683-480.webp 480w, /assets/img/legacy/template-bd220f2683-800.webp 800w, /assets/img/legacy/template-bd220f2683-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/template-bd220f2683.png" alt="Quickstart Template"></picture>

</div>

</div>

<div class="caption" markdown="1">

Quickstart Template:screen of templates

</div>

---

### Step 3: Configure the Template

Now configure your template settings.

<div markdown="1">

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/config1-2765658d3a-480.webp 480w, /assets/img/legacy/config1-2765658d3a-800.webp 800w, /assets/img/legacy/config1-2765658d3a-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/config1-2765658d3a.png" alt="Configuration template"></picture>

</div>

</div>

<div class="caption" markdown="1">

Configuration template:create new template and adjust details

</div>

---

### Step 4: Create Datastreams

Now we need to create two datastreams for our project:

- One for reading the gas sensor value.
- One for controlling the system (ON/OFF switch).

---

#### 1. Create Gas Sensor Datastream

- In your template, go to the **Datastreams** tab.
- Click on **New Datastream** and select **Virtual Pin**.
- Set the following options:
  - **Name:** Gas Value
  - **Virtual Pin:** V1
  - **Data Type:** Integer
  - **Min Value:** 0
  - **Max Value:** 1023
  - **Unit:** AQ (or PPM)
- Then click **Create**.

<div markdown="1">

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/config3-e47d0b3533-480.webp 480w, /assets/img/legacy/config3-e47d0b3533-800.webp 800w, /assets/img/legacy/config3-e47d0b3533-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/config3-e47d0b3533.png" alt="Configuration datastream1"></picture>

</div>

</div>

<div class="caption" markdown="1">

Configuration datastream: create new datastream

</div>

<div markdown="1">

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/config4-cfb21bd3e6-480.webp 480w, /assets/img/legacy/config4-cfb21bd3e6-800.webp 800w, /assets/img/legacy/config4-cfb21bd3e6-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/config4-cfb21bd3e6.png" alt="Configuration datastream2"></picture>

</div>

</div>

<div class="caption" markdown="1">

Configuration datastream: adjust pins

</div>

---

#### 2. Create Switch Control Datastream

- Again, click on **New Datastream** and select **Virtual Pin**.
- Set the following options:
  - **Name:** System Control
  - **Virtual Pin:** V0
  - **Data Type:** Integer
  - **Min Value:** 0
  - **Max Value:** 1
- Then click **Create**.

<div markdown="1">

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/config5-f1afd674ce-480.webp 480w, /assets/img/legacy/config5-f1afd674ce-800.webp 800w, /assets/img/legacy/config5-f1afd674ce-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/config5-f1afd674ce.png" alt="Configuration datastream3"></picture>

</div>

</div>

<div class="caption" markdown="1">

Configuration datastream: adjust switch control

</div>

---

### Step 5: Set Up the Dashboard

At this stage, you must design a dashboard to monitor and control your system.
You can either use the Web Dashboard or the Mobile Dashboard, depending on your preference.
In this guide, we are showing how to use the Web Dashboard, but the same widgets and data bindings are available on the mobile app as well.

---

#### 1. Open Web Dashboard

- In your template, go to the **Web Dashboard** tab.

---

#### 2. Add Gas Sensor Display

- Select the **Gauge** widget.
- Drag and place it where you want.
- Click on the widget to edit its settings:
  - **Datastream:** Select **Gas Value (V1)**.
  - **Label:** Gas Level

<div markdown="1">

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/web-dashboard-1-76b20e67a2-480.webp 480w, /assets/img/legacy/web-dashboard-1-76b20e67a2-800.webp 800w, /assets/img/legacy/web-dashboard-1-76b20e67a2-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/web-dashboard-1-76b20e67a2.png" alt="Configuration dashboard1"></picture>

</div>

</div>

<div class="caption" markdown="1">

Configuration dashboard: add new widget

</div>

<div markdown="1">

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/web-dashboard-2-377e3833b2-480.webp 480w, /assets/img/legacy/web-dashboard-2-377e3833b2-800.webp 800w, /assets/img/legacy/web-dashboard-2-377e3833b2-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/web-dashboard-2-377e3833b2.png" alt="Configuration dashboard2"></picture>

</div>

</div>

<div class="caption" markdown="1">

Configuration dashboard: Guage settings

</div>

---

#### 3. Add System Control Switch

- Select the **Switch** widget.
- Drag and place it.
- Click on the widget to edit its settings:
  - **Datastream:** Select **System Control (V0)**.
  - **Label:** System ON/OFF

<div markdown="1">

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/web-dashboard-3-8059793cc2-480.webp 480w, /assets/img/legacy/web-dashboard-3-8059793cc2-800.webp 800w, /assets/img/legacy/web-dashboard-3-8059793cc2-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/web-dashboard-3-8059793cc2.png" alt="Configuration dashboard3"></picture>

</div>

</div>

<div class="caption" markdown="1">

Configuration dashboard: Switch settings

</div>

---

#### 4. Save Changes

After adding and configuring the widgets, click **Save** to apply the changes.

---

### Step 6: Add Device

After setting up the template and Web Dashboard, it's time to create a device based on your template.

---

#### 1. Go to the Devices Page

- In the **Dashboard**, click on the **Devices** tab.
- Then click **New Device**.

<div markdown="1">

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/newdevice-b2f15feeca-480.webp 480w, /assets/img/legacy/newdevice-b2f15feeca-800.webp 800w, /assets/img/legacy/newdevice-b2f15feeca-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/newdevice-b2f15feeca.png" alt="Add device"></picture>

</div>

</div>

<div class="caption" markdown="1">

Add device in webdashbord

</div>

---

#### 2. Create Device from Template

- Select **From Template**.
- Choose your created template.
- Give your device a name.
- Click **Create**.

<div markdown="1">

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/fromtemplate-f9d78a00c9-480.webp 480w, /assets/img/legacy/fromtemplate-f9d78a00c9-800.webp 800w, /assets/img/legacy/fromtemplate-f9d78a00c9-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/fromtemplate-f9d78a00c9.png" alt="Create Device from Template1"></picture>

</div>

</div>

<div class="caption" markdown="1">

Create Device from Template: choosing way to create new device

</div>

<div markdown="1">

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/fromtemplate2-b3bfd90e80-480.webp 480w, /assets/img/legacy/fromtemplate2-b3bfd90e80-800.webp 800w, /assets/img/legacy/fromtemplate2-b3bfd90e80-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/fromtemplate2-b3bfd90e80.png" alt="Create Device from Template2"></picture>

</div>

</div>

<div class="caption" markdown="1">

Create Device from Template: choosing template

</div>

---

#### 3. Get Authentication Token (Auth Token)

- After the device is created, open the **Device Settings** (click on **Developer Tools**).
- You can either copy the **Auth Token** directly, or copy the complete **Firmware Configuration** from the Firmware Info section, as shown below.

<div markdown="1">

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/firmware-fa33daa1f1-480.webp 480w, /assets/img/legacy/firmware-fa33daa1f1-800.webp 800w, /assets/img/legacy/firmware-fa33daa1f1-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/firmware-fa33daa1f1.png" alt="Auth Token"></picture>

</div>

</div>

<div class="caption" markdown="1">

Get Authentication Token (Auth Token)

</div>

You will need this token later when programming your NodeMCU (ESP8266) to connect to the Blynk Cloud.

---

### Step 7: Enable Notifications (Optional but Recommended)

To receive notifications (e.g. alerts when gas levels are high), you need to define an event in Blynk and enable push notifications.

#### Steps:

1. Go to the **Event & Notification** section in the Blynk Console (from the left sidebar).
2. Click **New Event** to create a custom event.
3. Fill in the required details such as:
   - **Event Name** (e.g. `Gas_Alert`)
   - **Severity Level** (e.g. Warning or Critical)
   - **Notification Settings**
4. Make sure to **enable push notifications** so that you receive alerts via the mobile app.

> ⚠️ **Important:**  
> Push notifications only work if you are logged into the Blynk mobile app with notifications enabled for the app on your phone.

Once the event is configured and triggered from your device's code (e.g. via `Blynk.logEvent("Gas_Alert")`), you'll get a notification on your phone instantly.

### Source Code:

> **Note**  
> You need to change the following credentials before uploading the code to your ESP8266:
>
> ```cpp
> #define BLYNK_TEMPLATE_ID "TMPL4j48PdzNW"
> #define BLYNK_TEMPLATE_NAME "gas leakage detection"
> #define BLYNK_AUTH_TOKEN "vM_Sx9J_PK_6RYtQZCvijW6_OlN72Ic0"
>
> char ssid[] = "xxxxxxxxxx";
> char pass[] = "xxxxxxxxxx";
> ```

> The above details should be updated according to your specific WiFi network and Blynk credentials.

Then We Uploading the Code In ESP8266

```python
// Blynk template credentials
#define BLYNK_TEMPLATE_ID "TMPL4ezsC8keZ"
#define BLYNK_TEMPLATE_NAME "gas leakage detection"
#define BLYNK_AUTH_TOKEN "UnSt9REz59sPpVGMfypVL2iebBSuWbZt"

#include <ESP8266WiFi.h>
#include <BlynkSimpleEsp8266.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// Pin and threshold definitions
#define MQ_PIN A0              // Analog pin connected to MQ gas sensor
#define BUZZER D5              // Buzzer pin
#define LED_NORMAL D6          // Green LED - Normal status
#define LED_ALERT D7           // Red LED - Gas alert
#define GAS_THRESHOLD 900      // Threshold for gas detection

// Wi-Fi credentials
char ssid[] = "your wifi";
char pass[] = "password of wifi";

// LCD and Blynk timer
LiquidCrystal_I2C lcd(0x27, 16, 2);
BlynkTimer timer;

// Flag to control system ON/OFF via Blynk switch
bool systemActive = true;

// Blynk virtual pin V0 - Toggle system ON/OFF
BLYNK_WRITE(V0) {
  int value = param.asInt();
  systemActive = (value == 1);

  if (systemActive) {
    Serial.println("System activated");
    lcd.setCursor(0, 1);
    lcd.print("System ON       ");
  } else {
    Serial.println("System deactivated");
    lcd.setCursor(0, 1);
    lcd.print("System OFF      ");

    // Turn off all outputs
    digitalWrite(LED_ALERT, LOW);
    digitalWrite(LED_NORMAL, LOW);
    digitalWrite(BUZZER, LOW);
  }
}

// Send sensor data to Blynk
void sendToBlynk() {
  if (!systemActive) {
    Blynk.virtualWrite(V1, "System Off");
    return;
  }

  int gasValue = analogRead(MQ_PIN);
  Blynk.virtualWrite(V1, gasValue);

  if (gasValue > GAS_THRESHOLD) {
    Blynk.virtualWrite(V1, "Gas Alert!");
    Blynk.logEvent("gas_alert", "Gas level is HIGH!");
  } else {
    Blynk.virtualWrite(V1, "Normal");
  }
}

void setup() {
  Serial.begin(115200);

  pinMode(MQ_PIN, INPUT);
  pinMode(LED_NORMAL, OUTPUT);
  pinMode(LED_ALERT, OUTPUT);
  pinMode(BUZZER, OUTPUT);

  // Initial hardware states
  digitalWrite(LED_NORMAL, HIGH);
  digitalWrite(LED_ALERT, LOW);
  digitalWrite(BUZZER, LOW);

  // Initialize LCD
  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("Gas Detector");
  delay(1000);
  lcd.clear();

  // Connect to Blynk
  Blynk.begin(BLYNK_AUTH_TOKEN, ssid, pass);
  timer.setInterval(1000L, sendToBlynk); // Run every 1 second
}

void loop() {
  Blynk.run();
  timer.run();

  if (!systemActive) {
    return;  // System is off; skip all processing
  }

  int gasValue = analogRead(MQ_PIN);
  Serial.print("Gas value: ");
  Serial.println(gasValue);

  // Display gas value on LCD
  lcd.setCursor(0, 0);
  lcd.print("Gas: ");
  lcd.print(gasValue);
  lcd.print("    "); // Clear extra characters

  // Gas leak detection
  if (gasValue > GAS_THRESHOLD) {
    digitalWrite(LED_NORMAL, LOW);
    digitalWrite(LED_ALERT, HIGH);
    digitalWrite(BUZZER, HIGH);

    lcd.setCursor(0, 1);
    lcd.print("!!! GAS ALERT !!!");

  } else {
    digitalWrite(LED_NORMAL, HIGH);
    digitalWrite(LED_ALERT, LOW);
    digitalWrite(BUZZER, LOW);

    lcd.setCursor(0, 1);
    lcd.print("Status: Normal   ");
  }

  delay(1000); // Basic delay for stability
}
```

### Project Demo

In this project, I tested the gas leakage detection system by turning on the gas. After a few seconds, the MQ-2 sensor detected the gas. The Blynk Web Dashboard showed the gas status with a red LED indicator, while the LCD displayed an alert message and the buzzer beeped.

When the gas level is below 900, the system returns to a normal condition: the green LED turns on, and the buzzer stops beeping.

---

### References

<a href="https://justdoelectronics.com/mq2-gas-leakage-detection-with-blynk-notification/" target="_blank"><strong>MQ2 Gas Leakage Detection with Blynk Notification – JustDoElectronics</strong></a>

<a href="https://iotcircuithub.com/mq2-gas-sensor-rain-detection-blynk-notification/" target="_blank"><strong>MQ2 Gas Sensor & Rain Detection with Blynk – IoT Circuit Hub</strong></a>

<a href="https://www.viralsciencecreativity.com/post/mq2-gas-leakage-smoke-detection-system" target="_blank"><strong>MQ2 Gas Leakage Smoke Detection System – Viral Science</strong></a>

<a href="https://www.gsnetwork.com/led-resistor-values-for-current-limiting-resistor/" target="_blank"><strong>LED Resistor Values for Current Limiting – GS Network</strong></a>

> Some parts of this project were inspired by the tutorials listed above.
> {% endraw %}
