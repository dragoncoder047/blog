Title: Schemascii &pm; 0
Date: 2023-02-01
Tags: programming, electronics, python

I have been working *really* hard this week on Schemascii. Like, maybe too much. But, I finally got Schemascii to the point that I could (if I wanted) upload it to PyPI and it would be a valid package.

Schemascii is also able to be called as a command-line program. I don't really need this, but now anyone who is able to install Schemascii (which is really anyone who has a computer now) can render a Schemascii diagram to SVG via the command line.

As-is, what I need for Schemascii is to embed it into a Python-Markdown website. I am using a Python-Markdown extension that makes this super easy -- all I need to do is provide a class and the callback function (in this case a super dumb wrapper around `:::py3 schemascii.render()`)

That way, I can turn this:

````markdown
```schemascii

 *--R1--*  R1:0.5k
 |      |
B1      C1 B1:5000m
 |      |
 *------*  C1:0.00033
```
````

Into this:

<p><svg width="335" height="110" viewBox="-10 -10 335 110" xmlns="http://www.w3.org/2000/svg" class="schemascii"><g class="wire"><polyline points="15,30 15,15 45,15" fill="transparent" stroke-width="2" stroke="black"></polyline></g><g class="wire"><polyline points="120,30 120,15 90,15" fill="transparent" stroke-width="2" stroke="black"></polyline></g><g class="wire"><polyline points="120,60 120,75 15,75 15,60" fill="transparent" stroke-width="2" stroke="black"></polyline></g><g class="component R"><polyline points="90,15 86.25,11.25 82.5,18.75 78.75,11.25 75,18.75 71.25,11.25 67.5,18.75 63.75,11.25 60,18.75 56.25,11.25 52.5,18.75 48.75,11.25 45,15" fill="transparent" stroke-width="2" stroke="black"></polyline><text x="67.5" y="7.5" text-anchor="middle" font-size="15" fill="black"><tspan class="cmp-id">R1</tspan> <tspan class="cmp-value">500 Ω</tspan></text></g><g class="component B"><text x="22.5" y="45" text-anchor="start" font-size="15" fill="black"><tspan class="cmp-id">B1</tspan> <tspan class="cmp-value">5 V</tspan></text><polyline points="18.75,52.5 11.25,52.5" fill="transparent" stroke-width="2" stroke="black"></polyline><polyline points="22.5,47.4 7.5,47.4" fill="transparent" stroke-width="2" stroke="black"></polyline><polyline points="18.75,42.6 11.25,42.6" fill="transparent" stroke-width="2" stroke="black"></polyline><polyline points="22.5,37.5 7.5,37.5" fill="transparent" stroke-width="2" stroke="black"></polyline><polyline points="15,60 15,52.5" fill="transparent" stroke-width="2" stroke="black"></polyline><polyline points="15,30 15,37.5" fill="transparent" stroke-width="2" stroke="black"></polyline></g><g class="component C"><polyline points="126,48.75 114,48.75" fill="transparent" stroke-width="2" stroke="black"></polyline><polyline points="126,41.25 114,41.25" fill="transparent" stroke-width="2" stroke="black"></polyline><polyline points="120,60 120,48.75" fill="transparent" stroke-width="2" stroke="black"></polyline><polyline points="120,30 120,41.25" fill="transparent" stroke-width="2" stroke="black"></polyline><text x="127.5" y="45" text-anchor="start" font-size="15" fill="black"><tspan class="cmp-id">C1</tspan> <tspan class="cmp-value">330 µF</tspan></text></g></svg></p>

Doesn't that look a whole lot nicer?

In the coming days I'll be going around to all of my other pages and updating them to use Schemascii. Hopefully this change will be for the better!
