---
layout: page
title: Laboratory photo archive
permalink: /laboratory-gallery/
nav: false
description: Historical photographs from the earlier academic website
---

These photographs and their original captions document past laboratory activities, student work and visits. Captions describe the historical source and do not establish current roles or affiliations.

{% for photo in site.data.laboratory_gallery %}
{% include figure.liquid path=photo.image alt=photo.caption caption=photo.caption loading="lazy" %}
{% endfor %}

[Graduate research archive]({{ '/student-research/' | relative_url }}) · [People]({{ '/people/' | relative_url }}) · [Original gallery](https://hadisadoghiyazdi1971.github.io/ThesisTitle/)
