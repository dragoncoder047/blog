Date: 2021-09-16
Title: Abbreviations in Context
Status: Draft
Tags: python, programming

While drafting out an idea I had, I came to the task of how to save to a file and load it again. The data I would be saving is highly repetitive, so I figured I could compress the file somehow to save space but still have it be human-readable. Gzip was out because although it offers great compression, it is a binary filetype (not human readable) and requires a huge external library (making it harder for other fellow programmers to understand).

Starting with the format I had already devised, the task boiled down to this very simple problem:

**Given a context of several different words, produce abbreviations for each, that given the context, are unambiguous as to which unabbreviated word they refer to.**

For example, given 'foo', 'bar', 'bam', and 'baz', they are each three bytes. Given 1000 of those tokens in the file, that's 3Kb. But if I could shorten the names -- they could be shortened to 'f', 'r', 'm', and 'z' respectively -- each token would only be one byte, cutting the file size by two-thirds. One letter is all that is needed to uniquely determine which it is --- given that the only choices are 'foo', 'bar', 'bam', and 'baz'.

It's intuitive to a human, but now the problem is, how do I get a computer to do that abbreviation, given the word to be abbreviated and the list of possibilities?

My first idea was simple: look at each letter in order, and if there are more than one different letter of the different possible words at that position in each word, output the letter in the word to be abbreviated, remove the other words that don't have that letter at that position from consideration, and repeat until there is only one word left, which should be the word to be abbreviated.

The un-abbreviation algorithm for this is also just as simple: go through each letter in the abbreviation, and filter the possibilities down when they have different letters at the next position.

```py3
def abbreviate(word: str, context: list[str], extra_char=' ') -> str:
    # The `extra_char` argument is a unique filler character,
    # used to pad the input strings when they are different lengths.
    out = ''
    ctx = [w.ljust(max(map(len, context)), extra_char) for w in context]
    i = 0
    while len(ctx) > 1:
        different_letters_at_this_pos = set(s[i] for s in ctx)
        if len(different_letters_at_this_pos) > 1:
            out += word[i] if i < len(word) else extra_char
            ctx = [w for w in ctx if w[i] == out[-1]]
        i += 1
    return out


def unabbreviate(abbr: str, context: list[str], extra_char=' ') -> str:
    ctx = [w.ljust(max(map(len, context)), extra_char) for w in context]
    i = j = 0
    while len(ctx) > 1:
        uniq_let = set(s[i] for s in ctx)
        if len(uniq_let) > 1:
            ctx = [w for w in ctx if w[i] == abbr[j]]
            j += 1
        i += 1
    if len(ctx) == 0:
        raise ValueError(f'abbreviation {abbr} ruled out everything')
    return ctx[0].rstrip(extra_char)

```

Notice how similar the abbreviation and unabbreviation algorithms are.

Here's some test results:

```py3
>>> c = ['foo', 'bar', 'baz', 'bam']
>>> for x in c:
...     print(x, '->', abbreviate(x, c), '->', unabbreviate(abbreviate(x, c), c))

foo -> f -> foo
bar -> br -> bar
baz -> bz -> baz
bam -> bm -> bam
```

Well... it works. But it isn't optimal.

MORE HERE
