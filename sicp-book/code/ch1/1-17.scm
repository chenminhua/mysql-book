(define (fast-expr x n)
  (cond 
    ((odd? n) (fast-expr (* x x) (/ n 2)))
    (else (* x(fast-expr x (- n 1))))))