; 逆序
(define (reverse l)
  (if (null? (cdr l))
      (list (car l))
      (append (reverse (cdr l)) (list (car l)))))
 
(reverse (list 1 4 9 16 25)) 
