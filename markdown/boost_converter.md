Title: A Boost Converter
Date: 2023-06-07
Series: roboraptor-upgrade
Tags: electronics

The original Roboraptor had dual power supplies. Two "AA" size batteries supplied 3 volts for the logic circuitry, and four batteries in a separarte circuit provided 6 volts for the motors. My redesign of the Roboraptor is designed to run off of a large single-cell 3.7 volt lithium battery -- but the motors run really sluggishly on only 3.7 volts (even though the torque is high as the battery can supply an incredible amount of current). So, to make the motors run faster, I need to increase the voltage.

Besides simply increasing the motor speeds, my idea includes a few more requirements:

1. When the Roboraptor is in a "sleep" state, it can turn off the boost converter to save power.
2. It can artificially reduce the output voltage to make the motors move smoothly and minimize PWM whine at slow speeds.
3. It can monitor the output voltage and current to be able to automatically stop the motors if they are drawing too much current (and trigger a routine to make the robot act "exhausted", perhaps).

This all needs to be controllable in software. In an ideal world, something like this is already implemented and all I have to do is wire it up. Unfortunately, after hours of searhing on multiple sites, I could not find any boost converters that had both of these features. I did find [this boost converter from Polulu](https://www.pololu.com/product/2890) that can be turned off using an enable signal, but this doesn't satisfy any of the other requirements without external current-sensing capabilities, not to mention the output voltage can't be adjusted in software, and it requires an extra GPIO pin for the enable signal (I'm running low on pins!).

So I figured I would have to make one using a microcontroller, and read data and send commands to it over I2C. I first looked up how a boost converter works. It's pretty simple, and I even found [this video](https://www.youtube.com/watch?v=QnUhjnbZ0T8) by Great Scott that even implements a boost converter using an ATtiny85 -- the same microcontroller I am using for peripheral tasks elsewhere in the robot. This is the circuit I settled on:

```schemascii
J1-------------*--L1---*---+D1--*----J2
               |       |        |    J1:Vin J2:Vout
               |       |        |    J3:SDA J4:SCL
        .~~~~. |       |        |    U1:ATtiny85,,PB3,,GND,PB0,PB1,PB2,VCC
       -: U1 :-*       d        |    D1:SB360 L1:220u
    *---:    :--J4  *gQ1  *-R1--*    Q1:nfet:IRL2703
    |  -:    :------*  s  |     +    R1:100k R2:10k C1:68u
  *-|---:    :--J3     |  |     C1   !padding=30!
  | |   .~~~~.         |  |     |    G:chassis
  | *---------------------*-R2--*
  |                    |        |
  G                    G        G
```

GreatScott's code is the bare-bones necessary for a boost converter: it simply monitors an ADC input, which is connected to the output through a resistor divider, and adjusts the PWM duty cycle on another pin controlling the transistor to keep the output voltage steady at the set point (voltage too high = reduce duty cycle; too low = increase duty cycle). In his video, is controlled by another ADC input connected to a potentiometer knob, but I'll be changing it over I2C.

[Previously]({filename}i_got_something.md) I found [this library](https://github.com/rambo/TinyWire) that allows the ATtiny85 to show up as an I2C slave device, and tested it out communicating with my ESP32 (no boost converter code yet). It worked-ish, but some subsequent testing (after that post) revealed that the ESP32 has a nasty silicon bug where it does not tolerate clock stretching (the ATtiny85 clock-stretches extensively because it runs so slow), causing batch reads to fail. Fortunately, there are software workarounds.

## Integration hell

After confirming the I2C code worked, I installed the boost converter code into the ATtiny85 and connected it to the circuit. For comparison purposes I connected a wire to the ATtiny85's reset pin, preventing it from running. The motor only saw the 3.3 volts coming from the regulator, and it ran sluggishly, as expected. When I unplugged the reset wire to turn on the boost converter, the motor quickly gained speed until it stabilized at about twice the 3.3V speed -- indicating that my boost converter is at least working doing that.

Then I tried to change the output voltage over I2C. Now the ATtiny85 didn't even ACK on its own address!

I figured that maybe the interrupts I was using to synchronize the ADC and the PWM signal were causing an issue, so I moved all the code for that out of the interrupt routines and put it in the main loop, so that it would be pre-empted by the I2C interrupt. Still not working... maybe it's running too much code to be able to quickly handle the I2C interrupts fast enough? I'll need to do some more debugging.
