---
layout: post
title: Loss function Lecture 1
date: 2024-10-02 
description: This lecture guide for better understanding of loss function mechanism
tags: formatting images
categories: sample-posts
thumbnail: assets/img/Blog/LossBlog/MainPage_Loss.JPG
---

# Loss function

Hadi Sadoghi Yazdi

A person clusters objects using a loss function that is specific to the conditions and the individual applying it. However, it is more accurate to say that they organize their actions based on the perceived benefits and losses.

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/Blog/LossBlog/LossinLife.jpg" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    Loss in mind.
</div>

Throughout their lives, whether consciously or unconsciously, humans think about concepts like death, health, poverty, pain, a short life, fear, and so on, which in a way represent the losses they face. Loss is also present in buying and selling, the stock market, marriage, partnerships, and life in general. Different people perceive loss in different ways. Some magnify mistakes, some trim them down, and others correct them.

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/Blog/LossBlog/PerspectiveofLoss.jpg" class="img-fluid rounded z-depth-1" zoomable=true %}
    </div>
</div>

## **Types of Loss Functions**
 
Loss functions are a key component in machine learning and statistical models, used to quantify the difference between predicted and actual values. They guide optimization algorithms to minimize error and improve model performance. Different types of loss functions are designed to handle various data characteristics and objectives, such as absolute errors, squared errors, or more robust alternatives like *Pseudo-Huber* and *LnCosh*, which manage outliers and non-differentiability effectively.

### absolute error loss function

In the absolute error loss function, a sample may fall in different directions relative to the reference index, resulting in positive or negative errors if we think in scalar terms. The loss that affects us generally takes the form of an absolute value. A widely used loss function in many applications is the *Absolute Error* loss function. Essentially, we place a function between the loss and error, transforming the concept of error into loss. If we introduce some degree of leniency into the loss function, a region of insensitivity to error can be added. Naturally, to achieve this, we lower the absolute value slightly by subtracting an amount of $$ \epsilon $$. The region of insensitivity is created using the function $$ \text{max}(e - \epsilon, 0) $$. However, calculating the absolute error index, which is not differentiable and has an insensitive region, presents challenges.

$$ e = x - \mu $$

Where:
- $$ e $$ = error
- $$ x $$ = sample
- $$ \mu $$ = reference index

To make the absolute error differentiable, *LnCosh* or *Pseudo-Huber* is used. To create an insensitivity region, the function $$ \text{max}(e^2 - \epsilon, 0) $$ is applied. Of course, solving this issue, where the absolute value is non-differentiable and creates an insensitive region, introduces difficulties in calculating $$ \mu $$, such as making the absolute value differentiable. For this, methods like *LnCosh* or *Pseudo-Huber* are employed. This helps when differentiation is needed in computations, allowing us to reach an optimal $$ \mu $$. Alternatively, magnifying the error function by using the sum of squared errors $$ e^2 $$ can also be applied. By subtracting an amount of $$ \epsilon $$ and using $$ \text{max}(e^2 - \epsilon, 0) $$, an insensitive region is created. This illustrates that by adding a degree of leniency or relaxation, the system becomes more robust to error changes.

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/Blog/LossBlog/LossTypes_1.jpg" class="img-fluid rounded z-depth-1" zoomable=true %}
    </div>
</div>

# Robust Absolout Error

The absolute function becomes smooth and differentiable with *lncosh*, and in clustering, *lncosh* can be modified, for instance, by adding the concept of fairness. This prevents outliers (very large errors) from skewing the decision-making system. From a data processing perspective, outliers are significant and can negatively affect the estimation of relevant parameters. The solution to dealing with outliers is to strengthen the function. The loss function, in a combination of *lncosh* and cross-entropy, is expressed as $$ 1 - e^{-\alpha \ln(\cosh(e))} $$. As seen in Figure 12, excessive increases in large errors do not distort the system.


<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/Blog/LossBlog/Robust_lncos.jpg" class="img-fluid rounded z-depth-1" zoomable=true %}
    </div>
</div>


# **Pinball Loss Function**  

From a socialist perspective, the transition from equality to equity emphasizes the need to address systemic disparities rather than merely treating everyone the same. While equality advocates for uniform treatment and access, equity recognizes that individuals come from diverse backgrounds and circumstances, necessitating tailored support to achieve true fairness. This shift aims to dismantle structural inequalities and ensure that resources and opportunities are distributed based on need, promoting a more just and inclusive society.

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/Blog/LossBlog/Equality_Equity1.jpg" class="img-fluid rounded z-depth-1" zoomable=true %}
    </div>
</div>


One of the commonly used loss functions that is also non-differentiable is the pinball loss function. This loss function is used when the error distribution is not symmetric. It is employed to transition from the concept of equality to equity. In this function, the errors are weighted in such a way that the positive errors are amplified while the negative errors are reduced.The angle coefficient of the pinball loss can vary, allowing the right and left sides to be adjusted.

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/Blog/LossBlog/PinBall_Loss.jpg" class="img-fluid rounded z-depth-1" zoomable=true %}
    </div>
</div>

Certain terms such as under-prediction, over-prediction, and non-normal error distribution may lead to the use of the pinball loss function. For instance, we might consider using the Pinball Loss Function in scenarios where we want to predict stock prices based on data such as news information, social information, and the mental state of people in society. This approach allows us to control the parameter τ externally, resulting in more accurate predictions.

Similarly, in determining an index, we may want to bias it in a certain direction based on available information. This information can be gathered either from the data itself or from higher-level insights to control the angle coefficient of the Pinball Loss. Additionally, we might incorporate the concept of insensitivity into the Pinball loss function.

# Concept of Inequality Equality Justice Equity

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/Blog/LossBlog/Inequality_Equality_Justice_Equity.jpg" class="img-fluid rounded z-depth-1" zoomable=true %}
    </div>
</div>


# **Inequality**

**Inequality** inherently exists in the model. For example, when data is represented and summarized by a single parameter, the error of each sample will naturally differ from one another based on its distance from the index. Similarly, when the data is modeled with a single plane, not all samples will lie on that plane, leading to inequality introduced by the model used. If we desire a model that perfectly fits the data, it would require a complex model that is not easily presented and lacks generalizability.

Inequality can be viewed as a type of noise in the modeling process, sometimes resembling the effects of system looseness that contributes to stability. This is similar to the looseness used in bridges, which dampens the effects of temperature changes or sudden forces.

# Equality

Equality means providing opportunities so that everyone is treated equally from the system's perspective. This does not imply that the system provides equal resources for each individual. Therefore, the loss function acts like a filter that is applied uniformly to all, but some may pass through while others may not. It utilizes a loss function that aggregates all into a cost function with equal weights, similar to:

$$ 
L_{\text{equality}} = \sum_{i=1}^{n} (y_i - \hat{y}_i)^2 
$$




