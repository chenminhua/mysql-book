(define (gcd a b)
  (cond ((= b 0) a)
        (else (gcd b (remainder a b)))))

(gcd 210 40)
(gcd 211 40)
(gcd 208 40)