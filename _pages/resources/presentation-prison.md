---
layout: legacy_page
title: Detection of Anomalous Behavior in Prisoner Gatherings Using Surveillance Cameras
permalink: /resources/presentation-prison/
description: Research presentation and project archive
nav: false
math: false
mermaid:
  enabled: false
  zoomable: false
legacy_source: https://hadisadoghiyazdi1971.github.io/presentation/prison/
legacy_group: Presentations and proposals
legacy_dir: ltr
lang: en
---

{% raw %}

## With Emphasis on Artificial Intelligence Applications

- <a href="https://h-sadoghi.github.io/" target="_blank"><strong>Hadi Sadoghi Yazdi</strong></a> : PhD in Electronics, Expert Consultant in Machine Vision/Learning and Data Systems
- Affilation and institute:
  - Professor of Electrical and Computer Engineering, Ferdowsi University of Mashhad
  - Director of Pattern Recognition Laboratory
  - Member of SCIIP - Center of Excellence on Soft Computing and Intelligent Information Processing

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/prison-ai-security-system-nature-inspired-55884ecba5-480.webp 480w, /assets/img/legacy/prison-ai-security-system-nature-inspired-55884ecba5-800.webp 800w, /assets/img/legacy/prison-ai-security-system-nature-inspired-55884ecba5-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/prison-ai-security-system-nature-inspired-55884ecba5.jpg" alt="Identification of Behavior in Prison with AI"></picture>

</div>

<div class="caption" markdown="1">

Identification of Behavior in Prison with AI

</div>

## Table of Contents

<!-- prettier-ignore -->
* TOC
{:toc}

## Introduction

### Objectives

- Develop AI-powered system for real-time anomaly detection in prison CCTV feeds.
- Reduce response times to threats (e.g., fights, self-harm).
- Ensure ethical compliance (privacy, bias mitigation).
- Achieve 90%+ accuracy in detecting crowd-based anomalies.

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/objective-5a25733afc-480.webp 480w, /assets/img/legacy/objective-5a25733afc-800.webp 800w, /assets/img/legacy/objective-5a25733afc-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/objective-5a25733afc.jpg" alt="AI-based real-time anomaly detection in prison CCTV"></picture>

</div>

<div class="caption" markdown="1">

AI-based real-time anomaly detection in prison CCTV

</div>

### Existing Implementations in Various Countries

- **China**: AI surveillance with facial recognition for threat detection (<a href="https://en.wikipedia.org/wiki/Prison" target="_blank"><strong>prison</strong></a> breaks impossible).

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/china-cf1c87ce37-480.webp 480w, /assets/img/legacy/china-cf1c87ce37-800.webp 800w, /assets/img/legacy/china-cf1c87ce37-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/china-cf1c87ce37.png" alt="Stephen Chenin Beijing, 1 Apr 2019"></picture>

</div>

<div class="caption" markdown="1">

Stephen Chenin Beijing, 1 Apr 2019

</div>

- **UK**: <a href="https://csecrosscom.co.uk/solutions/cctv-video-analytics/avigilon-unusual-activity-detection/" target="_blank"><strong>Avigilon</strong></a> (software for contraband and behavior monitoring). Avigilon's self-learning AI continuously improves detection accuracy by adapting to environments, reducing false alarms and enhancing security threat identification.
- **Singapore**: AI-based CCTV for fights and headcount checks.
- **India**: Facial recognition in Tihar jail for anomaly detection.

**Singapore**: AI-based CCTV for fights and headcount checks. New technology on trial at <a href="https://www.straitstimes.com/singapore/new-technology-on-trial-at-changi-prison-can-detect-cell-fights-through-video-analytics" target="_blank"><strong>Changi Prison</strong></a> can detect cell fights through video analytics.

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/changi-singapour-0e52744ff8-480.webp 480w, /assets/img/legacy/changi-singapour-0e52744ff8-800.webp 800w, /assets/img/legacy/changi-singapour-0e52744ff8-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/changi-singapour-0e52744ff8.png" alt="Fights and headcount checks"></picture>

</div>

<div class="caption" markdown="1">

Fights and headcount checks

</div>

