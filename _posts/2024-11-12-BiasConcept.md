---
layout: post
title: Bias Lecture 1
date: 2024-11-12 
description: This lecture guide for better understanding of bias
tags: formatting images
categories: sample-posts
thumbnail: assets/img/Blog\BiasBlog/biasInGeneral.jpg
---

# Bias

Maryam Shirazi Kharazi & Ilia Khosravi Khorashad

In this article, we explore the concept of bias through two distinct yet interconnected lenses: its role in human cognition and society, and its implications in the field of artificial intelligence (AI).
In the world of social and philosophy, Bias, or partiality, is the tendency to support a theory or proposition without examining its truth or falsehood, and it involves refraining from considering alternative logical viewpoints. Bias often unconsciously affects a person's judgment and frequently leads to misunderstandings and conflicts. Individuals can be biased in favor of or against a person, ethnicity, nation, religion, social class, political party, and theoretical and ideological patterns in scientific fields. Bias means one-sidedness and a lack of impartial perspective or an open mind. Bias can manifest in various forms and is related to prejudice and intuition. Many things can be biased: coins, dice, methods of predicting the weather, descriptions, policies (e.g., regarding admissions), laws, people (including judges, referees, parents, grandparents, teachers, etc.), their perceptions, beliefs, views, judgments, verdicts, actions, etc. This is a nice list of things that can be biased

In recent years, biases have been discussed under the title of Cognitive Biases. These types of biases emerge during human decision-making, judgment, and selection processes. Since humans are constantly making choices and decisions, awareness of these biases is very important.

Humans use shortcuts and simplifications to make quick decisions and avoid confusion. These simplifications are suitable for human survival and life, but the problem begins when incorrect shortcuts are taken. In fact, humans are influenced by their past experiences, assumptions, surroundings, and society, and they usually make decisions based on these parameters rather than the existing reality.

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/Blog\BiasBlog/biasInGeneral.jpg" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    bias in general.
</div>

In the world of programming and algorithms, specific code is written to solve each problem. However, in artificial intelligence, problems are solved with one algorithm, and the main difference lies in the data used. Therefore in AI, one of the most important factors is having appropriate, sufficient, and classified data.

One of the key issues that needs attention in AI to avoid errors is bias. Bias can occur for various reasons. In some cases, it can be beneficial, such as classifying data based on specific parameters. but, in most cases, bias is undesirable. For instance, in image processing, a person’s skin color should not affect the outcome of the model.

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/Blog\BiasBlog/biasExampleAI.jpg" class="img-fluid rounded z-depth-1" zoomable=true %}
    </div>
</div>

in this example of gender bias, adapted from a report published by researchers deom University of Virginia and the University of Washington, a visual semantic role labeling system has learned to identify a person cooking as female, even when the image is male.

## Types of Biases
we will discuss the types of bias from two perspectives: philosophy and artificial intelligence (AI)
### In philosophy
#### 1. Confirmation Bias:
The tendency to search for or interpret information in a way that confirms one's own beliefs or hypotheses. In fact, we will seek evidence and reasons that justify our beliefs and inclinations.
A simple definition of confirmation bias is that people prefer to pay attention to information that confirms their assumptions and positions.

Some psychologists restrict the term "confirmation bias" to selective collection of evidence that supports what one already believes while ignoring or rejecting evidence that supports a different conclusion. Others apply the term more broadly to the tendency to preserve one's existing beliefs when searching for evidence, interpreting it, or recalling it from memory. Confirmation bias is a result of automatic, unintentional strategies rather than deliberate deception.

Examples of confirmation bias are abundant and are often reminded to audiences in judgment and decision-making training to be careful of the confirmation error and not fall into the trap of this bias.


<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/Blog\BiasBlog/confirmation-bias.jpg" class="img-fluid rounded z-depth-1" zoomable=true %}
    </div>
</div>

#### 2. Attribution Bias:
Occurs when you use your past observations and experiences with an individual as a criterion and basis for judging that individual or others. This issue is very important in the hiring process.

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/Blog\BiasBlog/Attribution-Bias.jpg" class="img-fluid rounded z-depth-1" zoomable=true %}
    </div>
</div>

#### 3. Conformity Bias:
Conformity bias occurs when we voluntarily align our behaviors, beliefs, or attitudes with those of a group. This change      happens in response to either real or perceived group pressure: in other words, others can influence us even when they are not physically present. For example, whether we decrease our energy use at home, pay our taxes, or give to charities often depends on our perception of what others are doing.

Conformity, or the tendency to agree with the majority position, is a type of social influence. Social influence is a broad term used to describe the different ways others influence our behavior. The tendency to conform can be observed both in small groups and in society as a whole and may result both from subtle unconscious influences or overt social pressure.

