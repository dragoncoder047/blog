Date: 2022-12-30
Title: Systems Tested
Series: roboraptor-upgrade
Tags: electronics, reverse-engineering, programming

<!--- cSpell:ignore roboraptor --->

Over winter break I was able to get some more progress done building circuits to get closer to an upgrade of my old, broken Roboraptor. There are a zillion different components to this project, and I wanted to test each separately to make sure they work before I make a final board so I don't waste any effort or money.

What I've managed to do so far is less than half of what I need to do to get this whole thing where I want it in the end, but at least it's more than I expected I would be able to do in only a week.

The Roboraptor's internal circuit board is nicely labelled on the silkscreen, and so after a bit of poking around in the head to find which power rail the other components connected to I was able to interface my ESP32 into all of the sensors around my Roboraptor pretty easily as if they were just bare components.

## Infrared system

The original Roboraptor came with an infrared remote and a crude object-detection system, also using infrared. If I was going to be able to use the original remote with my upgraded Roboraptor, I would have to figure out how to decode that protocol.

David Conran wrote a [nice IR encoding/decoding protocol library](https://github.com/crankyoldgit/IRremoteESP8266), and I immediately tried it out. Unfortunately, the protocol registered as `UNKNOWN`, so I couldn't re-transmit any of the codes, save for sending the raw timing capture array, which should have worked except I wired up the IR LED's wrong.

After a [discussion](https://github.com/crankyoldgit/IRremoteESP8266/issues/1938) with David, he [added support](https://github.com/crankyoldgit/IRremoteESP8266/pull/1939) for the Roboraptor's protocol based on my raw capture arrays. After some rewiring I was successfully able to receive the remote's codes, and then re-transmit them and fool the Roboraptor's circuit board into thinking I had pressed a button on the remote. I was giddy with excitement after that worked so spectacularly. The codes I captured I saved in a [table in that issue](https://github.com/crankyoldgit/IRremoteESP8266/issues/1938#issuecomment-1367968228) for future reference.

## Audio output

The original Roboraptor used a specialized blob-of-epoxy sound IC and a one-transistor amplifier to play the sound effects. It was pretty crappy audio quality and I knew I could do better. I bought a MAX98357A amplifier from Sparkfun earlier and procrastinated testing it, but when I finally got around to it yesterday, it worked like a charm -- until I realized that I wasn't going to be able to wire it like it is supposed to.

The MAX98357A is a double-ended amplifier which uses two half-H bridges to alternately pull the speaker pins high and low, creating the alternating audio signal. Unfortunately, one end of the Roboraptor's speaker is permanently wired to the power supply rail, making it single-ended. I didn't want to cause a short circuit when the amplifier tries to pull that pin low, but I also didn't want to fuss around with re-wiring the head any more than I am already going to need to, so I got creative.

Having built a few audio amplifier circuits using the single-ended LM386 in the past, I tried a similar arrangement to those. I connected one end of the speaker to the supply rail like it would be, and the other end, through a large capacitor, to the positive output of the MAX98357A. Unfortunately, this severely reduced the output volume. I might not need the capacitor, but then I fear the audio quality would go down because the resulting setup would be eerily similar to the awful one-transistor amplifier in the original Roboraptor. I'll fiddle with it and get something to work.

## Microphones

The Roboraptor had two small electret microphones positioned in the "ears", and these fed into a simple peak-detector circuit that was really only good for detecting claps and other loud, sharp noises. Instead of limiting myself in hardware, I decided I would just connect the audio signal directly to my ESP32 and let it handle the feature detection in software.

Electret microphones require a preamplifier, so I Googled around for preamplifiers and found [this instructable](https://www.instructables.com/Electret-Mic-Preamp/), and luckily I had most of the parts on-hand. I built it with a fixed gain of 100, instead of the variable resistor to adjust the gain, used a 1000pF coupling capacitor instead of 0.1&micro;F, and omitted the low-pass filters for testing purposes. But overall, it appeared to work decently. I printed the result to the Arduino serial plotter (turning it into an oscilloscope) and I was clearly seeing a periodic audio wave in the monitor above the noise floor when I whistled into the microphone.

Using a standalone electret microphone I saved out of a broken intercom system produced a lot better results that the Roboraptor's internal microphones, but at least the result was noticeable above the noise. Maybe some low-pass filtering would smooth the noise out. I'll have to fiddle with it -- as with everything else -- until it works.

That's all, folks. I wish I could get more done, but there aren't enough hours in the day for that kind of work. See you in 2023.
