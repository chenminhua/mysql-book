(define (last-pair a)
  (if (null? (cdr a))
    a
    (last-pair (cdr a))))

(last-pair (list 1 3 4 5 7 9))