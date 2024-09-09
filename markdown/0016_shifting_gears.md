Title: Shifting Gears
Date: 2022-07-18
Series: roboraptor-upgrade
Tags: electronics, reverse-engineering

Aaah, that's been a nice break from coding. Four weeks with no commits pushed to Phoo. It's a shame I left it in a broken state. I haven't the slightest idea why it's broken --- but then again, all the other times Phoo broke, I never knew why either, and it just "fixed itself" after a while. Hopefully that will happen again.

Lately, I've worked on a different one of my interests: electronics. I ordered a bunch of interesting parts from [Sparkfun](https://www.sparkfun.com) and they arrived yesterday. Before I explain what those were for, let's rewind.

About eight years ago ago (wow, it was that long!) my parents bought me a [Roboraptor](https://wowwee.com/roboraptor-x) for Christmas. I like robots and dragons, so a dragon(ish) robot was the perfect gift for me. I played with that thing so much it eventually broke a couple years ago. It has been sitting on the shelf collecting dust and making me think ever since.

The only thing that I do not like is that the Roboraptor can't be programmed. And for a programmer and computer geek like me, that is the most annoying thing ever.

I had opened it up to try to fix the problem, and unfortunately. I couldn't. But while I had the Roboraptor in pieces on my workbench, I noticed that the motor mechanism is stupid simple: while I expected standard servos or some similar kind of closed-loop control, it was actually open-loop, just a cheap 96:1 gearmotor and some return springs to bring the motor back to center when power was turned off, a "poor man's servo" of sorts. This mechanism is incredibly wasteful of batteries -- the motor must be stalled and drawing maximum current to maintain any position other than middle -- and so I wanted to fix that, too.

From Sparkfun I ordered an [ESP32 Thing Plus C](https://www.sparkfun.com/products/18018) and a bunch of [ATtiny85s](https://www.sparkfun.com/products/9378), plus supporting components, and my idea is to use the ESP32 as the main processor and "talk" to all the ATtiny85s using I^2^C. The ATtiny85s would handle tasks that must be continuously monitored (such as watching the encoders' positions and turning the motors on when they're not where they're supposed to be) that, if done on the ESP32, would at best cause the otherwise fast ESP32 to bog down under a ton of interrupts, and at worst cause janky audio sounds and glitching.

I also ordered an [I^2^S DAC](https://www.sparkfun.com/products/14809) so I can play dragon sound effects from the ESP32. I also found [three](https://github.com/pschatzmann/arduino-SAM) [text-to-speech](https://github.com/pschatzmann/TTS) [libraries](https://github.com/pschatzmann/arduino-flite) that I could add to the ESP32, as well as a [tiny Lisp interpreter](http://www.ulisp.com/show?3TQF) that I could use as a scripting language.

Who knows where this is going to end up? I certainly don't.
