(define (map proc items)
  (if (null? items)
      null
      (cons (proc (car items))
            (map proc (cdr items)))))
(map abs (list -10 2.5 -11.6 17))

(define (for-each proc list) 
   (cond 
    ((null? list)) 
    (else (proc (car list)) 
          (for-each proc (cdr list))))) 
