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

Here it is, displayed using Chris Rowett's LifeViewer: (and the RLE file for Golly: [quinapalus_primes.rle]({attach}quinapalus_primes.rle){download="quinapalus_primes.rle"})

```lifeviewer
<< include aaaa/cellular automata/quinapalus_primes.rle >>
[[ STEP 64 ZOOM 1.0 ]]
```

I cobbled together a small Wireworld simulator in [Processing](https://www.processing.org), and made some investigations and modifications to the Quinapalus computer. I am not going to bother posting that anywhere because it is really slow, the graphics are laggy, and you can't make edits mid-simulation. I ended up converting everything to [Golly](http://golly.sourceforge.net) format. (If you don't know what Golly is, it's a cross-platform general purpose cellular automata simulator that uses Bill Gosper's ingenious [Hashlife](https://johnhw.github.io/hashlife/index.md.html) algorithm to run patterns insanely fast. Highly recommend it.)

Unfortunately, the Quinapalus guys did a pretty darn good job of optimizing their computer. Dissatisfied with the massive loops of electrons I searched for another computer in Wireworld and instead discovered another rule. The Wireworld++ rule, as described in [the paper by Gladkikh et al](https://wpmedia.wolfram.com/uploads/sites/13/2018/07/27-1-2.pdf) ([local copy]({attach}wireworld++.pdf)), is a fusion of two "flavors" of Wireworld into one another: a "strong" wireworld and a "weak" wireworld. With one flavor only it behaves exactly like regular Wireworld. But where the two flavors touch it enables creating some very tiny logic gates -- two strong wires touching a weak wire form an XOR gate, and two weak wires into a strong wire form an AND gate.

Here is the Wireworld++ rule file for running it in Golly: [Wireworld++.rule](https://raw.githubusercontent.com/dragoncoder047/wiki/main/Rule%3AWireworld%2B%2B){download="Wireworld++.rule"} The top also contains a Python function that was used to generate it.

And here is a comparison of the Wireworld++ AND and XOR gates (on the left) along with their conventional Wireworld counterparts (on the right), hooked up to period-24 loops that test all the possible inputs (00, 01, 10, and 11) at period 6:

```lifeviewer
x = 58, y = 33, rule = Wireworld++
17.C23.C$17.C23.C$17.C23.C$17.C4.2C2.C3.C.3C6.C$17.C3.C2.C.2C2.C.C2.C
5.C$17.C3.4C.C.C.C.C2.C5.C$17.C3.C2.C.C2.2C.C2.C5.C$17.C3.C2.C.C3.C.
3C6.C$17.C23.C$17.C20.2C.C$17.C19.C2.C$17.C19.C.3C$.10C6.C6.9CB3.C2.C
5.10C$A10.5CF.F4CA10.A2C.7CA10.C$.B4CAB3C13.B9C6.C5.B4CAB3C4$17.C22.C
$17.C22.C$17.C22.C$17.C3.C3.C2.2C2.3C5.C$17.C4.C.C2.C2.C.C2.C4.C$17.C
5.C3.C2.C.3C5.C$17.C4.C.C2.C2.C.C.C5.C$17.C3.C3.C2.2C2.C2.C4.C$17.C
22.C$17.C22.C$17.C22.C$16.2F21.3C$.10C6.F6.9CB5.C.C5.10C$A10.6C.5CA
10.A5C.5CA10.C$.B4CAB3C13.B9C5.3C5.B4CAB3C!
[[ THUMBNAIL AUTOSTART GPS 10 ]]
```

Notice how much smaller the Wireworld++ gates are compared to their Wireworld counterparts. All of the constructions discussed in the original paper work, and are smaller than their Wireworld counterparts.

## Crossovers

One of the focal points in the Wireworld++ paper is the tiny wire crossover. However, it isn't a double channel crossing, meaning that if two signals come in at the same time, they will crash into each other, and one or both will be lost. The equivalent Wireworld crossing is the double-ANDNOT gate, and while bulkier, it still suffers from the same problems:

```lifeviewer
x = 50, y = 7, rule = Wireworld++
9.C9.9CB7.2C$6C2.C.8CA10.A6C2.C.C.8C$6.C2F10.B9C8.5C$7.2FC27.C2.C$7.C
2.C8.10C8.5C$7C4.7CA10.7C2.C.C.8C$19.B4CAB3C7.2C!
[[ THUMBNAIL AUTOSTART GPS 10 ]]
```

A true double-channel crossing is made with three XOR gates like so:

```{.kroki type="svgbob"}
A ->-*------->-----.-----.
     |             | XOR +--------> B
     '-.-----.   .-'-----'
       | XOR +->-*
     .-'-----'   '-.-----.
     |             | XOR +--------> A
B ->-*------->-----'-----'
```

and in Wireworld:

```lifeviewer
x = 37, y = 13, rule = Wireworld++
23.2C$21.2C2.C$20.C3.4C$.9CB7.2C4.C2.2C$A10.A6C2.C3.4C.8C$.B9C8.4C2.C
$19.C2.3C$.10C8.4C2.C$A10.7C2.C3.4C.8C$.B4CAB3C7.2C4.C2.2C$20.C3.4C$
21.2C2.C$23.2C!
[[ THUMBNAIL AUTOSTART GPS 10 ]]
```

Knowing how small the XOR gate is in Wireworld++, I figured the crossover could be made much smaller -- and indeed it can:

```lifeviewer
x = 37, y = 13, rule = Wireworld++
23.2C$21.2C2.C$20.C3.4C$.9CB7.2C4.C2.2C$A10.A6C2.C3.4C.8C$.B9C8.4C2.C
$19.C2.3C$.10C8.4C2.C$A10.7C2.C3.4C.8C$.B4CAB3C7.2C4.C2.2C$20.C3.4C$
21.2C2.C$23.2C!
[[ THUMBNAIL AUTOSTART GPS 10 ]]
```

However after playing around a little more I made two iterations that were successively smaller:

```lifeviewer
x = 37, y = 7, rule = Wireworld++
.9CB13.2C.F$A10.A8C2.FC2.F.9C$.B9C9.C2F2.C.F$22.F2C$.10C9.C2F2.C.F$A
10.9C2.FC2.F.9C$.B4CAB3C13.2C.F!
[[ THUMBNAIL AUTOSTART GPS 10 ]]
```

```lifeviewer
x = 35, y = 7, rule = Wireworld++
.9CB$A10.A8C.2F.11C$.B9C9.C.FC$21.2F$.10C9.C.FC$A10.9C.2F.11C$.B4CAB
3C!
[[ THUMBNAIL AUTOSTART GPS 10 ]]
```

## Multiplexers

Looking back at the Quinapalus computer, I saw one big place where it could be optimized: the multiplexer that loads the new data into the memory loops.

The multiplexer they used was wired like this:

```{.kroki type="svgbob"}
     LOOP
.~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.
:                 .--------.  | .--------.
: .----<-- OUT ---| ANDNOT |<---| ANDNOT |<-------- DATA
: |               '--------'  : '--------'
: v                   ^       :     ^
: |                   |       :     |
: |               .--------.  :     |
: '------>--------|  OR    |<-------*-------------- SELECT
:                 '--------'  :
'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
```

In this demo, you can see the loop starts out originally with 1100 in it, and then 1010 is written to it.

```lifeviewer
x = 48, y = 9, rule = Wireworld++
9C.7CAB$9.C9.C.C$9.C10.3C$.C.C.C.C2.7C2.C.C.C.C$17.B.C4.41C2B4CAB4C2B
4CA$16.3A3.2C.C$17.C3.C$18.4C$22.36CAB4CAB4CAB4CA!
[[ GPS 10 T 24 PAUSE 1 T 72 PAUSE 1 LOOP 120 THUMBNAIL ]]
```

*(The loop was originally period 96, to fit 16 bits, but I shortened to to period 24, for the sake of brevity.)*


After some work, I reworked the multiplexer to use this design:

```{.kroki type="svgbob"}
     LOOP
.~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.
:                 .--------.  | .--------.
: .----<-- OUT ---|  XOR   |<---|  AND   |<-------- DATA
: |               '--------'  : '--------'
: v                   ^       :     ^
: |                   |       :     |
: |               .--------.  :     |
: '------>--------| ANDNOT |<-------*-------------- SELECT
:                 '--------'  :
'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
```

and the multiplexer was able to be shrunk to this:

```lifeviewer
x = 64, y = 5, rule = Wireworld++
19.4C.F20CAB4C2B4CAB4CB$17.2F4.C$8C.8CF.C.C2.F$8.C11.25CAB4CAB4CAB4CA
$9.3CBA4CBA.C!
[[ GPS 10 T 24 PAUSE 1 T 72 PAUSE 1 LOOP 120 THUMBNAIL ]]
```

While I was at it I also made a tiny demultiplexer too:

```lifeviewer
x = 44, y = 9, rule = Wireworld++
29.2C.2C.C$2C15.9CB2.C2.2C.C$.C10.4CA10.A2.C.C2.C$3C.6C.F5.B9C2.2C.2C
.2C$10.C$3C.4C2F.F5.10C2.2C3.C2.3C2.C$C.C5.F.6CA10.C.C.C.C.C2.C2.C.C$
3C14.B4CAB3C2.C.C.3C2.C2.3C$29.2C2.C.C2.C2.C.C!
[[ THUMBNAIL AUTOSTART GPS 10 ]]
```

# Adder and Incrementor

The next part of the computer that I improved was the serial adder.
