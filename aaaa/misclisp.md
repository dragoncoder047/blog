Title: Lisp Practice
Date: 2022-09-28

Today I decided I would have a little fun with Lisp. I wanted to try and make a program that you can type in a function and get a graph of it.

I started off with a function that takes an $x$-value and a list of coefficients, and evaluates the polynomial defined by those coefficients. Here's the function:

```lisp
(defun poly (x a)
    (let ((result 0) (n (length a)))
         (dotimes (k n)
             (setq result (+ (* (nth k a) (expt x (- n k 1))) result)))
         result))
```

And here's using it to evaluate the polynomial $2x^3-x^2+5x-10$ at $x=3$:

```lisp
(poly 3 '(2 -1 5 -10))
```

Then I thought how to turn each of those points into an ASCII-art graph.

The polt function uses two nested `:::lisp dolist` loops iterating over a list of x-values and y-values, and then at each point, it has to decide domehow whether to plot a point (by returning "#" insread of the background character). The simplest solution is to only plot it if $y = f(x)$ and don't otherwise, but this only works when lines cross exactly over the gridline.

After considering a number of other methods, I decided on the method that [mattbatwings](https://www.youtube.com/c/Mattbatwings) used in [his Minecraft graphing calculator](https://www.youtube.com/watch?v=EvvWOaLgKVU). This represents a function as 3D surface in $x$ and $y$, and then plotting all the points where the surface crosses the $x$-$y$ plane at $z=0$.

This function makes that decision. It takes the function $f$, the $x$ and $y$ coordinates, and $d$ which represents the distance between gird lines.

```lisp
(defun zerocross (f x y d)
    (or
        (eq (< 0 (funcall f x y)) (> 0 (funcall f (- x d) y)))
        (eq (< 0 (funcall f x (- y d))) (> 0 (funcall f x y)))
        (eq (< 0 (funcall f x y)) (> 0 (funcall f (+ x d) y)))
        (eq (< 0 (funcall f x (+ y d))) (> 0 (funcall f x y)))))
```

If there is a sign change in the function close to the point, it returns `:::lisp t`, otherwise it returns `:::lisp nil`.

Now all that's left to do is iterate over the provided ranges and call `zerocross` at each x- and y-value, and if there is no zero crossing, return the "background" characters.

`axis` returns a line character if it is on the axis, and dots for a grid at increments of 2.

```lisp
(defun axis (x y)
    (if (and (= 0 x) (= 0 y)) "+"
        (if (= 0 x) "|"
            (if (= 0 y) "-"
                (if (and (= 0 (mod x 2)) (= 0 (mod y 2))) "." " ")))))
```

`range` is an emulation fo the Python `:::py3 range` function, which returns a list of numbers from `min` up to `max` in increments of `step`.

```lisp
(defun range (min max step)
    (let ((l nil) (c min))
         (loop
             (push c l)
             (setq c (+ c step))
             (when (>= c max) (return l)))))
```

`plot` then iterates over the entire x-y plane within the given range, and plots the function:

```lisp
(defun plot (fx tx fy ty s fun)
    (with-output-to-string (out)
        (dolist (y (range fy ty s))
            (dolist (x (range fx tx s))
                (princ (if (zerocross fun x y s) "#" (axis x y)) out))
            (terpri out))))
```

If you're interested in the whole code, here it is: [plot.lisp]({attach}plot.lisp){download="plot.lisp"}

Here's using it to plot the function $y^3-x^2-10x-70=0$:

```lisp
(princ
    (plot
        -20 20 ; x-values
        -20 20 ; y-values
        1 ; step in each direction
        (lambda (x y) (+ (poly x '(1 -10 0)) (poly y '(1 0 0 -70))))))
```

This produces this neat graph:

```txt
                   |                    
 . . . . . . . . . | . . . . . . . . . .
                   |                    
 . . . . . . . . . | . . . . . . . . . .
                   |                    
 . . . . . . . . . | . . . . . . . . . .
                   |                    
 . . . . . . . . . | . . . . . . . . . .
                   |                    
 . . . . . . . . . | . . . . . . . . . .
                   |                    
 . . . . . . . . . | . . . . . . . . . .
                   |                    
 . . . . . . . . . | . . . . . . . . . .
         ###########                    
 . . .#################. . . . . . . . .
     ####          |####                
 . .## . . . . . . | . ##. . . . . . . .
    ##             |   ##               
----##-------------+---##---------------
    ##             |   ##               
 . ##. . . . . . . | . .## . . . . . . .
  ##               |     ##             
###. . . . . . . . | . . .###. . . . . .
##                 |       #####        
 . . . . . . . . . | . . . . ######. . .
                   |            ####### 
 . . . . . . . . . | . . . . . . . #####
                   |                   #
 . . . . . . . . . | . . . . . . . . . .
                   |                    
 . . . . . . . . . | . . . . . . . . . .
                   |                    
 . . . . . . . . . | . . . . . . . . . .
                   |                    
 . . . . . . . . . | . . . . . . . . . .
                   |                    
 . . . . . . . . . | . . . . . . . . . .
                   |                    
 . . . . . . . . . | . . . . . . . . . .
```

Pretty neat! An easy self-introduction to a programming language I though I'd never learn. Maybe I'll take some time to learn more.
