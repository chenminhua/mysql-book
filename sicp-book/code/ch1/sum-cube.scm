(define (cube x) (* x x x))

(define (sum-integers a b)
  (if (> a b)
      0
      (+ a (sum-integers (+ a 1) b))))

(define (sum-cubes a b)
  (if (> a b)
      0
      (+ (cube a) (sum-cubes (+ a 1) b))))

(define (pi-sum a b)
  (if (> a b)
      0
      (+ (/ 1.0 (* a (+ a 2))) (pi-sum (+ a 4) b))))

(sum-integers 2 4)
(sum-cubes 2 4)
(pi-sum 1 10000)

(define (sum term a next b) 
  (if (> a b)
    0
    (+ (term a) (sum term (next a) next b))))

(define (pi-sum2 a b)
  (sum (lambda (x) (/ 1.0 (* x (+ x 2)))) a (lambda (x) (+ x 4)) b))

(pi-sum2 1 100)
