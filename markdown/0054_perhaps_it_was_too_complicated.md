Title: Perhaps It Was Too Complicated
Date: 2024-05-01
Tags: programming, python, game-design

I guess I lied. About five months ago, I posted some thoughts about an upcoming Python interactive fiction engine, where the world model is not actually a tree, but simulated as such by relations. For example, there could be an apple inside of a refrigerator, and while it would make sense to put the apple as a child object of the refrigerator, the actual implementation would just store three objects in a flat list: the apple, the fridge, and a relation object specifying the apple is inside the fridge.

It turns out, that was a little difficult to implement. I may go back to it, but for now, my implementation does actually place the objects in a tree structure, with the fridge pointing directly to the apple as a contained object. Except in the current implementation, the apple also holds a pointer to the fridge as its parent object -- when the player takes the apple from the fridge, this enables the apple to be easily made a child object of the player only, and not both the player and the fridge at the same time (which wouldn't make much sense). Since the apple has a non-`:::py3 None` parent, before the apple's parent is set to the player, the apple's parent (i.e. the fridge) has the apple removed from its child object lists, ensuring the apple is only child of one thing at once.

I sorted this out, then started follwing [Inform 7's Standard Rules](https://zedlopez.github.io/standard_rules/) to implement the typical physics of interactive fiction. After looking at how Inform has the runtime system organized, I figured out that there was some duplication of things. For example, Inform separates different things being done into two basic categores -- "activities" and "actions". I'm not entirely sure what the difference is, even after reading the documentation. But here's a good example I came up with that demonstrates one of each:

```inform7
[This is a rule for the "printing-the-name-of activity"]
Before printing the name of an edible thing:
    say "[one of]yummy[or]scrumptious[or]delicious[or]tasty[or]delectable[at random] "

[This is a rule for the "opening action"]
Before opening an interdimensional chest (called C):
    repeat with D running through all interdimensional chests in the world:
        if D is not C, now every thing in D is in C.
```

The headers of the rules, which specify when the rule runs, look very similar. They both filter for a specific type of object. They both filter for a specific thing happening in the turn cycle. They both happen before the rest of the rule runs. Why should one be an "action" and the other an "activity"? I really don't know.

I simplified both "actions" and "activities" into one construct: "events". Every object can have event handlers attached to it, which function as the rules. When the action or activity happens, all the event handlers for the relevant objects are invoked, in order, until either one of the handlers cancels the whole action, or all handlers have been run.

The next thing I revised -- from both my previous two posts on this, as well as Inform's Standard Rules -- is that not every object has every possible attribute, such as having a capacity, or a luminosity, or anything else that differentiates a particular "type" of object from another. These are added by giving the game objects "traits".

As of right now, 202 out of the 373 lines in `thing.py` deal with managing traits on game objects. Most of those lines implement two key characteristics of traits: there can only be one of each trait on a particular object, and some traits can imply other traits -- so I have to do dependency analysis to figure out what has been added and what needs to be added. Then, since the "core" functionality is implemented by traits, there are a lot of aliases and attribute interception going on to automatically translate properties into trait lookup. It's a bit of a mess right now, and at any rate it's useless until I actually implement the rest of the library!

I suppose the lesson to be learned here is that of Occam's razor: that is, if it looks to be too complicated for what it's doing, it probably is.
