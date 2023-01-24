Title: Schemascii &pm; 1
Date: 2023-01-24
Categories: python, electronics

I spent the last two days fooling around with my half-idea of a diagramming program, Schemascii. What it's supposed to do is be able to make a diagram of a circuit (like the ones you might make in Eagle or KiCad before you plan a circuit board) out of a messy ASCII-art representation.

So far, I have implemented the routines that scan the file first for the components, and second for the connecting wires. The wires are also able to be rendered, but it's a little buggy.

For testing I have been using this diagram of a 555-timer charge-pump polarity inverter:

```
*--BAT1+--*-------*---*
|         |       |   |
|         R1    .~~~. |
|         |     :   :-*
|         o-----:   :---+C2--*--D2+--*----------J1
|         |     :U1 :        |       |
|        R2     :555:        |       |
|         |   *-:   :-*      |       |
|         C1  | :   : |      +       C3
|         |   *-:   : C4     D1      +
|         *---* .~~~. |      |       |
|         |       |   |      |       |
*---------*-------*---*------*-------*----------J2

BAT1:5
R1:10k
R2:100k
C1:10000p
C2:10u
C3:100u
C4:10p
D1:1N4001
D2:1N4001
U1:NE555,VCC,DIS,_TR,TH,GND,CTL,OUT,_RST
J1:-5V
J2:GND
```

So far, my program is able to run aroud and grab all of the components off the diagram, and also grab the "BOM data" that I placed at the bottom. It ends up in this big dictionary:

```py3
{   Cbox(p1=(3+0j), p2=(7+0j), type='BAT', id=1): [   Terminal(pt=(7+0j), flag='+', side=<Side.RIGHT: 1>),
                                                      Terminal(pt=(2+0j), flag=None, side=<Side.LEFT: 3>)],
    Cbox(p1=(16+2j), p2=(21+10j), type='U', id=1): [   Terminal(pt=(21+3j), flag=None, side=<Side.RIGHT: 1>),
                                                       Terminal(pt=(21+4j), flag=None, side=<Side.RIGHT: 1>),
                                                       Terminal(pt=(21+7j), flag=None, side=<Side.RIGHT: 1>),
                                                       Terminal(pt=(18+11j), flag=None, side=<Side.BOTTOM: 2>),
                                                       Terminal(pt=(15+4j), flag=None, side=<Side.LEFT: 3>),
                                                       Terminal(pt=(15+7j), flag=None, side=<Side.LEFT: 3>),
                                                       Terminal(pt=(15+9j), flag=None, side=<Side.LEFT: 3>)],
    Cbox(p1=(10+2j), p2=(12+2j), type='R', id=1): [   Terminal(pt=(10+1j), flag=None, side=<Side.TOP: 0>),
                                                      Terminal(pt=(10+3j), flag=None, side=<Side.BOTTOM: 2>)],
    Cbox(p1=(25+4j), p2=(27+4j), type='C', id=2): [   Terminal(pt=(27+4j), flag=None, side=<Side.RIGHT: 1>),
                                                      Terminal(pt=(24+4j), flag='+', side=<Side.LEFT: 3>)],
    Cbox(p1=(32+4j), p2=(34+4j), type='D', id=2): [   Terminal(pt=(34+4j), flag='+', side=<Side.RIGHT: 1>),
                                                      Terminal(pt=(31+4j), flag=None, side=<Side.LEFT: 3>)],
    Cbox(p1=(48+4j), p2=(50+4j), type='J', id=1): [   Terminal(pt=(47+4j), flag=None, side=<Side.LEFT: 3>)],
    Cbox(p1=(9+6j), p2=(11+6j), type='R', id=2): [   Terminal(pt=(10+5j), flag=None, side=<Side.TOP: 0>),
                                                     Terminal(pt=(10+7j), flag=None, side=<Side.BOTTOM: 2>)],
    Cbox(p1=(10+8j), p2=(12+8j), type='C', id=1): [   Terminal(pt=(10+7j), flag=None, side=<Side.TOP: 0>),
                                                      Terminal(pt=(10+9j), flag=None, side=<Side.BOTTOM: 2>)],
    Cbox(p1=(37+8j), p2=(39+8j), type='C', id=3): [   Terminal(pt=(37+7j), flag=None, side=<Side.TOP: 0>),
                                                      Terminal(pt=(37+9j), flag='+', side=<Side.BOTTOM: 2>)],
    Cbox(p1=(22+9j), p2=(24+9j), type='C', id=4): [   Terminal(pt=(22+8j), flag=None, side=<Side.TOP: 0>),
                                                      Terminal(pt=(22+10j), flag=None, side=<Side.BOTTOM: 2>)],
    Cbox(p1=(29+9j), p2=(31+9j), type='D', id=1): [   Terminal(pt=(29+8j), flag='+', side=<Side.TOP: 0>),
                                                      Terminal(pt=(29+10j), flag=None, side=<Side.BOTTOM: 2>)],
    Cbox(p1=(48+12j), p2=(50+12j), type='J', id=2): [   Terminal(pt=(47+12j), flag=None, side=<Side.LEFT: 3>)]}
```

