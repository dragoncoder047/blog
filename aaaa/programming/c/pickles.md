Title: Pickles!
Date: 2023-02-21

I've been playing around a little bit with LIL on my ESP32 arduino. It works, but there are a few things I don't like. LIL isn't object-oriented by default, so I can't do a lot of what I am used to writing code in Javascript and Python. LIL also forces the result of every expression (the `:::tcl expr` command) to be a number (so I can't do a `:::python "foo" * 3` to repeat a string), has no operator overloading because nothing is an object and supports overloading anyway, and (most importantly) doesn't support lexical closures.

LIL also does not have what I think is a really useful operator: the `|>` pipe operator, for function chaining. Javascript is working on one (it was [proposed](https://github.com/tc39/proposal-pipeline-operator) and it will be incredibly useful if and when it actually goes through.

There are several things about LIL that I do like, though: it has a nice recursive parser, a very simple hashmap implementation, and the use of arrays of pointers to implement list types. Back when I was working on TEHSSL, I actually decided against the last one because I (erroneously) feared that if I had to `:::c realloc()` the array, it would move objects and corrupt the pointers of every object that pointed to them. When I looked at LIL, it finally dawned on me that the array was an array of *pointers* to the objects, and `:::c realloc()`'ing the array would only move the *pointers*, not the objects, and so it's okay to use as long as you don't overrun your array before you `:::c realloc()` lit. 

As-is, there is one feature that I want in my scripting language that I don't see in any other language. It is the ability to **define custom operators**.

Suppose I am writing a little DSL for routing audio nodes (which seems a possibility in the future, I'm not sure why). Albeit, with a Tcl-like language, I can just have the user pass in a string of the code, and process it as the DSL. But then I'd be stuck writing the parser, interpreter, etc. for that all over again and I'd probably take away half of the features of the enclosing language in the process.

The code would be, I don't know, using the `<-` operator to link the node input to the node output. The `<-` operator wouldn't mean a darn thing to number objects (like 14 and 23.5), or anything else, for that matter, so a language that isn't designed with this in mind would probably never implement the `<-` operator.

However, if I can define a new operator, `<-`, with a specific precedence, and then link it to a special "magic method" (taking inspiration from Python) that gets called on the objects when they are operated on by that operator (such as `__left_arrow__` for `<-`), it would allow this DSL to be made in native code, and not sacrifice anything.
