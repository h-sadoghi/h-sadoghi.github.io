---
layout: page
title: Research topics
permalink: /research-topics/
nav: false
description: A thematic view of the publication catalogue
---

Topics follow the earlier academic website. Each link leads to a bibliographic record in the [publication catalogue]({{ '/publications/' | relative_url }}); papers can belong to several topics. Unverified titles are excluded from this view.

{% for group in site.data.research_topics %}

## {{ group.topic }}

{% for paper in group.papers %}

- [{{ paper.title }}]({{ '/publications/' | relative_url }}#{{ paper.key }}) ({{ paper.year }}){% if paper.publication_type == 'preprint' %} — Preprint{% endif %}
  {% endfor %}
  {% endfor %}
