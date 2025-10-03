Title: What's in a game?
Date: 2025-08-13
Tags: programming, gamedev
Series: aelith-game

"I have a cool game mechanic. Now what?"

Unfortunately for me, I don't have any good answer to that question. But I found myself asking it a few weeks ago as I worked on my puzzle platformer game, *Debugger*.

For the most part, all of the game's mechanics have been finalized. I'm quite pleased with the graphics as well, and haven't actually touched the main texture significantly for months. Apart from fixing bugs in both my code and the game engine (KAPLAY), I haven't really done anything significant. That's what I'm most annoyed at myself for.

The one thing that *Debugger* lacks completely right now is any kind of lore. It's fun to play, but apart from solving puzzles, there's not much else. I found myself wanting to tell a story through the game, but nothing came to mind. Nothing still has, for that matter.

I stalled for a while by adding various graphics enhancements to the game, such as a sprite-stacking "2.5D" effect using parallax scrolling, and lighting using a [plugin][kaplay-lighting] another KAPLAY user developed (and I promptly added a settings option to turn them both off and then did that, as they're rather GPU-intensive and were causing my laptop to overheat). I started drafting lore in a file, called `LORE.md` for obvious reasons, and left it open most of the time. Whenever I finished that day's worth of bugfixes and enhancements, I would commit and push my changes, and then close all of the open tabs, leaving only `LORE.md` open and reminding myself of how much I hadn't written.

[kaplay-lighting]: https://github.com/tristanperrow/kaplay-lighting

But what should I even write?

## Starting... somewhere

Perhaps part of the reason why I am having trouble coming up with ideas for *Debugger*'s lore is that I have never really played very much of established videogames with fully-developed storylines. On that effort, I decided I wanted to start playing some existing games to be able to see how their developers and story directors think.

### Minecraft

I had a [Minecraft][mc]{title="do I really need to give you a link to this?"} gift card lying around that my aunt had bought me years ago that I hadn't yet redeemed, so I redeemed it. And although I had seen many YouTube videos discussing Minecraft's lore, I wanted to start at the beginning and see how Minecraft introduces the player to is story.

[mc]: https://minecraft.net
<!--cSpell: ignore mojang -->

Unfortunately for me, Minecraft doesn't make any effort whatsoever to set up any kind of exposition. Upon creating a new survival-mode world and launching it, you (the player) are simply spawned in a random location in the world and you have to immediately start trying to survive (ahem, it's *survival* mode) and it's only after you have played for a long time that you find bits and pieces of Minecraft's lore in the form of the various structures that generate in various locations in the world across biome types, elevations, and dimensions. I didn't play long enough to get any of that before I got bored looking for it.

%%%
    ![image]({attach}minecraft_screenshot.png)

    %: I started by playing survival mode, but got quickly bored (and died 5 times in 2 minutes). Rather than bore myself any more I made a "redstone sandbox" creative mode superflat world and played around in that. The first thing I made was a 2x2 flush sliding piston door. I did not use any tutorials. I am pretty proud of myself.

There's no text[^1], which makes the lore extremely cryptic. Thankfully this crypticness has probably made it a lot easier for Mojang to add pretty much anything and still have it fit with the existing lore. A recent snapshot ([25w31a][]) added copper golems, which are basically little robots that run around and sort items for you. By what I have heard on YouTube, copper golems were added entirely by request from the Mineraft community who have been tired of having to waste time building item sorting machines to maintain organization when building -- thus copper golems are probably the best candidate for 'thing in Minecraft with absolutely no lore whatsoever'. (My creative mode inventory is rather disorganized, so I completely understand where this request is coming from!)

[25w31a]: https://www.minecraft.net/article/minecraft-snapshot-25w31a

That being said, Minecraft's style of dumping the player straight into the world with no explanation is kind of where *Debugger* is at already. I suppose that means that I should not worry too much about getting the player up to speed initially, as they will be getting all of that anyway as the game progresses and putting half of it upfront might just be wasting time.

[^1]: Except for the 'End poem' that you get after beating the Ender Dragon, but it's also just as cryptic and abstract as the rest of Minecraft's environment, and I could see it fitting in with any possible interpretation of Minecraft's lore. Hardly anyone who gets to that point ever stops to read it anyway these days from what I've seen, because they've either seen it all before, or don't care about it. It's a nice read though. Full disclosure - I never actually beat Minecraft and read it that way. I just looked at it from other places where it is posted online. Sure, boo me all you want, but playing Minecraft is not my job.

### Warframe

Being a college student with a $0 budget is quite limiting, and I have had a pretty hard time finding games that are both well-developed in terms of storyline and free to play. Thankfully, [Warframe][wf] is both. I initially resisted getting it as I'm not that big of a fan of fighting / shoot-'em-up games, but I was quickly getting bored by Minecraft, so I figured I should at least try a different game.

