Title: Langton's Ant Music
Date: 2022-06-22

Over the weekend I joined the [conwaylife.com forums](https://conwaylife.com/forums/index.php) because I am interested in cellular automata. I find watching the mechanisms mesmerizing, and building them exciting.

I also have an interest in music, and so a year or two ago I tried to generate music from cellular automata. I used one-dimensional rule 86, and then played notes depending on whether cells were on or off. The result sounded horrendously like a toddler banging on a piano. It's so bad I'm not going to share it.

I poked around the conwaylife forums, and learned about [Langthon's ant](https://en.wikipedia.org/wiki/Langton's_ant). Langton's ants are stateless Turing machines operating on a square grid. If an ant is on a white square it makes it black and turns right, and if it is on a black square it makes it white and turns left. Langton's ants have been generalized further, to include multiple colors and even internal states in the ant, in which case they are called turmites.

If there are N ants, only N cells will change at once, so I wondered if you could play notes depending on the actions of the ants. For example, play a low bongo drum when the ant turns left and a high bongo when the ant turns right.

I rigged up a Langton's Ant simulator and hooked it into [Tone.js](https://tonejs.github.io/) to play notes and drums, and devised a syntax to describe the actions of ants and a parser to load it. The result is here: <https://dragoncoder047.github.io/ca-experiments/langton-music/index.html>.

With only 2 colors and 1 state of ant, the result isn't very good. Hopefully I can come up with some better ants that make some more musical music.
