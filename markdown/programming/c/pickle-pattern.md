Title: Powerful PICKLE Pattern Matching
Date: 2023-07-02
Series: pickle

I did a lot of work on Tinobsy, the garbage collector for PICKLE. It's pretty robust now, and passes all my tests -- plus I translated it to C++ so I can take advantage of C++'s syntactic sugar for objects. All I think that I'll be doing with Tinobsy in the near future is maybe writing more tests. Now I am focusing more on the implementation of PICKLE itself, starting with the tokenizer.

Lexing and parsing stuff in C is considerably harder than Javascript, mostly due to the lack of regular expressions. But C does have the advantage of `:::c longjmp()`, which Javascript does not. I haven't finished writing the tokenizer/parser but it will be based off of the Javascript one pretty closely --- with a few key changes to accommodate some new ideas.

## More powerful pattern matching

I found Bob Nystrom's [Magpie] programming language a while ago and had a look at it. It didn't dawn on me the expressive power of Magpie's pattern matching until I took a closer look at their implementation explained in Bob's blog. In Magpie, the methods aren't ever attached to the objects they operate on -- while if you write `:::magpie "foo" length` it might look like you're calling a method attached to the string object, no, you're just calling a global method `:::magpie def (self is String) length`. Magpie pattern-matches the string argument and the `length` name and finds a method defined for it.

[Magpie]: https://magpie-lang.org/

Magpie even has -- you guessed it -- user-definable infix operators. And also being able to extend the Magpie parser. And a lot of other stuff, apparently, that I already thought of but just didn't know existed in another language. The unfortunate part is that Magpie is implemented in C# and Java, neither of which run on a microcontroller, which is one of the goals of PICKLE.

The idea I have come up with here is rather simple: there would be a function called something generic like `define` that would take a precedence, a pattern, and a code block, find a pattern variable named "@", and insert the pattern into the pattern lookup table of the class named by `@`. For example, here's some hypothetical code:

```pickle
define 3 [arg] |> [Callable @]:
    $@ $arg
```

The result of that code would be to define that applying the operator `|>` to an object that inherits from `Callable` (usually functions and stuff) with another object on the right of it is semantically equivalent to calling the callable object with the other as its sole argument (i.e. `:::pickle $foo $bar` can now be written as `:::pickle $bar |> $foo`), and the pattern has a precedence of 3. Infinitely many more syntaxes and operators are possible with just a few lines --- and it's not just limited to simple infix operators like this.

## Simplified parsing

In the [previous post about PICKLE]({filename}spoiled-pickles.md) I mentioned that unary operators would be applied first, then binary (infix) operators. The only problem with this arises when you throw whitespace into the mix: for example, consider a simple addition of two variables -- you could write it with whitespace, or without. In the old Javascript parser they would produce different sequences of tokens:

```pickle
## With space --> "$" "x" "+" "$" "y"
$x + $y
## No space   --> "$" "x" "+$" "y"
$x+$y
```

Note that without the whitespace, the `+` and `$` in the second line got unintentionally concatenated into the same symbol. This would not produce the intended behavior (look up `x`, look up `y`, add) -- it would instead look up `x` successfully, but then try to apply the value of `x` to the symbol `y` using the `+$` operator, which likely isn't defined.

I considered adding another parsing rule I called the "unary split rule" that defined that if a symbol ended with a prefix operator, or started with a postfix operator, the symbol would be "split" to apply the unary operator, which would solve the above problem.

However, I soon came up with a much simpler solution, with only **two rules** for the parser:

1. Whitespace *is* significant.
2. Symbols (operators, numbers, variable names, etc) are concatenated at runtime, not by the parser.

Rule 1 makes the most of a difference as it completely fixes the operator problem above. Combined with rule 2, it also enables the creation, at runtime, of any kind of syntactic literal.

Consider the expression `:::pickle $x / 2+3j`. With only rule 2 in play, the tokenizer effectively strips the whitespace and it results in the expression `:::pickle $x/2+3j`. The runtime engine can't tell that you intended to divide `x` by a complex number constant, and because division comes before addition, what it ends up doing is dividing `x` by 2 first and then adding an imaginary constant, not what was intended.

Making whitespace significant enables expressions with no whitespace to have a higher precedence (if so specified), so that `:::pickle 2+3j` can be made into a complex number *before* the division occurs.

Rule 2 would be augmented by a series of concatenation patterns, which govern how numbers and symbols "parse themselves." For example, if you write two numeric digits with no whitespace separating them, they would be concatenated into one number equal to the second digit plus ten times the first. There would also be rules for concatenation of symbols into variable names and operator symbols into operators. Nifty, huh?

## ETA, anyone?

I know PICKLE is still vaporware at this point. I haven't even finished the tokenizer yet. But half of the work has already been done in working towards having a working programming language -- it just needs to be implemented as computer-readable code.

Perhaps in the future there will be an AI program that will be able to read descriptions like this and produce working code off of it. It would be an interesting experiment to see if it ends up producing the same code as me.

Until then, you're just going to have to wait.
