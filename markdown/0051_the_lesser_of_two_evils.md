Title: The Lesser of Two Evils
Date: 2024-02-12
Series: pickle
Tags: programming, language-design, c

I've been trying to write some of the code to implement PICKLE's parser and evaluator -- it's not going well. The hard part is that *everything* in PICKLE is done using continuation-passing style. Everywhere the evaluator has a chance of calling user code (that may capture a continuation), it has to interrupt its own execution and package everything up into a continuation that will resume the process with whatever the user's code completes with. The result? Turns out, [callback hell][] in C++, or at least something like it, is possible. Just look at this mess:

[callback hell]: http://callbackhell.com/

```cpp
// do next is run body --> cont=apply match cont-> eval again -> original eval cont
vm->do_later(vm->make_partial(
    NULL,//matched_pattern->body(),
    NULL,
    env,
    vm->make_partial(
        vm->wrap_func(funcs::splice_match),
        vm->list(2, vm->append(ast, NULL), NULL/*matched_pattern->match_info()*/),
        oldenv,
        vm->make_partial(
            vm->wrap_func(funcs::eval),
            NULL,
            oldenv,
            cont,
            fail_cont
        ),
        fail_cont
    ),
    fail_cont
));
```

Yow --- that's a tad hard to see what's going on. These 20-odd lines of code implement only one thing in PICKLE's evaluation algorithm: "after finding a matched pattern, apply the match, and then go back to step 1 if there are more matches." It also exhibits symptoms of being spaghetti code -- the evaluation function calls out (indirectly) to the match-splicing function. However, this is the only place it is used. Why didn't I try to inline it? Because it would add more layers of nesting.

The whole reason this nesting is necessary anyway is that each little sub-step might trigger the execution of user code --- and so a continuation must be made. After finding the match, the match-splicing function must first call the user's definition of the pattern (necessarily in continuation-passing style). Then the "go back to step 1" part is implemented by calling `eval` again, naturally in continuation-passing style.

I really hate callback hell (or whatever you want to call this), especially because it is supposed to implement a simple, linear algorithm. It should all be at the same indentation level!

## Byte(ish)code to the rescue

So far, PICKLE has been the pattern-matching equivalent of a tree-walking interpreter. It recursively applies patterns until it reaches an atomic operation, and then the call stack -- which is really a chain of partial continuations allocated on the heap -- unwinds to return and allow the next pattern to match. These chains of continuations are created on-the-fly by the "callback hell" spaghetti code I have written so far.

There's one thing that I noticed while designing PICKLE: every major programming language that claims to be "interpreted" is still actually compiled -- just not into machine code like fully compiled languages are (unless it's got a JIT). They are compiled into bytecode, and then the bytecode is run in a virtual machine, which is usually either a stack machine or a register machine. I don't know much about bytecode, so I don't have a very good idea of how I could use it.

In terms of re-implementing PICKLE as a bytecode virtual machine, I have a few ideas, which may or may not work.

Looking at what's going on in term of the continuation chain, it isn't actually a chain. It's a tree -- each operation is able to trigger one of two continuations, one for when the operation succeeds, and one for when the operation fails. I recently learned that this practice of passing two continuations around is known as ["double-barreled" continuations][kseo], and, well, I'm not surprised that it's been named -- I didn't even think of it myself. I got it from SISC.

[kseo]: https://kseo.github.io/posts/2017-01-10-double-barrelled-continuation-passing-style-interpreter.html

Perhaps the one way to simplify this is to go the stack machine approach. Phoo, my previous attempt at a programming language, was a stack machine. [After Phoo imploded][phooey] I've had a bad taste in my mouth for stack-based stuff, but there must be a reason that other languages use them for their bytecode machines.

[phooey]: {filename}0038_phooey_phooey_phooey.md

## Instruction *stack*??

My first idea is to flatten the tree of continuations into a list, and then separate the "temporary state" saved in the continuations into a work stack of data values. The continuations' associated functions would be the bytecode instructions which would then push and pop form the stack.

When a compound instruction, that needs to call user code, is executed, it does what it can, then it pushes the remainder of the instructions of the compound operation to the instruction stack, so they'll be executed after the user code returns. Then the user code is pushed to the stack so it will be executed -- and the result of the user code is seamlessly inserted onto the stack for the remainder of the operations to use.

The differentaition between the normal success continuation and the failure continuation, and how to even switch continuations (when applying the captured one from a `:::scheme call/cc` construct), is actually kind of simple in this system. The solution I came up with is a little hokey, but it seems like it would work.

Each instruction in the instruction queue is "tagged" to indicate what type of operation it is. Each atomic operation returns a value to indicate which type of continuation to search for next. For example, if the instruction failed, it can push an error to the value stack instead of its typical return value, and the return "error" to the PICKLE virtual machine, to signal that it should discard all instructions from the instruction stack until it gets to an error handler instruction. [Tcl does something similar][tcl], by returning different "codes" along with the actual value.

[tcl]: https://www.tcl-lang.org/man/tcl/TclCmd/return.htm#M5

Here's an example. Let's evaluate the (hypothetical) expression `:::pickle print try 5/x rescue NaN`. Conceptually, what should happen is it should look up x, divide 5 by its value, and print that, except if the division throws an error (if it is 0 or NaN), and in that case just print NaN. I'm going to simplify the instructions, and skip steps along the way, but hopefully this should convey what I'm thinking.

To start everything `:::pickle eval` is called -- like so:

```txt
instructions: call
data: ((print try 5/x rescue NaN)) eval
```

The `:::pickle call` instruction simply launches into the evaluation process and begins matching patterns. Now the `:::pickle try ... rescue ...` pattern matches inside the `:::pickle print` expression, and begins with the following instructions and data. It might look like a lot, but all it does is evaluate the current expression's instructions, and then the last three instructions implement the "splice in the result, and go back to step 1" part.

