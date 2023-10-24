Title: A Very Confusing Data Model
Date: 2023-03-10
Tags: programming, python, game-design

For the past week or two I have been working on a few things simultaneously. I keep prototype code that I'm developing but not quite ready to release yet in private GitHub repositories, and publish them when I'm ready. Lately I've been working on two different and completely unrelated things.

The first is the programming language I started in my previous post, PICKLE (which I think will be the final name). I got the garbage collector to work, and I also implemented hashmaps capable of looking up object attributes. I also got the parser to generate an abstract syntax tree from the code, which is a lot farther than I got with my other failed attempt at creating a programming language, TEHSSL.

The other thing I am working on is at the request of a friend. He is currently working on a (cringey) interactive fiction game, currently using [Twine](https://twinery.org). But he wants to use a text-based engine, and none of the major ones have features he wants, so I have been asked to make one.

As-is, it's very much a concept.

I'm very much tailoring the engine to fit my friend's game, but I do want it to be able to be used for any generic type of game. So I have to do two things: 1) make it usable by a person who has never done programming before (although I do know my friend from *computer science* class) and 2) be story-agnostic, so it can be used for a fantasy story as easily as for a horror story or a science fiction story.

Number 2 necessitates abstracting the common characteristics of story elements into simple base classes, and then allowing the user to extend them to create the objects in the game.

After a lot of thinking (and consulting the [Interactive Fiction Wiki](https://www.ifwiki.org/Building_a_New_Interactive_Fiction_System)) I came up with a simple method of defining objects based on a few simple attributes:

* Physical attributes:
    * Size: how much space the object takes up. For example, a glass bottle might have a size of 1, and a brick might have a size of 2.
    * Volume: the amount of space is empty inside and can be filled with other objects. The bottle's volume might be 1 as well, and the brick's is of course 0 because it isn't a container. This can also be greater than the size for fictional objects that can hold more objects than the visible volume.
    * Weight: How heavy an object is. The player character has a limit to how much you can carry (which could be changed by a magic strength potion or such).
    * Entrance size: irrespective of volume, the largest item that will fit into or out of the object. For example, while a lime could probably fit inside a glass pop bottle, it wouldn't fit though the neck and so could not be put in the bottle, or could not be taken out if it was magically moved inside the bottle.
* Visual attributes:
    * Opacity: how easy it is to see objects inside of it. Things inside that are smaller than this percentage of the object's size are reduced to "and something else inside" when describing the object, and not mentioned at all if the opacity is 100%. For example, for a plastic jug with a size of 10 and an opacity of 90%, objects inside the jug that have a size less than 9 would have to be removed to be described clearly.
    * Luminosity: how much light the object emits; additionally, if the object does not have an opacity of 100% and there are light-emitting objects inside, they also change the luminosity.
    * Light color: an arbitrary string that usually serves no purpose, but it could be useful for color-coded hidden messages (such as a paper that reads "puasjeftbhveibernaasgskkjefy" normally but when viewed under red light it reads "usethebrasskey").
    * Fuel: how long the object will continue to emit light for. A match might only last for 2 turns, while a flashlight might last for 100 turns before the batteries die.
    * Switch state: a flashlight could be turned off, in which case it would stop emitting light, but the battery would stop draining too.
* Presentation attributes:
    * The usual name, description, and long description.
    * Whether the object is unique: if so, it will be printed as `the brass key` rather than `a brass key`, if not, multiple instances will be coalesced into one entry when listing inventory (so it will show `5 apples` rather than `an apple, an apple, an apple, an apple, and an apple`.)
    * Whether the object is a proper noun: if so, it will be printed as `John` rather than `the John`.
    * Whether the object is hidden: if so, it will never be printed when listing inventory, it will not appear in descriptions, and the game will always act as though the player doesn't have it. This is useful for intangible things like passwords, combinations, or incantations that must be learned or figured out before they can be used (the object can be silently inserted into the player's inventory when all the information necessary has been discovered) or "under" regions due to the limitation of the model that a table must be put over an under-the-table for other things to be able to be put under the table (which is really in the under-the-table).

(Wait... did I just say "a few?" I sinceeeerely apologizeeee........)

From this, special objects can be made with sentinel value of zero or infinity:

* Anything immovable has infinite weight.
* A non-container has zero volume, but nonzero size.
* A liquid has nonzero volume, but zero size.
* A room that is not self-lit has zero luminosity (i.e. you need to bring in a candle to see stuff, otherwise you'll just get `It's dark in here`).

Rooms additionally can reference each other (to implement passages) directly or through a door. Doors also have flags indicating if they are locked and closed.

Every object can also respond to events, which the vast majority of verbs is simply the verb. For example, typing `push the button` would invoke the `push` event on the button.

The difficulty with this data model is the ability to refer to any object from anywhere in the object tree. The engine has to account for the paradoxical possibility of a reference cycle, so the tree acts more like a doubly-linked list and the management of the nodes gets very confusing very fast and I haven't implemented any of it yet.

The second, unrelated problem I have is how to describe the game. I want to avoid the use of real Python code as much as possible, but to allow for anything to be modified in any way desired during the course of the game. I did find a simple description of using YAML (and by extension, JSON) as a templating language ([this](https://nathanpeck.com/is-yaml-a-real-programming-language/)), but it's not Turing-complete, and it's a templating language anyway (the constructs were designed without any side-effects in mind).

I have had several ideas over the course of thought:

1. Use [Tcl](https://docs.python.org/3/library/tkinter.html#tkinter.Tcl) embedded into Python to create a domain-specific language. This has the disadvantage in that it can't be run in the Web using Pyodide because Pyodide doesn't have access to libtcl.
2. Write my own Tcl-like parser in Python. This is conceptually easy (all it really needs to do is be able to balance brackets) but extremely difficult in practice.
3. Just give up and use Python, but make it really easy by using a decorator syntax, and naming conventions similar to the `do_X` standard expected by the Python [`cmd` module](https://docs.python.org/3/library/cmd.html).
4. Use YAML, and embed commands into the strings somehow. Blocks could be implemented by one-keypair dictionaries.

The approach I think I'm going to use is probably a mix of 3 and 4. For some reason I like Lisp, so I might end up using [Hy](https://hylang.org) as the expression syntax. A trivial fizzbuzz example would probably look like this:

```yaml
- for x (range 1 11):
  - if (= 0 (% x 15)):
    - print FizzBuzz
    elif (= 0 (% x 5)):
    - print Fizz
    elif (= 0 (% x 3)):
    - print Buzz
    else:
    - print {x}
  - inc x
```

Who knows. If you're interested in the outcome of this, monitor my GitHub repositories list for the appearance of something described as a Python text-based game engine. I don't even have a name for it yet!
