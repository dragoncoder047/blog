Title: The God Language
Date: 2023-12-21
Tags: programming, language-design, rant

I did a lot. In the two months since I last shared something I've worked on no less than four different projects, all while trying to slip them in between an avalance of schoolwork and college applications. Oh, and I also spent a week sick with COVID-19. (It's real, people!)

I left off with some decisions about a **Python** interactive-fiction engine I'm working on. Originally I had written it to use a **JSON DSL** that I created. I eventually abandoned that in favor of just using Python itself.

I also made some progress on another idea of mine: a virtual-reality cellular automata editor. I am writing the whole thing in **Javascript** so it can run in the browser, but user scripting is accomplished by writing code in **Scheme**. (Neither this nor the IF engine are released publicly yet.)

Recently I also fixed up the syntactic macro support in [my fork of **uLisp**][ulisp]. uLisp is writted in **C** and **C++**, but these need to be compiled -- my goal is to use uLisp as a scripting language for a microcontroller project I'm also working on. And I previously toyed around with **LIL** (a dialect of **Tcl**) for this.

In the past, I have played around with many other languages, including **Quackery**, **Phoo**, **Ruby**, **Java**, **Bash**, and **Prolog**.

Notice all the bolded words on the paragraphs above? Each of them is a different programming language. The simple fact is that there are literally *thousands* of programming languages out there, some similar, some not, each highly tailored to its specific use-case.

Part of what I have been doing in developing my programming language PICKLE is to strike a balance between all the languages I have seen so far and enable the writing of code that is easy to read, write, and think about, in the most sensible manner for the task at hand.

But at the end of the day, PICKLE is just going to be another programming language. At any rate, there will be other languages that have features that PICKLE doesn't, or some of PICKLE's limitations will get in the way, or something else will go wrong and knock PICKLE off the pedestal I carefully placed it on.

## The conundrum of computer code

Since they were invented, programming languages have been nothing more than a tool. We (humans) think in higher level steps - such as "command the robot to turn the bolt to the specified torque." However, a computer can only think in simple, atomic steps, such as "if register B is negative, go to line 42." The job of a programming language is to translate these high-level constructs into low-level machine code in order to make these incredibly stupid machines appear as though they are smart.

%%% float-left
    ```python
      File "xnum.py", line 112
        if (m = re.match(r"\d+", txt)) is not None:
            ^^^^^^^^^^^^^^^^^^^^^^^^^
    SyntaxError: invalid syntax. Maybe you meant '=='?
    ```

    %: No, that's exactly what I meant. Shut up and give my my match result!!

The inherent limitation present in all of the world's programming languages today is that they have a well-defined syntax. While that may seem like a benefit, in most cases the syntax is rather restrictive. Consider Python for an example. In version 3.8 the Python developers introduced [the `:::python3 :=` walrus operator][pep572]. This functions pretty much exactly the same as Python's existing `:::python3 =` assignment operator, except that `:::python3 =` is a statement and can't be used where the parser expects an expression, whereas `:::python3 :=` is an expression. Originally the deliberate lack of an assignment *expression* and only making it a *statement* was to prevent the common goof of writing it in the condition of an `:::python3 if` statement and clobbering the value you were trying to compare. But in some cases, this behavior is intended. What is *really* needed is an [anaphoric][] version of the if statement, but Python doesn't have one.

Common Lisp has its own share of nitpicks. The incredibly powerful [`:::lisp loop`][loop] macro is able to do pretty much anything you can do with a loop in a remarkably natural-language sounding syntax. The only downside is that as it's a finite Lisp macro, not every possible expression can be constructed with the macro's facilities alone. Everything else has to be expressed in Lisp code, which requires the expressions to be in prefix notation and enclosed in parenthesis. I know this is a bit of a contrived example, but unless you're already an experienced Lisp programmer, pages and pages of this parenthesis-heavy syntax is more than enough to make me retch.

The "God language," if there is one, wouldn't have any kind of restrictions. You would basically just be able to write what the computer should do, and the computer would either know how to do it, or it would ask you how to do a particular step. Better yet, the computer would be able to figure things out for itself using what has already been given to it.[^gpt] And ideally, the format of such a language should be such that a human reading any code written in it should be able to easily understand what that code is doing and how it is doing it. Unfortunately, no such language exists.

## Making money over making sense

Apparently, you can make money by selling software. I can't say I completely agree with it, but current copyright law allows a software developer to charge money before they provide the user with the program. And to be able to continue making money, the developer must protect their source code. If they did not, eventually some disgruntled user would post all the source code on the internet and suddenly anyone can download it, compile it, and use the program without paying the original developer. Sure, the developer could go around trying to sue everyone who downloads the pirated code, but it's a heck of a lot of effort to do that, and they can never be sure that they have gotten every last copy taken down.

Because there is this need for developers to protect their code, two things were invented. The first was almost by accident: once a compiler reduces the source down to executable machine code, the source is no longer needed for the program to run. As a result, developers often only release the executable. Even a good decompiler can't recover any of the function or variable names, and certainly not the comments -- which makes it hard to understand how the code works.

The second method is a little more devious. Javascript, the langauge of the Web, is such that you can't distribute a compiled binary[^wasm] to a Web page. You have to send the source code. Or, you can send a compressed and mangled, but equivalent, chunk of code. Not only does it does make your website load faster, but without the sourcemap it makes it difficult to follow what the code does. And you can do even more devious transformations to the code to make it even harder. Just look at [this mess of obfuscated Javascript][docs] taken out of Google Docs' codebase. Can you tell what it does? I can't. The strange part is Google appears to be using a few open-source projects -- just search for `SPDX-License-Identifier` and you'll find three results. What are those libraries? I doubt they would be revealing trade secrets for Google to acknowledge which projects they are incorporating into their own.

Regardless of whether I make PICKLE impossible to obfuscate, it will always have one limitation common to all programming languages: it's Turing-complete. The problem with that is any Turing-complete language can have a meta-circular interpreter for any other Turing-complete language written in it.

The result of that is that if I take a programming language where it's impossible to obfuscate code (perhaps PICKLE), and write a Javascript interpreter in it, now I can run obfuscated Javascript *in* PICKLE. Once you cross the boundary into the "data" of the Javascript source, you can no longer tell what the heck is going on. Being Turing-complete is a double-edged sword in this sense. It makes the language infinitely powerful to write clean, elegant, and understandable code, but if your goal is to hide what you're doing, there's nothing stopping you from using this device.

So the "God language" doesn't exist. It never did, and never will.

Sorry.

[^gpt]: Heck, ChatGPT isn't even at that point yet. Not completely, at least.
[^wasm]: I'm deliberately ignoring WebAssembly here, because it's a whole 'nother animal to Javascript, and surprisingly, doesn't have very wide support or use.

[ulisp]: https://github.com/dragoncoder47/ulisp-esp32
[pep572]: https://peps.python.org/pep-572
[anaphoric]: https://en.wikipedia.org/wiki/Anaphoric_macro
[loop]: https://cl-cookbook.sourceforge.net/loop.html
[docs]: https://docs.google.com/static/document/client/js/3964806806-kix_worker_binary_core.js