!!! info "Note on the complex numbers"
    I am (ab)using Python's `:::py3 complex` number as a point or vector, but this kind of makes sense -- think the complex plane. The rationale for this is a lot of the mathematical operations I need to do with points are already built-in on `:::py3 complex` objects, such as finding the midpoint (`:::py3 (p1 + p2) / 2`), finding the length (`:::py3 abs(pt)`), finding the angle (`:::py3 cmath.phase(pt)`), etc. [`svgpathtools` takes the same approach.](https://github.com/mathandy/svgpathtools#:~:text=%23%20Coordinates%20are%20given%20as%20points%20in%20the%20complex%20plane)

The code for the wire finding is also able to render the wires to SVG, and produces this output on the same circuit:

```xml
<g class="wire"><line x1="2.0" y1="0.0" x2="0.0" y2="1.2246467991473532e-16"></line><line x1="0.0" y1="12.0" x2="6.123233995736766e-17" y2="0.0"></line><line x1="10.0" y1="12.0" x2="0.0" y2="12.0"></line><line x1="18.0" y1="12.0" x2="10.0" y2="12.0"></line><line x1="10.0" y1="10.0" x2="10.0" y2="12.0"></line><line x1="22.0" y1="12.0" x2="18.0" y2="12.0"></line><line x1="18.0" y1="11.0" x2="19.0" y2="11.0"></line><line x1="14.0" y1="10.0" x2="10.0" y2="10.0"></line><line x1="10.0" y1="9.0" x2="11.0" y2="9.0"></line><line x1="29.0" y1="12.0" x2="22.0" y2="12.0"></line><line x1="22.0" y1="10.0" x2="22.0" y2="12.0"></line><line x1="14.0" y1="9.0" x2="14.0" y2="11.0"></line><line x1="37.0" y1="12.0" x2="29.0" y2="12.0"></line><line x1="29.0" y1="10.0" x2="29.0" y2="12.0"></line><line x1="15.0" y1="9.0" x2="16.0" y2="9.0"></line><line x1="14.0" y1="7.0" x2="14.0" y2="9.0"></line><line x1="47.0" y1="12.0" x2="37.0" y2="12.0"></line><line x1="37.0" y1="10.0" x2="37.0" y2="12.0"></line><line x1="15.0" y1="7.0" x2="16.0" y2="7.0"></line></g><g class="wire"><line x1="10.0" y1="0.0" x2="10.0" y2="2.0"></line><line x1="18.0" y1="0.0" x2="10.0" y2="1.2246467991473532e-16"></line><line x1="8.0" y1="0.0" x2="10.0" y2="0.0"></line><line x1="22.0" y1="0.0" x2="18.0" y2="1.2246467991473532e-16"></line><line x1="18.0" y1="1.0" x2="19.0" y2="1.0"></line><line x1="22.0" y1="3.0" x2="22.0" y2="0.0"></line><line x1="21.0" y1="3.0" x2="22.0" y2="3.0"></line></g><g class="wire"><line x1="15.0" y1="4.0" x2="10.0" y2="4.0"></line></g><g class="wire"><line x1="23.0" y1="4.0" x2="20.0" y2="4.0"></line></g><g class="wire"><line x1="29.0" y1="4.0" x2="26.0" y2="4.0"></line><line x1="31.0" y1="4.0" x2="29.0" y2="4.0"></line><line x1="29.0" y1="7.0" x2="29.0" y2="4.0"></line></g><g class="wire"><line x1="37.0" y1="4.0" x2="34.0" y2="4.0"></line><line x1="47.0" y1="4.0" x2="37.0" y2="4.0"></line><line x1="37.0" y1="7.0" x2="37.0" y2="4.0"></line></g><g class="wire"><line x1="22.0" y1="7.0" x2="22.0" y2="9.0"></line><line x1="21.0" y1="7.0" x2="22.0" y2="7.0"></line></g>
```

