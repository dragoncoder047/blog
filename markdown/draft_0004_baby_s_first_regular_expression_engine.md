Title: Baby's First Regular Expression Engine
Date: 2023-04-12
Status: Draft
Tags: programming, lisp

I spent spring break finding a whole lot of bugs in uLisp. There are probably more, and I expect I'll eventually find them. The bugs are fixed, and I've added a lot of improvements. And now all of a sudden, I thought, "I should add regular expressions to uLisp." Why? I don't know. Some part of me just wants to find a good regular expression library and hook it up into uLisp, just like I did with LIL. The other part of me says that's cheating, and I should write it myself. The other part won.

So what is a regular expression anyway? A regular expression, put formally, is a string of characters that describe another pattern of characters to be searched for in another string. The [Wikipedia article on regular expressions](https://en.wikipedia.org/wiki/Regular_expression#Basic_concepts) provides a pretty good explanation of regular expressions, and how they are written in major programming languages -- I'm going to try to mirror these pretty closely.

Most times, the regular expression engine begins by *compiling* the regular expression into an internal representation. From looking at the parts of a regular expression, any regular expression can be decomposed into a tree of atoms, concatenations or alternations, and repetition of items in the tree. An atom is any trivial pattern or seq of characters that can't match a variable number of times -- for example, the string `cat`, which matches `cat` and nothing else; the character class `[aeiou]`, which matches any vowel; the mixed string `gr[ae]y` (`gray` or `grey`), or even the Lua balanced-paren matcher construct `%b()` which matches `((())())` but not `(((()`. Then the rest of the regular expression is simply a tree of atoms combined with repetition, concatenation, or alternation.

Because I am writing a regular expression engine for uLisp I'll let the intermediate ("compiled") representation be a Lisp structure -- that way, it will be garbage collected; and I can also write out a regular expression in the verbose Lisp form to allow comments and such.

To that end, here are the list structures I'm using to represent different regular expression constructs:

```lisp
;; matches x1, x2, x3 in that order
(seq x1 x2 x3 ...)

;; matches x1 or x2 or x3, preferring ones listed first
(or x1 x2 x3 ...)

;; repetition of x -- max of nil means infinity
(repeat min max greedy-p x)

;; matches x, and then puts what matched into a capture group called name
(capture name x)

;; tries to match the same text as the capture group called name previously matched
(backref name)

;; the regular expression <(%S+).*?(?:/>|>.*?</%1>) (which matches well-formed XML tags) expands to:
(seq
    "<"
    (capture 'tag (repeat 1 nil t "%S"))
    (repeat 0 nil nil ".")
    (or
        "/>"
        (seq
            ">"
            (repeat 0 nil nil ".")
            "</"
            (backref 'tag)
            ">")))
```

<!--
(defmacro optional (greedy-p x) (list 'repeat 0 1 greedy-p x)) ;; x?
(defmacro some (greedy-p x) (list 'repeat 0 t greedy-p x)) ;; x*
(defmacro more (greedy-p x) (list 'repeat 1 t greedy-p x)) ;; x+
-->

I'll start with the engine that actually tries to match these constructs against a string; the compiler will come later.

Atomic expressions are rather simple, and I'll also leave those for later because the algorithm for those has no backtracking, it either matches everything or fails.

To "backtrack" I'll use returning nil as a signal for no match, and t for a match, and representing the current state as a three-element list containing the current string, the stack of capture groups, and the stack of saved backtracking points.

??? info "Utility functions here"
    ```lisp
    (defun save-waypoint (state)
        (push (cons (first state) (second state)) (nth 2 state)))

    (defun succeeded (state)
        (pop (nth 2 state)) ;; drop backtracking point, but don't backtrack
        t)

    (defun backtrack (state)
        (let ((old-pair (pop (nth 2 state))))
            (setf (first state) (car old-pair))
            (setf (nth 1 state) (cdr old-pair)))
        nil)
    ```

Here's the simplest one, `seq`. It simply iterates through the items, and fails when it gets to the first one that fails:

```lisp
(defun match-seq (state patterns)
    (save-waypoint state)
    (dolist (sub-pattern patterns (succeeded state))
        (when (null (match-pattern state sub-pattern))
            (backtrack state)
            (return nil))))
```

The one for `or` is similar -- it succeeds on the first one that succeeds. It's shorter because it doesn't need to backtrack when it fails as nothing succeeded.

```lisp
(defun match-or (state patterns)
    (dolist (sub-pattern patterns nil)
        (when (match-pattern state sub-pattern)
            (return t))))
```

`capture` simply tries to match, and if so, adds the capture to the captures stack, while `backref` tries to match the captured string:

```lisp
(defun match-capture (state pattern tag)
    (save-waypoint state)
    (if (match-pattern state pattern)
        (let* ((old-state (pop (nth 2 state)))
            (old-string (first old-state))
            (curr-string (first state)))
            (push (cons tag (subseq old-string 0 (- (length old-string) (length curr-string))))))
        (backtrack state)))

(defun match-backref (state tag)
    (let ((group (assoc tag (second state))))
        (unless group
            (error "capture group ~a is not valid here" tag))
        (if (string= (cdr group) (subseq (first state) 0 (length (cdr group))))
            (progn
                (setf (first state) (subseq (first state) (length (cdr group))))
                t)
            nil)))
```

TODO: FINISH ME
