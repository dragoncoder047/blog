Title: Manual Memory Management Madness
Date: 2023-03-17
Series: pickle

I've been working quite a lot on my second programming language attempt, PICKLE. Admittedly, programming it in C has been a real chore. I started following the [Make-A-Lisp](https://github.com/kanaka/mal/blob/master/process/guide.md) tutorial to try to give myself some plan for executing PICKLE. Mal, unfortunately, recommends dynamically typed languages; that unfortunately is a no-go because I have to write it in C/C++ so I can compile it onto a microcontroller.

So the first thing I set out to do was create a type system and garbage collector. I had already read up on garbage collectors -- Bob Nystrom's [Baby's First Garbage Collector](https://journal.stuffwithstuff.com/2013/12/08/babys-first-garbage-collector/) is my go-to-reference for creating mark-and-sweep collectors. I tend to stick with the "typed union" approach to storing object-specific data, as opposed to the cast-the-opaque-pointer approach of Python.

Regardless of the method of garbage collection, I always managed to run into some sort of roadblock.

With the pure mark-and-sweep of TEHSSL, it was necessary to store intermediate values needed during execution on a temporary garbage-collector-protection stack, and pop them back off when they are no longer needed, to allow them to be collected, but this really clutters the code. It also it got confusing for me to think about as to when a value must be put on/popped off the stack (of course, this only applies if someting is being done in the meantime that could trigger the garbage collector, that is, the allocation of more objects).

The next approach I tried was a reference-counting garbage collector. There is, technically, a mark-and-sweep running in the background, but it is only explicitly called when needed to take care of circular references that arise. Reference-counting collectors, as I talked about in the previous post in this series, have the advantage that objects are immediately freed when they are no longer needed, and so can be quickly recycled. The disadvantage is that C (or even C++) does not keep track of references for you; you have to explicitly increment and decrement reference counts which clutters up the code.

I quickly noticed that there is an almost-one-to-one relationship between garbage collection stack pushes and pops, and incrementing and decrementing references:

```cpp
push(vm->gc_stack, foo);
do_something(foo);
pop(vm->gc_stack);
// equivalent to:
incref(foo);
do_something(foo);
decref(foo);
```

In terms of code clutter, there is no advantage, and maybe a slight disadvantage for a reference-counting garbage collector because there is some required overhead when re-assigning a pointer:

```cpp
decref(foo->bar);
foo->bar = baz;
incref(baz);
```

Both of these are just confusing, and because there is no C equivalent of Python's `:::python with` block or a C++ `:::cpp try`/`:::cpp finally` construct (and I've yet to try any kind of C preprocessor macro hack) I have to explicitly stop, decref all the objects I used, and then return (even if it is a quick abort in the middle because of an error). And this is all messed up if I end up using `:::c longjmp()`-based error handling, which means a function may never even return to be able to clean up those dangling references. I don't like using `:::c goto` excessively, even if it is for an obvious `:::c goto done;` but I probably will have to.

---

Now that I've got *that* off my head, I can get to the next thing: how the language is actually going to work. I'm not writing another Lisp.

To summarize what I've written so far:

* A reference-counting garbage collector with a mark-and-sweep cycle buster.
* Two type systems:
    * One that leaves every object as an opaque type and leaves it up to "type functions" given to the VM to mark and sweep the objects.
    * Another that defines 23 builtin types, with the data scattered thoughout a complex tree of `:::c union` and `:::c struct` blocks, and the VM uses a large lookup table to find which parts of the object contain pointers and things to be freed.
* One parser, that despite the weirdness of the garbage collector and type system, is still able to produce a sensible abstract syntax tree.

I've been looking around at a lot of other embedd~~ed~~able scripting languages lately as I've been working on PICKLE. LIL is certainly a large inspiration for the syntax, and Python contributed the indented blocks.

Bob Nystrom's [Wren](https://wren.io) programming language provided some help on operator and method overloading. Wren acheives method overloading by looking at the number of arguments when the method is called, and then finding a method definition with the same number of arguments -- so `:::wren foo.bar(1)` and `:::wren foo.bar(1, 2)` are actually two different methods (the first one is called `:::wren bar(_)` and the second one is called `:::wren bar(_,_)`). This implicitly means that declaring a method that takes a variable number of arguments (i.e. varargs, argument unpacking, "expandos", etc) is impossible and I don't like that.

Wren, however, allows *operator* overloading as well, and its implementation is dead simple: to overload the `+` operator, you simply declare a method named `+` that takes one argument. That's it.

Unfortunately, this model doesn't quite work for PICKLE: the operators are baked into the Wren grammar, and you can't define more.

However, one idea I had myself in the process of thinking about how to implement custom operators is to simply have a second hashmap on each object, alongside the normal one for attributes, and use it to map operator symbols the object responds to to their associativity, arity, and precedence. Lookup would recurse through the prototype tree as with any other object property.

Operators would be parsed identically to symbols, and if they aren't next to any object that responds to that operator, they would behave identically to one.

When an expression is evaluated:

1. Each element in the expression is evaluated (recursively). Most literals evaluate to themselves, so this really doesn't change much. The result of this is a list of values, some of which may be operator symbols.
2. PICKLE scans each of the elements and looks to either side of it and makes a note when the middle object responds to either of the symbols on the left and right as operators.
3. From these, if any are unary (prefix or postfix), it picks the highest precedence one and evaluates it by calling the appropriate method on the object and then splices the result back in to the in-progress list of values.
4. Once the unary operators are exhausted, PICKLE picks the highest-precedence binary operator according to associativity rules and then calls the method on one object, passing the other object as a parameter, and splices in the return value to the list of values.
5. It then checks that return value for operators it responds to and goes back to step 2.
6. Once all the operators are exhausted, it simply calls the first object with the rest as arguments.

This, conveniently, would simplify parsing, quite a lot, and allow for me to use Python style infix assignment operators instead of an annoying `:::tcl set` command. The way it would work is variable names are parsed as symbols, and symbols would respond to the `$` dereferencing operator. When the operator is applied to the symbol, it responds by looking up the variable with the same name. Similarly, objects would respond to the `.` operator, which would perform attribute lookup, and the `=` operator, which would create a temporary set-attribute object, which, when combined with the `.` operator, would signal to an object to set the property to the computed value.

This, however, does have some issues. Consider this (hypothetical) code:

```pickle
class A:
    postfix 3 !!:
        do_something
class B:
    prefix 3 !!:
        do_something_else
let x = A.new
let y = B.new
x!!y
```

Here, it creates two objects, one that responds to `!!` as a prefix operator, and the other to the same operator as postfix. The key here is that both operators have the *same precedence*. When PICKLE tries to execute the last line, it runs into an ambiguity problem: does the `!!` apply to `x` or `y`? I'm not sure what I'll do here, whether it's just bail and throw an error, or define some sort of deterministic left-to-right order, but hopefully it will be something that makes sense.

That's it for now. I'm going to try to rewrite PICKLE in C++ and see if that makes things any easier.
