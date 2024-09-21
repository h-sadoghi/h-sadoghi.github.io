---
layout: page
title: Interactive wall
description: Augmented Reality (AR)
img: assets/img/catalog-front-new.jpg
importance: 1
category: work
related_publications: true
---

Interactive wall is an interactive system using a 3D camera, like Kinect, for engaging children in educational and entertainment activities. The components of this system are:

### System Components and Workflow

1. **3D Camera (Kinect)**:
   - **Purpose**: Captures 3D depth images of the environment and objects.
   - **Challenges**:
     - **Depth Estimation**: Accurately measuring the distance of objects from the camera.
     - **Camera Tilt**: Understanding how tilting affects depth perception and image quality.
     - **Calibration**: Ensuring the camera is correctly calibrated to provide accurate depth information.

2. **Image Processing Processor**:
   - **Purpose**: Performs real-time image processing algorithms on the 3D data to interpret and interact with the images.
   - **Challenges**:
     - **Processing Speed**: Ensuring the algorithms run quickly enough to provide real-time feedback.
     - **Algorithm Accuracy**: Developing algorithms that can accurately interpret depth data and handle variations in lighting and perspective.

3. **Artificial Intelligence Engine (Python)**:
   - **Purpose**: Uses AI algorithms to enhance interactivity, such as recognizing gestures or analyzing the child's actions.
   - **Challenges**:
     - **Integration**: Ensuring smooth communication between the Python-based AI and the image processing module.
     - **Model Training**: Training AI models to recognize and react to the various inputs from the Kinect.

4. **Software for Initial Settings and Game Type Determination (C#)**:
   - **Purpose**: Provides a user interface for setting up the system and selecting different games or educational activities.
   - **Challenges**:
     - **User Interface Design**: Creating an intuitive interface for users to configure settings and choose games.

5. **Game Development (UNITY)**:
   - **Purpose**: Creates the interactive games or educational activities.
   - **Challenges**:
     - **Integration**: Integrating real-time 3D data with the Unity game environment.
     - **Interactivity**: Ensuring the games respond correctly to the child’s actions and movements.

### Applications

- **Education**:
  - **Language Learning**: Games can be designed to teach new vocabulary or language skills through interactive play.
  - **Math Education**: Educational games can help teach basic arithmetic and problem-solving skills in a fun and engaging way.

- **Entertainment**:
  - **Engagement**: Creating interactive experiences that keep children entertained while also learning.
  - **Children with Autism**: Developing tailored activities that can help improve social interaction, motor skills, or sensory processing.

### Addressing Challenges

- **Camera Calibration**: Use calibration tools and techniques to ensure the camera’s depth measurements are accurate. This might involve capturing calibration patterns or using known reference objects.
  
- **Depth Estimation**: Implement algorithms that can handle variations in object distance and environmental factors. Machine learning models can be trained to improve depth estimation accuracy.

- **Tilt Compensation**: Use mathematical models or calibration data to adjust for camera tilt, ensuring that depth information remains accurate even if the camera is not perfectly aligned.

- **Real-time Processing**: Optimize algorithms and code to handle real-time data processing. This may involve using efficient data structures, parallel processing, or dedicated hardware acceleration.

By addressing these challenges and leveraging the strengths of each component, you can create a robust system that provides interactive and educational experiences for children.

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/catalog-front-new.jpg" title="example image" class="img-fluid rounded z-depth-1" %}
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/catalog-back-new.jpg" title="example image" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    Interactive Wall Catalog
</div>
<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/InteractiveWall_1.jpg" title="example image" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    Atractive Game 
</div>

Interactive Smart Wall:
- Created an Interactive Smart Wall, enabling the display of interactive images on an ordinary wall.
- Developed diverse interactive games for entertainment and engagement on the wall.
- Implemented intelligent and interactive advertising features on the wall, providing an innovative promotional platform.

<div class="row justify-content-sm-center">
    <div class="col-sm-8 mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/InteractiveWall_2.jpg" title="example image" class="img-fluid rounded z-depth-1" %}
    </div>
    <div class="col-sm-4 mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/InteractiveWall_3.jpg" title="example image" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    Game for children in Ferdowsi University of Mashhad
</div>



{% raw %}

```html

```

{% endraw %}