Example: Conformity bias 
Your friends are making plans for an upcoming concert that they are very excited about. Last time they went to a concert, they were talking about it for a week afterwards, and you felt left out because you did not go with them. Although you are not really keen on that kind of music, you decide to join them this time so as not to feel left out.

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/Blog\BiasBlog/Conformity-Bias.jpg" class="img-fluid rounded z-depth-1" zoomable=true %}
    </div>
</div>

#### 4. Halo Bias and Horn Effect:
The halo effect occurs when you become aware of an outstanding feature or issue about a person and try to attribute this excellence to other areas. Conversely, the horn effect happens when a negative trait or issue is attributed to other areas and characteristics of a person.

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/Blog\BiasBlog/Halo-effect-1.jpg" class="img-fluid rounded z-depth-1" zoomable=true %}
    </div>
</div>

#### 5. Gender Bias:
A tendency or prejudice where an individual judges another solely based on gender. This issue is seen in the hiring process, during promotions, group task assignments, and even in daily workplace behaviors.

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/Blog\BiasBlog/Gender-Bias-Training-12.4.19-3.jpg" class="img-fluid rounded z-depth-1" zoomable=true %}
    </div>
</div>

#### 6. Age Bias:
This bias in the workplace leads to having a positive or negative view solely based on a person's age. For example, it is often said that younger individuals are preferred for hiring over others, or that the opinions of younger people are incorrect.

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/Blog\BiasBlog/agebias.jpg" class="img-fluid rounded z-depth-1" zoomable=true %}
    </div>
</div>

#### 7. Implicit Bias:
Research on “implicit bias” suggests that people can act on the basis of prejudice and stereotypes without intending to do so. While psychologists in the field of “implicit social cognition” study consumer products, self-esteem, food, alcohol, political values, and more, the most striking and well-known research has focused on implicit biases toward members of socially stigmatized groups, such as African-Americans, women, and the LGBTQ community.

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/Blog\BiasBlog/bias.jpg" class="img-fluid rounded z-depth-1" zoomable=true %}
    </div>
</div>

### In AI
#### 1. Sampling Bias: 
Occurs when one feature is overrepresented in data collection compared to others. Sampling should either be random or representative of the population to avoid bias.

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/Blog\BiasBlog/sampling_bias.jpg" class="img-fluid rounded z-depth-1" zoomable=true %}
    </div>
</div>

#### 2. Measurement Bias: 
Occurs when data is not measured or recorded correctly. For example, regional differences in employee salaries could affect data measurement in salary estimation models.

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/Blog\BiasBlog/measurement_bias.jpg" class="img-fluid rounded z-depth-1" zoomable=true %}
    </div>
</div> 

#### 3. Exclusion Bias: 
Similar to sampling bias, exclusion bias arises from data that's inappropriately removed from the data source. When you have petabytes or more of data, it's tempting to select a small sample to use for training -- but in doing so, you might inadvertently exclude certain data, resulting in a biased data set. Exclusion bias also happens when duplicates are removed from data where the data elements are actually distinct.

#### 4. Prejudicial Bias:
Refers to human prejudice. When using historical data to train models, care must be taken to ensure previous biases do not transfer to new models.
#### 5. Bandwagon Effect:
Happens when a trend in data grows, leading to more data collection around that trend. This can overemphasize an idea and introduce bias into models.

## Solutions to Eliminate Bias (Increasing Fairness in Models)
#### 1. Feature Blinding:  
Feature blinding involves removing attributes as inputs in models -- in other words, blinding the model to specific features or protected attributes such as race and gender. However, this method isn't always sufficient, as other attributes can remain that correlate with different genders or races, enabling the model to develop a bias. For instance, certain genders might correlate with specific types of cars.
#### 2. Objective Function Modification: 
Instead of optimizing for accuracy alone, this method adjusts the model’s objective function to improve fairness.
#### 3. Adversarial Classification: 
Adversarial classification involves optimizing a model not just for accurate predictions, but also inaccurate predictions. Though it might sound counterintuitive, poor predictions point out weak spots in a model, and then the model can be optimized to prevent those weaknesses.

These techniques help reduce bias and improve fairness in machine learning models.


## Why Should We Eliminate Bias in AI?
Eliminating bias in machine learning systems is crucial because they learn from data. If the data contains bias, the results will also be skewed. This is particularly important in supervised learning, where high-quality and unbiased data is essential.

AI systems with bias can cause issues, especially in automated decision-making, autonomous operations, and facial recognition software. For example, Google has misidentified images of minorities, gender discrimination has occurred in credit rating apps, and racial biases have appeared in criminal conviction software.

These errors can harm individuals and businesses, reduce trust in AI technology, and lead to legal and financial problems.

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/Blog\BiasBlog/bias.jpg" class="img-fluid rounded z-depth-1" zoomable=true %}
    </div>
</div> 


## How to Identify Bias in AI
Identifying and measuring bias in AI is challenging especially with deep learning algorithms that operate like a "black box." This means it’s difficult to understand which part of the data the model is working on, and only the results are visible. Due to this opacity, it is hard to detect biases. This is why researchers are developing Explainable AI (XAI), aiming to increase transparency in AI models and turn the "black box" into a "white box."

