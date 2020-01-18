; 计算函数不动点
(define tolerance 0.00001)

(define (close-enough? x y)
  (< (abs (- x y)) tolerance))

(define (fixed-point f first-guess)
  (define (try guess)
    (let ((next (f guess)))
    (if (close-enough? guess next)
      next
      (try next))))  
  (try first-guess))

(fixed-point cos 1.0)

(define (f x)
  (+ 1 (/ 1 x)))

(fixed-point f 1.0) ; 黄金分割率