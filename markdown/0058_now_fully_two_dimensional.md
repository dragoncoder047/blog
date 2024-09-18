Title: Now Fully Two-Dimensional
Date: 2024-09-17
Tags: programming, electronics, python

Last time I mentioned something about Schemascii, I had [just completed the first version]({filename}0033_schemascii_±_0.md). It works well for what I need it for, but the internals are very crude. Schemascii doesn't even have advanced components such as op-amps and logic gates -- something that has prevented me from fully being able to convert all of the circuit diagrams that I have posted to Schemascii format. I couldn't come up with a simple way of specifying what shape the IC should have (other than hard-coding it and causing inevitable problems) so I just gave up and moved on to other projects.

<!-- cSpell: ignore Nadim Khemir Asciio -->

In July of 2023 I was contacted by Nadim Khemir, one of the developers of the program [Asciio][]. I had never heard of Asciio before -- it turns out it is a rather old and large Perl program that lets you edit box-and-arrow diagrams, drawn using ASCII art as one would expect. He [asked][] if I would be interested in collaborating on making both Schemascii and Asciio play nicely with each other -- Schemascii gets a GUI editor, and Asciio gets an SVG renderer (at least for circuit diagrams). I can't say I wasn't interested, but at the time I wasn't really up to anything that would require modifying the scope of Schemascii. I realized I had written some terrible spaghetti code in getting Schemascii to work, and adding more new features would have just made my brain hurt more. I didn't really touch Schemascii much after that.

Fast-forward to the middle of August 2024. I was going through and cleaning up old issues in GitHub and found the one from Nadim. It sparked my interest (again), and I read what I originally wrote in reply to Nadim:

> Schemascii's internal representation is pretty much just the raw text, no structure or anything, and any coordinate information is thrown out after rendering each component or line to a string. If you connect two separate wires using the G symbols, electrically, they are connected (both ground), but Schemascii has no idea and ends up making them appear as two separate wires when you hover over them. So I doubt I'd be able to add any thing to export a Schemascii diagram to any of the other formats.

And then I opened up the source code and was reminded of how messy Schemascii is. The messy code, the lack of op-amps, and the weird "G" issue led me to decide that, well, I would need to do some refactoring.

"Some refactoring" turned out to be a royal understatement. What I ended up doing was completely re-writing Schemascii from the inside out. The only thing left from the "old" Schemascii was the utility functions that performed some basic mathematical operation on the points -- and even with some of those, I was able to revise their algorithms to run faster and/or produce shorter results.

## Eliminating cramming

One of the biggest problems with Schemascii's first syntax, as I saw it, is that the directives that indicate the value of each component have to be crammed into the area of the drawing. Inevitably they never fit, and so I have to put them outside the area of the drawing -- which ends up making the "area of the drawing" bigger as far as Schemascii is concerned, and the drawing ends up with an awkwardly large and often asymmetric margin around it.

The solution was to move these formatting directives - which I called "BOM data" for lack of a better term - completely outside of the drawing. Schemascii won't even look for them there. Instead, Schemascii now forces them to be in a separate section below the document.

Freed from the restriction that it has to fit within the document, I decided that all of the different drawing elements -- wires, components, annotations, etc. -- would be put into an "inheritance hierarchy" of sorts, much like HTML elements being targeted by CSS. Then, the formatting directives would be grouped into rules, with selectors that can match some of the different elements.

Since it reminded me of CSS, the syntax for it I designed is a lot like CSS. It's not quite CSS, though. Why I didn't just pick an existing structured data format, such as JSON, YAML, or TOML, I am not quite sure. I think the main reasons why I decided to "roll my own" syntax was a combination of not liking the verbosity and lack of comments in JSON, having to add a dependency for YAML, and having to require Python 3.12 for TOML.

The syntax I have implemented so far is a little like CSS, but not quite. Here is a little example:

```text
* {
    %% * = global config options
    color = black
    width = 2; padding = 20;
    format = symbol
    mystring = "hello\nworld"
}

R* {tolerance = .05; wattage = 0.25}
```

## Confronting Schemascii's dimensionality

Schemascii is, by nature, two-dimensional. While it's not exactly 2-D *code* (compared to an actual Turing-complete programming language such as [Befunge][]), writing a parser for it is still pretty difficult.

