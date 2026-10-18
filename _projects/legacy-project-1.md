---
layout: legacy_page
title: Firefighter locator and vital-sign recorder
permalink: /projects/legacy-project-1/
description: Research and engineering project — archived description
nav: false
math: false
mermaid:
  enabled: false
  zoomable: false
legacy_source: https://hadisadoghiyazdi1971.github.io/projects/project-1/
legacy_group: Engineering projects
importance: 20
category: work
img: assets/img/legacy/outline-project1-fd238de324.png
legacy_dir: ltr
lang: en
---

{% raw %}
<picture><source type="image/webp" srcset="/assets/img/legacy/outline-project1-fd238de324-480.webp 480w, /assets/img/legacy/outline-project1-fd238de324-800.webp 800w, /assets/img/legacy/outline-project1-fd238de324-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/outline-project1-fd238de324.png" alt="outline_project11"></picture>

## Abstarct

This work presents the design and fabrication of a portable locator kit equipped with a transmitter and recorder for monitoring firefighters’ vital signs. The system integrates real-time physiological data acquisition with location tracking to enhance safety during emergency operations. A compact transmitter relays heart rate, temperature, and oxygen levels to a remote station for continuous monitoring. The proposed solution improves situational awareness, enabling rapid intervention in hazardous conditions.

## Key features

- **Integrated Monitoring:** Measures vital signs such as heart rate, body temperature, and oxygen saturation in real-time.
- **Location Tracking:** Built-in transmitter provides accurate firefighter positioning inside hazardous environments.
- **Data Recording & Transmission:** Stores and wirelessly transmits vital data to a remote monitoring station for rapid response.
- **Rugged & Portable Design:** Compact, durable, and heat-resistant kit suitable for extreme firefighting conditions.
- **Enhanced Safety:** Enables early detection of health risks and supports timely rescue operations.

## Specialist Features

- **LifePulse Capture** – Receives the firefighter's vital signs in real-time.
- **Intra-Rescue Locator** – Obtains precise coordinates inside the building.
- **GuardianLink Transmission** – Sends vital signs, coordinates, and movement route to the operations control center.

## Processor System Architecture: Understanding Information Flow

This comprehensive guide explores the **fundamental processor system architecture** that forms the backbone of modern computing systems. The diagram illustrates a basic information processing system with four key components connected in a network structure, representing how data moves through a processing pipeline from input source to final output destination.

<picture><source type="image/webp" srcset="/assets/img/legacy/processorsystemdiagram-02415eb59c-480.webp 480w, /assets/img/legacy/processorsystemdiagram-02415eb59c-800.webp 800w, /assets/img/legacy/processorsystemdiagram-02415eb59c-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/processorsystemdiagram-02415eb59c.png" alt="ProcessorSystemDiagram1"></picture>

_Figure 1: Processor System Architecture Diagram showing the flow of information between system components_

### Key Components of the Processor System Architecture

**Sender Component**

- The origin point of data transmission
- Initiates the information flow process
- Provides raw input to the system

**Input Information Channel**

- Communication pathway from sender to processor
- Transmits data in a structured format
- Ensures integrity of incoming information

**Central Processing Unit (Processor)**

- The computational heart of the system
- Executes instructions on received data
- Transforms input into meaningful output

**Output Delivery System**

- Transmits processed information to destination
- Completes the information processing cycle
- Delivers results in usable format

<picture><source type="image/webp" srcset="/assets/img/legacy/constructed-1431fb7f49-480.webp 480w, /assets/img/legacy/constructed-1431fb7f49-800.webp 800w, /assets/img/legacy/constructed-1431fb7f49-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/constructed-1431fb7f49.png" alt="Constructed1"></picture>

## Transmission Phase

### Input information travels through dedicated channels

This diagram depicts the directional data flow between a laboratory environment and a central server system. The arrow indicates that information, experimental data, or research results are transmitted from the laboratory (smaller entity) to the central server (larger entity) for storage, processing, or further distribution. This represents a typical data management architecture in research or clinical settings.

<picture><source type="image/webp" srcset="/assets/img/legacy/laboratorycentralserverdiagram-c4f4c8ac7b-480.webp 480w, /assets/img/legacy/laboratorycentralserverdiagram-c4f4c8ac7b-800.webp 800w, /assets/img/legacy/laboratorycentralserverdiagram-c4f4c8ac7b-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/laboratorycentralserverdiagram-c4f4c8ac7b.png" alt="LaboratoryCentralServerDiagram"></picture>

Figure 2: Laboratory to Central Server Diagram- Data communication flow from laboratory to central server infrastructure.

## Indoor positioning system

<a href="https://en.wikipedia.org/wiki/Indoor_positioning_system#:~:text=An%20indoor%20positioning%20system%20(IPS,parking%20garages%2C%20and%20underground%20locations." target="_blank">
      <strong>Indoor positioning system</strong>
    </a> Using a GPS-independent positioning system called Pedestrian Dead Reckoning (PDR) which is developed based on the Indoor Positioning System (INS)
Using a low-power long-range network called LoRa to communicate between the firefighter kit and the operations control center server and also obtaining the location of a node in the network by detecting the signal strength of that node with three independent servers around the building Hardware consists of two parts: 
**Kit with firefighter**
**Server in the operation control center**

### Components

a) INS Positioning
b) Using Kalman Filter
c) External Modifier in Indoor Environment: Positioning by LoRa Network

<picture><source type="image/webp" srcset="/assets/img/legacy/insflowchart-05bdb364ac-480.webp 480w, /assets/img/legacy/insflowchart-05bdb364ac-800.webp 800w, /assets/img/legacy/insflowchart-05bdb364ac-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/insflowchart-05bdb364ac.png" alt="INSFlowchart1"></picture>

This flowchart outlines the operational framework of an Inertial Navigation System <a href="https://en.wikipedia.org/wiki/Inertial_navigation_system" target="_blank">
<strong>INS</strong>
</a>

, which determines position, velocity, and orientation in 3D space. The system integrates sensor inputs—accelerometers for linear acceleration, gyroscopes for angular velocity, and optionally magnetometers for compass reference—along with previous state data. External correctors such as GPS periodically calibrate errors. Through continuous algorithmic processing, the INS outputs location, speed, and heading in real time, enabling reliable navigation even without external signals, crucial for aviation, maritime, space, and autonomous vehicles.

## Demonstration of the performance of the inertial positioning system at <a href="https://www.um.ac.ir/" target="_blank"><strong>Ferdowsi University of Mashhad</strong></a>

<picture><source type="image/webp" srcset="/assets/img/legacy/ips-fum-87869130eb-480.webp 480w, /assets/img/legacy/ips-fum-87869130eb-800.webp 800w, /assets/img/legacy/ips-fum-87869130eb-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/ips-fum-87869130eb.png" alt="IPSFFUM1"></picture>

## Related Links and products

- <a href="https://equivital.com/products/ex-eq02-lifemonitor" target="_blank">
      <strong>Integrated Monitoring</strong> 
  </a> – Measures vital signs such as heart rate, body temperature, and oxygen saturation in real-time.
- <a href="https://us.msasafety.com/connected-firefighter/firegrid?locale=en" target="_blank">
      <strong>Data Recording &amp; Transmission</strong> 
  </a> – Stores and wirelessly transmits vital data to a remote monitoring station for rapid response.
- <a href="https://connect.na.panasonic.com/toughbook/solutions/firefighter" target="_blank">
        <strong>Rugged &amp; Portable Design</strong> 
    </a> – Compact, durable, and heat-resistant kit suitable for extreme firefighting conditions.
  {% endraw %}
