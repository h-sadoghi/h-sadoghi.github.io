---
layout: page
title: IPS project
description: Indoor positioning System for Engineering Department of Ferdowsi University of Mashhad, Iran
img: assets/img/EngineeringFUM.jpg
importance: 2
category: work
giscus_comments: true
---

## Applications of Indoor Positioning

Modern outdoor positioning systems, such as the **Global Positioning System (GPS)**, offer high accuracy for navigation in open spaces but face challenges when used indoors due to **weakened satellite signals** inside buildings. To overcome this limitation, a variety of *indoor positioning systems* (IPS) have emerged. IPS is extensively applied in environments like schools, offices, supermarkets, hospitals, and universities. For instance, in supermarkets, shoppers can use digital guide screens on carts equipped with RFID tags to easily locate products. In museums, visitors can access exhibit information using Bluetooth and Wi-Fi devices. IPS also aids students in navigating specific shelves in libraries and is utilized in targeted marketing, such as sending personalized advertisements to individuals based on their location within a building.

## Problem Statement and Research Motivation

Visitors to large complexes like hospitals, offices, stores, and universities often face difficulties in **finding optimal routes to their destinations**, leading to wasted time and energy. To address this issue, the research focuses on developing a **ubiquitous and cost-effective indoor positioning system** that leverages **existing infrastructure**. The goal is to design an IPS prototype for mobile phones, tested at the **Faculty of Engineering at Ferdowsi University of Mashhad**. This system will utilize the building's **Wi-Fi access points** for positioning, eliminating the need for additional infrastructure or high-cost solutions.

## System Overview

This production presents contributions in two key areas: **software development** and **machine learning**. First, the floor plan of the Faculty of Engineering was converted from AutoCAD to **GeoJSON**, an open-source format compatible with applications. An **Android app** was developed using Flutter to capture Wi-Fi signals and display the predicted location on a map. The data collected is stored on a **server**, where machine learning operations are also carried out. 

The machine learning component employs the **fingerprinting method** for positioning. During the offline phase, the data is cleaned, preprocessed, and stored in a database. To improve positioning accuracy, **Gaussian Process Regression** was used to enrich the offline data by considering the effect of the number of reference points. In the online phase, a **buffering mechanism** was introduced to provide smoother, more reliable location predictions. The final location is determined using the **weighted k-nearest neighbors (k-NN) algorithm**, and various **distance metrics** were analyzed for their impact on prediction accuracy.


<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/EngineeringFUM.jpg" title="example image" class="img-fluid rounded z-depth-1" %}
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/FingerprintingDiagram.jpg" title="example image" class="img-fluid rounded z-depth-1" %}
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/mobileapppic2.jpg" title="example image" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
  **Left to right:** Map of the Engineering Department at Ferdowsi University of Mashhad, Designed System for FUM, Mobile App

</div>
<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/ENG_FUM.jpg" title="example image" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
   IPS applied at the Engineering Department of Ferdowsi University of Mashhad, Iran 
</div>

Locations of Wi-Fi access points installed as part of the Indoor Positioning System (IPS). These access points are strategically placed to ensure optimal signal coverage and accurate positioning throughout the building. Their placement is crucial for minimizing dead zones and improving the overall precision of the system.

<div class="row justify-content-sm-center">
    <div class="col-sm-8 mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/ComputerGroup_ENG_FUM.jpg" title="example image" class="img-fluid rounded z-depth-1" %}
    </div>
    <div class="col-sm-4 mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/WiFiLocation.jpg" title="example image" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    Wifi Locations
</div>

## The Proposed Method

### Software Contributions

#### Indoor Mapping
Indoor positioning using **fingerprinting** relies on **supervised learning**, which requires **labeled data** to train the model. Many studies emphasize the modeling process, often overlooking the critical role of labeling in ensuring the system's comprehensiveness and usability. Traditionally, the positioning task is treated as a classification problem, with predefined reference points where signals are collected. While this method works well in controlled settings, it is not feasible in more dynamic environments like a university campus. To address these challenges, a **mobile-compatible map format** was necessary.

The original map, available in AutoCAD format, was unsuitable for mobile applications due to its proprietary nature. After considering several alternatives, ***GeoJSON*** was selected due to its open-standard and broad compatibility with modern software platforms. Consequently, the indoor map of all floors and corridors of the Faculty of Engineering at Ferdowsi University of Mashhad was converted into GeoJSON format. This approach allowed for the precise identification of all points on the map, across multiple floors, using **geographical coordinates (latitude and longitude)**, making them ideal as labels for the learning model.


*Faculty of Engineering Indoor Map*

#### Mobile Application and Server-Side Code
An **Android application** was developed using the *Flutter* framework to facilitate positioning. The app’s main feature is an interactive indoor map, allowing users to navigate easily through touch gestures—zooming, panning, and rotating the map. Additional features like switching between floors and displaying room names and hallways further enhance the user experience, enabling users to locate their desired destination.

The app serves two key functions:
1. **Recording Wi-Fi signals for training data** and transmitting this data to the server.
2. **Capturing Wi-Fi signals during testing**, sending them to the server, and **displaying the predicted location** on the map, as determined by the learning model.

*Mobile App*

Once the signals are captured, users can send the recorded data to the server. This data includes the **timestamp**, **device model**, **latitude and longitude** of the signal capture, **floor number**, and a list of detected Wi-Fi signals. For each Wi-Fi access point, the list records the **SSID**, **BSSID**, and **received signal strength** in ***dBm (decibel-milliwatts)***.

Communication between the mobile app and server is facilitated through a *Flask API*, and upon receipt, the data is stored in a *SQLite database*.

$$
dBm = 10 \times \log_{10}\left(\frac{P}{1 mW}\right)
$$




{% raw %}

```html

```

{% endraw %}
