Title: uLisp Thoughts
Date: 2022-09-27
Series: arduino-scripting
Tags: programming, c, arduino, language-design

For a while I have been trying to work out some bugs in David Johnson-Davies' uLisp interpreter for Arduinos. I ported some macro and quasiquote extensions for an older version of uLisp to the current version, and apparently I did not do something right -- it crashes whenever I try to use those extensions.

Now, I really want to be able to use those extensions to write concise macros. The easiest example is that I need to be able to dynamically inject variables into a scope, and then evaluate a form in that scope so it has access to those variables. Unfortunately, uLisp doesn't have the `:::lisp declare` functionality to make a variable `:::lisp special` so that `:::lisp eval` will pull it into scope. I eventually figured out I can use a quasiquote to construct a `:::lisp let` block on the fly and then evaluate the form inside the `:::lisp let` block. Sort of like this:

```lisp
(defun eval-in-scope (forms vars) (eval `(let ,vars ,@forms)))
;; then use it like so:
(defvar var1 4)
(defvar var2 5)
(eval-in-scope
    '((print (* x y))
      (terpri)
      (print (+ x y)))
    `((x ,var1)
      (y ,var2)))
;; => 20
;;    9
```

Unfortunately, whenever I tried to use the quasiquote functionality, something dereferenced a null pointer and crashed my microcontroller. I don't know what went wrong, but I'm now thinking about completely starting over from scratch.

There are a few reasons why I'd like to be able to do this:

1. uLisp is an Arduino sketch, not C++. This makes it hard to integrate as a library into other projects in other IDEs (such as PlatformIO).
2. uLisp is really, really, really long -- like 7,000 lines at last count. This makes it hard to maintain especially in the Arduino IDE which stutters on large files.
3. uLisp uses `:::cpp longjmp` to provide the error-handling capabilities, and the semantics of it are very confusing.
4. uLisp is optimized for RAM-starved AVR microcontrollers such as the ATmega328P, and so the data is stored in flash memory in a huge lookup table. This is a double whammy; not only does it make dynamically adding extensions on-the-fly impossible, it also requires manually maintaining four tables (the builtins enum, the string name list, the documentation list, and the main lookup table) in perfect synchrony, and if they get out of sync then Bad Stuff happens. I am targeting the ESP32, which has *megabytes* of both RAM and flash, so super-optimization is not really a concern.
5. uLisp's optimizations to find whether the builtin function is a special form, tail-recursive, a keyword, or just normal, involves checking its index in the lookup table against boundary sentinels. This means if you want to insert new special forms (such as macros and quasiquotes) you have to insert them in the middle of the table, running the risk that you'll screw up and get it out of order, making *everything* after it incorrect.[^1]
6. Having the documentation built-in to the uLisp binary is unnecessary and a waste of precious flash space in my opinion -- if you are able to download uLisp, you can also access the online documentation.

To start, I first had a look at the in-memory construction of the Lisp cons cell. The current typedef is this:

```cpp
typedef struct sobject {
  union {
    struct {
      sobject *car;
      sobject *cdr;
    };
    struct {
      unsigned int type;
      union {
        symbol_t name; // type == SYMBOL
        int integer;  // type == NUMBER
        int chars;  // type == CHAR || type == STRING
        float single_float; // type == FLOAT
      };
    };
  };
} object;
```

David describes what those fields mean a little better than I would be able to, so you're probably better off reading his explanation: <http://www.ulisp.com/show?1BLW>

Packing everything into those 64 bits is hard, and to implement a mark-and-sweep garbage collector, David had to do some terrible type punning on the `car` pointer of each cell to mark it, taking advantage of the fact that the bottom bit of the `car` pointer will always be zero (if things go well!) This is necessary for optimization, but I don't like having to do that.

In order to simplify, I am going to revise the representation of the Lisp cell. My new definition is a lot longer syntactically, but it will simplify the code a bit:

```cpp
typedef struct sobject {
  uint8_t objflags; // 0=markbit, 1=seen, 2=packed, 3=caught, 4=builtin, 5-7=unused
  uint8_t type;
  union {
    struct { // type = CONS
      sobject *car;
      sobject *cdr;
    };
    double floatnum; // type == FLOAT
    int64_t intnum; // type == NUMBER
    struct { // type == STRING || type == SYMBOL
      uint32_t chars;
      sobject *next;
    };
    struct { // type == FUNCTION
      uint32_t info;
      fn_ptr_type *cfun;
    }
    union { // type == ERROR
      uint64_t code;
      sobject *detail;
    };
  };
} object;
```

This has several advantages:

1. Because the type has been moved out of the main 64 bit field, the entirety of it can be used to store data: now I can use a `:::cpp double` instead of a `:::cpp float` and have more precision.
2. The C++ functions themselves will be stored in the global environment in the usual way (as the `:::lisp cdr` of a `:::lisp assoc` pair)
3. Error objects are returned if something went wrong, and if the error hasn't been caught (by something like `:::lisp ignore-errors` or `:::lisp unwind-protect`) it can be returned again from a recursive call and propagate up the C call stack.
4. It allows extensions functions to be added, simply by pushing a new assoc pair to the global environment

Oh - and I also want to be able to write Lisp code with less parenthesis. Something like this:

```txt
@defun eval-in-scope %forms vars
  %eval `%let ,vars ,forms
%defvar var1 4
%defvar var2 5
@eval-in-scope
  '@
    %print %* x y
    %terpri
    %print %+ x y
  `%(x ,var1) (y ,var2)
```

That is just a hypothetical syntax: The `%` means `(` and automatically close it on the end of the line, and `@` means `(` and automatically close it using Python block indentation rules. The block above would compile to the same Lisp as I wrote above, for reference.

Who know where this will go? I certainly don't.

[^1]: Editor's note: this was the case in uLisp 4.3, but in uLisp 4.4, which was released after I wrote this article, the built-ins table format was changed to make it easier to add special forms and tail forms without inserting them in the middle.
