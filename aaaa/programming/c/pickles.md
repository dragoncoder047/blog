Title: Pickles!
Date: 2023-02-21

I've been playing around a little bit with LIL on my ESP32 arduino. It works, but there are a few things I don't like. LIL isn't object-oriented by default, so I can't do a lot of what I am used to writing code in Javascript and Python. LIL also forces the result of every expression (the `:::tcl expr` command) to be a number (so I can't do a `:::python "foo" * 3` to repeat a string), has no operator overloading because nothing is an object and supports overloading anyway, and (most importantly) doesn't support lexical closures.

LIL also does not have what I think is a really useful operator: the `|>` pipe operator, for function chaining. Javascript is working on one (it was [proposed](https://github.com/tc39/proposal-pipeline-operator) and it will be incredibly useful if and when it actually goes through.

There are several things about LIL that I do like, though: it has a nice recursive parser, a very simple hashmap implementation, and the use of arrays of pointers to implement list types. Back when I was working on TEHSSL, I actually decided against the last one because I (erroneously) feared that if I had to `:::c realloc()` the array, it would move objects and corrupt the pointers of every object that pointed to them. When I looked at LIL, it finally dawned on me that the array was an array of *pointers* to the objects, and `:::c realloc()`'ing the array would only move the *pointers*, not the objects, and so it's okay to use as long as you don't overrun your array before you `:::c realloc()` it. 

LIL also forces the use of curly brackets (`:::tcl { }`) for delimiting code blocks (which are really just strings), which as a Python programmer, I don't like. One modification I would like to add is the use of a ":" to delimit a block of code.

As-is, there is one feature that I want in my scripting language that I don't see in any other language. It is the ability to **define custom operators**.

Suppose I am writing a little DSL for routing audio nodes (which seems a possibility in the future, I'm not sure why). Albeit, with a Tcl-like language, I can just have the user pass in a string of the code, and process it as the DSL. But then I'd be stuck writing the parser, interpreter, etc. for that all over again and I'd probably take away half of the features of the enclosing language in the process.

The code would be, I don't know, using the `<-` operator to link the node input to the node output. The `<-` operator wouldn't mean a darn thing to number objects (like 14 and 23.5), or anything else, for that matter, so a language that isn't designed with this in mind would probably never implement the `<-` operator.

However, if I can define a new operator, `<-`, with a specific precedence, and then link it to a special "magic method" (taking inspiration from Python) that gets called on the objects when they are operated on by that operator (such as `__left_arrow__` for `<-`), it would allow this DSL to be made in native code, and not sacrifice anything.

So, I think I'm at least going to try to implement my own language. I'll be able to fall back on LIL if all goes horribly wrong, but if it works, I'll have something that works better for me, and maybe for someone else.

Here are my goals:

* Be small enough to fit on an Arduino -- specifically, an ESP32, with 16MB of program storage space and 124KB of RAM.
* Be thread-safe and re-entrant (except for stuff like global variables, which are shared via mutexes) so I can use FreeRTOS tasks to implement co-operative threading
* Have the aforementioned user-definable operators
* Be object-oriented
* Have closures, classes, lambdas, etc. that a good high-level scripting language like Python or Javascript has
* Allow operator overloading on objects
* Utilize dynamic typing
* Utilize dynamic memory allocation and a garbage collector
* Include code<-->data interoperability
* Possibly implement syntactic macros

## Objects and inheritance

The inheritance system I'm probably going to go with is Javascript's primitive prototype-based inheritance, even though the only way it supports multiple inheritance is through monkey-patching. The easy way I see to allow multiple inheritance is to allow an object to have, well, multiple prototypes, which are searched recursively. That would also circumvent an (intentional) bug in Python where this code would crash because it creates an ambiguous inheritance order (see if you can spot why):

```python3
class A: pass
class B: pass
class X(A, B): pass
class Y(B, A): pass
class Crash(X, Y): pass
```

Paste it into a Python console -- you'll get `TypeError: Cannot create a consistent MRO for bases A, B`. The reason why Python crashes is because `Crash` inherits from `X` and `Y`, and each of those inherit from `A` and `B`, but in a different order, so Python doesn't know whether to look at `A` or `B` first. How my new language would go about it is that because `Crash` listed `X`, first, it would search in the order `Crash, X, A, B, Y, B, A`.

Another thing I am going to take from Javascript is that everything in the "global" scope is really properties of a global object (called `globalThis` for some reason, per the spec) and so that simplifies scope management a whole lot.

One thing I am *not* going to take from Javascript is the indistinction of items and properties of objects. Think of a Python dictionary: it has methods such as `copy()`, but you cannot access them by writing `:::python mydict["copy"]()` like would work if it was Javascript. Neither can you access dictionary items stored with `:::python mydict["foobar"]` using the `mydict.foobar` syntax.

## The garbage collector

When I was working on TEHSSL, I had implemented a pure mark-and-sweep garbage collector. Mark-and-sweep collectors are *perfect*, that is, they always collect all the unreachable objects and never leak memory, but this got really hard to manage in TEHSSL. For example, specifically when I create a whole bunch of intermediate objects that are used once and then never again (like during compilation) causing the number of objects to hit the high-water mark and activate the garbage collector, freeing all those objects that I am done with, but also the ones I'm *not* done with, corrupting my pointers. The common way to prevent that (used by uLisp) is to use a temporary garbage collector stack to store those objects on, but that made it even more confusing.

The approach Python takes is a little different: Python uses a reference counting garbage collector. That is, each object maintains a count of how many C pointers and other objects point to it, and when it drops to zero the object is immediately freed. This does suffer from problems when objects point to each other and create a reference cycle, preventing those objects from ever being freed. Python does have a "cycle-busting" mechanism in place, but as far as I know, it isn't described very thouroughly. Perhaps it's just a mark-and sweep collector.

The garbage collector I am going to implement will use reference-counting for most things, and then only call a mark-and-sweep at strategic times to clean up the reference cycles, when I am sure there aren't any intermediate objects that are still in use being pointed to by C variables.

## Closures

LIL does not have closures. That is, this code:

```tcl
set bar "global text"
func foo {bar} {
  set closure [func {} {print $bar}]
  return $closure
}
set baz [foo "closed text"]
$baz
```

prints "global text" -- the passed-in value of "closed text" is lost.

But, `func` is a function itself, that creates functions when executed. Couldn't the returned function have a pointer to the enclosing scope it was declared in, so that it could use closed-over variables? That's what I'm going to do in my program.

Bob Nystron's [*Crafting Interpreters* book](https://craftinginterpreters.com/closures.html) utilizes the Lua-like method of storing "upvalues" in a special closure wrapper of a plain function, which has the advantage that closures only close over the values they actually will use, saving memory (maybe). But because of Tcl's `:::tcl upeval` (and LIL's extension `downeval`) those "possibly-untouched" closure values may actually be used after all. The semantics of `:::tcl upeval` and closures I'll figure out when I get there. Storing the entire scope seems like an easy way to allow `:::tcl upeval` to work okay.

## Colon blocks

Python is probably the first scripting language to use indentation to delimit blocks of code. Python is also bytecode-compiled, so every single function, if statement, loop, etc. is compiled into bytecode and as such all the "colon plus indent" blocks must be valid code. Also, only certain constructs can take a block after them, and those cannot be added to.

However, I realized it would be more than simple to add colon-delimited blocks to a Tcl-like language. The way it would work is that when the compiler sees a colon followed by a newline, it treats it like a `{` and begins collecting a string. Except instead of counting the nesting depth of the `{`-`}` pairs, it would simply look at each line's indent level and stop when it detects a dedent. The final string would have the leading indentation stripped from each line. So these two pieces of code would be equivalent:

```tcl
while {foo} {
  bar
}
baz
```

And:

```tcl
while {foo}:
  bar
baz
```

This saves a line, and it looks a lot cleaner. An interesting side effect is that you can append a "block" to the end of any function, and it will take it as a string. So you coule write this:

```tcl
print:
  foo
  bar
```

Which would print `foo bar` each on their own line, and with no indentation.

## Naming it


