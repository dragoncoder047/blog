Title:  (Almost) No Javascript!
Date: 2022-09-07
Tags: css

I did a total redesign of my Langton's Ant simulator last week -- and most of the formatting I was able to do with pure CSS - no Javascript needed for layout control.

Previously I had a rather crude layout consisting of a fixed-size canvas and a textbox below it. The canvas was defined to be 1280x640 no matter the screen size, and my fear was that on smartphones it would spill over off the screen, and the image would be cut off. Additionally, the touch drag action on the canvas pans around, and so it effectively prevents the user from scrolling down and reaching the text box as well.

I decided I would redesign everything to fix these problems. In total, I made quite a few major changes:

1. I redesigned the parser to use XML instead of a impossible-to-maintain custom parser. It's quite more verbose than the original format, but by nature of the "X" in XML, it is extensible.
2. I replaced the plain old `:::html <textarea>` with an [Ace editor](https://ace.c9.io/) to allow syntax highliting and other helpful features for working with XML.
3. I made extensive use of CSS flexboxes to position buttons and controls in neat rows that wrap around when they get full.
4. I added some Javascript to the drag manager class that automatically resizes the canvas to fill its parent element and maintain the 1:1 aspect ratio and prevent blurry drawing. There's an (intentional?) but in the HTML5 `:::html <canvas>` that causes the drawing to become distorted if the `:::html <canvas>`'s `width` and `height` attributes aren't the same (or proportional to) its CSS `width` and `height`. No CSS will fix this, so I had to resort to Javascript.
5. I moved the ~~textarea~~ Ace to a separate popup window so that both it and the canvas could take up the entire screen without the user having to scroll. This, surprisingly, required absolutely no Javascript.

#5 I am the most proud of, and here's how I did it:

First, everything tha is *not* the popup (what would normally just be the `:::html <body>`) gets put in the `:::html <main>` element.

The body's scroll is disabled:

```css
body { overflow: hidden }
```

And the `:::html <main>` is expanded to fill the entire window:

```css
main { width: 100%; height: 100%; position: absolute; top: 0; left: 0; margin: 0 }
```

Then, the popover is added adjacent to (not in) the `:::html <main>` element:

```html
<main>
    <!-- main content -->
</main>
<div id="dump" class="popover">
    <div>
        <!-- popover content- notice the nested <div> -->
    </div>
</div>
```

Notice the popover has two nested `:::html <div>`s -- the outer is the "greyed-out" background, and the inner is the actual popover content. Here's the CSS that does that:

```css
.popover {
    background: rgba(0, 0, 0, 50%); z-index: 999999; position: absolute; top: 150vh; left: 0; width: 100%; height: 100%;
    display: flex; justify-content: center; align-items: center
}
```

The first line is pretty much the same as the CSS that was applied to the `:::html <main>` element -- it makes it fill the screen. Notice, however, that the `top` is `:::css 150vh` instead of `:::css 0` -- this pushes it down off the screen where it can't be viewed.

The second line centers the nested `:::html <div>`, which is styled with this CSS:

```css
.popover>div { background: white; width: 80%; height: 80%; border: 2px solid black; padding: 1em }
```

There's one last thing that is missing from this:

```css
.popover:target { top: 0 }
```

The `:::css :target` pseudoclass is relatively new, and matches only when the hash of the URL (everything after the `#`) is equal to the selected element's `id`. This allows the popup to be shown and hid by using only simple `:::html <a>` links that change the hash!

I added a link to `#dump` (which shows the popup) on the main screen, and within the popup a link to `#` (clearing the hash and hiding the popup). With this, no Javascript is needed (except to make the popup close or open automatically).

I haven't had any pure CSS solution as elegant as this since I got the sticky header on this site working (yes, no Javascript on that too). I don't know who should be prouder: me, or the CSS Working Group!
