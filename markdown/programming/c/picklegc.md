Title: Yet Another Garbage Collector
Date: 2023-05-18
Series: pickle

Yet again I find myself writing a garbage collector.

I did a little work on PICKLE's Javascript implementation, and perhaps Javascript is not the right choice. Because Javascript's inheritance model is *so similar* to PICKLE's, yet slightly different, implementing the inheritance (even with ES6 [`:::js Proxy`][proxy]s) is difficult.

[proxy]: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Proxy

So now I find myself writing another garbage collector, in C, with the intention of writing PICKLE in C, using that garbage collector.

This time, however, I'm not going to let it get out of hand in one big file. I'm separating the key components into their own separate files. Because the garbage collector is the base for something, I've put it in its own repository. It's called "[Tinobsy]" (TINy OBject SYstem) because I couldn't think of any better thing to call it.

[Tinobsy]: https://github.com/dragoncoder047/tinobsy/

While I initially complained about the verbosity of reference-counting garbage collectors, C preprocessor macros can help with that. To simplify the updates that need to occur when a new value is assigned, I created this macro to replace the assignment operator:

```c
#define SET(x, y) do { \
    tincref(y); \
    tdecref(x); \
    (x)=(y);
} while (0)
```

This takes care of the overhead needed to update reference counts when a value is reassigned. The old value that is being overwritten loses a reference, the new value gains a reference, and then the C pointer is actually updated. The `:::c tincref()` must come first to prevent an object from reaching zero references and being freed in the pathological case of an object being assigned to itself. The only caveat with this macro is it evaluates each of its arguments twice, so it can't be used with compound statements that have side-effects (such as a function call).

Once I got that figured out, I was able to write this bit:

```c
ttype cons_type = {"cons", OBJECT, OBJECT};
tobject* cons(tvm* vm, tobject* x, tobject* y) {
    tobject* cell = talloc(vm, &cons_type);
    SET(cell->car, x);
    SET(cell->cdr, y);
    return cell;
}

#define PUSH(vm, x, y) do { \
    tobject* cell__ = cons((vm), (x), (y)); /* Create an object */\
    SET(y,cell__); /* Do something with the object */\
    tdecref(cell__); /* Done with it, clean up references */\
} while (0)
```

This bit, while it isn't part of Tinobsy proper, is probably going to end up in PICKLE -- I figure I'm going to use some sort of Lisp-like object structure and cons cells are the basis of it.

The `PUSH` macro shows the general method of memory management in Tinobsy: allocate some memory, use it, and then drop references to it so it can be freed as soon as possible.

I included `:::c longjmp()`-based control flow capabilities in Tinobsy, but as of right now I haven't written any macros that utilize it yet. I'm modeling it after uLisp's error handling, simply returning a value when there isn't an error, and `:::c longjmp()`'ing back out to the last saved catchpoint (with `:::c setjmp()`) when there is an error.

I'm not sure how returning the actual error object will occur, as `:::c setjmp()` returns an `:::c int`, not a pointer. It would be much easier to pass back a pointer to an object in a cross-platform manner, but casting the `:::c int` to a pointer type is only guaranteed to work on 32-bit platforms because `:::c int`s are 32 bits. Oh well. I'll think of something smart eventually. And PICKLE *will* get implemented, in some form or fashion, at some point.
