; 自己实现序对，不用任何数据结构
(define (cons x y)
  (define (dispatch m)
    (cond ((= m 0) x)
          ((= m 1) y)
          (else (error "argument not 0 or 1 --CONS" m))))
  dispatch)

(cons 1 2)

(define (car z) (z 0))
(define (cdr z) (z 1))

(car (cons 1 2))
(cdr (cons 1 2))
