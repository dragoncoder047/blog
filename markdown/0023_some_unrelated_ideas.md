Title: Some Unrelated Ideas
Date: 2022-10-26
Series: arduino-scripting
Tags: programming, c

Immediately after I wrote the last post I stumbled upon the [Cognate programming language](https://github.com/cognate-lang/cognate). It is sort of a weird cross between Forth, Lisp, and Tcl, all at once, and I strangely like it. Currently Cognate is only implemented by a Cognate-to-C transpiler, so I won't be able to run it directly on a microcontroller (although a pure interpreter [is in the works](https://github.com/cognate-lang/cognate/issues/18#issuecomment-1282710633)).

I have some ideas on how to improve it. I [proposed a few](https://github.com/StavromulaBeta/cognate-rewrite/issues/1), and I'll see what happens.

Cognate is notable because it is a concatenative programming language, but it doesn't read like any other concatenative programming language that I know of. Instead of using postfix (reverse Polish) notation used in Forth and my other programming language Phoo, Cognate uses prefix. However, it is in no way like Lisp in that functions can take as many arguments as you give them. The `+` function, for example, still takes 2 arguments, and so if you want to add 3, 4, and 5, it is simply the reverse of what Forth would look like (`:::forth 3 4 5 + +`): in Cognate you write `+ + 3 4 5`.

Functions in Cognate are defined with a parser macro called `Def` (and yes, it must be capitalized; I'll explain that later). `Def` expects a symbol on the stack and a lambda under it, and sets the symbol to be that function. However, you don't write it `(<code>) \Foo Def`; that's posifix; you write `Def Foo (<code>)`. (Also, you don't need the slash to make it a literal symbol, the parser automatically handles that when it comes right after `Def`.)

The other interesting thing about Cognate is its use of "informal syntax." Every word in Cognate that is meant to be treated as an actual instruction must be capitalized or start with punctuation; otherwise it is treated as a comment and completely ignored. For example, you can write `For each in Range 1 to 10 (+) from 0` to get the sum of all numbers 1 to 10, and all Cognate will see is `For Range 1 10 (+) 0` -- but the rest of the words that are ignored make the program a heck of a lot easier to understand what it does.

Because of the way Cognate is implemented (a Cognate-to-C transpiler) it's a bit hard to understand what exactly is going on in the parser (I figured out that Cognate pre-executes some of the stack shuffle operations, `Twin`, `Swap`, and `Drop`, in the complier, and only when needed at runtime) and how to actually generalize some of the parser constructs into any kind of macros that a microcontroller would be able to differentiate and skip evaluation early. I'll have to think about it a bit. Perhaps I'll come up with a completely new language!