```txt
instructions: call (error ('<continuation> call)) cons call call
data: ((5/x)) eval (<spliceinfo> (print ...)) splice eval
```

The `call` instruction calls the function with its arguments above it, and so the expression `:::pickle 5/x` is evaluated. `:::pickle eval` matches the variable lookup pattern first, and sets up instructions to apply that and return to evaluation:

```txt
instructions: getattribute cons call call (error ('<continuation> call)) cons call call
data: x <env> (<spliceinfo> (5/...)) splice eval (<spliceinfo> (print ...)) splice eval
```

The `getattribute` instruction takes two things from the stack (a symbol and an object) and looks up the attribute on the object -- in this case the object is the environment itself, so the value of the variable x is returned. The three instructions under that are identical to the first time `:::pickle eval` was called -- except this time they are nested two deep because two patterns have matched inside each other.

Suppose x is 0. At the moment the division occurs, the state is this:

```txt
instructions: divide cons call call (error ('<continuation> call)) cons call call
data: 0 5 (<spliceinfo> (...)) splice eval (<spliceinfo> (print ...)) splice eval
```

Because you can't divide by 0, `divide` fails. An error gets pushed to the stack, and now the PICKLE machine does something different: it skips ahead until it gets to an `error` instruction group -- in this case, the instruction is to apply a continuation. Now what?

## It's *literally* just stack switching

Recall that a continuation is simply a chunk of data that when applied, causes a jump to a different point in the program. How is that done in this PICKLE machine? By switching stacks. The continuation, internally, holds what the instruction stack and data stack were at the time it was captured -- or, rather, what they should be swapped out with when the continuation is invoked. In the case of the error handler discussed above, applying the continuation replaces the remaining instructions of the body with the instructions of the error handler, and replaces all the data *except* for what it is called with (in this case the error object), which is what is "passed" to the continuation.

```txt
instructions: ignore 'NaN cons call call
data: <error> (<spliceinfo> (print ...)) splice eval
```

The `ignore` instruction discards the error (the handler doesn't use it), and then the default value (NaN) is pushed to the stack. Fantastic! The remaining instructions splice this value back into the `print` expression, which prints whatever it is passed. Then the program exits because its instruction stack is empty.

## Look Mom, I have *N*-barrel continuations now!

Now an implementation of continuations wouldn't be complete without thought about context managers. Suppose you are writing a library. One of the library functions allows the end-user to pass in a callback, and it calls the callback while some managed resource is in use. In something like Python, that isn't a problem. If the user function raises an error, you can catch the error, close the resource, and then re-raise the error. Once you return from the library function and close the resource, you can be sure it will never be opened again without running the initialization routines.

Continuations throw a monkey wrench in all of that. Suppose the user's callback captures a continuation and then returns. The library function closes the resource like usual, and then the user's program decides to invoke the continuation, jumping back into the middle of the data-processing section of the library function, without running the initialization section. Suddenly the program finds itself trying to operate on a closed resource, and bad stuff starts happening.

The solution is what the Scheme community calls `:::scheme dynamic-wind` -- a construct that traps continuations and forces entrance and exit handlers to run before the jump is made. After control flow exits a `:::scheme dynamic-wind` (via normal returning or a continuation), the exit handler runs. Before control flow enters, the entrance handler runs. These two handlers can be used to open and close the managed resource, preventing invalid read states.

And to implement them, PICKLE is going to need a new kind of bytecode instruction. A `:::scheme dynamic-wind` block will leave "cookies" on the instruction stack, in the form of enter- and exit-type instructions, that are picked up by continuations when they are invoked. All exit handlers that the continuation would displace are run in the appropriate order, and then all of the entrance handlers are run in the appropriate order, and *then* the continuation's control is resumed. Problem solved.

## No bytes here

After I came up with this idea for continuations, the next thing I immediately thought of was how could I use it? The insane power of first-class continuations allows a lot of things to be done -- my initial idea was to use this in a robot, and when the robot "goes to sleep," it could capture a continuation which saves the entire program state, and then serialize the continuation to permanent memory. Then the robot could safely shut down completely, and when it wakes up it just resumes the continuation it saved, and the program continues on as though nothing ever happened.

After thinking of that, I got another idea: the continuation could be serialized and then *sent to another computer* and resumed on that computer. Wouldn't that be cool? Something like this could probably be used to make a multiplayer turn-based game, where you take your turn, then freeze the game's program and send the program state to your opponent. They unfreeze the game on their machine, play their turn, and send the updated state back to you. They don't even need to have downloaded their own copy of the game, because the entire game state will contain the game's code with it.[^1]

[^1]:  On second thought, this may be of little practical use. For a complicated game with lost of code, it would involve sending large game-state files back and forth.

Serializing the continuation would be an important part of implementing this. I explored a couple of different methods to serialize state like this, and the hard part to serialize was the C function pointers. The internal representation of core C++ functions includes the address of the function pointer so it can call the function -- but I can't guarantee that the address will be the same on every system. If the address was sent as-is, the receiving machine would assume it's still a valid function pointer, and then try to call it, but the function pointer may not point to anything useful, and would probably cause a segmentation fault.

So I came up with the idea of "named functions" -- simply put, all of the C function instructions that go on the instruction stack, must be named with a symbol. The symbol would be associated with the C function using a hash-map, and then when the program state is serialized the *symbol* would be saved as the function, bot the function itself.

So it turns out, all of the internal data is just Lisp structures. Maybe I don't even have to worry about making another garbage collector and using Tinobsy -- I could just use uLisp's and rewrite `read()` and `eval()`. Or maybe I do need to rewrite it. I'll see what happens!
