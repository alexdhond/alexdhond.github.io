---
layout: archive
title: "CV"
permalink: /cv/
author_profile: true
redirect_from:
  - /resume
---

{% include base_path %}

Education
======
* DPhil (PhD) in Biology, University of Oxford (2024 - present)
* MSc in Ecology, Evolution and Conservatio GitHub University (2021)
* B.S. in Molecular Environmental Biology, University of California, Berkeley (2020)

Publications
======
  <ul>{% for post in site.publications reversed %}
    {% include archive-single-cv.html %}
  {% endfor %}</ul>
  
Talks
======
  <ul>{% for post in site.talks reversed %}
    {% include archive-single-talk-cv.html  %}
  {% endfor %}</ul>
