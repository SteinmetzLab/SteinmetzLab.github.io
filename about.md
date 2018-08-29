---
layout: page
title: Our Research
permalink: /about/
---

<p>Our goal is to understand the neural mechanisms underlying perception, cognition, and action. In particular, we study how these brain functions are distributed across diverse neural circuits, and how these distributed populations of neurons coordinate their activity to generate useful behaviors. </p>

<p>Our approach is to employ state-of-the-art methods for measuring and manipulating neural activity at large scale and high resolution, combined with sophisticated, quantifiable behavioral tasks and mechanistic modeling. </p>

<p>Our work specifically involves studying visually-guided behaviors in mice, using techniques such as next-generation Neuropixels electrophysiology, large-scale calcium imaging, systematic optogenetic manipulations, and advanced data analysis and modeling. </p>

<section class="blog">
	<div class="container">
		<div class="post-list" itemscope="" itemtype="http://schema.org/Blog">
			{% assign projects = site.data.research.projects %}
			{% for project in projects %}

				{% include project.html %}
			{% endfor %}

		</div>
	</div>
</section>
