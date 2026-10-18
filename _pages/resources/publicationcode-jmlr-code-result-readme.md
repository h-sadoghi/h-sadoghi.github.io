---
layout: legacy_page
title: "Capability-Aware Imbalance in Composite Decision Systems: An Optimal Transport
  View"
permalink: /resources/publicationcode-jmlr-code-result-readme/
description: Research presentation and project archive
nav: false
math: false
mermaid:
  enabled: false
  zoomable: false
legacy_source: https://github.com/hadisadoghiyazdi1971/hadisadoghiyazdi1971.github.io/blob/master/PublicationCode/JMLR_Code_Result/ReadMe.md
legacy_group: Research artifacts
legacy_dir: ltr
lang: en
---

{% raw %}

# Capability-Aware Imbalance in Composite Decision Systems: An Optimal Transport View

**Authors:** Hadi Sadoghi Yazdi  
**Legacy status:** The source labels this work “Under review (JMLR 2026)”. Acceptance and current review status have not been independently verified.

## Overview

This work reframes **structural imbalance** in composite decision systems (Mixture-of-Experts, Boosting, hierarchical classifiers, distributed systems) as a natural and often _optimal_ outcome rather than a flaw.

Using the lens of **Optimal Transport**, we prove that when task difficulty is heterogeneous, the cost-minimizing assignment is necessarily non-uniform — a phenomenon we call **Constructive Imbalance**.

## Key Contributions

- **Fundamental Theorem of Constructive Imbalance**: Optimal routing is non-uniform whenever task difficulty is non-uniform.
- Effective Complexity as the primal transport cost.
- Complexity attenuation via rare specialization (highly complex experts add almost zero global cost if rarely used).
- Unified framework connecting MoE routing, Boosting reweighting, load balancing, and hierarchical decomposition.
- Theoretical link between transport-optimal routing and Rademacher generalization bounds.
- Empirical validation + corrections to previous claims (harmonic mean bound, marginal cost equalization).

## Repository Contents

- [run_experiments.py](/assets/code/constructive-imbalance/run_experiments.py) — Reproducible main script
- [results.json](/assets/code/constructive-imbalance/results.json) — All raw experimental results

## Reproducibility

```bash
python run_experiments.py
```

{% endraw %}
