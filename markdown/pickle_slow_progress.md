Title: A Hash-Mapped Mess
Date: 2024-04-05
Series: pickle
Tags: programming, c, garbage-collector, language-design

It has not been a good week. I set out on Tuesday to actually add real objects to PICKLE, with a hashmap of properties and multiple inheritance and everything. Suffice to say, that wasn't easy. Between null pointer dereferencing, sloppy APIs, and an incomplete algorithm, it took several hours' work total to root out all the bugs.

The hashmap design I used was a sort of "binary trie", based on [this gist][hmap] of Tim Caswell. The design of it seems simple enough -- each node can store a key-value pair, and to find an element you first check to see if the root node holds the key you're looking for, if it doesn't, you treat the hash value of the key as a bit string and get the next-most-significant bit of the hash, and recurse on the left or right child node depending on whether the bit is a 0 or a 1.

[hmap]: https://gist.github.com/creationix/3ea0d27dd100c5b53ca8546a2084ad47

Except, in practice, it's not that simple.

Obviously, hashmaps for object properties aren't static -- they will have properties inserted, updated, and removed. Updating an existing property is almost trivial -- you just find the corresponding node in the hashmap and replace the value.

The algorithms outlined for adding or deleting a property end up causing problems. Deleting a property just clears the node, it doesn't delete the node, and so the property-addition algorithm can check for and re-use cleared nodes instead of creating new children. This means that a simple add-or-update implementation might end up accidentally inserting the value twice, because it found a cleared node higher-up in the tree than the existing node's position and stopped too soon.

```{.mermaid .float-right}
graph TD
    foo --> bar
    foo --> baz
```

Consider what happens if you have, say, three nodes called `foo`, `bar`, and `baz`. First `foo` is inserted to an empty tree, so it becomes the root node, Then `bar` and `baz` are added, and become children of `foo`.

```{.mermaid .float-right}
graph TD
    foo[ ] --> bar
    foo --> baz
```

Now `foo` is deleted. The first node matching it is cleared - no problem. There are no `foo`s in the tree.

```{.mermaid .float-right}
graph TD
    foo["bar (new)"] --> bar["bar (old)"]
    foo --> baz
```

`bar` is updated. Since there is a free node above the old `bar`, there ends up two `bar` nodes.

Up until now, there isn't any problem. Finding any node, even in the tree with the duplicated `bar`, finds the correct value.

```{.mermaid .float-right}
graph TD
    foo[ ] --> bar["bar (old)"]
    foo --> baz
```

The problem arises when you try to delete `bar` on this duplicated tree -- and since the old `bar` node wasn't ever deleted, this "shadow" node now rears it ugly head and causes the key `bar` to revert to its old value, instead of being deleted like it was supposed to be.

I spent a long time trying to figure out how to combat this problem. The easiest solution, which I implemented, is to traverse the entire hash's search path, not just stopping at the first free node, when updating a value. If the new value is set by filling a free node (rather than simply updating the existing node with the same key), there may be shadow nodes under it, so the rest of the tree has to be traversed, and these shadow nodes cleared. This guarantees there will only be one node for any given key in use at the same time.

---

The one last bug, that I still haven't fixed, is the way these hashmaps work with the garbage collector. When you delete a node, you don't actually *delete* the node, you just clear it / mark it as free. The memory is still in use as far as the garbage collector is concerned, and is never freed. Even if the an object has no properties currently, if the object had, say, a thousand different properties at some point in the past, there will now be a thousand unused nodes in the hashmap that the garbage collector just won't collect.

I am not sure how to fix this. If I go start removing empty nodes willy-nilly, how will that impact looking up existing non-empty nodes? How do I put the tree back together after I delete a node? I don't know quite yet. A search trie is (yet again) something new to me, and I'll have to do more research. Every day is a learning experience -- that is to be celebrated.
