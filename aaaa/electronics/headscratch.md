Title: Scartching My Head Again
Date: 2022-10-19
Series: arduino-scripting

Again I find myself scratching my head over a simple scripting language. [Yisp](https://github.com/dragoncoder047/yisp) got way too complicated; [tinyTcl](https://github.com/dragoncoder047/tinytcl) leaked memory; and [MicroPython](https://micropython.org) can't be extended with custom functions. All I want to do is have a scripting engine for my ESP32 that can run scripts off an SD card!! Argh!! Obviously, I can't think like a C programmer should.

I can't ignore the previous experience that I had with those two languages (minus MicroPython, of course, I never even tried). I learned how to make a dynamically typed object; I learned how to parse the source code recursively; I learned how to do tail-call optimization; I learned how to use a linked list; and I learned how a mark-and-sweep garbage collector works. And my experience writing [Phoo](https://github.com/phoo-lang/phoo) should help with making a concatenative language as well.

## Lisp-like languages

Yisp (at least the part that I implemented), as well as any Lisp, represent all objects as `cons` cells. The first implementation I encountered, David Johnson-Davies' [uLisp](http://www.ulisp.com), packed each cell into 64 bits. The top 32 bits are a pointer to the `car` cell, and the bottom 32 point to the `cdr`. Now, of course, not everything in Lisp is a cons cell -- there are numbers, symbols, strings, characters, arrays, etc. And all of the objects must have some place to mark them for the garbage collector.

uLisp takes advantage of the fact that a valid pointer will always be aligned to even byte boundaries, so the low bit will always be 0. This is set as the "mark bit" for the garbage collector. The other types are identified by a specific low pointer in the `car` half, which would normally point to an invalid address. For example, a `SYMBOL` contains `:::c 0x00000002` for the `car` pointer, an `INTEGER` contains `:::c 0x00000006`, and  a `STRING` contains `:::c 0x00000100`, for example. Structures that can't be represented as one single cell (i.e. strings, arrays, long symbols) are represented as a chunk of the value in one field and a pointer to the next chunk in the other field.

uLisp's memory allocation scheme is a little weird, admittedly. uLisp begins by statically allocating a huge (~10,000 item) array of empty cells, and then running up from the far end, setting the pointers of each cell to make a large linked list containg all of the free cells; this is called the `Freelist`. When a new object is needed the pointer to the `Freelist` is updated to the second cell in the `Freelist`, and the first one is returned to be used. During the sweep phase of grabage collection, the `Freelist` is simply re-constructed using the unmarked cells -- and at the beginning, everything's unmarked, so this is effectively the same action. It skips over the marked cells.

uLisp -- unline other Lisps -- also implements tail-call optimization, which saves an entry on the call stack when a function ends by immediately returning the call of another function. The way this is done is any forms which do an "implicit `:::lisp progn`", instead of evalutating the last statement in the `:::lisp progn`, they simply return it unevaluated, and then signal to `:::lisp eval` that the returned form should be evaluated again. For example, consider the factorial function:

```lisp
(defun factorial (x) (if (< 0 x) 1 (factorial (1- x))))
```

`:::lisp if` supports tail-recursion, and so does the "implicit `:::lisp progn`" performed by the function body. Normally, if the stack limit was X, trying to get the factorial of anything greater than X would overflow the stack. The way `:::lisp if` eliminates that looks like this:

Without tail recursion:

```txt
eval(factorial(5))
                  --calls-->
                            if_function()
                                         --calls-->
                                                   eval(factorial(4))
                                                                     --> and so on until the stack overflows

```

With tail recursion:

```txt
eval(factorial(5))
                  --calls-->
                            if_function()
                  <--returns next call to factorial(4)--
eval(factorial(4))
                  --calls-->
                            if_function()
                  <--returns next call to factorial(3)--
--> and so on, the stack never needing more than 1 entry
```

The neat part about this is the compiler doesn't need to "guess" when tail recursion will happen. Because tail-call optimization applies *only when a function ends by immediately returning the call of another function*, when it evaluates a block of code, it can evaluate everything *except* the last line, and instead return the last line to be evaluated *after* the C call frame is removed from the stack. Neato!

## Tcl

Tcl's mantra is "Everything Is A String." Each line (terminated by a newline or semicolon) is one command, and the line is split. Then the procedure named by the first token is called with the rest of the tokens as arguments. Consider how the `if-else` statement works in Tcl:

```tcl
if {condition} {
    # true code here
} else {
    # false code here
}
```

This isn't some special compiler construct; becuase the braces trigger the tokenizer to group everything inside of it as one literal (escaped) string, Tcl treats that snippet as *one line*. When the `:::tcl if` procedure is called, it `:::tcl eval`'s the condition, and if it is true, it `:::tcl eval`'s the true block, otherwise it `:::tcl eval`'s the false block. In Tcl, valid code is represented no differently than a raw string.

The tiny implementation of Tcl I found -- [Serge Zaitsev's ParTcl](https://github.com/zserge/partcl) -- takes the Everything Is A String mantra to the extreme, `:::c sprintf()`'ing numbers back to strings after arithmetic is done on them and (in my opinion) wasting precious memory. It stores *everything* -- strings, commands, numbers, lists, you name it -- as C `:::c char*` strings delimited in the same way as commands, and to access an item of a list, it `:::c malloc()`'s enough memory and then *copies* the chunk of that string representing the requested item into a new string. When you're done with it, you can `:::c free()` the string withut having to worry about corrupting where you got it from. (I did; perhaps that's why my extensions have memory leaks.)

The memory management strategy of ParTcl could probably be called the "No-GC" approach to GC: instead of having one object with multiple pointers to it, you have multiple identical objects that each only ever have one pointer to them (i.e. the C variable). Because each object is only ever pointed to in one place, and the VM knows what it's doing with each object and when it's done with them, it also knows when to `:::c free()` each object. This, unfortunately, means that objects are inherently immutable, and wastes memory making copies of objects. 

ParTcl's approach to variables, however, looks a lot like ... drumroll please ... Lisp! The ParTcl VM maintains a pointer to a linked list of all the global variables, and each variable cell contains a pointer to the next variable cell, its name (a string), and its value (another string). The `:::tcl set` command mutates these pointers.

Tcl also has an interesting approach to return values. Each procedure, instead of returning a value, instead sets it on the Tcl VM's `result` field, and returns instead one of the standard Tcl "return codes" which are numbers, not strings -- one of `TCL_OK` for a normal call, `TCL_ERROR` if something went wrong (and then the `result` field is an error message), `TCL_RETURN` which is returned by the `:::tcl return` command to signal that a procedure is returning and subsequent commands should be skipped, and `TCL_BREAK` / `TCL_AGAIN` which are returned by the `:::tcl break` and `:::tcl continue` commands to signal to loops that the appropriate action should be taken.

## Other Thoughts

In trying to find more information about a scripting language for Arduino I discovered several helpful resources pertaining to building a scripting language itself (which is what I'll have to do if I can't find anything suitable).

First up is Bob Nystrom's blog post ["Baby's First Garbage Collector"](http://journal.stuffwithstuff.com/2013/12/08/babys-first-garbage-collector/) and [its code](https://github.com/munificent/mark-sweep/).

I'll note here that while I was playing around with uLisp, I came up with an idea of how to eliminate the need for a huge statically allocated array that you have to play around with the size of until it fills *just enough* RAM but not *too much*. The idea I came up with was the reverse of the `Freelist` idea: a `Usedlist` of sorts, where whenever an object is allocated, another "shadow" object is allocated alongside it and linked into the `Usedlist` to be able to point to the object that was allocated. The downside of this scheme is it uses double the memory (one cell for the object, another cell for the `Usedlist` entry).

Bob's garbage collector takes pretty much same approach to garbage collection as uLisp -- in that you maintain a list of "all objects" (using the large array, or a `Usedlist`), recursively mark everything, and then free the unmarked objects. Bob's collector differs from uLisp in that the "all objects" list is formed by the objects themselves: as well as slots to hold the `car` and `cdr` pointers (or whatever else data they need to store) there is another slot, hidden from the end-user, that always points to the previous object that was allocated. That way, the garbage collector can run through these pointers, ignoring all the data in the rest of the object, and when it gets to an unmarked object, splice it out of the list and `:::c free()` it. The disadvantage is objects take up more memory, running the risk the objects won't be an even multiple of four bytes, and so `:::c malloc()` will leave "holes" in the heap and waste memory.

The next thing is a technique known as **NaN-boxing**.

Most computers represent floating-point numbers (i.e. non-integers) according to the IEEE 754 standard. The 64 bits of a C `:::c double` are split into 1 sign bit, 11 exponent bits, and 52 fraction bits. When you divide by zero (or any other operation that would result in a mathematically undefined value) the operation returns (in hexadecimal) `:::c 0xFFF8000000000000`. But only the top 13 bits (`:::c 0xFFF8...`) must be set to make it a NaN value, so the other 51 can be used for anything you like -- storing a pointer, an integer, a singleton ID, etc. And, of course, doubles.

[Viktor S&ouml;derqvist's `nanbox` library](https://github.com/zuiderkwast/nanbox/) implements most of this bit-fiddling, so I may not have to  do it all myself. The downside of NaN-boxing is that in the 51-bit "payload" you can only store one pointer, so I can't implement two-pointer cons cells, or two-number complex values, or anything that requires more than 52 bits.

I'm not sure what I'm going to do with this all. Maybe I will write another scripting language. Maybe I'll find one. One of those two!
