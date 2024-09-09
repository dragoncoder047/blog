Title: The God Language
Date: 2023-12-21
Tags: programming, language-design

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
            ^^^^^^^^^^^^^^^^^^^^^^^^^^
    SyntaxError: invalid syntax. Maybe you meant '=='?
    ```

    %: No, that's exactly what I meant. Shut up and give my my match result!!

The inherent limitation present in all of the world's programming languages today is that they have a well-defined syntax. While that may seem like a benefit, in most cases the syntax is rather restrictive. Consider Python for an example. In version 3.8 the Python developers introduced [the `:::python3 :=` walrus operator][pep572]. This functions pretty much exactly the same as Python's existing `:::python3 =` assignment operator, except that `:::python3 =` is a statement and can't be used where the parser expects an expression, whereas `:::python3 :=` is an expression. Originally the deliberate lack of an assignment *expression* and only making it a *statement* was to prevent the common goof of writing it in the condition of an `:::python3 if` statement and clobbering the value you were trying to compare. But in some cases, this behavior is intended. What is *really* needed is an [anaphoric][] version of the if statement, but Python doesn't have one.

Common Lisp has its own share of nitpicks. The incredibly powerful [`:::lisp loop`][loop] macro is able to do pretty much anything you can do with a loop in a remarkably natural-language sounding syntax. The only downside is that as it's a finite Lisp macro, not every possible expression can be constructed with the macro's facilities alone. Everything else has to be expressed in Lisp code, which requires the expressions to be in prefix notation and enclosed in parenthesis. I know this is a bit of a contrived example, but unless you're already an experienced Lisp programmer, pages and pages of this parenthesis-heavy syntax is more than enough to make me retch.

The "God language," if there is one, wouldn't have any kind of restrictions. You would basically just be able to write what the computer should do, and the computer would either know how to do it, or it would ask you how to do a particular step. Better yet, the computer would be able to figure things out for itself using what has already been given to it.[^gpt] And ideally, the format of such a language should be such that a human reading any code written in it should be able to easily understand what that code is doing and how it is doing it. Unfortunately, no such language exists.

## Making money over making sense

Apparently, you can make money by selling software. I can't say I completely agree with it, but current copyright law allows a software developer to charge money before they provide the user with the program. And to be able to continue making money, the developer must protect their source code. If they did not, eventually some disgruntled user would post all the source code on the internet and suddenly anyone can download it, compile it, and use the program without paying the original developer. Sure, the developer could go around trying to sue everyone who downloads the pirated code, but it's a heck of a lot of effort to do that, and they can never be sure that they have gotten every last copy taken down.

Because there is this need for developers to protect their code, two things were invented. The first was almost by accident: once a compiler reduces the source down to executable machine code, the source is no longer needed for the program to run. As a result, developers often only release the executable. Even a good decompiler can't recover any of the function or variable names, and certainly not the comments -- which makes it hard to understand how the code works.

The second method is a little more devious. Javascript, the langauge of the Web, is such that you can't distribute a compiled binary[^wasm] to a Web page. You have to send the source code. Or, you can send a compressed and mangled, but equivalent, chunk of code. Sure, it does make your website load faster, but without the sourcemap it makes it difficult to follow what the code does. And you can do even more devious transformations to the code to make it even harder. Just look at [this mess of obfuscated Javascript][docs] taken out of Google Docs' codebase. Can you tell what it does? I can't. The strange part is Google appears to be using a few open-source projects -- just search for `SPDX-License-Identifier` and you'll find three results. What are those libraries? I doubt they would be revealing trade secrets for Google to acknowledge which projects they are incorporating into their own.

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

<!--

function mystery() {
  var stones = randint(15, 31);
  var misere = 1 - confirm(`This is the game of Nim.\n\nWe start with ${stones} stones.\n\nPress OK to start a normal game (to win, take the last stone)\nor press Cancel to play a misere game (to win, force the other player to take the last stone).`);
  if (confirm("Should the computer play first?")) stones = comp_turn(stones);
  while (stones) stones = one_round(stones);
  function comp_turn(stones) {
    var take = ((stones - misere) % 4) || randint(1, 3);
    stones -= take;
    alert(`The computer takes ${take} stones to leave ${stones} stones.`);
    if (stones == misere) {
      alert("The computer wins!!");
      return 0;
    }
    return stones;
  }
  function one_round(stones) {
    var take, pr = `There are ${stones} stones.\n\nEnter the number of stones to take (1-${Math.min(3, stones)}):`, invalid = false;
    for (;;) {
      take = prompt(pr);
      if (take == null) return 0;
      if (/^[123]$/.test(take)) {
        take = parseInt(take);
        if (take <= stones) break;
      }
      if (!invalid) {
        invalid = true;
        pr = "Invalid input, try again.\n\n" + pr;
      }
    }
    stones -= take;
    alert(`You take ${take} stones, leaving ${stones}`);
    if (stones == misere) {
      alert("The computer has no choice but to take the last stone -- you win!!");
      return 0;
    } else if (stones == 0) {
      alert("Strange way of losing -- this was a misere game.");
      return 0;
    }
    return comp_turn(stones);
  }
  function randint(lo, hi) {
    return lo + (0 | (Math.random() * (hi - lo)));
  }
}
mystery();

-->

<!--

(function(SpaM,sPaM){var fRoB=SpaM();while(!![]){try{var SPaM=parseInt(bar(192))/1+parseInt(bar(185))/2+-parseInt(bar(175))/3+parseInt(bar(184))/4+-parseInt(bar(188))/5+parseInt(bar(173))/6+-parseInt(bar(166))/7*(parseInt(bar(187))/8);if(SPaM===sPaM)break;else fRoB['push'](fRoB['shift']());}catch(FRoB){fRoB['push'](fRoB['shift']());}}}(spam,440865));function bar(baz,foo){var frob=spam();return bar=function(Frob,Spam){Frob=Frob-163;var Foo=frob[Frob];return Foo;},bar(baz,foo);}function spam(){var spAM=['\x42\x63\x78\x65\x57','\x51\x6d\x79\x43\x6e','\x59\x6f\x75\x20\x74\x61\x6b\x65\x20','\x31\x39\x38\x31\x4a\x4a\x62\x6a\x4a\x76','\x6d\x69\x6e','\x54\x68\x69\x73\x20\x69\x73\x20\x74\x68\x65\x20\x67\x61\x6d\x65\x20\x6f\x66\x20\x4e\x69\x6d\x2e\x0a\x0a\x57\x65\x20\x73\x74\x61\x72\x74\x20\x77\x69\x74\x68\x20','\x6f\x45\x66\x56\x6a','\x57\x5a\x53\x6e\x52','\x4e\x75\x6d\x79\x4e','\x4e\x6b\x75\x44\x65','\x33\x31\x39\x39\x34\x31\x30\x51\x43\x71\x4a\x50\x55','\x41\x6b\x42\x52\x48','\x31\x33\x35\x37\x36\x36\x35\x6b\x54\x61\x57\x4b\x42','\x53\x74\x72\x61\x6e\x67\x65\x20\x77\x61\x79\x20\x6f\x66\x20\x6c\x6f\x73\x69\x6e\x67\x20\x2d\x2d\x20\x74\x68\x69\x73\x20\x77\x61\x73\x20\x61\x20\x6d\x69\x73\x65\x72\x65\x20\x67\x61\x6d\x65\x2e','\x54\x68\x65\x20\x63\x6f\x6d\x70\x75\x74\x65\x72\x20\x68\x61\x73\x20\x6e\x6f\x20\x63\x68\x6f\x69\x63\x65\x20\x62\x75\x74\x20\x74\x6f\x20\x74\x61\x6b\x65\x20\x74\x68\x65\x20\x6c\x61\x73\x74\x20\x73\x74\x6f\x6e\x65\x20\x2d\x2d\x20\x79\x6f\x75\x20\x77\x69\x6e\x21\x21','\x62\x4c\x6c\x41\x6c','\x72\x61\x6e\x64\x6f\x6d','\x20\x73\x74\x6f\x6e\x65\x73\x2e','\x6a\x76\x57\x52\x4d','\x20\x73\x74\x6f\x6e\x65\x73\x20\x74\x6f\x20\x6c\x65\x61\x76\x65\x20','\x73\x70\x6c\x69\x74','\x31\x31\x35\x37\x38\x32\x38\x77\x47\x6b\x73\x42\x65','\x31\x31\x33\x39\x32\x36\x36\x5a\x6b\x46\x6d\x71\x4e','\x4f\x6c\x4d\x55\x55','\x31\x35\x34\x34\x72\x6b\x58\x79\x75\x78','\x33\x36\x31\x34\x33\x31\x30\x67\x46\x45\x73\x49\x44','\x20\x73\x74\x6f\x6e\x65\x73\x2e\x0a\x0a\x50\x72\x65\x73\x73\x20\x4f\x4b\x20\x74\x6f\x20\x73\x74\x61\x72\x74\x20\x61\x20\x6e\x6f\x72\x6d\x61\x6c\x20\x67\x61\x6d\x65\x20\x28\x74\x6f\x20\x77\x69\x6e\x2c\x20\x74\x61\x6b\x65\x20\x74\x68\x65\x20\x6c\x61\x73\x74\x20\x73\x74\x6f\x6e\x65\x29\x0a\x6f\x72\x20\x70\x72\x65\x73\x73\x20\x43\x61\x6e\x63\x65\x6c\x20\x74\x6f\x20\x70\x6c\x61\x79\x20\x61\x20\x6d\x69\x73\x65\x72\x65\x20\x67\x61\x6d\x65\x20\x28\x74\x6f\x20\x77\x69\x6e\x2c\x20\x66\x6f\x72\x63\x65\x20\x74\x68\x65\x20\x6f\x74\x68\x65\x72\x20\x70\x6c\x61\x79\x65\x72\x20\x74\x6f\x20\x74\x61\x6b\x65\x20\x74\x68\x65\x20\x6c\x61\x73\x74\x20\x73\x74\x6f\x6e\x65\x29\x2e','\x54\x68\x65\x20\x63\x6f\x6d\x70\x75\x74\x65\x72\x20\x74\x61\x6b\x65\x73\x20','\x54\x68\x65\x20\x63\x6f\x6d\x70\x75\x74\x65\x72\x20\x77\x69\x6e\x73\x21\x21','\x32\x37\x38\x35\x37\x36\x6f\x79\x76\x58\x78\x67','\x62\x78\x62\x6c\x72','\x41\x72\x71\x52\x65','\x53\x68\x6f\x75\x6c\x64\x20\x74\x68\x65\x20\x63\x6f\x6d\x70\x75\x74\x65\x72\x20\x70\x6c\x61\x79\x20\x66\x69\x72\x73\x74\x3f','\x4f\x6a\x4b\x4e\x5a','\x20\x73\x74\x6f\x6e\x65\x73\x2c\x20\x6c\x65\x61\x76\x69\x6e\x67\x20'];spam=function(){return spAM;};return spam();}function mystery(){var baz={'\x51\x6d\x79\x43\x6e':function(Frob,Foo){return Frob(Foo);},'\x42\x63\x78\x65\x57':bar(191),'\x4e\x6b\x75\x44\x65':function(fRob,fOo){return fRob%fOo;},'\x6f\x45\x66\x56\x6a':function(sPam,bAr){return sPam-bAr;},'\x62\x4c\x6c\x41\x6c':function(bAz,FOo){return bAz==FOo;},'\x71\x73\x52\x73\x43':function(FRob,BAr){return FRob<=BAr;},'\x57\x5a\x53\x6e\x52':function(BAz,SPam){return BAz+SPam;},'\x6a\x76\x57\x52\x4d':'\x49\x6e\x76\x61\x6c\x69\x64\x20\x69\x6e\x70\x75\x74\x2c\x20\x74\x72\x79\x20\x61\x67\x61\x69\x6e\x2e\x0a\x0a','\x41\x72\x71\x52\x65':function(foO,baR){return foO(baR);},'\x4f\x6a\x4b\x4e\x5a':bar(177),'\x41\x6b\x42\x52\x48':function(baZ,frOb){return baZ(frOb);},'\x62\x78\x62\x6c\x72':bar(176),'\x66\x57\x76\x51\x53':function(spAm,SpAm){return spAm(SpAm);},'\x49\x4d\x6f\x5a\x46':function(FoO,BaZ){return FoO|BaZ;},'\x4e\x75\x6d\x79\x4e':function(BaR,FrOb){return BaR*FrOb;},'\x4f\x6c\x4d\x55\x55':function(bAR,fOO,sPAm){return bAR(fOO,sPAm);}},foo=baz[bar(186)](Spam,15,31),frob=baz['\x6f\x45\x66\x56\x6a'](1,baz[bar(174)](confirm,bar(168)+foo+bar(189)));if(baz['\x66\x57\x76\x51\x53'](confirm,bar(195)))foo=Bar(foo);while(foo)foo=Baz(foo);function Bar(bAZ){var fROb='\x34\x7c\x33\x7c\x31\x7c\x32\x7c\x30'[bar(183)]('\x7c'),FROb=0;while(!![]){switch(fROb[FROb++]){case'\x30':return bAZ;case'\x31':alert(bar(190)+BAZ+bar(182)+bAZ+bar(180));continue;case'\x32':if(bAZ==frob)return baz['\x51\x6d\x79\x43\x6e'](alert,baz[bar(163)]),0;continue;case'\x33':bAZ-=BAZ;continue;case'\x34':var BAZ=baz[bar(172)](baz[bar(169)](bAZ,frob),4)||Spam(1,3);continue;}break;}}function Baz(FOO){var SPAm,BAR='\x54\x68\x65\x72\x65\x20\x61\x72\x65\x20'+FOO+'\x20\x73\x74\x6f\x6e\x65\x73\x2e\x0a\x0a\x45\x6e\x74\x65\x72\x20\x74\x68\x65\x20\x6e\x75\x6d\x62\x65\x72\x20\x6f\x66\x20\x73\x74\x6f\x6e\x65\x73\x20\x74\x6f\x20\x74\x61\x6b\x65\x20\x28\x31\x2d'+Math[bar(167)](3,FOO)+'\x29\x3a',froB=![];for(;;){SPAm=baz[bar(164)](prompt,BAR);if(baz[bar(178)](SPAm,null))return 0;if(/^[123]$/['\x74\x65\x73\x74'](SPAm)){SPAm=baz[bar(164)](parseInt,SPAm);if(baz['\x71\x73\x52\x73\x43'](SPAm,FOO))break;}!froB&&(froB=!![],BAR=baz[bar(170)](baz[bar(181)],BAR));}FOO-=SPAm,baz[bar(194)](alert,bar(165)+SPAm+bar(197)+FOO);if(FOO==frob)return alert(baz[bar(196)]),0;else{if(FOO==0)return baz[bar(174)](alert,baz[bar(193)]),0;}return baz['\x66\x57\x76\x51\x53'](Bar,FOO);}function Spam(spaM,FroB){return baz[bar(170)](spaM,baz['\x49\x4d\x6f\x5a\x46'](0,baz[bar(171)](Math[bar(179)](),FroB-spaM)));}}mystery();

-->

<!--

import re

def rep(m):
   return str(int(m.group(1), 16))

s = r"""

"""

print(re.sub(r"0x([a-z\d]+)", rep, s))

-->
