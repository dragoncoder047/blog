Title: Well, I Got Something...
Date: 2023-03-05
Series: roboraptor-upgrade

Today I did a quick test of my little ATtiny85 microcontrollers' capabilities. I had them sitting in a jar for a while, and I wanted to see if I could use them in conjunction as a coprocessor to manage some mundane task like regulating a motor. I have previously written I do not like the way the motors are mounted in my old Roboraptor, and I was thinking if I removed the springs and added a position sensor, I could operate the motors as if they were servos. Unfortunately, although I can find analog Hall-effect position sensors for dirt cheap, I'm not even sure it one can just buy a bare servo controller chip without also buying the motor and gearbox it goes in. At any rate, I never found one!

The ATtiny85's I had bought seem like a logical solution: They have ADC pins for reading the position sensor, and PWM pins for controlling the speed of a motor. Additionally, there is [a library](https://github.com/rambo/TinyWire/) that can implement I^2^C in software, so the ATtiny85 can communicate with the master.

I also bought some L293D motor drivers, and they seemed simple to wire up to the ATtiny85: One pin for forward, one pin for backward, and the enable pin permanently pulled high.

Unfortunately, the only available pins for the I^2^C library occupied one of the only two available PWM pins on the ATtiny85, so I got creative. Instead of having a forward and backward, pin, I had a speed and direction pin. The direction pin, which can't do PWM, is connected to the forward input of the L293D, and through an inverter into the backward input. The speed control pin feeds into the enable input.

Just to test if the ATtiny85 could also handle reading the ADC while it is handling the I2C bus at the same time, I connected a potentiometer to the last open pin, which happened to be an ADC pin (whew!) and reprogrammed the ATtiny85 to read the ADC. The master code simply reads the ADC register of the ATtiny85, translates it into a speed and direction, and sends it back to the ATtiny85 which then controls the motor.

Here's the code for both, as reference:

=== "ATtiny85"
    ```ino
    #define I2C_SLAVE_ADDRESS 0x4 // the 7-bit address (remember to change this when adapting this example)
    #include <TinyWireS.h> // Get this from https://github.com/rambo/TinyWire
    #ifndef TWI_RX_BUFFER_SIZE
    #define TWI_RX_BUFFER_SIZE (16) // The default buffer size, though we cannot actually affect it by defining it in the sketch
    #endif
    volatile uint8_t i2c_regs[] = { // The "registers" we expose to I2C
        0x0, // Speed
        0x0, // Direction
        0x0  // ADC
    };
    const byte reg_size = sizeof(i2c_regs);
    volatile byte reg_position; // Tracks the current register pointer position
    void requestEvent() {  
        TinyWireS.send(i2c_regs[reg_position]);
        reg_position++; // Increment the reg position on each read, and loop back to zero
        if (reg_position >= reg_size) reg_position = 0;
    }
    void receiveEvent(uint8_t howMany) {
        if (howMany < 1) return; // Sanity-check
        if (howMany > TWI_RX_BUFFER_SIZE) return; // Also insane number
        reg_position = TinyWireS.receive();
        howMany--;
        if (!howMany) return; // This write was only to set the buffer for next read
        while (howMany--) {
            i2c_regs[reg_position] = TinyWireS.receive();
            reg_position++;
            if (reg_position >= reg_size) reg_position = 0;
        }
    }
    void setup() {
        pinMode(4, OUTPUT); // Dir control
        pinMode(1, OUTPUT); // Speed control
        digitalWrite(1, LOW);
        pinMode(3, INPUT);
        TinyWireS.begin(I2C_SLAVE_ADDRESS);
        TinyWireS.onReceive(receiveEvent);
        TinyWireS.onRequest(requestEvent);
    }

    void loop() {
        TinyWireS_stop_check();
        digitalWrite(4, !!i2c_regs[1]);
        analogWrite(1, i2c_regs[0]);
        i2c_regs[2] = analogRead(3) >> 2;
    }
    ```
=== "Master"
    ```ino
    #include <Wire.h>
    void setup() {
        Wire.begin();
        Serial.begin(115200);
    }
    void loop() {
        byte x, d, s;
        Wire.beginTransmission(0x04);
        Wire.write(2);
        Wire.endTransmission();
        delay(10);
        Wire.requestFrom(0x04, 1);
        x = Wire.read();
        Serial.println(x);
        if (x <= 127) {
            d = 1;
            s = (127 - x) << 1;
        } else {
            d = 0;
            s = (x - 128) << 1;
        }
        Wire.beginTransmission(0x04);
        Wire.write(0);
        Wire.write(s);
        Wire.write(d);
        Wire.endTransmission();
        delay(10);
    }
    ```

And at long last, after much `:::ino delay()` tomfoolery, I got something to work.

I quickly discovered that the ADC read (i.e. the `:::ino analogRead()` call) takes a bit of time, and during that interval, the ATtiny85 effectively drops off the I^2^C bus. Weird, but workable.

Oh well. I don't have half the parts I need to finish anything, so I'll have to wait.
