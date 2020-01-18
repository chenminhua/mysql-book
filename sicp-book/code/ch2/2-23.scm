(define (for-each f items)
	(if (null? items)
    '()
    (cons (f (car items)) (for-each f (cdr items)))))

(for-each display (list 1 2 3))
