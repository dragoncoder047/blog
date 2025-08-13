Title: So far ahead, yet so far behind
Date: 2025-01-13
Tags: programming, javascript, gamedev
Series: debugger-game

I finally got around to testing the game I have been making, *Debugger*, using a game controller. For the most part, it went off without a hitch, but there were several problems I encountered -- and none of them were fixable, because they were not bugs in my code, nor in the game library I am using ([KAPLAY.js][kaplay]). They were problems with the browser itself.

KAPLAY uses the [Web Gamepad API][gamepad_api] internally to detect and process game controllers, like the one I am using. Despite the fact that MDN claims that it's been available and fully supported, I found it wasn't. Some browsers supported it only partially, while others claimed to support it but actually implemented it in an undocumented, noncompliant manner.

## Safari

Safari on Mac, surprisingly enough, actually supported all of the APIs that were required to run *Debugger*. I added some code to give haptic feedback using the game controller's rumble motors, and after testing in several browsers it turns out that Safari was the only browser I could get haptic feedback working in -- even though MDN claims that all major browsers have supported it for like 5 years.

## Chrome

Chrome is usually the browser that releases experimental features first -- and so I kind of suspected that gamepad rumble would work in Chrome too, but I was sorely disappointed. All of the *inputs* defined in the spec work perfectly (buttons, triggers, sticks, etc), and so the game is technically playable, but it is missing the haptic feedback. For the Chrome developers to say that they can't implement it because they can't access the right OS-level system calls is a lousy excuse, because Safari can.

Interestingly enough, my classmate who I had elisted to alpha-test, reported that controller rumble *did* work in Chrome.

![me: ok i fixed the death menu being broken now. also can you test it in safari cause the controller rumble only seems to work in safari. friend: the controller rumble was working for me and i was using chrome]({attach}rumbleinchrome.png)

He was using an Xbox controller, while I was using a PS5 controller. If the reason it worked for him and not me was because Chrome only implemented haptic actuator support for Xbox controllers... well, that's also inexcusable, because the PS5 has been around long enough for the protocol to have been reverse-engineered. Heck, a cheap $30 ESP32 microcontroller can do better than Safari and implement [trigger rumble][bluepad32_triggerrumble] as well as regular rumble. If I were a browser developer, I would be embarrased that at this point the Web Gamepad API still isn't fully supported.

## Firefox

Now don't even get me started on how broken Firefox is to begin with. Firefox's implementation of the Gamepad API is so broken that it makes Debugger unplayable -- so much so that I did this:

```js
K.onGamepadConnect(g => {
    if (isFirefox()) {
        showModal(true, "&msg.dialog.firefoxDontWorkWithGamepads", true);
    }
});
```

-- where `msg.dialog.firefoxDontWorkWithGamepads` is a internationalization substitution that, in English, expands to:

> You appear to be using Firefox. Unfortunately for you, Firefox's implementation of the web game controller API is so horribly messed up as to be unusable. You can continue with your mouse and keyboard.
>
> If you really want to use a game controller, please use another browser like Chrome, Opera, or Safari.

How bad is it, really?

First off, the four face buttons on the right (X/Y/A/B, square/cross/circle/triangle, etc.) are in the wrong order. The Gamepad API spec requires that browsers order the buttons based on the physical position, not the name of the button. This means that the button on the bottom (the "south" button) is A on Xbox controllers, B on Nintendo Switch controllers, and cross on Playstation controllers. But Firefox reorders the buttons -- on my PS5 controller, when I press the cross button, it triggers the action associated with the "east" button, despite the fact that the circle button is physically the "east" button. KAPLAY follows the spec and looks in the right index in the buttons array, but since the array is out-of-spec, it does the wrong thing by no fault of its own. I don't know about you, but if the game tells you "press X to do this", you press X, and the game does something totally different, it would be incredibly frustrating.

Firefox also maps the analog triggers in a noncompliant manner. The spec provides three fields in the [`GamepadButton`][gamepad_button] interface to handle special buttons like this -- the `value` field is where the analog value is supposed to go. Firefox only uses the Boolean `pressed` field for the analog triggers, and instead puts the analog values into a third `axes` entry -- despite the fact that the `axes` array was *only* meant for the sticks or other inputs that have a logical X and Y position. The analog trigers aren't like that! Debugger doesn't use the analog values, but I'm sure there are web games out there that do, and people playing those games in Firefox are probably having a hard time because the game can't find the analog value and defers to the digital one, making the triggers ridiculously finicky.

The d-pad is the weirdest of all in Firefox. Per the spec, it's supposed to be mapped to four buttons, because that's what it is. But Firefox chooses to map it to an entry in `axes`, of all things -- and it's not even the way you would expect, with two entries for X and Y that only ever take on the values -1, 0, or 1. Firefox chooses to roll both into a single value, so that the `axes` array ends up with an odd length (which never happens in spec-compliant browsers). The numbers that this single axis value uses to represent each of the eight directions are also rather odd:

| Actual Buttons Pressed | `:::js axes[6]` |
|:----------------------:|:---------------:|
| None | 1.29 |
| Up | -1 |
| Up + Right | -0.71 |
| Right | -0.43 |
| Right + Down | -0.14 |
| Down | 0.14 |
| Down + Left | 0.43 |
| Left | 0.71 |
| Left + Up | 1 |

I can tell it's trying to represent it as an angle somehow, but it's not any standard unit for angle, and what's up with the 1.29 representing "nothing pressed"? That's not even a valid value for an entry in `axes` anyway. Just why, Firefox?

## The verdict

There's enough support out there for the Gamepad API that you're actually able to play *Debugger*. That being said, it took a lot of work to get there. To be able to display the right button names for the controller the player is using, I had to implement some horrible string-munging code to try to parse the `id` value that the browser gives for each connected game controller, figure out which kind it is, and then swap out the button names using the internationalization string mechanism. There's also the code to check if the browser is Firefox and warn the user about the above bugs when they try to use a game controller.

Until and unless browser developers get their sh*t together and fix all these problems, I'm probably not going to make any Web-based thing that interfaces with game controllers. The sad truth is that no matter how widely-supported the Web Gamepad API claims to be, it just isn't.

[kaplay]: https://v4000.kaplayjs.com
[gamepad_api]: https://developer.mozilla.org/en-US/docs/Web/API/Gamepad_API
[bluepad32_triggerrumble]: https://github.com/ricardoquesada/bluepad32/blob/6efa7123fe8badf5a40ad1205743a80b31c00ea4/src/components/bluepad32/parser/uni_hid_parser_ds5.c#L367-L389
[gamepad_button]: https://developer.mozilla.org/en-US/docs/Web/API/GamepadButton

<!--- cSpell: ignore kaplay --->
