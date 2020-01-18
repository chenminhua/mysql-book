; 计算函数不动点
(define tolerance 0.00001)

(define (close-enough? x y)
  (< (abs (- x y)) tolerance))

(define (fixed-point f first-guess)
  (define (try guess)
    (let ((next (f guess)))
    (if (close-enough? guess next)
      next
      (try next))
      (display next)
      (newline)
      ))  
  (try first-guess))

(fixed-point (lambda (x) (/ (log 1000) (log x))) 2.0)