Title: Segfaults
Date: 2022-11-16
Series: arduino-scripting
Tags: programming, c

Today I did a little more work on my programming language TEHSSL. And in testing it, I discovered some anomalies.

The first one is that -- because of a typo on my part -- testing TEHSSL will occasionally segfault when it tries to print the type of the "next" object after freeing the last one -- there is no "next object", so it dereferences a null pointer and crashes. I fixed that, and it appears to work. However, it worked just fine when I pasted it into [cpp.sh](https://cpp.sh), and didn't hang or anything, so I'm not sure what's up with that.

Valgrind reports no memory leaks from the garpage collector after I fixed things (woohoo!), so that's good. However, in testing those bugs, I discovered another anomaly: when the tests de-allocate and free everything at the end, it prints out how many objects it freed. This count varies based on the compiler -- without me changing any code at all!!

When I run `:::bash make test` (i.e. running it natively on my computer, using `:::bash g++`), the output shows [56 objects freed](https://github.com/dragoncoder047/tehssl/blob/ea16652/test_reports/output.txt#L271) at the end.

When I paste it into cpp.sh (which uses Emscripten), it says there are 51 objects freed.

What happened to the other 5 objects? Is it something to do with Emscripten vs `:::bash g++`? I'm not sure. But it has no memory leaks, and that's what I am really happy about.
