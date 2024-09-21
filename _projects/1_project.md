---
layout: page
title: Interactive wall
description: Augmented Reality (AR)
img: assets/img/1.jpg
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



---

To give your project a background in the portfolio page, just add the img tag to the front matter like so:

    ---
    layout: page
    title: project
    description: a project with a background image
    img: /assets/img/12.jpg
    ---

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/1.jpg" title="example image" class="img-fluid rounded z-depth-1" %}
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/3.jpg" title="example image" class="img-fluid rounded z-depth-1" %}
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/5.jpg" title="example image" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    Caption photos easily. On the left, a road goes through a tunnel. Middle, leaves artistically fall in a hipster photoshoot. Right, in another hipster photoshoot, a lumberjack grasps a handful of pine needles.
</div>
<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/5.jpg" title="example image" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    This image can also have a caption. It's like magic.
</div>

You can also put regular text between your rows of images, even citations {% cite einstein1950meaning %}.
Say you wanted to write a bit about your project before you posted the rest of the images.
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