**India**: <a href="https://www.newindianexpress.com/cities/delhi/2024/Aug/16/tihar-installs-1248-cctvs-with-facial-recognition" target="_blank"><strong>Tihar Jail</strong></a>, one of the largest prison complexes in India, has been implementing a facial recognition, anomaly system and enhance security.

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/jail-486d1251dd-480.webp 480w, /assets/img/legacy/jail-486d1251dd-800.webp 800w, /assets/img/legacy/jail-486d1251dd-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/jail-486d1251dd.png" alt="Tihar installs 1,248 CCTVs with facial recognition"></picture>

</div>

<div class="caption" markdown="1">

Tihar installs 1,248 CCTVs with facial recognition

</div>

## Methodology

### Data Collection

- Gather anonymized CCTV footage (ethical approvals).
- Label data for normal vs. anomalous behaviors (e.g., fights, gatherings).
- **Example**: <a href="https://arxiv.org/abs/2409.05383" target="_blank"><strong>Deep Learning for Video Anomaly Detection: A Review</strong></a>

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/datacollectionreview-ea78be5318-480.webp 480w, /assets/img/legacy/datacollectionreview-ea78be5318-800.webp 800w, /assets/img/legacy/datacollectionreview-ea78be5318-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/datacollectionreview-ea78be5318.jpg" alt="Illustrations of frame-level (Top) and pixel-level (Bottom) output"></picture>

</div>

<div class="caption" markdown="1">

Illustrations of frame-level (Top) and pixel-level (Bottom) output

</div>

### Model Development

- **Frame Analysis**
  - Use CNNs for video frame analysis, RNNs for temporal tracking.
- **Frame Encoding**
  - EfficientNet-B7 (pretrained on Kinetics-700) for high-resolution feature extraction.
  - 3D Convolutional Blocks (I3D) for short-term spatiotemporal features (5-frame snippets).
- **Temporal Context**

  - Bidirectional Quasi-Recurrent Neural Networks (QRNNs): Lightweight alternative to LSTMs/GRUs. Processes sequences with parallel convolution + recurrent pooling (reducing latency 40% vs. GRU).
  - Attention Mechanisms: Self-attention layers to weight critical frames (e.g., sudden motion/occlusion).

- **Implement anomaly detection**
  - use YOLO v7, Autoencoders
  - use Adaptive frame skipping based on optical flow magnitude.
- **Edge Computing Deployment**
  - Hardware: NVIDIA Jetson AGX Orin (48 TOPS) / Google Coral TPU.
  - Model Distillation: Teacher (EfficientNet-B7 + QRNN) → Student (MobileNetV3 + QRNN).

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/deepnet-237819c6ab-480.webp 480w, /assets/img/legacy/deepnet-237819c6ab-800.webp 800w, /assets/img/legacy/deepnet-237819c6ab-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/deepnet-237819c6ab.png" alt="Deep Neural Network"></picture>

</div>

<div class="caption" markdown="1">

Deep Neural Network

</div>

### Deployment

- Deploy on CCTV with AI accelerators (e.g., NVIDIA Jetson).
- Pilot testing in controlled prison settings.
- Conduct ethical audits (GDPR <a href="https://gdpr-info.eu/" target="_blank"><strong>(General Data Protection Regulation)</strong></a>-like policies, bias checks).

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/deployment1-38b70f9cb0-480.webp 480w, /assets/img/legacy/deployment1-38b70f9cb0-800.webp 800w, /assets/img/legacy/deployment1-38b70f9cb0-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/deployment1-38b70f9cb0.png" alt="Deployment of AI-enabled CCTV system on-site with automotive-grade accelerators for real-time monitoring."></picture>

</div>

<div class="caption" markdown="1">

Deployment of AI-enabled CCTV system on-site with automotive-grade accelerators for real-time monitoring.

</div>

### Technology Stack

| Component | Description                              |
| --------- | ---------------------------------------- |
| Hardware  | High-res CCTV with IR, motion sensors    |
| Software  | Python (OpenCV, TensorFlow), MQTT alerts |
| AI Models | CNN-RNN, YOLO, GANs for synthetic data   |
| Security  | Encrypted storage, access controls       |

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/technologystackvisualization-1f8c02eaf6-480.webp 480w, /assets/img/legacy/technologystackvisualization-1f8c02eaf6-800.webp 800w, /assets/img/legacy/technologystackvisualization-1f8c02eaf6-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/technologystackvisualization-1f8c02eaf6.png" alt="Technology Stack Visualization"></picture>

