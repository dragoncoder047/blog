Title: Generalized Wire Cellular Automata
Date: 2022-06-14

In fooling around with different variants of the Wireworld cellular automaton I was wondering if Wireworld and its variants can be generalized.

Vanilla Conway's Game of Life and its variants has been generalized, up to the point of being able to express a rule concisely in a single line following a standard format as described [here](https://conwaylife.com/wiki/Cellular_automaton#Life-like_cellular_automata):

* B3/S23 (Life) -- a dead cell is born if it has 3 live neighbors ("B3") and a live cell survives if it has 2 or 3 ("S23").
* B2-a/S12 (Just Friends) -- born if there are 2 live neighbors ("B2") except ("-") if they are adjacent ("a"), and survives if there are 1 or 2 live neighbors ("S12").
* B2/S345/4 (Star Wars) -- cells are born if there are 2 neighbors ("B2"), survive if there are 3, 4, or 5 ("S345") and upon dying, pass through two additional 'dying' states before returning to 'dead' ("G4").
* B3aijn4cw5cek6n/S2-in3-ky4ejntwy5ijnr6cen7c (Wildfire) -- I'm not going to explain this one here!

Now, Wireworld is obviously not one of these rules as stae 0 never changes; but when it is seen as one of those rules confined to a wire, it can be seen that the rule emulated by the wire is B12/S/G3. Going in that vein (some rule confined to a wire) there has been [Wire2](https://conwaylife.com/forums/viewtopic.php?f=11&t=3380) (B2/S/G3 -- Brian's Brain -- confined to a wire), [wireweird](https://conwaylife.com/forums/viewtopic.php?f=11&t=5502&) (B3/S/G3), and [Bliptile](https://conwaylife.com/forums/viewtopic.php?f=11&t=907) (B1/S/G3V, the "V" deoting the von Neumann neighborhood).

While this is useful, it gets old real fast, and especially clumsy and large the more transitions are restricted. This also doesn't cover hybrid rules such as [Wireworld++]({file}wireworld++.md), which includes two separate and largely independent Wireworld universes, and the transition between the two is asymmetric.

Let me begin by defining what exactly a generalized wire cellular automaton is:

1. State 0 (the background) always remains the background. This eliminates construction rules such as WWEJ3 (but as that is an extension of Wireworld, a universal-construction GWCA would naturally also be an extension).
2. There exists a subset of states $S$ such that $S\subset U$.
3. If there are multiple subsets (multiple types of wire), the multiple sets $S_1, S_2, ... S_n$ are partitioned such that all sets are mutually disjoint, that is,
