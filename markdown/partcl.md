Title: ParTcl
Date: 2022-10-14
Series: arduino-scripting
Tags: programming, c

C headers are annoying. I was getting fed up with uLisp/Yisp and so I decided to run another Google search for "embeddable scripting language for Arduino".

It turned up [mruby-arduino](https://github.com/kyab/mruby-arduino) -- poorly documented, and a little too big for my needs.

It turned up [eLua](http://www.eluaproject.net/) -- which unfortunately is just a flashable firmware with no C interface for custom functions (just like with MicroPython).

And it turned up Serge Zaitsev's [ParTcl interpreter](https://zserge.com/posts/tcl-interpreter/). It's a bare-bones interpreter for the [Tcl](https://en.wikipedia.org/wiki/Tcl) programming language which implements only 5 core functions (`:::tcl subst`, `:::tcl set`, `:::tcl while`, `:::tcl if`, and `:::tcl proc`) as well as `:::tcl puts` and some math functions.

Despite this minimalism, it is simple to understand as most things are abstracted away into functions and datatypes -- and, leveraging the fact that "everything in Tcl is a string," `:::c malloc` and `:::c free` can be used easily for dynamic memory management.

Additionally, from the Github readme:

> * Can be extended with custom Tcl commands
> * Runs well on bare metal embedded MCUs (~10k of flash is required)

...which is exactly what I need to use it as an Arduino library!

There are a few bugs -- namely this one:

> In the default implementation lists are implemented as raw strings that add some escaping (braces) around each iterm. It's a simple solution that also reduces the code, but in some exotic cases the escaping can become wrong and invalid results will be returned.

Using my experience from Lisp lists, I saw that Tcl lists could be implemented as a linked list as well. I [proposed it](https://github.com/zserge/partcl/issues/14) and we'll see what Serge says. I could probably fork ParTcl and add it myself anyway.

This seems like the best solution so far, and what I'll probably go with.

One last thing, with the regard to the name -- do you think ParTcl would run on a [Particle](https://www.sparkfun.com/products/13774)?
