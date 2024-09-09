Title: Hairy Circuit Layout Issues
Date: 2023-01-17
Series: roboraptor-upgrade
Tags: electronics

I'm starting to finalize the circuit boards needed for my Roboraptor upgrade. I am doing everything with THT components, which take up a lot of space, but I can solder by hand easily. Unfortunately, this means everything takes up a lot of space.

The top board, which will go in the same spot as the original board, is limited to about 2 inches by 3 inches of board area and not a lot of vertical space. Fortunately there are a bunch of spaces in the rest of the Roboraptor's structure that I can squeeze a small co-processor circuit board to run a few motors. But there isn't really anywhere else I can put the amplifiers for the audio system.

The electret microphones' preamplifier is a LM358, fixed with resistors to give a gain of +20dB (if I did the math right; it's an arithmetic gain of 100), and conveniently the LM358 is a dual op-amp so I only need one chip for the two microphones.

![LM358 preamp]({attach}circuits/RR_Mic_Preamp.png)

I was running low on pins coming out of the ESP32, so I ditched the MAX98357A (which requires 3 pins for the I<sup>2</sup>S bus) in favor of a simple one-pin solution: use the ESP32's internal DAC. This requires an amplifier, so I turned to the trusty LM386.

![LM386 amplifier]({attach}circuits/RR_Spk_Amp.png)

So far, here's what I need to put on the top:

* Sockets for everything:
    * My ESP32 board
    * The 2 head plugs from the original Roboraptor
    * Connector to the jaw actuator
    * Connector to the tail touch sensors
    * Connector to the high-power I<sup>2</sup>C bus that goes to the motors
* A MCP23008 GPIO expander to watch the touch sensors
* The microphone preamplifier:
    * LM358
    * 8 resistors
    * 2 small capacitors
* The speaker amplifier
    * LM386
    * 2 large capacitors
    * 1 resistor
* 2 2N7000 MOSFET's for amplifying the IR LED's
* Jaw actuator driver:
    * L293D
    * ATtiny85
    * 2 inverters (each a 2N7000 and resistor)

Whew, that's a lot... and that's only one board out of probably, like 5 of them... I have some serious work to do!
