Title: Continuations and the thunk queue
Date: 2023-09-21
Series: pickle
Tags: programming, c, javascript, language-design

After I made the last post -- where I decided that PICKLE would be done in continuation-passing style -- I revisted one extremely simple toy programming language done in continuation-passing style I found online ([here](https://curiosity-driven.org/continuations#interpreter)). I figured it would be a good example of how I could implement PICKLE. The only problem is the interpreter makes heavy use of closures -- so heavy that I almost couldn't understand it.

Closures, however, were a smart choice, at least in terms of being particularly low-hanging fruit in the Javascript sense. The "current continuation", generally speaking, is just an object that contains some information on what computations need to be done after the current one completes (and passes its result to the continuation). A closure here would hold the code needed to perform the next action, and also close over the data (i.e. the abstract syntax tree being executed) representing the *real* program. While C++ doesn't have any (useful) closures per se, I already have garbage-collected objects, and closures and objects are [somewhat equivalent](https://wiki.c2.com/?ClosuresAndObjectsAreEquivalent).

The one part of the little language that really caught my eye was the [trampoline](https://en.wikipedia.org/wiki/Trampoline_(computing)#High-level_programming). For a language that supports tail call elimination such as Scheme or C, continuations blowing up the call stack aren't really a concern. But until Javascript supports tail-call elimination, calling a continuation will continuously add call frames to the stack, guaranteeing a recursion error if the stack gets too large.

The trampoline solves this by delaying the actual application of the continuation function. It bundles the function and arguments into a thunk, and then adds the thunk to a queue. The trampoline returns normally (continuations usually never return) causing the call stack to unwind. *Then* the trampoline calls the thunk. The thunk just ends up calling what it thinks is a continuation, but it's really the trampoline, and so the process ends up repeating (wrap continuation, call current thunk, get next thunk in queue, unwind stack) until the final continuation doesn't push any thunk and the queue is empty. The program could even implement an infinite loop using recursion and the stack would never grow at all because there is effectively no call stack because of the trampoline. There is a catch: while the *stack* doesn't grow at all, the individual continuations will use up more and more and more memory as they close over more and more and more call frames.

An interesting thing occurs when multiple programs are using the same trampoline. This effect can be seen by opening the page for the programming language above and scrolling down to the code block immediately above the "Simplifying web applications" header. Replace it with this and press "execute".

```js
// set up the dependencies
function noop(){}
var dependencies = lists.get() + ' ; ' + cond.get();
interpret(parse(lexer(dependencies), operators), globals, trampoline.wrap, noop);
trampoline.execute();
// set up 4 separate programs
interpret(parse(lexer('display(a); display(a); display(a); display(a)'), operators), globals, trampoline.wrap, noop);
interpret(parse(lexer('display(b); display(b); display(b); display(b)'), operators), globals, trampoline.wrap, noop);
interpret(parse(lexer('display(c); display(c); display(c); display(c)'), operators), globals, trampoline.wrap, noop);
interpret(parse(lexer('display(d); display(d); display(d); display(d)'), operators), globals, trampoline.wrap, noop);
trampoline.execute();
```

Notice that despite there being four separate programs that print the same letter every time -- the first one just prints `a`, `a`, `a`, `a` -- the output ends up having the `display` calls from all the programs *interleaved*.

And therein lies the power of the trampoline: as well as eliminating the call stack, it allows for a very simple method of threadless concurrency. PICKLE never looked so real at this point! The other amazing part is the sheer simplicity of the main evaluation loop I drafted based on this:

```cpp
void pickle::mainloop() {
    for (;;) {
        if (this->queue_head == NULL) return; // Exhausted all continuations, program is complete
        this->gc();
        this->run_next_thunk();
    }
}
```

where the `:::cpp run_next_thunk()` method simply pops the next thunk off the queue, and if it's a C++ function, calls it, and if it's a user-defined code block, puts another continuation on the queue that calls the C++ "eval" function with the code block as the argument.

The evaluation function is also dead simple: it finds the best-matching pattern using PICKLE's pattern-matching engine, and if there is a match, it creates a continuation chain to apply the match and then return to the evaluator. If there are no matches, it does nothing, and returns the eval'ed element unchanged to its own continuation.

The only downside to this is that because PICKLE technically doesn't have function calls, it just emulates them using a pattern, it means that PICKLE doesn't support tail-call elimination. When a function is in tail position, and the call-a-function pattern matches, the result is first spliced into the code, checked for patterns again, and then returned, resulting in the continuation chain growing unnecessarily.

There's probably some clever optimization I haven't found yet that will enable this. Considering my relative na&iuml;vete when it comes to pattern-matching languages, there's definitely more for me to learn.
