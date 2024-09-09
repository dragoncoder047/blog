Title: LILduino
Date: 2023-01-04
Series: arduino-scripting
Tags: programming, arduino, c

Congratulations, you have reached the end of this series.

I finally found a programming language that I can use on my Arduino: [LIL](https://runtimeterror.com/tech/lil/), written by Kostas Michalopoulos. It's a lot like Tcl (but not quite), and it has a simple to use C API so I can add custom Arduino functions. I added a few, and after working out the bugs, it worked perfectly.

My only gripe is that LIL has absolutely no garbage collector. Whenever it needs two of a value, LIL allocates memory for a copy, instead of simply pointing to it and garbage-collecting unreachable objects like other languages do. This inherently means that everything is immutable. The other problem is that LIL stores everything as a string, including numbers. So if you try to pass a non-number string to a function that expects a number, it won't throw an error, it will simply use 0 instead of what you had meant to pass in. And this everything-is-a-string scheme also increases memory: a 64-bit integer could take up to 19 bytes of a string, but it will only take 8 bytes if actually stored as a number (and would be faster).

I'll try to improve LIL a little bit as well as writing extension modules for it to utilize all the capabilities of my ESP32 Arduino board. I have already written a few modules, and patched LIL to allow hexadecimal number literals (instead of just base 10). Using my experience from all the other programming languages I've tried to use and/or write, I might also patch the `lil_value_t` struct to allow the number to be represented as an actual `double` or `int64_t` instead of a string, add a type field to distinguish between them, and then the converter functions (`lil_to_X`) would ["shimmer"](https://wiki.tcl-lang.org/page/shimmering) the value back and forth as needed between string, int, and float.

Not sure if this is going to work at all, but it seems like it would. I'm deathly afraid of memory leaks, but LIL's code is easy enough to understand and it is pretty clear when it's allocating and freeing memory. Hopefully, LIL will continue to work. If it doesn't, well, then I guess my exclamation in the top of this post was a little premature.
