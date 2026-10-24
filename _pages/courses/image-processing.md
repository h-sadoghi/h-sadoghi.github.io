---
layout: page
title: Image Processing
permalink: /teaching/image-processing/
nav: false
course_id: image-processing
published: true
description: Course materials for Image Processing.
---

{% assign managed_course = site.data.teaching_courses | where: 'id', page.course_id | first %}

<div class="text-center my-4">
  <img
    src="{{ managed_course.image | relative_url }}"
    alt="Image Processing course"
    width="180"
    height="180"
    class="img-fluid rounded"
  >
</div>

Learning materials cover selected chapters of <cite>Digital Image Processing</cite> (4th ed.) by Rafael C. Gonzalez and Richard E. Woods. This site provides original notes, diagrams, and code prepared for the course.

- **[Gonzalez — notes and learning files]({{ '/teaching/image-processing/gonzalez/' | relative_url }})** — numbered chapter packages and optional PDF notes.
- **[Student assignments and projects]({{ '/teaching/image-processing/student-work/' | relative_url }})** — approved course work shared by students.
- **[Interactive course book]({{ '/teaching/image-processing/book/' | relative_url }})** — a three-column Jupyter Book for notes and notebooks.
