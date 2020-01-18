(define (make-monitored f)
  (define calls 0)
  (lambda (x) 
    (if (eq? x 'how-many-call?)
        calls
        (begin 
          (set! calls (+ calls 1))
          (f x)
        )
    )
  )
)

(define s (make-monitored sqrt))

(s 100)
(s 81)

(s 'how-many-call?)