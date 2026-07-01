---
layout: archive
title: "Publications"
description: "Academic publications by Chris Soria on social networks, cognitive aging, dementia, and computational methods in social science research."
permalink: /publications/
author_profile: true
---

{% if author.googlescholar %}
  You can also find my articles on <u><a href="{{author.googlescholar}}">my Google Scholar profile</a>.</u>
{% endif %}

{% include base_path %}

{% include archive-collapse-style.html %}

## Peer-Reviewed

{% for post in site.publications reversed %}
  {% if post.type == "peer-reviewed" %}
    {% include archive-single-collapse.html %}
  {% endif %}
{% endfor %}

## Pre-Print

{% for post in site.publications reversed %}
  {% if post.type == "preprint" %}
    {% include archive-single-collapse.html %}
  {% endif %}
{% endfor %}
