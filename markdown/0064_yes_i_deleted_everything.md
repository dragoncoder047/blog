Title: Yes, I deleted everything.
Date: 2025-10-03
Tags: programming, gamedev
Series: aelith-game

And I don't regret it for one second.

In the previous post I detailed a (very long) series of thoughts I had during development of the platformer game I have been working on. That mental planning really enabled me to make headway on the game.

Among other things, it's not called *Debugger* anymore. After finishing a complete draft of the game's plot, that title no longer fit. I'm not going to leak the story quite yet, but it is centered around an industrial complex called the *Aelith*, which is also now the title of the game.

![*Aelith* logo]({attach}aelith_logo_1.png){style="margin:inherit auto"}

In the process of making the game fit with the story I wrote (rather than the other way around) I decided that rather than trying to refactor the messy spaghetti code I already had, it would be more efficient to just get rid of it and start again from scratch! (Of course, I didn't *delete* the old code; I merely archived it in a separate folder, so I could go back and copy old useful snippets that I had when needed, without having to futz around with git recovering it.)

Now that I was freed from the tyranny of my old code, I decided that I would do two things. The first one is to try some established game development techniques rather than just reinventing the wheel (badly) on my own. The first one I found was the concept of automatic tile selection based on neighbors - if there are two adjacent tiles of the same type, the sprites used for each are chosen to make the texture seamlessly join. I kind of already had this -- the original floor and walls were just a single 32x32 sprite that tiled nicely with itself on all directions (no code required) -- but it was a little bland. I found [this tileset template](https://opengameart.org/content/seamless-tileset-template) that came with a simple bit-twiddling method of selecting the tiles, and once I made the tileset and got it working it was quite surprising how clean it looked.

<instagram post="DO2IppJjDBw" />

I also added back in the pseudo-3D depth effect to the tiles after I got the automatic sprite selection working, and it actually ran better than it did in my original code. Although I'm not sure if that is because it wasn't being taxed by the other code or not, since my test map was much smaller than the average size of the maps in the old code. I don't have any screenshots of it directly, but it is visible in the third slide of the post below.

<instagram post="DPRv5rMDxFm" />

What the post below is *really* trying to show is the new character models I have developed. In the old code and assets, I "baked" animations such as walk, blink, and jump into the character's sprites, so while activating those animations was [dead simple](https://v4000.kaplayjs.com/docs/api/SpriteComp/#SpriteComp-play) it didn't allow for more complex layered animations, and if I wanted to add another animation (even a simple one) I would have to copy-and-paste countless more frames in the character's spritesheet.

It isn't visible in any of those screenshots or animations, but I implemented all of that using one of the as-yet-unreleased features of KAPLAY - inverse kinematics and distance constraints. Granted, these features didn't exist 6 months ago when I made the original spritesheet animations, but now they do, and I am glad that I decided to use them, since they make the character's movement so much more natural. (I am a terrible animator!)

One of the other advantages I gained from completely scrapping the code from the *Debugger* implementation is that I could now do everything with a *data pack*. Instead of all of the game's assets and logic being hardcoded in the source file, the source file is only just a generic "engine" and it downloads the data pack to begin with and then constructs everything. Implementing logic in JSON is actually kind of difficult, but it's obviously possible, as Minecraft has "function" files in its data packs that can execute complex logic when combined with temporary entities and other game objects.

Now that I've done that in *Aelith*'s engine, it doesn't even make any specific designation as to which entity is the player; that is defined in the datapack and/or savefile. Previously, I hardcoded that player into a variable, and then imported it pretty much everywhere I implemented interactivity logic. As more and more things needed to reference the player (even just to check if something is the player or not) this ended up creating circular imports and hard-to-track-down bugs. Now with the engine no longer hardcoding the player, that logic, of course, must change.

Suffice to say *Aelith* is nowhere near complete yet -- at this moment, I haven't added **any** player input to the engine at all, so the game is unplayable! -- but I have an end in sight. I still don't know when the game will be done, but this will surely end up being one of my largest (if not *the* largest) project I have ever completed, and I can't wait for that to be true.