When put into a `:::xml <svg>` and styled, it reveals a crapload of bugs:

<style>svg.schemascii {
    background: black;
}

svg.schemascii .wire {
    filter: drop-shadow(0 0 0.5px var(--sch-wireshadow, yellow));
}

svg.schemascii .wire line {
    stroke: var(--sch-wirecolor, blue);
    stroke-width: 0.7;
    stroke-linecap: round;
    transition-duration: 0.2s;
}

svg.schemascii .wire:hover {
    --sch-wirecolor: red;
    --sch-wireshadow: lime;
}</style>
<svg class="schemascii" viewBox="-1 -1 50 15" width="500" height="150" xmlns="http://www.w3.org/2000/svg">
<g class="wire"><line x1="2.0" y1="0.0" x2="0.0" y2="1.2246467991473532e-16"></line><line x1="0.0" y1="12.0" x2="6.123233995736766e-17" y2="0.0"></line><line x1="10.0" y1="12.0" x2="0.0" y2="12.0"></line><line x1="18.0" y1="12.0" x2="10.0" y2="12.0"></line><line x1="10.0" y1="10.0" x2="10.0" y2="12.0"></line><line x1="22.0" y1="12.0" x2="18.0" y2="12.0"></line><line x1="18.0" y1="11.0" x2="19.0" y2="11.0"></line><line x1="14.0" y1="10.0" x2="10.0" y2="10.0"></line><line x1="10.0" y1="9.0" x2="11.0" y2="9.0"></line><line x1="29.0" y1="12.0" x2="22.0" y2="12.0"></line><line x1="22.0" y1="10.0" x2="22.0" y2="12.0"></line><line x1="14.0" y1="9.0" x2="14.0" y2="11.0"></line><line x1="37.0" y1="12.0" x2="29.0" y2="12.0"></line><line x1="29.0" y1="10.0" x2="29.0" y2="12.0"></line><line x1="15.0" y1="9.0" x2="16.0" y2="9.0"></line><line x1="14.0" y1="7.0" x2="14.0" y2="9.0"></line><line x1="47.0" y1="12.0" x2="37.0" y2="12.0"></line><line x1="37.0" y1="10.0" x2="37.0" y2="12.0"></line><line x1="15.0" y1="7.0" x2="16.0" y2="7.0"></line></g><g class="wire"><line x1="10.0" y1="0.0" x2="10.0" y2="2.0"></line><line x1="18.0" y1="0.0" x2="10.0" y2="1.2246467991473532e-16"></line><line x1="8.0" y1="0.0" x2="10.0" y2="0.0"></line><line x1="22.0" y1="0.0" x2="18.0" y2="1.2246467991473532e-16"></line><line x1="18.0" y1="1.0" x2="19.0" y2="1.0"></line><line x1="22.0" y1="3.0" x2="22.0" y2="0.0"></line><line x1="21.0" y1="3.0" x2="22.0" y2="3.0"></line></g><g class="wire"><line x1="15.0" y1="4.0" x2="10.0" y2="4.0"></line></g><g class="wire"><line x1="23.0" y1="4.0" x2="20.0" y2="4.0"></line></g><g class="wire"><line x1="29.0" y1="4.0" x2="26.0" y2="4.0"></line><line x1="31.0" y1="4.0" x2="29.0" y2="4.0"></line><line x1="29.0" y1="7.0" x2="29.0" y2="4.0"></line></g><g class="wire"><line x1="37.0" y1="4.0" x2="34.0" y2="4.0"></line><line x1="47.0" y1="4.0" x2="37.0" y2="4.0"></line><line x1="37.0" y1="7.0" x2="37.0" y2="4.0"></line></g><g class="wire"><line x1="22.0" y1="7.0" x2="22.0" y2="9.0"></line><line x1="21.0" y1="7.0" x2="22.0" y2="7.0"></line></g>
</svg>

You can mouse over the wires here to see what is connected to what...

...and this reveals the length-2 parts of the wires are getting yanked weirdly to the side, and the length-1 wires aren't getting rendered at all. This is a cause of great frustration for me, because it doesn't make sense that it doesn't render length-1 wires at all. They need to be rendered!

I'm guessing half of the bugs here in my code are caused by stupid off-by-one errors in the search loops, and the rest are just bad algorithms on my part. I really hope I can get these fixed!
