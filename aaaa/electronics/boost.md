Title: A Boost Converter
Date: 2023-06-07
Series: roboraptor-upgrade
Status: draft

The original Roboraptor had dual power supplies. Two "AA" size batteries supplied 3 volts for the logic circuitry, and four batteries in a separarte circuit provided 6 volts for the motors. My redesign of the Roboraptor is designed to run off of a large single-cell 3.7 volt lithium battery -- but the motors run really sluggishly on only 3.7 volts (even though the torque is high as the battery can supply a lot of current). So, to make the motors run faster, I need to increase the voltage.

Some of the other requirements I had for this is 1. when the Roboraptor is in a "sleep" state, it can turn off the boost converter to save power, 2. it can artificially reduce the output voltage to make the motors move slowly if needed, and 3. monitor the output voltage and current to be able to automatically stop the motors if they are drawing too much current (and trigger a routine to make the robot act "exhausted", perhaps). This all needs to be controllable in software.

Unfortunately, I could not find any boost converters that had both of these features. I found [this boost converter from Polulu](https://www.pololu.com/product/2890) that can be turned off using an enable signal, but this doesn't satisfy any of the other requirements without external current-sensing capabilities -- and it requires an extra GPIO pin to the enable signal (I'm running low on pins!).

So I looked up how a boost converter works. It's pretty simple, and I even found [this video](https://www.youtube.com/watch?v=QnUhjnbZ0T8) by Great Scott that even implements a boost converter using an ATtiny85 -- the same microcontroller I am using for peripheral tasks elsewhere in the robot.