Example: Image Classification with a Neural Network (Black Box) to an Explainable Model (White Box)
Black Box Scenario:
Task: An AI model (e.g., a deep neural network) is trained to classify medical images, such as distinguishing between images of healthy lungs and those with pneumonia.
Problem: The deep learning model achieves high accuracy but does not provide any explanation about why it classified an image a certain way. Doctors are hesitant to trust the model because they cannot see what features (parts of the image) the model focused on to make its decision.
Turning the Black Box into a White Box:
To make this model more explainable, researchers can apply various Explainable AI (XAI) techniques that provide transparency. One commonly used method is Grad-CAM (Gradient-weighted Class Activation Mapping). Here's how this would work:

Model Explanation Using Grad-CAM:

Grad-CAM visualizes the areas of the image that are most important for the model's decision.
After the model classifies an image, Grad-CAM creates a heatmap overlay on the image, highlighting the regions that the neural network paid the most attention to when making the decision. For example, if the model classified an image as showing pneumonia, the heatmap might highlight areas in the lungs where abnormal features (such as fluid buildup) are present.
Results of Explainability:

The doctor can now see the exact areas of the X-ray where the AI model detected patterns associated with pneumonia.
If the heatmap corresponds to regions where human doctors would also look for pneumonia, it increases trust in the model’s decisions.
Outcome:

The model is no longer a black box because users (like doctors) can understand why the AI made its decision. They have a visual explanation of what the model focused on, making the AI more transparent and interpretable. Thus, the black box is effectively turned into a white box.

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/Blog\BiasBlog/pneumonia_Grad.jpg" class="img-fluid rounded z-depth-1" zoomable=true %}
    </div>
</div> 

Bias in data often arises due to the inappropriate selection of training datasets. If the dataset is limited to a subset of the population, the model will provide incorrect results in real-world scenarios. Companies are working to increase diversity in datasets to combat these biases and improve machine learning models.

## Solutions to Eliminate Bias (Increasing Fairness in Models)
1. **Feature Blinding**:  Feature blinding involves removing attributes as inputs in models -- in other words, blinding the model to specific features or protected attributes such as race and gender. However, this method isn't always sufficient, as other attributes can remain that correlate with different genders or races, enabling the model to develop a bias. For instance, certain genders might correlate with specific types of cars.
2. **Objective Function Modification**: Instead of optimizing for accuracy alone, this method adjusts the model’s objective function to improve fairness.
3. **Adversarial Classification**: Adversarial classification involves optimizing a model not just for accurate predictions, but also inaccurate predictions. Though it might sound counterintuitive, poor predictions point out weak spots in a model, and then the model can be optimized to prevent those weaknesses.

These techniques help reduce bias and improve fairness in machine learning models.

## Example in production

Here is an example of AI bias: the problem arises because we have more normal images than pneumonia images in the dataset. Due to the imbalance in the number of images, the model becomes biased in its results.

```python
import tensorflow_addons as tfa
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

from tensorflow.keras.metrics import FalsePositives, FalseNegatives, TrueNegatives, TruePositives

batch_size = 32
img_height = 100
img_width = 143

train_ds = tf.keras.preprocessing.image_dataset_from_directory(
  'Data',
  validation_split=0.1,
  subset="training",
  seed=123,
  batch_size=batch_size
)

val_ds = tf.keras.preprocessing.image_dataset_from_directory(
  'Data',
  validation_split=0.1,
  subset="validation",
  seed=123,
  batch_size=batch_size
)

model = keras.models.Sequential([
  layers.experimental.preprocessing.Rescaling(1./255),
  layers.Conv2D(2, 3, padding='same', activation='relu'),
  layers.MaxPooling2D(),
  layers.Conv2D(4, 3, padding='same', activation='relu'),
  layers.MaxPooling2D(),
  layers.Conv2D(8, 3, padding='same', activation='relu'),
  layers.MaxPooling2D(),
  layers.Conv2D(16, 3, padding='same', activation='relu'),
  layers.MaxPooling2D(),
  layers.Conv2D(32, 3, padding='same', activation='relu'),
  layers.MaxPooling2D(),
  tfa.layers.SpatialPyramidPooling2D([1, 2, 4]),
  layers.Flatten(),
  layers.Dense(32, activation='relu'),
  layers.Dense(1, activation='sigmoid')
])

model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy', FalsePositives(), FalseNegatives(), TrueNegatives(), TruePositives()])

history = model.fit(
  train_ds,
  validation_data=val_ds,
  epochs=3
)
```

When the dataset consists of 35% abnormal images and 65% normal images, the model achieves an accuracy of 76%. However, when the distribution is 55% normal images and 45% abnormal images, the accuracy increases to 93%.

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/Blog\BiasBlog/chest_x_ray.jpg" class="img-fluid rounded z-depth-1" zoomable=true %}
    </div>
</div> 
