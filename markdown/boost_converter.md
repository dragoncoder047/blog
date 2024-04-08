Title: Not Your Daddy's Boost Converter
Date: 2023-06-07
Modified: 2024-04-08
Series: roboraptor-upgrade
Tags: electronics, youtube

The original Roboraptor had dual power supplies. Two "AA" size batteries supplied 3 volts for the logic circuitry, and four batteries in a separarte circuit provided 6 volts for the motors. My redesign of the Roboraptor is designed to run off of a large single-cell 3.7 volt lithium battery -- but the motors run really sluggishly on only 3.7 volts (even though the torque is high as the battery can supply an incredible amount of current). So, to make the motors run faster, I need to increase the voltage.

<youtube id="NnDvN9RbQGY?si=ahxCAqWVCsQAkOef">

On top of that, my idea includes a few more requirements:

1. When the Roboraptor is in a "sleep" state, it can turn off the boost converter to save power.
2. It can artificially reduce the output voltage to make the motors move smoothly and minimize PWM whine at slow speeds.
3. It can monitor the output voltage and current to be able to automatically stop the motors if they are drawing too much current (and trigger a routine to make the robot act "exhausted", perhaps).

This all needs to be controllable in software. In an ideal world, something like this is already implemented and all I have to do is wire it up. Unfortunately, after hours of searhing on multiple sites, I could not find any boost converters that had both of these features. I did find [this boost converter from Polulu](https://www.pololu.com/product/2890) that can be turned off using an enable signal, but this doesn't satisfy any of the other requirements without external current-sensing capabilities, not to mention the output voltage can't be adjusted in software, and it requires an extra GPIO pin for the enable signal (I'm running low on pins!).

So I figured I would have to make one using a microcontroller, and read data and send commands to it over I2C. I first looked up how a boost converter works. It's pretty simple, and I even found [this video](https://www.youtube.com/watch?v=QnUhjnbZ0T8) by Great Scott that even implements a boost converter using an ATtiny85 -- the same microcontroller I am using for peripheral tasks elsewhere in the robot. This is the circuit I settled on:

```schemascii
!padding=30!   J1 R1:100k R2:10k C1:1000u
G:chassis      | D1:SB360 L1:220u Q1:nfet:IRLZ44N
J3:SDA J4:SCL  | U1:ATtiny85,,PB3,,GND,PB0,PB1,PB2,VCC
J1:Vin J2:Vout *--L1###--*--+D1--*---*---J2
               |         |       |   |
               |         |       +   |
        .~~~~. |         |       C1  |
       -: U1 :-*         d       |   R1
  *-----:    :--J4    *gQ1       G   |
  |    -:    :--------*  s           |
  |  *--:    :--J3       G  *--------*
  |  |  .~~~~.              |        |
  |  G                      |        R2
  |                         |        |
  *-------------------------*        G
```

GreatScott's code is the bare-bones necessary for a boost converter: it simply monitors an ADC input, which is connected to the output through a resistor divider, and adjusts the PWM duty cycle on another pin controlling the transistor to keep the output voltage steady at the set point (voltage too high = reduce duty cycle; too low = increase duty cycle). In his video, the setpoint is controlled by another ADC input connected to a potentiometer knob, but I'll be changing it over I2C.

[Previously]({filename}i_got_something.md) I found [this library](https://github.com/rambo/TinyWire) that allows the ATtiny85 to show up as an I2C slave device, and tested it out communicating with my ESP32 (no boost converter code yet). It worked-ish, but some subsequent testing (after that post) revealed that ~~the ESP32 has a nasty silicon bug where it does not tolerate clock stretching (the ATtiny85 clock-stretches extensively because it runs so slow), causing batch reads to fail~~. Fortunately, there are software workarounds. EDIT -- such as *fixing my own code*. I was helped a lot in this regard by switching to Spence Konde's [ATTinyCore](https://github.com/SpenceKonde/ATTinyCore/), which includes a built-in fork of the TinyWire library linked above as well as extensive documentation.

## Integration, hell and back

After confirming the I2C code worked, I installed the boost converter code into the ATtiny85 and connected it to the circuit. For comparison purposes I connected a wire to the ATtiny85's reset pin, preventing it from running. The motor only saw the 3.3 volts coming from the regulator, and it ran sluggishly, as expected. When I unplugged the reset wire to turn on the boost converter, the motor quickly gained speed until it stabilized at about twice the 3.3V speed -- indicating that my boost converter is at least working doing that.

Then I tried to change the output voltage over I2C. Now the ATtiny85 didn't even ACK on its own address!

After a *lot* of debugging, a [month-long rabbit hole](https://github.com/technoblogy/ulisp-esp/issues/75) trying to figure out why reads didn't work, and finding out I was using several outdated packages (and updating), I finally, at long last, got the voltage to change by sending commands over I2C. Whew!!

The [code used is on GitHub](https://github.com/dragoncoder047/super85/tree/master/smartboost). And the circuit is above.
