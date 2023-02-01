Title: Schemascii &pm; 0
Date: 02-01-2023

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

```schemascii

 *--R1--*  R1:0.5k
 |      |
B1      C1 B1:5000m
 |      |
 *------*  C1:0.00033
```

Doesn't that look a whole lot nicer?

In the coming days I'll be going around to all of my other pages and updating them to use Schemascii. Hopefully this change will be for the better!
