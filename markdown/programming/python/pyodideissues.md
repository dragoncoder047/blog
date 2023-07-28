Title: Pyodide Issues
Date: 2022-05-19

I am currently working on an online console for [Quackery](https://github.com/GordonCharlton/Quackery) that is using the [Pyodide](https://github.com/pyodide/pyodide) in-browser Python interpreter. The only bad thing is, Python's `:::py3 input()` function blocks until input is provided, which can't be done in the browser because everything is asynchronous. The only way for it to work is an annoying `:::js prompt()` box.

I thought, maybe I could automatically rewrite the Quackery source code and patch in an async input function, then make everything else that needs to be async, async.

The general process of patching went as follows:

1. Find and replace the offending `:::py3 input()` function with an async patched version.
2. Find all the functions that are now invalid (i.e. are not declared with `:::py3 async def` but now have an `:::py3 await` inside of them) and make them `:::py3 async def`.
3. Find all the places where those functions are called, and `:::py3 await` them.
4. If something changed, go back to step 2.

My [first attempt](https://github.com/dragoncoder047/QuackeryFork/blob/00868e13b0fa3f9671e109037b861f72b8759b21/webapp_start.py#L24-L127) used the Python [AST](https://docs.python.org/library/ast.html) module to walk the abstract syntax tree and replace `:::py3 FunctionDef` nodes with `:::py3 AsyncFunctionDef` nodes and wrap their calls in `:::py3 Await` nodes. For some reason, that either crapped out halfway through or hung forever. I don't know why.

My [second attempt](https://github.com/dragoncoder047/QuackeryFork/blob/a21709138de87326603f2686ffa44b166d113b65/webapp_start.py#L26-L77) was to use the regular expression module to find all the non-`:::py3 async` functions that have `:::py3 await` inside of them, and insert `:::py3 async` onto the definition, then find their references and insert `:::py3 await`. This proved tricky using regular expressions and often produced absurd (and incorrect) results such as `:::py3 async async def` (until I checked and removed all occurrences of `:::py3 async async` and `:::py3 await await` manually) or even `:::py3 self.string_await from_stack()` (because `from_stack` happened to be processed before `string_from_stack` and their names overlapped).

My [third attempt](https://github.com/dragoncoder047/QuackeryFork/blob/9bb91407bddebfa69297a7f9315ad8350e06189c/quackery_OOP_ASYNC.py) was to simply manually go through and make the edits. The tricky thing here is, even though I am sure I have asynced and awaited everything I need to, Quackery operators (Python functions) are passed by reference to the interpreter, and some must be made async and some are not. And that wreaks havoc on the entire program, because it is impossible to predict whether that passed-by-reference function is async or not and whether it should be awaited. Whereas in Javascript -- and Phoo, too -- `:::js await undefined` works, simply returning `:::js undefined` immediately, `:::py3 await None` throws `TypeError: object NoneType can't be used in 'await' expression` and crashes the whole program. So the `:::py3 TypeError` must be suppressed with a try-catch block. Unfortunately, this causes some other problems, which I don't really understand and so I can't fix them.

I sure hope the Pyodide people can get the async input fixed soon!
