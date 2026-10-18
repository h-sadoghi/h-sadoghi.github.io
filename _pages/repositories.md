---
layout: page
permalink: /repositories/
title: repositories
description:
nav: true
nav_order: 4
---

{% if site.data.repositories.github_users %}

## GitHub users

<div class="repositories d-flex flex-wrap flex-md-row flex-column justify-content-between align-items-center">
  {% for user in site.data.repositories.github_users %}
    {% include repository/repo_user.liquid username=user %}
  {% endfor %}
</div>

---

{% if site.repo_trophies.enabled %}
{% for user in site.data.repositories.github_users %}
{% if site.data.repositories.github_users.size > 1 %}

  <h4>{{ user }}</h4>
  {% endif %}
  <div class="repositories d-flex flex-wrap flex-md-row flex-column justify-content-between align-items-center">
  {% include repository/repo_trophies.liquid username=user %}
  </div>

---

{% endfor %}
{% endif %}

## Research and teaching code

- [Laboratory Pattern Recognition on GitHub](https://github.com/LaboratoryPatternRecognition)
- [Constructive imbalance: research artifact]({{ '/resources/publicationcode-jmlr-code-result-readme/' | relative_url }})
- [RC filter design: implementation notes]({{ '/resources/teaching-circuiteffort-wiseeda-rc-filter-readme/' | relative_url }})
- [Location-wizard source archive](https://github.com/hadisadoghiyazdi1971/hadisadoghiyazdi1971.github.io/tree/master/fingerprinter-multi-modal-location-wizard)

The source archive links to code as originally published; it is separate from the running academic website.
{% endif %}

{% if site.data.repositories.github_repos %}

## GitHub Repositories

<div class="repositories d-flex flex-wrap flex-md-row flex-column justify-content-between align-items-center">
  {% for repo in site.data.repositories.github_repos %}
    {% include repository/repo.liquid repository=repo %}
  {% endfor %}
</div>
{% endif %}
