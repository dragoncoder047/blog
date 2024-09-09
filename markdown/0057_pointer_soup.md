Title: Pointer Soup
Date: 2024-08-06
Tags: programming, c, lisp, language-design

I never realized that the concept of a pointer could get so confusing. Over the last two months I came up with a number of different ideas that all involve pointers and got my brain all twisted up in knots when I got to the pointer part.

When I left off in June I had spent the month discussing a whole bunch of my ideas for uLisp with David Johnson-Davies, uLisp's maintainer. He put out a new release -- version 4.6 -- that incorporated a number of these changes, but not all of them. The reason why he had not implemented many of them was that they affected the way uLisp interprets pointers, and my suggestions were so different than the current method that David (rightly) felt apprehensive.

One of the suggestions that I sent to David was that the symbol representation might be able to be sped up.

Currently, uLisp has three different representations of symbols: built-in symbols, packed symbols, and long symbols. All of the symbol objects contain a number in the `cdr` pointer, but whether it represents a pointer or not depends on the kind of symbol:

1. Built-in symbols are represented as a number that is the index of the symbol in the built-in symbol table. However, to allow them to be distinguished from other kinds of symbols the index is "twisted" into a slightly different format by first adding a constant that has the top two bits set (specifically, `:::c 0xF4240000` on 32-bit uLisp), and then performing a rightwards bit rotation by 2 bits. The effect is that the bottom two bits of a built-in symbol's representation will always be 1 (mathematically, the resultant number will be congruent to 3 modulo 4).

    As a pointer, this is almost universally invalid; processors typically choke on pointers that aren't aligned to a multiple of the processor's word size (which is either 4 or 8 bytes).

2. Packed symbols are a way to save memory for common symbol names by encoding them as a base-40 number instead of storing every character. If the name contains only valid characters (namely, letters, digits, `$`, `-`, and `*`) and is short enough, the name is encoded in base-40 and then the resultant number is "twisted" in the same manner as built-in indexes (just with a different constant) again to ensure that at least one of the bottom two bits is set to 1.

3. Long symbols are sort of the "fallback" option: if no other representation fits, the symbol is encoded in the same manner as a uLisp string, with the characters stored in a linked list of chunks inside the uLisp `Workspace`, and then the symbol object's value is a pointer to the head of the list. Since it's obviously a valid pointer, the bottom two bits of a long symbol are guaranteed to be both 0's.

When the symbol is printed, the determination as to which kind of symbol it is has a few steps. If the bottom two bits are 0, then it's obviously a long symbol, and it is printed in the same manner as a string (just without quotes). If either of the bottom two bits are 1 (a "misaligned" pointer), then it is either a built-in symbol or a packed symbol. The number is un-rotated, and if it is greater than the built-in symbols' scaling constant, then it must be a built-in, otherwise it's a packed symbol.

Suffice to say that this pointer-twisting was twisting my brain up in knots. This representation is a very smart, well-thought out, and headache-inducing encoding method -- but kudos to David for coming up with it, because it works very well.

In figuring out how exactly this pointer-twisting scheme worked I noticed that there's one assumption that this encoding scheme makes: *all* values with the bottom two bits set to 0 (i.e. the ones that represent valid pointers) must be reserved for long symbols. In reality, it's only the values that are valid pointers *into the block of allocated objects* -- the `Workspace` -- that are the values reserved as long symbols. Of course, depending on the platform and the compiler, this block of addresses may be different. But what's wrong with actually using the addresses of the top and bottom of the `Workspace` in the encoding/decoding computations?

I proposed changing the representations of the built-in symbols to point directly to the table entry that they came from. Since it's another pointer, the bottom two bits would now always be 0, instead of always being 1. Long symbols and packed symbols would be represented *exactly the same way*.

The process for determining which kind of symbol a pointer represents would still involve pointer-twisting, but only for the packed symbols. If the pointer is not misaligned, then it's either a built-in symbol pointer, or a long symbol pointer. The determination as to which it is, is made by -- you guessed it -- checking whether the pointer points to valid memory within uLisp's `Workspace`. If it is within the bounds of the `Workspace`, it's a long symbol. If it points to memory outside of the `Workspace`, then it is assumed to point to a table entry of a built-in symbol. Easy as that.

The added benefit of having the built-in symbols point directly to their table entries is that looking up the built-in function is made a heck of a lot faster -- now it is just one pointer dereference, versus having to untwist the number first to get the index, which is itself a handful of instructions, and then using that index to find the entry in the built-in symbol table, another few instructions. The built-in functions are used a *lot* (by definition), so making them faster is an important optimization.

Unfortunately, David didn't implement that. Granted, I still haven't, either, but for a valid reason: thinking about pointers is difficult. Especially if they are part of a C `:::c union` and you have to tell then apart from other "kinds" of pointers!
