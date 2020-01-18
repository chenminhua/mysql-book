(define (square-list items)
  (if (null? items) 
      ()
      (cons (square (car items)) (square-list (cdr items)))))

(define (square-list2 items) 
  (map (lambda (x) (square x)) items))

(define (square-list3 items)
  (map square items))

(define items (list 1 2 3))
(square-list items)
(square-list2 items)
(square-list3 items)
