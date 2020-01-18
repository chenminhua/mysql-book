(define (factorial n)
  (define (iter product counter)
    (if (> counter n)
      product
      (iter (* counter product)
            (+ counter 1))))
  (iter 1 1))

(factorial 5)

(define (factorial2 n)
  (let ((product 1) (counter 1))
    (define (iter) 
      (if (> counter n)
        product
        (begin 
          (set! product (* counter product))
          (set! counter (+ counter 1))
          (iter))))
          (iter))
)

(factorial2 5)