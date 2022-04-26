Title: Wireworld++
Date: 2022-04-18
Status: draft

Several years ago I discovered the wonderful world of cellular automata.

??? note "What's a cellular automaton? (open this if you don't know)"
    If you don't know what a cellular automaton is, it is simply a geometric tiling of some mathematical space, where each shape is called a "cell" and can be in one of a number of "states", and every time step (called a "generation") each cell looks at the cells around it in some predefined relation (called the "neighborhood") and updates its state according to some set rules.

    Many cellular automata have been devised on many different grids and using many different rules. Most use a square grid of cells (because it's easy to simulate on a computer), but some have been devised that use hexagonal or triangular grids, and in both two and three dimensions. There has even been a cellular automata designed for the Penrose tiling, which, despite being aperiodic, actually works!

    The most heavily-studied one is called **Conway's Game of Life** (due to its creator, the mathematician John Conway) and is on a square grid where each cell can be in one of two states, "alive" or "dead". A dead cell will be "born" and become alive in the next generation if exactly 3 of its 8 neighbors touching it are alive, and an alive cell will remain alive if 2 or 3 of its neighbors are alive.

    I won't bore you with the details of this specific cellular automaton because it has so heavily been researched. Nathaniel Johnston has set up an entire website to host a wiki, forums, several old pages of discoveries from the 1970s-1990s, and even a book he co-authored. That site is <https://conwalife.com/> -- go there if you are interested. You can also find that link at the bottom of every page.

After some Googling I discovered a cellular automata called Wireworld that is designed to simulate electronic circuits. Each of its square cells can be in one of four states, "empty" (which always stays empty, and is shown here in black), "electron head" (which subsequently turns to a tail, and is shown in blue), "electron tail" (which subsequently turns to wire), and "empty wire" (which remains wire unless exactly 1 or 2 of the 8 neighbors is a "head", and is shown in orange.) [Wikipedia page on Wireworld](https://en.wikipedia.org/wiki/Wireworld)

Almost simultaneously with that I discovered a magnificent computer constructed in Wireworld by David Moore and Mark Owen. They also have a rudimentary introduction to Wireworld construction on their website along with an overview of their computer -- <http://quinapalus.com/wi-index.html>. The link to Julien Thevenon's reverse engineering is down, but after some more Googling I found it buried at pages 120-164 of <http://1010.co.uk/org/erdsir_modes_reader.pdf>. I have extracted the relevant pages [here]({attach}quinapalus_computer_reverse_engineering.pdf) so you don't have to scroll, and in case that goes down too.

Here it is, using displayed using Chris Rowett's LifeViewer: (and the RLE file for Golly: [quinapalus_primes.rle]({attach}quinapalus_primes.rle){download="quinapalus_primes.rle"})

```lifeviewer
<< include aaaa/cellular automata/quinapalus_primes.rle >>
[[ X 335 Y 95 STEP 64 ZOOM 1.0 ]]
```

I cobbled together a small Wireworld simulator in [Processing](https://www.processing.org), and made some investigations and modifications to the Quinapalus computer. I am not going to bother posting that anywhere because it is really slow, the graphics are laggy, and you can't make edits mid-simulation. I ended up converting everything to [Golly](http://golly.sourceforge.net) format. (If you don't know what Golly is, it's a cross-platform general purpose cellular automata simulator that uses Bill Gosper's ingenious [Hashlife](https://johnhw.github.io/hashlife/index.md.html) algorithm to run patterns insanely fast. Highly recommend it.)

Unfortunately, the Quinapalus guys did a pretty darn good job of optimizing their computer. Dissatisfied with the massive loops of electrons I searched for another computer in Wireworld and instead discovered another rule. The Wireworld++ rule, as described in [the paper by Gladkikh et al](https://wpmedia.wolfram.com/uploads/sites/13/2018/07/27-1-2.pdf) ([local copy]({attach}wireworld++.pdf)), is a fusion of two "flavors" of Wireworld into one another: a "strong" wireworld and a "weak" wireworld. With one flavor only it behaves exactly like regular Wireworld. But where the two flavors touch it enables creating some very tiny logic gates -- two strong wires touching a weak wire form an XOR gate, and two weak wires into a strong wire form an AND gate.

Here is the Wireworld++ rule file for running it in Golly: [Wireworld++.rule](https://raw.githubusercontent.com/dragoncoder047/wiki/main/Rule%3AWireworld%2B%2B){download="Wireworld++.rule"} The top also contains a Python function that was used to generate it.

And here is a comparison of the Wireworld++ AND and XOR gates along with their conventional Wireworld counterparts:

```lifeviewer
x = 42, y = 16, rule = Wireworld++
34.2C.4C$.C2.C2.C.2C22.C2.C$C.C.2C.C.C.C3.A3C2F12.C.3C$3C.C.2C.C.C9.
5C7.C2.C$C.C.C2.C.2C4.A3C2F9.A2C.7CA$36.C4$30.A4C$C.C.3C.2C5.A5C.F12.
C$.C2.C.C.C.C10.2F3C8.4C$C.C.3C.C6.A5C13.C2.5C$34.4C$35.C$30.A4C!
[[ T 0 PAUSE 1 LOOP 15 ]]
```

Notice how much smaller the Wireworld++ gates are compared to their Wireworld counterparts. All of the constructions discussed in the original paper work, and are smaller than their Wireworld counterparts.

Now, the next thing I noticed with Wireworld++ is the tiny wire crossover. However, it isn't a double channel crossing, meaning that if two signals come in at the same time, they will crash into each other, and one or both will be lost. The equivalent Wireworld crossing is the double-ANDNOT gate, and while bulkier, it still suffers from the same problems:

```lifeviewer
x = 19, y = 14, rule = Wireworld++
A8C$9.C$A7C2F$8.2F9C$8.C$9.10C2$A6C$7.C.C$6.13C$6.C2.C$6.13C$7.C.C$A6C!
[[ T 0 PAUSE 1 LOOP 20 ]]
```

A true double-channel crossing is made with three XOR gates like so:

```{.kroki type="svgbob"}

A ---*-----------.----.
     |           |XOR +--------> B
     '-.----.  .-'----'
       |XOR +--*
     .-'----'  '-.----.
     |           |XOR +--------> A
B ---*-----------'----'
```

and in Wireworld:

```lifeviewer
x = 24, y = 19, rule = WireWorld
.10CAB10C$C22.C$C22.C$C10.2C10.C$C8.2C2.C9.C$C7.C3.4C7.C$.5CBA4.C2.8C
$8.C3.4C$7.4C2.C$7.C2.3C$7.4C2.C$8.C3.4C$.7C4.C2.8C$C7.C3.4C7.C$C8.2C
2.C9.C$C10.2C10.C$C22.C$C22.C$.10CAB10C!
[[ AUTOSTART GPS 15 LOOP 108 ]]
```
