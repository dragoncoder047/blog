Title: Zero-Thickness Tree
Date: 2023-10-24
Tags: programming, python, gamedev

In a [previous post]({filename}0036_a_very_confusing_data_model.md), I started some mental planning for an interactive fiction engine in Python. I picked it up again last week and started working on a new version. Custom logic is implemented using a tiny Python library I created called [`json_runner`](https://github.com/dragoncoder047/json_runner), which as you might guess, is capable of running JSON objects as if they were code.

To test my code, I came up with a "test game". Naturally as a programmer I started by calling the game "Foo Bar", and a series of wordplays ensued -- one of the things I came up with is putting vodka and orange juice in a cocktail shaker, and pulling out a screwdriver, and then using the screwdriver to unscrew the lock of the door to open it.

I was basing the method of scripting a lot off of Inform 7, just without the insane verbosity that comes along with a almost natural-language environment.

In the process of testing I found a number of bugs in `json_runner`'s parser, and was able to fix them. But there were still a lot of lingering inconsistencies and kludges: the format of the game data file made is very difficult to incorporate custom actions. For example, a complex phrase like *CUT THE ORANGE WITH THE KNIFE* would be dispatched to the orange object's `cut` action handler, which would have to first check if the player can use the knife (they are holding it or can take it), check if the player specified the right object (they could have equally written *CUT THE ORANGE WITH THE SPOON*, which wouldn't work) and then if everything is OK, print special messages, change the orange's description, etc. which seems a little unnecessary. It was also compounded by the fact that I neglected to include any type annotations in my Python code, which made it easy to assume a different object type and wind up with an `AttributeError`.

Besides, moving objects around in the world was a total nightmare. Because objects were stored as a tree and had no reference to their parent, I had to implement a `purge_item()` method on the top-level object, which recursively removes the mentioned item from itself and any children -- like if Inform 7's `:::inform7 move X to Y` was actually implemented as `:::inform7 remove X from play, now Y contains X`. Seems a little unnecessary.

After I read the Inform documentation a little more, I finally figured out how to solve each problem. These are based on Inform's structure:

* The world is composed of a long list of objects, which can be subclassed -- this is effectively what `:::inform7 An X is a kind of Y` does.
* An object would have simple attributes representing states and properties (open, locked, lit, capacity, volume, etc).
* The world also contains a long list of facts about relations. For example `:::inform7 X is in Y` would be represented by a `:::python3 Fact(Containment, X, Y)`.
* The world would have a list of `Action`s and `Activity`s, and the rules that implement each would be executable code registered in some manner.
* Relations would register with each other which are mutually exclusive (so that when a fact that mentions one is asserted, it clears existing facts that contradict with it), and also whether they are transitive (i.e. if X is in Y and Y is in Z, then X is in Z).

To remove an object from play would simply involve deleting all of the Facts that mention it.

And after considering all of the bugs that cropped up in `json_runner`, I decided on a better option:

Drumroll please...

Plain old Python.

No need to maintain a complicated and buggy JSON-code parser. No dependency on PyYAML to read the game file. No need to write basic interface functions into the JSON-code API manually. And the extra bonus with using pure Python is that it can interface with *any* other libraries that the story author wants to -- the possibilities are unlimited.

By the end of it I will have both a functioning engine, and a functioning game. I've never written an interactive fiction game before, so it might be a little weird.
