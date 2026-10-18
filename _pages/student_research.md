---
layout: page
title: student research
permalink: /student-research/
description: A dated archive of graduate research from the Pattern Recognition Laboratory.
---

This archive preserves the thesis and dissertation records listed on the [earlier laboratory website](https://hadisadoghiyazdi1971.github.io/ThesisTitle/). The dates and research topics describe those records; they do not identify current enrolment or employment. See [people]({{ '/people/' | relative_url }}) for the existing profile collection and [publications]({{ '/publications/' | relative_url }}) for bibliographic records.

{% assign levels = site.data.student_research | group_by: 'level' %}
{% for level in levels %}

## {{ level.name }}

{% assign topics = level.items | group_by: 'topic' %}
{% for topic in topics %}

### {{ topic.name }}

{% for research in topic.items %}

- **{{ research.title }}** — {{ research.student }} (<time datetime="{{ research.date }}">{{ research.date }}</time>).
  {% endfor %}
  {% endfor %}
  {% endfor %}

[Historical laboratory photographs]({{ "/laboratory-gallery/" | relative_url }}).
