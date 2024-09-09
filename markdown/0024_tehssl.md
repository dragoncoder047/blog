Title: TEHSSL
Date: 2022-11-02
Tags: programming, c, language-design

I started writing a new programming language, TEHSSL, a few days ago. Starting from scratch (again!) wasn't easy, and I'm nowhere near done yet. I have got two things working so far: the garbage collector, and the tokenizer. I have no idea how to handle the glue in between (parser, evaluator, macros, builtin functions), or even what the glue will do and how it will work.

## Garbage collector

The garbage collector is just a simple mark-and-sweep garbage collector, and I took inspiration from Bob Nystrom's [`mark-sweep`](https://github.com/munificent/mark-sweep) implementation, which, conveniently, was written in C.

Adding some debug `printf()`'s to the code to see what the collector was freeing and when, I hooked up a simple test that created objects and then deliberately did nothing with them, to create garbage, while pushing some to the stack to make them "not garbage." Here is the code:

```c
tehssl_vm_t vm = tehssl_new_vm();
// Make some garbage
for (int i = 0; i < 5; i++) {
    tehssl_make_number(vm, 123);
    tehssl_make_number(vm, 456.789123);
    tehssl_make_string(vm, "i am cow hear me moo");
    tehssl_make_symbol(vm, "Symbol!", SYMBOL_WORD);
    // This is not garbage, it is on the stack now
    tehssl_push(vm, &vm->stack, tehssl_make_number(vm, 1.7E+123));
    tehssl_push(vm, &vm->stack, tehssl_make_string(vm, "Foo123"));
}
printf("%lu objects\n", vm->num_objects);
tehssl_gc(vm);
printf("%lu objects after gc\n", vm->num_objects);
tehssl_destroy(vm);
```

And here is the output:

```txt
16 objects
Freeing a SYMBOL name-> "Symbol!"
Freeing a STRING name-> "i am cow hear me moo"
Freeing a NUMBER number-> 456.789
Freeing a NUMBER number-> 123
12 objects after gc
Freeing a LIST
Freeing a LIST
Freeing a LIST
Freeing a LIST
Freeing a LIST
Freeing a LIST
Freeing a LIST
Freeing a LIST
Freeing a LIST
Freeing a STRING name-> "Foo123"
Freeing a LIST
Freeing a NUMBER number-> 1.7e+123
```

Everything that comes after the `12 objects after gc` mark is what happens when the entire VM is freed (i.e. the `tehssl_destroy()` call). `tehssl_destroy()` simply marks *everything* as garbage, and then garbage collects -- that way all objects are freed, and all that's left to do is free the VM itself.

This output also demonstrates TEHSSL's string and number interning; since strings and numbers are immutable, it only has to store one of each different value in use and just point to it multiple times. I don't know how this affects the speed of TEHSSL, but that's not something I'm terribly concerned about: if any routine is terribly speed-critical, it can just be written in C!

## Tokenizer

TEHSSL tokens fall into one of three categories: a paren (square, round, or curly), a semicolon, or a word. The tokenizer reads from a C `FILE*` pointer to allow for files and stdin and custom streams to be used as input irrespective of what; and returns the next token in the stream in a dynamic `malloc()`'ed string. I hope Arduino uses GNU C extensions so I can use [`fopencookie()`](https://linux.die.net/man/3/fopencookie) to create wrappers for common protocols such as I2C, SPI, Serial, etc.

Here's the tokenizer test code. It outputs the tokens in between backticks (`` ` ` ``) so I could paste them into this Markdown document.

```c
const char* str = "Def Myfunction as {\n    ~~Hello world! I am in a block!\n    DoSomething with: \\a-symbol and a number 45678;\n    Print \"Did something!!\";push a block{Foo bar Baz};\n    and then Do it\n}\n";
printf("%s", str);
FILE* s = fmemopen((void*)str, strlen(str), "r");
char* token = NULL;
while (!feof(s)) {
    token = tehssl_next_token(s);
    if (token == NULL) { printf("**ERR!**"); break; }
    if (strlen(token) == 0) { printf("**EOF.**"); free(token); break; }
    printf("`%s` ", token);
    free(token);
}
fclose(s);
```

For reference, here's what the tokenizer is tokenizing, without the C backslash escapes:

```tehssl
Def Myfunction as {
    ~~Hello world! I am in a block!
    DoSomething with: \a-symbol and a number 45678;
    Print "Did something!!";push a block{Foo bar Baz};
    and then Do it
}
```

And it produced these tokens: `Def` `Myfunction` `{` `DoSomething` `with:` `\a-symbol` `45678` `;` `Print` `"Did something!!` `;` `{` `Foo` `Baz` `}` `;` `Do` `}` **EOF.**

5 things are happenning here:

1. The comment on line 2 is discarded entirely.
2. The parens and semicolons are being separated out into their own tokens.
3. All of the `lowercase` words are being discarded, because they are "informal syntax" that are treated as comments.
4. The `with:` is *not* discarded, because it is a keyword property that actually means something.
5. The string token (`"Did something!!`) doesn't have the closing quote. This is so the parser (which reads the tokens) can look at the first character to determine the type of symbol, and in the case of a string, it can just slice off the first character without having to blank out the last as well (which is considerably harder in C than in another language such as Python) to get the raw string contents.

TEHSSL is more than just a grabage collector and a tokenizer, but that's all I have written at this moment. But apparently it looks promising, because David Kobalia starred TEHSSL on GitHub yesterday!