</div>

<div class="caption" markdown="1">

Technology Stack Visualization

</div>

## Challenges and Mitigations

- **Privacy Concerns**: GDPR-like policies, data anonymization.
- <a href="https://hadisadoghiyazdi1971.github.io/physics/machine%20learning/What-Bias/" target="_blank"><strong>AI Bias</strong></a>: Diverse training data, fairness algorithms.
- **False Positives**: Fine-tune models with prison-specific data.

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/concerns-23f4a27d8c-480.webp 480w, /assets/img/legacy/concerns-23f4a27d8c-800.webp 800w, /assets/img/legacy/concerns-23f4a27d8c-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/concerns-23f4a27d8c.jpg" alt="Privacy, fairness, and accuracy: GDPR-like privacy with anonymization, bias mitigation through diverse data and fairness algorithms, and reduced false positives via prison-specific fine-tuning."></picture>

</div>

<div class="caption" markdown="1">

Privacy, fairness, and accuracy: GDPR-like privacy with anonymization, bias mitigation through diverse data and fairness algorithms, and reduced false positives via prison-specific fine-tuning.

</div>

## Expected Outcomes

- 30-50% reduction in security incidents (inspired by India).
- Cost savings via automated monitoring (like Singapore).
- Scalable system for global adoption.

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/expectedoutcomes-be381cfd96-480.webp 480w, /assets/img/legacy/expectedoutcomes-be381cfd96-800.webp 800w, /assets/img/legacy/expectedoutcomes-be381cfd96-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/expectedoutcomes-be381cfd96.png" alt="Significant security gains, cost savings, and scalable global deployment"></picture>

</div>

<div class="caption" markdown="1">

Significant security gains, cost savings, and scalable global deployment

</div>

## Additional Service Offerings

- <a href="https://limablog.org/it-is-time-to-start-thinking-about-smart-prisons/" target="_blank"><strong>Smart Prisons</strong></a>: Closing the gap between smart-city innovations and their application in correctional facilities.
- <a href="https://www.g4s.com/en-gb/news/2016/12/06/trial-of-new-technology-to-tackle-contraband" target="_blank"><strong>Tackle Prison Contraband</strong></a>: Trial of new technology to tackle prison contraband.
- <a href="https://www.skysafe.io/industries/correctional-facilities" target="_blank"><strong>Guarding the Perimeter</strong></a>: Drone Detection and Neutralization in Prisons

<div markdown="1">

    <picture><source type="image/webp" srcset="/assets/img/legacy/drone-3b05c5d8d7-480.webp 480w, /assets/img/legacy/drone-3b05c5d8d7-800.webp 800w, /assets/img/legacy/drone-3b05c5d8d7-1400.webp 1400w" sizes="(min-width: 930px) 900px, 95vw"><img loading="lazy" src="/assets/img/legacy/drone-3b05c5d8d7.jpg" alt="Protect Your Correctional Facility From Drone Threats"></picture>

</div>

<div class="caption" markdown="1">

Protect Your Correctional Facility From Drone Threats

</div>

## References

- AI surveillance systems in China, Hong Kong, Singapore (2023 reports).
- UK Altcourse prison: Avigilon software (2022).
- India Punjab jails: AI CCTV deployment (2024).

## Contact Me

<div markdown="1">

    <p><strong>Hadi Sadoghi Yazdi</strong></p>
    <p>AI and Data Specialist</p>
    <p>Email: <a href="mailto:h-sadoghi@um.ac.ir">h-sadoghi@um.ac.ir</a></p>
    <p>Phone: <a href="tel:+985138805117">+98-51-38805117</a></p>
    <p>
    Website:
        <a href="https://h-sadoghi.github.io/" target="_blank">https://h-sadoghi.github.io/</a> |
        <a href="/" target="_blank">https://hadisadoghiyazdi1971.github.io/</a>
        </p>

</div>

{% endraw %}
