(define x (list (list 1 2) (list 3 4)))

(define (deep-reverse l)
  (if (null? l)
      ()
      (append (deep-reverse (cdr l)) (
        if (pair? (car l))
          (list (reverse (car l)))
          (list (car l))
      ))))
(deep-reverse (list (list 1 2) (list 3 4)))