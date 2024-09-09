Title: Error: out of memory
Date: 2023-07-23
Modified: 2023-07-28
Series: roboraptor-upgrade
Tags: programming, electronics, c

I've been doing a little bit of everything lately. I've done a little work on PICKLE, trying to implement it first in Python so I don't have to worry about the garbage collector. (The pattern-matching code is extremely complicated and screwed with my brain until I realized that I'm basically writing a regular expression engine, which just added to the confusion.) I made some more headway on the text-adventure game engine I [mused]({filename}0036_a_very_confusing_data_model.md) about, starting with a pseudo-scripting language that is embeddable in a JSON document, and some Python code to run it ([this mess](https://github.com/dragoncoder047/json_runner)). I got a few new Lispy features added to uLisp and David even [mentioned](http://forum.ulisp.com/t/ulisp-extensions-add-catch-throw-and-backquote/1249) them on the uLisp forum. The boost converter mentioned previously I got working, and I've published the code and circuit [on Github](https://github.com/dragoncoder047/super85/tree/master/smartboost).

The next thing I am working on is rather simple: a motor controller, that's all. When it's done, it will end up in the super85 repository along with the boost converter.

The motor is hooked up to an L293D H-bridge and an AS5600 absolute encoder. You may recognize this one as the exact same encoder I discovered inside of the Feedback 360 servo -- in fact, it's the *same physical IC* in play here -- I bought the Feedback 260 precisely for the encoder.

The ATtiny85 implements a rather simple algorithm to allow the host microcontroller to give high-level commands. The ATtiny85 is sent a target position and a maximum speed; it then checks the motor's position and sets the target velocity to positive or negative of the maximum speed depending on the error in position; then in turn it checks the motor's velocity and increments or decrements the current PWM power depending on the error in velocity. Essentially, it's a proportional controller with $K_p = \infty$ watching the position and controlling the setpoint of a pure integral controller with a very large $K_i$ watching the velocity.

The AS5600 is configured to output the position encoded as the duty cycle of a 910 Hz PWM signal, and the ATtiny85 is able to read that using a combination of a hardware timer and a pin-change interrupt. It's also conveniently able to use the input PWM signal as a stable timebase to base speed calculations upon.

The vexing part of the code is actually calculating the speed. Doing this is not just as simple as subtracting the old position from the new position every tick, for a number of reasons.

The interrupt routine outputs the current angle as a number in the range of 0 to 255. The interrupt fires at 910 Hz. Now, if the position were to change by only 1/256th every interrupt, the *minimum* speed would be a whopping 213 RPM, which is way too high for my application. The maximum speed representable in a signed 8-bit value (127) represents an equally-ridiculous 27,000 RPM, which isn't even physically possible to achieve using this setup due to Nyquist sampling problems.

The solution I came up with is to compute a rolling sum of the last *N* values -- essentially a rolling average, but multipled by the window size (and then the back-to-back divide-multiply can be eliminated). The range of speeds appropriate for my application (around 0.5 - 50 RPM) results in an *N* of 512.

This is a problem: the ATtiny85 only has 512 bytes of RAM. Eating up the the *entire* RAM for the buffer of the last 512 values ain't gonna happen -- there won't be any remaining space for *anything* else, and there's no way, even with some clever assembly, I'm going to be able to pack everything else into the 32 CPU registers.

So this is a very difficult problem to solve, one that I have not yet been able to hurdle. It is not something I'm going to give up on either.
