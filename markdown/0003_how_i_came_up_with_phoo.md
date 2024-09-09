Date: 2022-03-21
Title: How I came up with Phoo
Tags: programming, phoo, language-design

Several moths ago I stumbled upon Gordon Charlton's [Quackery](https://github.com/GordonCharlton/Quackery) language while paroosing Github for something. Usually I don't pay much attention to obviously irrelevant search results, but this one seemed worth a look. I found Quackery to be a simple stack-based semi-compiled language that makes infrequent use of duck-themed puns. I downloaded it and tried it out, finding it easy to understand and easier to write. But then I realized that I had not read the documentation. (Somehow I end up doing that. A lot.) I was inclined to just skip ahead to the tutorial, but the table of contents links don't work on the Github preview. So I just read down through it from the top.

In the description it said this:

> The Python code is optimised *\[sic]* for legibility and makes minimal use of Python libraries, uses a tiny subset of Python 3 and avoids the use of idioms that may be unfamiliar to non-Python programmers wherever reasonable, to make it amenable to re-implementation in other languages.
>
> (*The Book of Quackery*, page 3)
> {style="text-align: right"}

Hey, I thought, maybe I can make a Javascript clone of this. I figured it would be easy enough. As I began translating it I noticed in many places it was a little too verbose for my liking. Many of the predefined Python functions at the top that everything else is based on contained a lot of code like this:

```py3
def from_stack():
	nonlocal qstack
	expect_something()
	return qstack.pop()

def expect_number():
	expect_something()
	if not isNumber(top_of_stack()):
		failed('Expected number on stack.')

#snip

def greater():
	expect_number()
	a = from_stack()
	expect_number()
	bool_to_stack(from_stack() > a)
```

If you walk yourself through what happens when `:::py3 greater()` is called, you will notice that `:::py3 expect_something()` is called *twice* (once by `:::py3 expect_number()`, and again by `:::py3 from_stack()`) before the item is popped and returned. This really annoyed me and I wanted to fix that. Also, the basic Python functions are actually local subroutines in the main `:::py3 quackery()` function, so more functions can't be programmatically injected in to provide extra functionality in a line-by-line direct translation (even in Javascript), but I wanted to be able to do that too.

The fix to the first problem was quite simple. Instead of having one function that checks and fails if the top of stack is missing or not the requested type, and a second that pops and returns it, I rolled them both into one function that pops, does the type check, and returns it, all in one function call. That was really a drop-in substitution and it didn't cause any errors.

The second problem is when I started getting errors. Instead of having sub-functions that are looked up and called, and have access to the stacks when called because they are in the scope of the stacks, I had moved them out to a separate dictionary, so more could be added. I provided access to the stacks by passing in a context object with the push and pop methods described above. During compilation of the standard library -- the *standard library!!* -- I got a 'Maximum recursion depth exceeded' error from Javascript. I traced that back to the use of the `failed` word rather than just throwing an error. The `failed` word compiles and runs a short snippet of Quackery code to stringify the work stack and return stack, and includes those in the error message it then throws. During compilation it hit an error (what it was I will never know), calling `failed`, and during compilation of the snippet it hit another error, calling `failed` again, and so on and so forth until the Javascript engine detects it's using too much memory for the call stack and bails. I looked through the Quackery documentation again and found this (emphasis added by me):

> When a virtual processor problem arises, Quackery generates a `QuackeryError` and passes diagnostic information back to Python. The simplest way to format the diagnostics is with a short Quackery program, compiled with the Python Quackery compiler `build()`, and run using the Virtual Processor, `traverse()`. **During development these tools were not available, so the Quackery Stack and Return Stack were printed as Python lists.**
>
> (*The Book of Quackery*, page 158)
> {style="text-align: right"}

So I removed the Quackery from `failed` and relied on Javascript to stringify the arrays. And for some reason the standard library compiled and ran just fine now. (Beats the heck out of me why!)

Then I tried to run the demo program. Immediately I started getting weird errors such as `Return stack unexpectedly empty`, `Peek index outside nest`, `actions isn't a forward reference` (it is), `Expected number on stack`, and lots more. Barely anything ran as expected. And because of the way the Quackery compiler works, instead of being the nicely formatted named arrays the Python implementation prints out, everything was obliterated into tens of thousands of lines of compiled arrays and it was impossible to decipher what it was trying to do. (It's like using GDB on a compiled C++ program -- only a select few people in the world can really tell you what all those numbers mean.)

Eventually I got so fed up with these errors that I just decided to start over, from scratch this time. I am pretty sure that the problem was due to there being a Python/Javascript compiler *and* a Quackery compiler that were messing with each other. To reflect the new overhaul I decided to give it a new name: **Phoo**.

Phoo has grown a lot since then. They syntax has changed dramatically, the module loading system has become more complex (almost too much so), and even the internals have changed. (I went back to the two-function method used in the Python `:::py3 greater()` implementation, using one optional `:::js expect()` function to require the top to be a specific type and only checking for the existence of an item in the `:::js pop()` method.) In many ways, Phoo is less like Quackery (or even Forth) and more like Python and Javascript!

You can find the code for Phoo here: <https://github.com/dragoncoder047/phoo>
