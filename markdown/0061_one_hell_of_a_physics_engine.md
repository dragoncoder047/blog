Title: One Hell of a Physics Engine
Date: 2025-02-22
Tags: programming, javascript, gamedev
Series: debugger-game

I've been working on my upcoming platformer game, Debugger, way too much. And I haven't really had the chance to add much of anything to the game itself. All I have been dealing with is trying to eliminate any source of lag in the game by any means possible.

Sure, the game never got a smooth 60 frames per second, even at the start. I knew that a Javascript game like Debugger was never going to have buttery-smooth graphics, even with a KAPLAY using a WebGL backend for all the drawing. The main source of lag is in the physics engine -- and there's a lot of reasons why that will usually be the bottleneck.

Detecting collisions is an integral component of any platformer game's physics --- without collision detection, the player falls straight through the platforms. But in larger platformer games -- and in general, any physics-based game -- doing that collision check takes a huge amount of processing power (and mostly time), so a plethora of algorithms have been developed to speed up collision checking. KAPLAY's integrated physics is no exception, but it's currently a little underpowered.

## Failure mode #1: The game lags to the point of being unplayable

This was the case once I had the mechanics of the game down and started adding to the world. I opened a test build of the game in my browser one day and found that I was getting an eye-watering 5 frames per second --- technically, it was playable (I deliberately designed the game to never rely on swift reflexes or split-second timing), but the latency on even the keyboard controls was extremely bad and unresponsive, and in addition to that, it turned my laptop's fan into a jet engine.

After discussing the implementation of KAPLAY's physics engine with the developer in charge of it, Marc Flerackers, I was made aware that KAPLAY uses a one-dimensional [sweep-and-prune](https://en.wikipedia.org/wiki/Sweep_and_prune) to filter the possible pairs of objects down to remove ones it knows can't possibly collide.

By default, KAPLAY's sweep-and-prune sweeps horizontally, culling objects that have vertical space between them. But with thousands of objects spread out both vertically and horizontally over the plane (and in my game mostly vertically), this didn't filter much and the game wasted a lot of unnecessary checks.

Marc quickly drafted up a vertical version of the sweep-and-prune and I patched it in, hoping that if the game is oriented more vertically than horizontally, this would speed it up. It turns out it did, but not by much. I clocked it at 7 FPS -- and this was in Google Chrome, which has a more aggressive Javascript optimizer and JIT compiler than either of Firefox and Safari. Those two were still stuck at 5 FPS.

Obviously, to be able to cater to any kind of game with minimal configuration, KAPLAY needs to be able to adapt to whichever direction the user's game is oriented in. Marc whipped up a quick double sweep-and-prune function that sweeps in both directions and then only takes the colliding pairs that were in both horizontal and vertical sweeps. I patched it in, enabled it in my game, and...

## Failure mode #2: Collisions just completely stop working

Suffice to say there is still a bug in Marc's na&iuml;ve bidirectional sweep-and-prune. When I opened a test build with this code, it showed a more-reasonable 18 FPS --- but my joy was quickly turned to horror as I watched the player fall straight through the floor and out the bottom of the world.

When I told Marc this, he pointed me to an old file containing code for a spatial hash grid that never got integrated, but he thought it might work. I patched it in and -- no joy, it didn't work. But at least it was actually able to get 22 FPS this time, which I guess showed that the hashgrid had less overhead that two sweep-and-prune instances.

Then out of his sleeve Marc produced some (very) old code that implemented not a hashgrid, but a spatial quadtree. And it worked, at least with the little demo he wrote for it, which used only 200 objects and maybe 5 levels of tree. My game needed significantly more -- and combined with my (almost certainly terrible) code to allow the tree to expand and rebalance itself if objects leave the bounding area of the root node, it certainly stressed the quadtree to the maximum. It turns out that maximum was...

## Failure mode #3: The browser crashes

When a Web page completely stops working, it is without a doubt a sign that something has gone horribly wrong, and you should look at the error messages in the browser developer tools console to see where you should go to fix the error. Unfortunately in the rare case where the page manages to break the browser itself, no one is able to help you because there are no stack traces or console messages (the developer tools won't even open). It's the equivalent feeling to what you'd have if your dog poops on your lap while you're in the park with no cleaning supplies for miles. Seeing the little "Aw, Snap!" icon come up made me feel like my game had just been reduced to a hot, steaming pile of shit and I had no way to tell why.

Of course that didn't mean that the *entire* quadtree implementation was bad. I managed to run a profiler on the page before it crashed, and the report indicated that the bottleneck was in updating the different nodes in the tree. When an object moves and has to be removed from one node and inserted into another, the array in the old node containing the objects has to have the object spliced out of it using the [`:::js Array.splice()`][splice] method. And it turns out that `:::js splice()` is slow. Like, *really* slow. Because it has to move all of the elements ahead of the one deleted back by one index, it takes longer if the element is closer to the beginning.

I tried changing the implementation to simply set the removed object to `:::js undefined` instead of `:::js splice()`'ing it out, but that still didn't speed it up. *Now*, the bottleneck was the `:::js indexOf()` call, used to find which element needs to be deleted. It's $O\left(n\right)$ linear search either way. An ES6 [`:::js Set`][Set] would use a binary tree or something that is a bit faster (probably $O\left(\log n\right)$ but it depends on the implementation), but I saw no way to be able to use it, since when the quadtree is queried for all possible objects that may be colliding, it only needs to yield each pair once -- a simple double loop would produce $[b, a]$ as well as $[a, b]$, which would effectively double the time it takes to process each collision, since they are being processed twice. It's super easy to avoid this with an array by watching the index variables, but sets are unordered so that won't be possible. There's probably an algorithm that works for unordered and unindexable sets, but I need some time.

There's one thing for sure that can be had form all of this: KAPLAY's physics engine is one hell of a program and by working on it, I've certainly learned a lot more about physics simulations than I ever bargained for.

[splice]: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/splice
[Set]: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Set
