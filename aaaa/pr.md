Title: First Pull Request
Date: 2022-04-26

Today I managed to submit my first ever Github pull request. In develpoing Phoo I made some changes to the meta-words from its predecessor Quackery, and they seemed backportable to Quackery. So I forked Quackery and submitted a [pull request](https://github.com/GordonCharlton/Quackery/pull/6) with those changes.

In the name of trying to bootstrap Phoo as much as possible, I had substituted the limited `:::phoo ]if[`, `:::phoo ]iff[`, and `:::phoo ]else[` with what Gordon later called a 'relative GOTO' in `:::phoo ]cjump[` which can be (ab)used to jump backwards. I like being able to do that at least with Phoo. Of course with the Quackery system you can have all sorts of `:::phoo ' if take` fun (which is prevented easily by Phoo's dynamic resolution - but `:::phoo ' if resolve take` would work too), but a `:::phoo ]cjump[` also seemed useful in a sense to be able to look ahead with `:::phoo ]'[` and then jump back and allow it to be executed with `:::phoo false -1 ]cjump[` if it didn't turn out to be what was expected.

Well, at the very least I got some syntax fixes to my name there. I have another couple of ideas, and I'll add a pull request and/or another post here when I get around to them.