Unlike Minecraft, Warframe actually has plot-developing cutscenes and guided introductory missions that the player has to complete before they can continue. Combined with the fact that it's nearly impossible to die to the point of having to completely restart the mission (at least in the beginning, I haven't got past that yet) -- even the starter warframes are quite overpowered compared to the enemies, and you also get four revives for free every time -- the game feels more like a guided story than a game to me at least, and *oh boy* is it a long story.

Warframe is actually a few years younger than Minecraft (12 compared to 16 years), yet there's already more pages in the Warframe fan wiki compared to Minecraft ([9,276][wfwiki] compared to Minecraft's [7,514][mcwiki] at the time I wrote this). From a cursory look, the majority of pages in the Warframe wiki are dedicated to lore, revolving around both the game's immense number of items (also more than Minecraft!) and just pages and pages of nothing but history of the Warframe universe, whereas the Minecraft wiki's pages largely just detail the properties (of items) and behaviors (of mobs) of each thing in the game, and don't connect things together too much.

[wf]: https://warframe.com
[mcwiki]: https://minecraft.fandom.com/wiki/Minecraft_Wiki
[wfwiki]: https://warframe.fandom.com/wiki/WARFRAME_Wiki

Due to the fact that I'm not a terribly avid gamer, I'm probably never going to get through all of Warframe's missions. (By the time I get through all of the ones that exist right now, they'll probably have added many more!)

Regardless, this is actually kind of similar to how I envisioned (and currently have) *Debugger*'s lore set up: even though the player has to retrace their steps and pass through the same area multiple times, there's still a linear pathway they have to follow, so it's looking like I will probably be able to write a fairly linear storyline and have it work.

### Honorable mention: Undertale (and Deltarune)

For a text-driven narrative, some of the best examples I can think of are Toby Fox's games. I am completely sure that if it weren't for the fact that I haven't played either of them, these would be first in the list of games I have explored here and not pushed down to the "honorable mention" level.

With how popular they are, avoiding Undertale and Deltarune memes, fan art, and "[character] out of context"-style quotings has been next to impossible for me. It's quite apparent that the reason why Toby Fox's characters have been so popular is that they balance the right amount of deadpan humor, fourth-wall breaking, and unreliable-narrator-ness to make the game strangely addictive. Even the ["about" page for Undertale][undertale] has this same kind of irreverence:

[undertale]: https://undertale.com/about/

> So, did you learn what the game's about?
>
> Hmmm.
>
> Well, it's too late.
>
> There's no "BACK" button on this page.
>
> You're going to be trapped here...
>
> For ALL ETERNITY!!!
>
> Urrahhhh ha ha ha!!
>
> This ABOUT PAGE is gonna be your GRAVE!
>
> AHAHAHAHAHAHAHAHAHAHAHAHAHA!!!!
>
> Oh! And here's my Twitter.

I don't want to just "mimic Toby Fox," but I definitely admire deadpan comedy and farcical situations like this and are probably where all of the iconic memes and quotes have come from. I want my characters to have their own style, and doing this is going to be a challenge.

## Going

I have not played any of those games to the point of seeing a resolution to the story. Granted, there may not even be a resolution (Minecraft hardly has any lore, and Warframe is said to be in 'perpetual beta'; in both cases the developers are just continuously adding stuff to their game), but even with that, I haven't even gotten out of the exposition in either game.

Constructing a complete story arc is surprisingly difficult whether it's a videogame backstory or a novel. Heck, even getting this very blog post to a sensible conclusion was difficult. Nevertheless the general theme of what I've learned with these is that everything including the the environment has to play a role or be otherwise connected to the story in a visible manner for the influence of the story to be the strongest. It's the old principle of [Chekhov's gun](https://en.wikipedia.org/wiki/Chekhov%27s_gun) -- if something is displayed prominently - anywhere - and not immediately used, the player *must* come back to it later and use it. If it's never used, including it is pointless for the story and potentially confusing to the player.

The current way I have of presenting lore in the game is via dialog boxes that are styled to look like a Linux `man` page, and all of the items you can pick up in the game have entries in this system -- some are longer than others, but at least for what I have written currently, they only describe the items' functionality in the style of a man page giving hints to how you can use it, and don't really take part in any story. There's only eight entries (because there's only eight unique items), and there's not much you can do to tell a full story in eight panels that are presented only when the user asks to look at them by pressing a button -- you could play the whole game and never read a single word of any of them. So I definitely need some other way of giving out bits and pieces of the lore.

My half-assed first draft and *Debugger*'s lore document included a nameless, faceless 'computer' narrator, and I had deliberately ignored how I was going to actually integrate such a thing into the game for the sake of expanding the draft. After suffering from writers' block for a few days I decided my time would be better spent trying to figure out how to actually present the narration or narrator.

My initial idea was a little floating companion that follows the player around throughout the game and displays speech bubbles after key events happen (when the player picks up a certain item, when the player enters a certain area, etc) and the player can click on the thing to move to the next speech bubble's worth of text if it doesn't fit in one.

