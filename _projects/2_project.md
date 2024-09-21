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
        {% include figure.liquid loading="eager" path="assets/img/5.jpg" title="example image" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    This image can also have a caption. It's like magic.
</div>

You can also put regular text between your rows of images.
Say you wanted to write a little bit about your project before you posted the rest of the images.
You describe how you toiled, sweated, _bled_ for your project, and then... you reveal its glory in the next row of images.

<div class="row justify-content-sm-center">
    <div class="col-sm-8 mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/6.jpg" title="example image" class="img-fluid rounded z-depth-1" %}
    </div>
    <div class="col-sm-4 mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/11.jpg" title="example image" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    You can also have artistically styled 2/3 + 1/3 images, like these.
</div>

The code is simple.
Just wrap your images with `<div class="col-sm">` and place them inside `<div class="row">` (read more about the <a href="https://getbootstrap.com/docs/4.4/layout/grid/">Bootstrap Grid</a> system).
To make images responsive, add `img-fluid` class to each; for rounded corners and shadows use `rounded` and `z-depth-1` classes.
Here's the code for the last row of images above:

{% raw %}

```html
<div class="row justify-content-sm-center">
  <div class="col-sm-8 mt-3 mt-md-0">
    {% include figure.liquid path="assets/img/6.jpg" title="example image" class="img-fluid rounded z-depth-1" %}
  </div>
  <div class="col-sm-4 mt-3 mt-md-0">
    {% include figure.liquid path="assets/img/11.jpg" title="example image" class="img-fluid rounded z-depth-1" %}
  </div>
</div>
```

{% endraw %}
