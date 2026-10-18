---
layout: page
title: presentations
permalink: /presentations/
nav: true
nav_order: 5
description: Research presentations, engineering proposals and archived concepts
---

These materials describe research ideas and engineering approaches from the earlier website. A proposal does not establish a deployed system or a validated outcome.

{% for resource in site.data.legacy_resources %}
{% if resource.group == 'Presentations and proposals' %}

- [{{ resource.title }}]({{ resource.destination_url | relative_url }})
  {% endif %}
  {% endfor %}

See also the [resource library]({{ '/resources/' | relative_url }}) and [projects]({{ '/projects/' | relative_url }}).
