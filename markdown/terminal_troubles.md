Title: Terminal Troubles
Date: 2022-03-23
Tags: programming, phoo, javascript

I have finally gotten to the point in Phoo's development that I am ready to set up the web interface.

I chose xterm.js for the terminal interface because I intend for Phoo to be able to be run in Nodejs as well as in the browser, but I don't really use Nodejs much, so I wanted to have a simulated terminal to run it in.

It took me a while to set up the terminal so that it came up properly. I then had the problem of how to get input from the user. I searched around for xterm.js addons and I found [local-echo](https://github.com/wavesoft/local-echo), made by a guy named Ioannis Charalampidis. With a few patches ([#24](https://github.com/wavesoft/local-echo/issues/24), [#30](https://github.com/wavesoft/local-echo/issues/30), and [#34](https://github.com/wavesoft/local-echo/issues/34)) I had a little shell running. It seemed to work well enough with just a simple echo backend (not actually invoking Phoo), but I quickly encountered a few more problems:

## Issue [#25](https://github.com/wavesoft/local-echo/issues/25)

![xterm_typetypetype.png]({attach}/xterm_images/xterm_typetypetype.png)

The first line is being duplicated in the view every time you press a key, but the actual input buffer is fine, as shown by the red text. I think this is just some off-by-one typo, but it has been quite a problem.

## Issue [#50](https://github.com/wavesoft/local-echo/issues/50)

This one was completely new:

![xterm_clobber.png]({attach}/xterm_images/xterm_clobber.png)

What happened *here* is that I just typed the text (in red), and then pressed enter. With the cursor **on the last line**, it works (the top part), it works fine. But with the cursor **not on the last line** (I put it in the middle of the b's) it assumes it *is* on the last line and in doing so clobbers over however many lines of input on the subsequent lines. This is *baaaaaad*. To be honest I actually spent more time trying to fix this than working on the actual web app for a day or two.

As a side note I also noticed another issue ([#51](https://github.com/wavesoft/local-echo/issues/51)) where the up/down keys didn't behave as I expected and changed the history regardless of what line you were on. Really annoying and takes some time to get used to, but not a priority.

These two issues practically make the entire interface totally unusable and I'm back to square zero.

Not to mention that there hasn't been an official release of local-echo since 2018, so I had to manually cobble together a pseudo-'build' that works with xterm.js version 4. I probably broke something in there.

Hoefully either me or someone else will fix these issues.
