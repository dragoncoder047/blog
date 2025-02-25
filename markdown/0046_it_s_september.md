Title: It's September!!
Date: 2023-09-18
Series: pickle
Tags: gamedev, language-design, programming

Unfortunately that time of year has crept up... school has started again. And not just any kind of school: I find myself in 12^th^ grade, balancing seven classes, two with AP tests at the end, three with huge final projects. I'm also trying to apply to college at the same time. Not to mention that I also have a bunch of my own personal projects that I'm trying to work on too.

Thankfully I have had a small amount of time to spend on planning a couple of different things.

## Parasite

I completed and published Parasite last week. It's not terribly polished and the game is practically unplayable, but I am still pretty impressed with where it is so far. It's a bit of an interesting experiment to see what you can do with a bunch of completely untrained neural networks. I encourage you to [try it out](/parasite/) and tell me what you think.

### Things left to do

* Implement the last two actions which allow the snakes to mate with each other and create more snakes. Right now they just do nothing with this one. I'm also not sure how to merge the AI models of each of the parent snakes when creating the new ones.
* Create real levels, with playable goals. This is hard because each level's goal has to be assessed in a different way and so a Javascript function has to be used to test what it needs to and decide if the level is beaten. The other hard part is coming up with the goals!
* Create a pre-trained model for the snake AIs, so they actually act like snakes and not noodles. I'm also not sure what would be the best approach to doing this. My best idea is to run a specially modified world that automatically rewards and punishes the snakes as they move around, let that run for a long time, and then export the snake models as JSON and load them in later. Unfortunately the system is so complex I'm not sure if I will have to run the training world for two hours, or two weeks.
* One of the snakes' actions is to make "sound" that all of the other snakes "hear", but currently there's no code that will output the sounds for what the player snake "hears" out the player's speakers. I would do this except I don't have a good pair of headphones and I'm trying to develop this where (if I were to be making horrible noises using my computer) I would be disturbing other students, so I decided against that.

### Future additions

The last thing I want to do but can't at this moment. The game is currently playable using a keyboard and mouse, but I wanted to also be able to add [gamepad support](https://developer.mozilla.org/en-US/docs/Web/API/Gamepad_API). I don't own any gamepads, so that's going to have to wait.

Another idea I considered would be to add a "sandbox" level at the end, in which the player would have more freedom to do anything they wanted, with no "goal" to determine when the level is complete. I haven't implemented any of this yet but I might. Nothing is certain at this point.

## PICKLE

Not much has happened with PICKLE since my last post about it. However, in my investigation of other things I came up wth a few more substantial ideas, which are outlined below.

### No-colon colon blocks

Currently the indentation feature is triggered by the sequence of colon plus newline plus an indented block, like this:

```pickle
## This parses as a colon block string, and a single line.
foo bar:
    baz bam

## This causes (or will cause) an "unexpected unindent" error.
foo bar
    baz bam
```

The mandatory colon has been haunting me for a while and I finally figured out how to remove it.

Normally, the parser "looks ahead" to check if there is a colon block and if there is it removes the colon from the previous token. However, I realized that it would still be able to detect the indent regardless: when it is parsing the colon block it strips the indent from all of the lines. Functions that take blocks of code instead of strings will trigger the colon block to be parsed, and by then the indent will be gone, so the parser only needs to care about if there *is* an indent, not the *size* of the indent (just enough to verify that it's all valid).

When it detects a newline, it looks to see if the next line is indented, and if so, it takes back the newline token and starts chucking the (stripped) lines into a buffer. When it detects a line with no indent, it emits the indent-block string onto the same line as the block header and then finally emits a newline.

Conveniently, this also fixes a problem where the parser wouldn't accept a comment between the colon and the newline when opening a colon-block, because now the colon is just another operator.

### Pre-concatenation

While working on parsers for some other mini-languages I discovered an interesting problem that arises when the language includes alphabetic operators such as `:::python and` and `:::python or` and *also* allowes unquoted strings (there are no symbols). The problem arose when an unquoted string contained a keyword: if I wrote `sandbox world`, it would actually be interpreted as if I had typed `s and box w or ld`. This caused a lot of head-scratching until I figured out what was going on and quoted the strings.

PICKLE has symbols, instead of unquoted strings, but the problem could still happen with the every-character-is-its-own-symbol rule I presented previously. This would be solved immediately if I automatically concatenated symbols in the same class to each other before any rules were applied. The most basic rules I can think of would be categories of letters and underscores, digits, and punctuation characters (excluding parentheses which are handled specially by the parser).

The next step could be to add patterns for different number formats, etc. but I want to avoid locking-in specific formats. One of the goals of PICKLE is to have no fixed formats and that would go against it. The easiest solution to this would be to combine PICKLE's pattern matching with a feature of Tcl: each token always has a string representation. That way, when tokens match concatenation rules they could dig up the original string that the programmer wrote and parse *that* instead of trying to muck around with the object that the token turned into. Better yet, each token could also remember *where* it was originally written, to be able to give helpful error messages.

### Resumable exceptions

In playing around with the Scheme programming language, I had a few ideas. Compliant Scheme systems implement everything in continuation-passing style. That is, instead of simply returning a result to the caller, each operation calls the current continuation with the result. If the operation could not be completed, it calls the failure continuation with the details of the error.

Continuations are best illustrated, I think, using Javascript `:::js Promise`s. They are, in effect, a limited form of `call-with-current-continuation-and-current-failure-continuation`:

```js
new Promise((resolve, reject) => {
    // resolve is the current continuation
    // reject is the failure continuation
});
```

Scheme also has a construct known as `:::scheme dynamic-wind` that functions a lot like Python's `:::python with` blocks. `:::scheme dynamic-wind` takes three thunks, the first is called whenever code in the second starts running, and the third is called whenever code in the second stops running. Entry and exit in Python is only possible by way of normal control flow or thrown exceptions, but in Scheme it's possible to ender and exit the same block many times, using continuations.

The idea I had came after seeing a little snippet demonstrating the use of SISC Scheme's `:::scheme with-failure-continuation`, which acts almost like a Python `:::python except` block, *except* for the fact that it is also passed the current continuation at the point where the error occurred. This is extremely powerful.

Consider a simple divide-by-zero error. The current continuation of the division expression still exists, and now the failure handler can decide whether to resume or propagate the exception. Python doesn't let you decide what to do in this situation: the result is always an exception being thrown. However, in Scheme, the failure handler can instead resume the computation with a substitute value: in some situations it would be appropriate to return $\pm\infty$ for a division by zero; in other situations a `:::js NaN` value; and in others to propagate the error.

When errors are resumable, it unlocks a lot of possibilities. One useful example I can think of is quantities (numbers with units): a quantities package could install a failure handler that would intercept errors caused by trying to call a number with arguments (which normally would make no sense) and resume the call with a quantity.

For example `:::scheme (10 'miles)` normally would normally not work (Guile gives the message "Wrong type to apply: 10"), but if the error included details of what was being called and with what arguments, a handler could transform this call into a quantity representing a distance of 10 miles.

So I've decided that in PICKLE, continuations will be supplied with every error, so the computation can be resumed with any specific values.

---

That's all for now. I hope to be able to implement some of this soon!
