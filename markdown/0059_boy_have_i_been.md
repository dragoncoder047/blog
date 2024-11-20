Title: Boy, Have I Been...
Date: 2024-11-20
Tags: javascript, game-design, youtube, programming, code-nostalgia

Back in July, I had the following conversation with a friend over lunch:

> **Friend**: What's the most confusing computer science topic you've ever encountered? Explain it to me.
>
> **Me**: [Continuations](https://en.wikipedia.org/wiki/Continuation). They're a way for a program to manipulate its own call stack as if it were data. For example, if you have the expression $f(x)$, and you're evaluating $x$, then the continuation of the expression $x$ is $f$.
>
> **Friend**: How is that confusing?
>
> **Me**: Well, suppose you stuff 'the continuation of $x$' into a variable, let's call it $k$. And then evaluate $g(k(y))$. The super weird part is because $k$ is a continuation, it throws out the $g$ and you get $f(y)$. It jumps back in the program to where the original expression was, and forces that code to run again.
>
> **Friend**: That *is* confusing... I bet you could make a game out of continuations.
>
> **Me**: Gosh, that would require some thinking...

And think I did. That's what I've been working on for the past few months; I kind of forgot that I even had a blog or a YouTube channel. Developing the game has been taking up way too much time and I probably should have prioritized my studies over finishing the game, instead of the other way around. But the game is now 90% complete (or more), so I thought it would be fun to take a trip down memory lane and look at what the game looked like in its earliest stages.

I quickly decided it was going to be a platformer game and be playable in the browser. That left it still pretty wide open in terms of game engine, and so I settled on [Kaplay.js](https://kaplayjs.com/). While I worked on the game description, I also played around with Kaplay and put together a bit of code to test what I could do.

Digging through old git commit history, I resurrected the very first test I ever made using Kaplay. It is date-stamped July 19.

%%% figure
    <iframe src="kdemo.html" height="125" width="450" style="margin-left:auto;margin-right:auto"></iframe>

    %: You can click on the canvas and use the left and right arrow keys to move the red rectangle (the player) and the up key to jump. There's not much to do, but hey... it works!

Compared to what the game is now, that first demo was laughably primitive. There wasn't even any art, but with a good eye you can see how it resembles -- just barely -- the full game that I have put together.

<youtube id="66vBqb_Jda4?si=k7doYZbl3srXPBkK"></youtube>

By the end of July I had put together a short description of the game mechanics. I realize now that my initial idea is completely backwards compared to what the game turned into, but let's just have some fun looking at the earliest draft ever of the game description:

> Game premise: you are a bug in a computer system, and a rogue AI program is messing with the computer's jobs. Using the power of continuations, you have to work your way up and down the programming language stack, beating increasingly hard challenges, until finally resetting the AI's memory into a stable state and averting total corruption.

Compare that to what's going on in game above, and you can see why it's taken me so long to put this game together. It's been revised so much that it's almost the exact converse of what I originally wrote -- instead of being a bug, the player character is fighting bugs.

---

Putting together a game like this is incredibly fun -- and exhausting. When I started, I thought I would be able to throw it together in, like, a week. It turns out it's not that simple: I was constantly running into weird bugs in the game engine itself!

All of those bugs would need fixing if my game was going to work, so I reported them all to Kaplay's maintainers, one by one, as I discovered them.. Later on, I forked Kaplay and fixed them myself.

As I explored Kaplay's codebase, I learned more and more about how the game engine works, and I started noticing things that could be improved, even stuff that my game didn't encounter as a problem. The speed at which I was finding and fixing issues must have been unusual, because once I joined the Kaplay Discord server in September, I was quickly reminded of my "meme" status:

![lajbel: you have reached the final issue, a dragoncoder047 issue]({attach}kdmeme.png)

It was all in good fun, though; I was never harassed over it except for this tongue-in-cheek ribbing. The Discord server also gave me the unexpected opportunity to help others quickly -- since I kind of knew what the game engine was doing internally, I could explain a lot of the errors that other users were encountering and point them in the right direction.

---

In early October, the Kaplay team announced that they would be hosting a game jam in November, and then dropped a huge surprise in my lap: the main developer asked me to be a judge of the game jam.

![lajbel: Hey dragoncoder047! I'm searching for judges on our upcoming game jam. What do you think?]({attach}kajamjudgereq.png)

I turned him down, mostly because I knew that I should be prioritizing my studies over judging a game jam and I wouldn't be able to commit to the time. Unfortunately, that meant that I would have more time to work on my game... and so I did that. I recruited a classmate from my calculus class to beta-test my game and it ballooned exponentially from there. I kept creating more and more additions to my game, and finding more things to fix in Kaplay. It was so much that I actually am now the 5^th^ place developer by number of commits, after only the original developer (of Kaboom.js, Kaplay's predecessor), and Kaplay's development team.

[![6 top developers to Kaplay by number of commits]({attach}kcontr.png)](https://github.com/kaplayjs/kaplay/graphs/contributors)

I'd say it's been a productive 3 months.

<!-- cSpell: ignore kaplay -->
