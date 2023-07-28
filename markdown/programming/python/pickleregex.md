Title: PICKLE Has Regular Expressions, Apparently
Date: 2023-07-28
Series: pickle

I worked for a while last week on the PICKLE implementation in Python. As I no longer have to work on the garbage collector, after I wrote a little "glue code" I immediately dove into the core functionality of PICKLE: the pattern-matching engine. Once I get the algorithm down, I'll port it to the C++ implementation.

While fleshing out PICKLE's syntax I decided that there would be two phases in PICKLE's evaluation algorithm of a line. [Previously]({filename}../c/pickle-pattern.md) I determined that whitespace would be significant, and this now opens the door for syntactic macros.

The way it would work when evaluating each logical line is as follows:

1. Apply only patterns that don't contain whitespace (or are otherwise marked as macros) until none apply. <-- MACROS APPLIED HERE
2. Evaluate all the elements (recursively if there are any sub-expressions).
3. Apply *all* patterns until none match. <-- OPERATORS APPLIED HERE
4. Call the first value in the resultant list with the remainder as arguments. <-- FUNCTIONS CALLED HERE

1 and 3 are the hardest part because they invoke the pattern matching algorithm. The reason they are so difficult is that, to be able to support any kind of pattern, it necessitates including constructs for alternation and repetition. There are also combinators for matching an element and storing it in a variable. To that end I came up with these combinators:

```python
# matches the current item if it is an instance of CLS, and if so stores it as a reference under NAME
Var(cls: type, name: str)
# tries each match in order until one matches
Alternate(*patterns: Pattern)
# repeats the inner match from MIN to MAX times
Repeat(what: Any, min: int, max: int, greedy: bool)
```

The repetition is the hardest part, as it has to contend with both greedy and non-greedy matches. The approach I used was highly recursive, riddled with edge-case bugs, and was generally slow.

After a while I realized how similar these constructs were to regular expressions, especially with the `Repeat` combinator:

```python
Alternate("a", "b", "c")    # --> a|b|c
Var(int, "foo")             # --> (?P<foo>[0-9]+)
Repeat("a", 0, 1,    True)  # --> a?
Repeat("a", 0, 1,    False) # --> a??
Repeat("a", 0, None, True)  # --> a*
Repeat("a", 1, None, True)  # --> a+
Repeat("a", 0, None, False) # --> a*?
Repeat("a", 4, 10,   True)  # --> a{4,10}
```

Searching for regular expression algorithms led me to some (absolutely ancient) pages written by Russ Cox about [Thompson's algorithm](https://swtch.com/~rsc/regexp/). Seems like a simple enough algorithm; I hadn't thought of compiling a regular expression into a nondeterministic state machine before.

However, the paper doesn't explain everything in detail; I included patterns with capped counts of repeats for some reason. Perhaps that isn't needed, but I thought it would be easy to implement.

The code from the article is in C, and fragmented among the different parts of the page, but I'll have a go at implementing it. The Pythonic approach is tending towards dataclasses over structs, so I expect to take advantage of Python 3.10's `:::python3 match` feature too.