%%%
    ![image]({attach}idea_debugger_computer.png)

    %: Everything in pink is just a doodle that I made on top of the screenshot as a 30-second mockup.

After admiring my hot pink scribble, I started to think about how exactly the narrator companion would talk in-game. I narrowed it down to two options for myself:

1. Play off the current generative AI boom and tools like ChatGPT, and make the narrator character sickeningly sycophantic. I've never used AI and experienced that yes-man tendency some large language models are said to exhibit, but I could probably check with friends or just come up with something that sounds that way. From the popularity of ChatGPT, it's obvious that people have no problem with this kind of conversational style, so maybe I can capitalize on that. Maybe I can even run my drafts through ChatGPT itself to make them sound more like AI!

2. Make the narrator snarky and superficially unhelpful, similar to the character GLaDOS from the game *Portal* (another one which I have not played). Back when *Portal* was a new game, apparently GLaDOS enjoyed the same memeworthiness and quotability as *Deltarune*'s characters do today, largely in part due to her chillingly callous and snarky retorts during and after each level.

Then there's always the third option in the middle of the two: start out with one of them, and gradually transition to the other one as gameplay progresses. I might do this only because I will probably get bored or blank if I try to write the entire thing using one static tone.

Having the text come in small snippets also opens up the possibility of having randomized or changing text, in case the player encounters the same text trigger multiple times. Obviously this means that if I do this, I will have to write much more text than just one complete pass through the game, which just adds to the difficulty level.

## Gone

Probably the most important thing about a game's storyline is the ending of it. It needs to tie up all of the loose ends with the story, so that the game actually feels complete rather than just being that way, and leaves the player with a nice feeling that they'll remember after having not played for a while.

At one point during the development of *Debugger* I did have an area that could be called an ending in some regards, but it was little more than just a text box announcing 'Congratulations! You have reached the end of the game!'. I eventually scrapped that area as it was obvious that despite the game announcing to the player that it was so, the game would not *feel* complete without the rest of the story coming to a close around it. And at that point, there wasn't really any story that I could do anything to conclude, so that area was worthless.

In some places, I've heard that when designing a story like this it helps to work backwards -- determine what the ending/resolution will look like, and then figure out how the player will get there. I'm finding this extra difficult because the part of the game I have implemented currently is the *beginning* of the game, and having to ignore that and come up with an ending hasn't been easy as I am constantly being pulled back to the part I have made already during development, which is not the end.

That being said I am probably going to start working on the conclusion next, just to keep my sanity, and to give myself a known ending to work towards. Up until now, *Debugger* has been steadily progressing towards something, but without a clear destination, I've been largely unable to stop working on it.

## With a bang

And let's not forget one of the other important aspects of a good videogame: the background music. Even if there's sound effects, without any music, the game just feels empty and lifeless.

That being said, 'empty and lifeless' is kind of the aesthetic I was going for to begin with, so I initially did not have any music. But my alpha-tester classmate pointed this lack of music out, and he said that for what he could see the game would be better served by some background music.

I currently have 10 different songs written for *Debugger*, and they are more or less designed to be seamlessly transitioned into each other. They're all scored using simple 8-bit style synthesizers (mostly because I decided to limit myself to use [ZzFXM][]) and have a range of moods, from hyperactive and fast to dark and foreboding.

[ZzFXM]: https://keithclark.github.io/ZzFXM/

My initial plan was just to assign one song to each room in the game, and then whenever the current song ends, just check which room the player is in, and switch to the song assigned to it. This is sort of what other games like *Undertale* do, where each area has its own theme music, each boss has their own battle music, etc. But after a while, I realized that I would have to add new rooms as I expanded the game, and having to design the level *and* compose another song for it just makes the whole thing harder.

Since I didn't have the right number of songs to go along with the current number of levels I had designed, I just abandoned that idea entirely and made the songs switch between each other totally at random. But after stalling for a while (and composing a few more of the songs) I came up with a better idea: the player's actions would bias the choices of songs. Each time the player does something significant, it will change a parameter variable (such as speed, danger, repetitiveness, etc.), and once the current set of parameter variables is far enough from the current song's assigned parameters, the song will change to another song that is closer to the current parameter values. Of course, making sure that the song fits the actions is completely governed by what numbers I assign to each song, and fine-tuning those will present its own set of problems.

## Yet

If there's anything I've gained from this experience, it's a healthy respect for other indie game developers (and ones at big established studios, too). Games are art, with a little bit of programming thrown in, and not the other way around. I probably should have realized this earlier on, but my na&iuml;ve enthusiasm for the game mechanic I came up with largely blinded me to the level of creativity I need to develop in order to get *Debugger* across the finish line.

I may still not appreciate it fully, but I now have a healthier understanding of what it takes to make a game, and what it takes to finish a game as well. Here's hoping that with this new knowledge, I will be able to push myself to make *Debugger* a great game.
