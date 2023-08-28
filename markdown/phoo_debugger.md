Title: Debugger, Almost
Date: 2022-12-19
Tags: programming, phoo, javascript

Today I started work on the Phoo debugger. As-is, it is very simple -- I already programmed in a "tick" function into Phoo that gets called every item, and so my debugger only needs to patch itself into this function.

However, the three buttons -- "Into", "Over", and "Out" -- caused me some headache.

The behavior of each, while completely different, is all related to a "hide depth", which causes the debugger to stop breaking if the return stack gets deeper than the "hide depth".

Implementing this na&iuml;vely would increment the "hide depth" when you click "Into", decrement it when you click "Out", and do nothing (except run one step) when you click "Over".

I quickly discovered that this is badly bugged code. It assumes that every time you click "Into", there is actually something to jump into, but what if there isn't? The "hide depth" still gets incremented, and when code proceeds to something to jump into, the debugger jumps in, even if you pressed "Over" or "Out", not "Into".

So I tried another approach: the increment or decrement is only applied if the return stack length changes on that tick. Unfortunately, that caused a lot more bugs than it fixed.

I'm still not sure how to do it properly; maybe there's no correct way, only the one that works best. Will see what happens later.
