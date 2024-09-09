Title: I Still Have No Idea
Date: 2022-12-16
Tags: programming, phoo, javascript

I was working yesterday on trying to root out the bug in Phoo's online shell; but I never found it.

Currently Phoo works-ish; except that in the online shell, the error behavior is backwards:

* Case A: When you give a bad input (that would crash), it prints no error message.
* Case B: When you give a good input (does not error), it suffers a fatal crash and exits from the REPL and you are forced to reload the page.

That's totally backwards; and I cannot for the life of me figure out where the bug is. A simple workaround is to append `asdf` (or some other undefined word) to every input to trigger case A and keep it from exiting. The only downside to this is that if there actually was a bug in your code and it aborted before it got to the `asdf`, all you'll be left with is a pile of junk on the stack with no way of concretely knowing what went wrong.

It is compounded by the fact that Phoo is currently a royal pain in the you-know-where to debug. The only useful thing I can do in the browser devtools is set a breakpoint on `Thread.tick()` and step tediously through each and every non-Javascript word's definition (even stupid simple ones, like `:::phoo swap` and `:::phoo times`, that I know work). There's no "step over" for Phoo words; you just have to open up `:::js this` (which is the `Thread`), note the original return stack depth, and then spam the Javascript "step over" button until the return stack returns to the depth noted. This is what the Javascript debugger is already doing with the Javascript return stack; but since Phoo's return stack is not coupled to the Javascript debugger, it can't use it in this manner.

I've traced the bug down to somewhere in `:::phoo try` / `:::phoo except`, where it is not properly managing the return value or error value, corrupting the stack. However, it could be in `:::phoo ]sandbox[` or `:::phoo await` for all I know, which are also used by the shell to catch errors, because the "crash" on good code is always caused by a `:::phoo drop` when there are no items on the stack (specifically, [here](https://github.com/phoo-lang/phoo-lang.github.io/blob/dcb368e34524a9742f125960ecd2193f2b7a2cc7/app/shell.ph#L120)). I also think it is in here because the shell broke right after I refactored `:::phoo try` to only catch the error, and added `:::phoo except` to handle it.

I should probably write a Phoo debugger. Even if it doesn't help me, it will probably help anyone else who wants to write anything in Phoo. Anyone else want a debugger?
