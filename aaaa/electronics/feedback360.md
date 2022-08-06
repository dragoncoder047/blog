Title: Two Down, A Zillion More To Go
Date: 2022-08-06

I have finally written code that actually compiled and ran on the little ESP32 board I bought, and I hate the blasted thing already.

For starters, the process is slow, annoying, and tedious:

1. I click <small>UPLOAD</small>, and the Arduino IDE begins compiling by ... dumping preferences.
2. It then has to shuffle around a few files for specifying the flash partitions and other build options - which are not necessary on the Arduino Uno or ATtiny85, because their flash memories don't include a built-in filesystem like the ESP32 does.
3. Then it has to figure out which libraries have been included (as if it doesn't know that already) which takes like 30 seconds for some reason.
4. Compiling those libraries from scratch takes about 25 seconds *per library* (I plan on using like 15 different libraries!), and while these dependencies are cached on subsequent builds, actually finding the cached files takes 10 seconds.
5. Generating the function prototypes for the `.ino` file to make it into a valid `.cpp` file the compiler will tolerate takes another 15 seconds.
6. Then the ESP32 core must be compiled. Which takes 5 minutes - not surprising, because it incudes FreeRTOS or some portion of it. Thankfully this is cached as well.
7. Now the Arduino IDE's build console prints out `Linking everything together...`, and that's my cue to press and hold the incredibly tiny <small>BOOT</small> button down so that the ESP32 will enter bootloader mode when the program is starting to upload. Once the upload starts, I can release the button.
8. For some large programs, the upload takes 2 minutes.
9. Finally the board can be unplugged and the <small>RESET</small> button can be pressed, running the code.

A similar program compiling for the Arduino Uno would take about five seconds *total*, and upload another five, and I do not need to hold a tiny button during upload because the Optiboot bootloader the Uno uses runs automatically on chip reset, every time, before running the user code.

This is a second additional reason why I so badly want to use [uLisp](http://www.ulisp.com/) on my ESP32, because all I need to do with that is save Lisp code to a microSD card, eject it, insert it into the socket on my ESP32 board, and press <small>RESET</small> again.

In other news, I finished a small Arduino library to control the Parallax Feedback 360 servo I also bought. It can read the position of the encoder, keep track of turns count, and calculate instantaneous angular velocity. It's on GitHub: <https://github.com/dragoncoder047/feedback360/>

Actually, "control" would be a but of a misnomer here, because all the control this library does is set the power applied to the motor, and can't regulate speed or position out-of-the-box. I tried to do this using one of the many PID libraries out there, and had a bit of success regulating the speed (amid my mother shouting "You're going to break your motor grabbing it like that!"), but not much luck regulating the position. It always resulted in oscillation around the setpoint, but never actually stopping. I eventually figured out that the Feedback 360's internal driver circuit has a delay between when the input control signal changes and when the motor actually responds, and I never was able to tune the PID's constants to work with this or even with other methods (feeding the speed into the PID loop as well, having one PID loop modulate another sub-loop controlling speed, etc). If you have success controlling the position of a Feedback 360 servo with no oscillation, PLEASE let me know!

That's only two pieces of the puzzle that is my hacked Roboraptor. There's also converting the other motors into servos (which involves a magnet, a Hall effect sensor, and an ATtiny85), re-wiring the head and tail to add more sensors and glowing LED eyes, cramming a small micro servo into the body compartment in order to separate the head and jaw motion, and hooking up the two microphones and a DAC to be able to play sound effects and listen to the environment. Whew! That's a lot. Will probably take me a while.

Not to mention the fact that the ATtiny85's and H-bridges that I ordered are *still* on back-order... Damn this chip shortage!
