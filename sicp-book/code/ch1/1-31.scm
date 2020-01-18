(define (pi a b)
  (if (> a b)
      1
      (* (* (/ (- a 1) a) (/ (+ a 1) a)) (pi (+ a 2) b))))

(pi 3 1000)