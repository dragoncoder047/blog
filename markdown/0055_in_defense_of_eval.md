Title: In Defense Of Eval
Tags: programming, python, rant
Date: 2024-05-31

Your honor, this programmer has obvious disregard for the rules of Sane Programming. We can agree that it is common knowledge that there are certain features of programming languages that are available, but are not to be used. Anyone who does use them is deserving of shame. I present to you Exhibit A, a snippet of code taken from one of the defendant's projects:

```python
def __init__(self, game):
    # ... snip ...

    self.cff = inspect.currentframe().f_back

def create_new_gameobj(self):
    for varname, value in self.cff.f_locals.items():
        if value is self.game:
            break
    else:
        raise ValueError
    g = {}
    eval(self.cff.f_code, g, g)
    return g[varname]
```

This code uses `inspect` to capture and save the current stack frame, which it later references in another method, that also makes a forbidden call to `:::python3 eval()`. May I remind the jury of the widely-accepted programming adage, "eval is evil?" Case closed.

---

Okay, okay, I know what you're thinking. Did I write that code? Yes, I did. And there's a very good reason why I could *only* use `:::python3 eval()` for that code, and why I *had* to save a reference to the current stack frame.

This chunk of code is taken from one of my as-yet-unreleased projects, the interactive fiction framework that I have written about a couple of times before. I've gotten it to the point of being able to run a very basic and limited and rather unplayable game, but at least it works. Since terminals can't change font, I decided that to be able to use proportional-width fonts for formatting, I would have to take advantage of a web browser.

The entire game object, that holds the state of the interactive fiction story, is created when the story file is run (it's just Python), and the world state is manipulated by injecting the player's commands. When the game is running in a terminal, there is only one session going at once, so the original game object passed in can be used, no problem.

Weird stuff starts happening if the same game object is used for the Web server mode of presentation. Because the game object holds the state of the game, if the same game object is shared across two supposedly separate game sessions, the two sessions will end up sharing game state. That is bad.

The solution I came up with was simple: just serialize the game object and stuff it in a hidden `:::html <input>` in the game page that the server sends. Then when the player submits their command, the game object is deserialized from scratch, and essentially creates a new, cloned game object each time that never shares any state with any other game object in any session. Or so I thought.

Turns out, simply serializing and then deserializing the game object wasn't enough to truly and fully clone it into a noninteracting, independent session. In writing the test game, I made judicious use of some advanced pointer structures -- most notably impure functions and lexical closures -- that Python's standard `pickle` module couldn't handle. So I had to turn to the third-party [`dill` package](https://pypi.org/project/dill/). And this was when I ran into another issue.

Impure functions are simply functions that refer to and assign to variables from outside their own scope. To be able to do that, and simultaneously make the function a first-class object that can be passed around (and even through the network, as I was attempting to do), Python has to give the function object a pointer to all of the scopes it references, so it can still manipulate the variables even after the referenced scopes are popped off the call stack. Lexical closures are the same thing, except at some point, the function object is the only object that refers to the scope -- at this point, the scope is said to be "closed over," and the function a "closure." Python employs some other optimization tricks to reduce memory consumption (such as only giving the function a reference to the variables it interacts with -- known as the "cell variables" -- and discarding the rest of the scope), but the point is this: *some part of the global scope is still alive* even after it is not directly accessible by the program.

The `dill` package is able to serialize these impure functions and their references to global variables, with one critical caveat that I found out the hard way: When it detects an impure function is refering to a module-level global scope, it doesn't serialize the scope, it only makes a note in the serialization output that the scope is referred to. Then, when the object is deserialized, `dill` just adds a pointer to the already-existing scope. In the name of saving memory, `dill` has just created shared state.

So that's the reason for why I use `inspect` and `:::python3 eval`. The only way I can create a clean clone is by re-running the code, every time, in a clean scope. When the server is created, it saves a snapshot of where it was called from, which gets it the module code needed to recreate the game object. Then when it starts a new session, it creates a new, empty scope, and `:::python3 eval`'s the code within that scope. Problem solved.

*This* is the reason I used `:::python3 eval`. *This* is the reason `:::python3 eval` exists. *This* is the reason `:::python3 eval` can never die.