Consider the task of extracting the wires. Any characters that are allowed in wires -- namely `-`, `|`, `(`, `)`, and `*` -- are part of some wire or another. Then Schemascii must determine which characters are parts of which wire.

From the top-level, it seems obvious: just "follow" the wires until you reach the ends, splitting at junctions, and continuing straight at crossings. I implemented just that, and ended up with [this 128-line monstrosity][wires.py]. The entire file implements that one algorithm, as a depth-first search. There is no other functionality in that entire file except for internal functions that implement some part of that algorithm.

At any rate, the algorithm is not *quite* a straight flood fill, and this is why I probably didn't use it. But when I rewrote Schemascii, flood fill seemed close enough to try -- and I was right.

Flood fill is a devilishly simple algorithm by itself:

1. Start with a set of known "seed" cells as the "frontier" set.
2. Pick a point in the "frontier" set (it doesn't matter which).
3. Add all the valid neighbors adjacent to that point that also aren't already in the "seen" set to the "frontier" set.
4. Move the point you just picked from the "frontier" set into the "seen" set.
5. Repeat steps 2-4 until the "frontier" set is empty. The result is all of the points that are now in the "seen" set.

As-is, this can't just be used to find wires, because by definition, the wires have a *directionality* to them. The algorithm outlined above doesn't care which direction it's expanding into when chooses the neighbors in step 3. I figured out that the simplest way to make the code "follow" the wires and not inadvertently merge two wires that cross each other is to make each of the "frontier" points remember the direction that their previous neighbor was. That way, when it is picking neighbors in step 3, it can check to see which direction it came "in" to the cell from, and based on the character in the cell, it restricts what directions it is allowed to go "out" of the cell by.

For example, the horizontal line character `-` can still be crossed vertically. When the search comes in from the right or left, it is not allowed to spill out to the top and bottom, and likewise if it comes in from the top or bottom it is not allowed to go to the side. Except if it's an asterisk `*`, which is used to join wires -- in that case, it is allowed to exit in all four directions no matter which direction it enters from. It's literally that simple, and it works[^1].

## The one remaining problem

Previously, Schemascii only allowed two formats for drawing the components: "small components," which were just the reference designator optionally padded with `#`'s on the left and right, and "large components", which were restricted to being a rectangle drawn using `:` and `~` for the sides and `.` for corners. It was quite awkward, and since everything was rectangular, I couldn't make anything fancy like the triangular shape of op-amps.

I looked back at the example drawings I had already made, and the code I had already written, and it dawned on me that I could just use `#`'s for the components and then flood-fill to find them all. It no longer mattered that the components weren't rectangular -- it would still find all of them. And I had already written flood fill code that - surprise surprise! - worked perfectly to find all of the `#`'s that made up the component's area.

So I drew up the draft for an XOR gate and an op-amp :

```text
  # ######                   #
   # ########                ###
----# #########         ----+#####
    # #U1G1#####----         #U2A###-----
----# #########         -----#####
   # ########                ###
  # ######                   #
```

The code worked perfectly - it spat out a list of 25 points corresponding to the extent of the triangle, when given the three points that form `U2A`.

I quickly discovered that there's still one thing I haven't thought through completely yet. Visually, it's obvious that the op-amp's shape is supposed to be a nice, clean triangle, but how that exactly is created from all of the points is something I have not been able to figure out yet.

For example, if the rule is "find all of the points that aren't completely surrounded by any of the other points, then sort," you end up with a horrible jagged saw-tooth pattern along the sloped sides of the triangle. Applied to the XOR gate, it produces jagged, pixelated edges, and completely garbles the double line in the back.

There's probably an incredibly clever solution to this that I have not been able to think of, but I am sure I will think of it eventually, or stumble upon it on the Internet. The next version of Schemascii is *so close* to being complete.

[Asciio]: https://github.com/nkh/P5-App-Asciio/
[asked]: https://github.com/dragoncoder047/schemascii/issues/8
[Befunge]: https://esolangs.org/wiki/Befunge
[wires.py]: https://github.com/dragoncoder047/schemascii/blob/a76158b6dfa26384f8e2fc8bdce52b5efca728bd/schemascii/wires.py

[^1]: It's still not perfect -- there are some rare but strange edge cases in my current code. One example is if the same wire is looped over itself. The code will follow the wire around the loop and then, finding that the intersection point is already in the "seen" set, stop and miss the rest of the wire.
