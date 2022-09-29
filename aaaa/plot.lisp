(defun poly (x a)
    (let ((result 0) (n (length a)))
         (dotimes (k n)
             (setq result (+ (* (nth k a) (expt x (- n k 1))) result)))
         result))

(defun zerocross (f x y d)
    (or
        (eq (< 0 (funcall f x y)) (> 0 (funcall f (- x d) y)))
        (eq (< 0 (funcall f x (- y d))) (> 0 (funcall f x y)))
        (eq (< 0 (funcall f x y)) (> 0 (funcall f (+ x d) y)))
        (eq (< 0 (funcall f x (+ y d))) (> 0 (funcall f x y)))))

(defun axis (x y)
    (if (and (= 0 x) (= 0 y)) "+"
        (if (= 0 x) "|"
            (if (= 0 y) "-"
                (if (and (= 0 (mod x 2)) (= 0 (mod y 2))) "." " ")))))

(defun range (min max step)
    (let ((l nil) (c min))
         (loop
             (push c l)
             (setq c (+ c step))
             (when (>= c max) (return l)))))

(defun plot (fx tx fy ty s fun)
    (with-output-to-string (out)
        (dolist (y (range fy ty s))
            (dolist (x (range fx tx s))
                (princ (if (zerocross fun x y s) "#" (axis x y)) out))
            (terpri out))))

(princ
    (plot
        -20 20 ; x-values
        -20 20 ; y-values
        1 ; step in each direction
        (lambda (x y) (+ (poly x '(1 -10 0)) (poly y '(1 0 0 -70))))))