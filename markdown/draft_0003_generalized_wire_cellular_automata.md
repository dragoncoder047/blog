Title: Generalized Wire Cellular Automata
Date: 2022-06-16
Status: draft
Tags: cellular-automata, programming

In fooling around with different variants of the Wireworld cellular automaton I was wondering if Wireworld and its variants can be generalized.

Vanilla Conway's Game of Life and its variants has been generalized, up to the point of being able to express a rule concisely in a single line following a standard format (called Hensel notation after the guy who invented it, Alan Hensel) as described [here](https://conwaylife.com/wiki/Cellular_automaton#Life-like_cellular_automata):

* `B3/S23` (Life) -- a dead cell is born if it has 3 live neighbors (`B3`) and a live cell survives if it has 2 or 3 (`S23`).
* `B2-a/S12` (Just Friends) -- born if there are 2 live neighbors (`B2`) except (`-`) if they are adjacent (`a`), and survives if there are 1 or 2 live neighbors (`S12`).
* `B2/S345/G4` (Star Wars) -- cells are born if there are 2 neighbors (`B2`), survive if there are 3, 4, or 5 (`S345`) and upon dying, pass through two additional 'dying' states before returning to 'dead' (`/4`).
* `B3aijn4cw5cek6n/S2-in3-ky4ejntwy5ijnr6cen7c` (Wildfire) -- I'm not going to explain this one here!

Now, Wireworld is obviously not one of these rules as state 0 never changes; but when it is seen as one of those rules confined to a wire (state 3 -- wire -- as the "background", state 1 as "live", state 2 as "dying"), it can be seen that the rule emulated by the wire is `B12/S/G3`. Going in that vein (some rule confined to a wire) there has been [Wire2](https://conwaylife.com/forums/viewtopic.php?f=11&t=3380) (`B2/S/G3` -- Brian's Brain -- confined to a wire), [wireweird](https://conwaylife.com/forums/viewtopic.php?f=11&t=5502&) (`B13/S/G3`), and [Bliptile](https://conwaylife.com/forums/viewtopic.php?f=11&t=907) (`B1/S/G3V`, the `V` denoting the von Neumann neighborhood).

While this is useful, it gets old real fast, and especially clumsy and large the more transitions are restricted. This also doesn't cover hybrid rules such as [Wireworld++]({filename}0011_wireworld.md), which includes two separate and largely independent Wireworld universes, and the transition between the two is asymmetric.

Let me begin by defining what exactly a generalized wire cellular automaton is:

1. State $0$ (the background) always remains the background. This forbids patterns from expanding and eliminates construction rules such as WWEJ3 (but as that is an extension of Wireworld, a universal-construction GWCA would naturally also be an extension).
2. If there are multiple types of wire, the multiple subsets of states $S_1, S_2,...S_n$ are partitioned such that all sets are mutually disjoint from each other, that is, $S_1\cup S_2 ...\cup S_n\equiv U$ and $S_p\cap S_q \equiv\emptyset\longleftrightarrow p\not = q$.
3. No cell in a state $s_1$ where $s_1\in S_k$ will ever transition to a state $s_2$, $s_2 \not\in S_k$ -- that is, a cell in some wire type will always remain the same wire type.
4. Each subset $S$ can each be partitioned into $n$ subsets of types $T_n$, $1\le n\le 4$.
5. If a cell in state $p$, $p\in T_k$, changes state to a new state $q$, then $q\in T_{k+1}$. Alternatively, if $x$ and $y$ are states, $x\in T_k$, and $y\in T_k$, a cell cannot transition from $x$ to $y$ without going through one or more additional states.

*[GWCA]: Generalized Wire Cellular Automata

The Wireworld++ rule I discovered fits these rules: States 1, 2, and 3 are the "strong" wire type, and 4, 5, and 6 are the "weak" type. The strong type always stays the strong type and the weak type always stays the weak type. 1 always changes to 2, 2 always changes to 3, and 3 changes back to 1. Likewise, 4 changes to 5, 5 to 6, and 6 back to 4. State 0 remains 0.

Now, under those constraints, how to serialize this into a rule string?

My first idea was simply an extension of the B/S notation used above: repeat a rule for each wire type separated by commas, and for the asymmetric transitions insert `+N:` (N being the index of the extra wire type, starting from 0) and followed by the additional transitions from that wire. The whole rule stars with `GW` do designate it as a GWCA rulestring.

Using that notation, Wireworld is `GWB12/S/3`. Wireworld++ is `GWB12/S/3+1:B2,B12/S/3+0:B1`. Pushing it even further, Lode Vandevenne's [WireWorldRgb](https://lodev.org/ca/wireworldrgb.html) is `GWB12/S/3+2:B12,B1/S/3+0:B1,B2/S/3+1:B1`. WireWorldRYGB (same page) is `GWB12/S/3+3:B1+1:B2,B12/S/3+0:B12,B12/S/3+3:B1+3:B2,B12/S/3+2:B12` (Whew!)

Now, that is getting a little cumbersome even for only three or four types of wire. [LLLL](https://lodev.org/ca/llll.html) has *eight* -- I'm not going to even try that one.

And this notation also doesn't cover four-state wire types that have separate "on" and "off" wires (such as LLLL) or multiple different types of "head" or "tail", i.e. some $T$ sets have more than one element, or where the "tail" lasts longer than one generation (such as NoTimeAtAll).
