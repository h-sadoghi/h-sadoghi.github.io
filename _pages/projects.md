---
layout: page
title: projects
permalink: /projects/
description: Pattern Recognition Lab projects of Ferdowsi university of Mashhad
nav: true
nav_order: 3
display_categories: [work, fun]
horizontal: false
---

<!-- pages/projects.md -->
<div class="projects">
{% if site.enable_project_categories and page.display_categories %}
  <!-- Display categorized projects -->
  {% for category in page.display_categories %}
  <a id="{{ category }}" href=".#{{ category }}">
    <h2 class="category">{{ category }}</h2>
  </a>
  {% assign categorized_projects = site.projects | where: "category", category %}
  {% assign sorted_projects = categorized_projects | sort: "importance" %}
  <!-- Generate cards for each project -->
  {% if page.horizontal %}
  <div class="container">
    <div class="row row-cols-1 row-cols-md-2">
    {% for project in sorted_projects %}
      {% include projects_horizontal.liquid %}
    {% endfor %}
    </div>
  </div>
  {% else %}
  <div class="row row-cols-1 row-cols-md-3">
    {% for project in sorted_projects %}
      {% include projects.liquid %}
    {% endfor %}
  </div>
  {% endif %}
  {% endfor %}

{% else %}

<!-- Display projects without categories -->

{% assign sorted_projects = site.projects | sort: "importance" %}

  <!-- Generate cards for each project -->

{% if page.horizontal %}

  <div class="container">
    <div class="row row-cols-1 row-cols-md-2">
    {% for project in sorted_projects %}
      {% include projects_horizontal.liquid %}
    {% endfor %}
    </div>
  </div>
  {% else %}
  <div class="row row-cols-1 row-cols-md-3">
    {% for project in sorted_projects %}
      {% include projects.liquid %}
    {% endfor %}
  </div>
  {% endif %}
{% endif %}
</div>

## Research concepts and materials

- [AI-assisted patient guidance]({{ '/resources/projects-patientguidbyai/' | relative_url }}) — a data-free summary of a research proposal.
- [Orthopedic team allocation]({{ '/resources/projects-smartallocationorthopedicteamspoweredbyai/' | relative_url }}) — an archived scheduling concept, without clinical case data.
- [Constructive imbalance in composite decision systems]({{ '/resources/publicationcode-jmlr-code-result-readme/' | relative_url }}) — a provisional research artifact with code and numerical results.

See [presentations]({{ '/presentations/' | relative_url }}) for additional engineering proposals.

## Pattern Recognition Team

{% include figure.liquid path="assets/img/PR_Goup.jpg" class="img-fluid" loading="lazy" alt="Pattern Recognition Laboratory team" %}
