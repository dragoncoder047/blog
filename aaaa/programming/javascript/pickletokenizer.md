Title: Pickle Tokenizer
Date: 2023-04-20
Modified: 2023-04-21

I'm starting to work on my Pickle programming language, this time in Javascript. After only a few days' work, I'm surprised I got so much working. Currently I have both the tokenizer and the inheritance system working. The syntax of Pickle is pretty much in place now, and I just have a few tweaks left for the tokenizer, and hooking it up to a parser, before I am able to write the evaluator.

## Tokenizer

In contrast to my previous attempt in C, I actually wrote a tokenizer. But in all honesty, the tokenizer really does 90% of the parsing -- it just doesn't recursively build up a tree of expressions using the parens (that will be done by the parser).

I got the tokenizer working in a little demo page I dubbed the "seeder" for some reason. Currently it is able to tokenize this code

```pickle
defun fib(x):
    if $x == 0 or $x == 1:
        return 1
    else:
        return (fib $x - 1) + (fib $x - 2)
print (fib 10)
```

into this stream or tokens:

```txt
[1:1 - 1:6]	symbol 	"defun"	
[1:7 - 1:11]	symbol 	"fib"	
[1:11 - 1:12]	paren 	"("	
[1:12 - 1:13]	symbol 	"x"	
[1:13 - 1:14]	paren 	")"	
[1:14 - 6:1]	string (block)	"if $x == 0 or $x == 1:\n    return 1\nelse:\n    return (fib $x - 1) + (fib $x - 2)"	
[6:1 - 6:6]	symbol 	"print"	
[6:7 - 6:8]	paren 	"("	
[6:8 - 6:12]	symbol 	"fib"	
[6:13 - 6:15]	number (integer)	"10"	
[6:15 - 6:16]	paren 	")"	
```

The tokenizer is also a bit unique in that it can recover from a syntax error and keep scanning, allowing you to see and fix multiple syntax errors all at once. And it's also nice that the [Ace.js](https://ace.c9.io) code editor allows you to place annotation markers in the gutter, which is what I did in the "seeder".

The only bug I can see here with this example is that the colon-block string part consumes the newline at the end of the block, so the `print` is considered to be on the same logical line, but it shouldn't be. A simple `;` before the `print` would fix that, but I feel that this kind of indented block structure where an unindent ends both the block and the line, would be more common than having the string continue the line -- in other words, having the default be to continue it and adding punctuation to end it would result in more "punctuation overload" versus having a special punctuation character mean continue the line and the default be to end it. Unfortunately, the former appears to be whet is implemented in the Javascript tokenizer.

## Inheritance

In [my earlier post about Pickle]({filename}../c/pickles.md), I mentioned that Pickle would have a multiprototype-based inheritance system, a strange mix of Python and Javascript. Python supports multiple inheritance, but chokes on "ambiguous" inheritance trees, while Javascript only supports single inheritance through prototypes. But I think I've found a simple solution that implements multiprototype-based inheritance. Here's a pared-down example:

```js
class PickleObject {
    constructor(name, ...prototypes) {
        this.name = name;
        this.prototypes = prototypes;
    }
    toJSON() {
        return this.name;
    }
    getMRO() {
        var fun = x => [x].concat(x.prototypes.map(fun));
        return fun(this).flat(Infinity);
    }
}

var A = new PickleObject("A");
var B = new PickleObject("B");
var X = new PickleObject("X", A, B);
var Y = new PickleObject("Y", B, A);
var Crash = new PickleObject("Crash", X, Y);
alert(JSON.stringify(Crash.getMRO()));
// -> ["Crash","X","A","B","Y","B","A"]
```

This is exactly the same code that I posted earlier that Python can't handle -- but here, `:::js Crash.getMRO()` simply returns a flat array that can be searched linearly. I'm not sure how fast this is, but I do have some optimization tricks that I could apply.

## What's next?

I don't know exactly what, but Pickle is still only half-written. After I write the parser, I'll need to then write the evaluator. And the evaluator is going to be extremely complicated and probably very slow, although I do hope it will be somewhat readable due to Javascript's built-in functional programming constructs that C doesn't have natively.

Pickle does look like it's going to be simpler than Phoo, certainly. Although Phoo did get complicated because I split everything into a zillion different files. One huge file for everything may be a bit much, but having a bazillion files and none have any more than 100 lines apiece is also a bit much. Aside from the weird operator semantics, I do hope Pickle's flow will be easier to follow.
