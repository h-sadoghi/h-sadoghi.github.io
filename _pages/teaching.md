---
layout: page
permalink: /teaching/
title: teaching
description: AI-related courses taught, covering key areas Pattern Recognition, Machine learning, Circuit and Electronics, Signal and System and Introduction of AI.

nav: true
nav_order: 6
---

## Course Topics

The [resource library]({{ '/resources/' | relative_url }}) brings together circuit and electronics notes, pattern recognition studies, data engineering materials, and student-authored contributions from the earlier website. See also the [dated graduate research archive]({{ '/student-research/' | relative_url }}).

- ![PatRec](../assets/img/PR1.JPG)[**Pattern Recognition**](https://laboratorypatternrecognition.github.io/PatternRecognition_S/pattern_recognition.html) : Techniques for identifying patterns in data with applications in image, speech, and biometrics.
- ![MacLear](../assets/img/machinelearning1.JPG)[**Machine learning**](https://laboratorypatternrecognition.github.io/MachineLearningS/machine_learning.html): Core algorithms and models for data-driven decision-making and predictive analysis
- ![Cir](../assets/img/startPic.jpg)[**Circuit analysis**](https://laboratorypatternrecognition.github.io/CircuitElectronics/Introduction_CircuitElectronics.html): Principles of circuit analysis and the operation of electronic components like diodes, transistors, and op-amps
- ![Sig](../assets/img/ECG_1.jpg)[**Signal processing**](https://laboratorypatternrecognition.github.io/SignalSystem/SignalSystemStart.html): Techniques for analyzing, filtering, and transforming signals in both time and frequency domains
- ![AIEssen](../assets/img/DeepDream2.JPG)[**AI Essentials**](https://laboratorypatternrecognition.github.io/AI-Essentials/Home_Page.html): Fundamentals of artificial intelligence, covering problem-solving, search algorithms, and basic machine learning concepts

## Additional teaching materials

{% if site.data.teaching_courses and site.data.teaching_courses.size > 0 %}

## Locally managed courses

{% for course in site.data.teaching_courses %}
{% if course.published != false or jekyll.environment == 'development' %}

- [**{{ course.title | escape }}**]({{ course.permalink | relative_url }}){% if course.description %}: {{ course.description | escape }}{% endif %}
  {% endif %}
  {% endfor %}
  {% endif %}

- [Data acquisition, processing and management]({{ '/resources/teaching-dataengcourse-data/' | relative_url }})
- [AI for high-school students]({{ '/resources/teaching-ai-hs-introduction/' | relative_url }})
- [AI applications in organizations]({{ '/resources/teaching-organizations-organ-ai/' | relative_url }})

The [resource library]({{ '/resources/' | relative_url }}) also groups student contributions in circuits, electronics, pattern recognition and machine learning, alongside the research toolkit.
