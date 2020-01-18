(cons 1 (cons 2 (cons 3 ())))
(list 1 2 3)

(define one-through-four (list 1 2 3 4))
(car one-through-four)      ; 1
(cdr one-through-four)      ; (2 3 4)
(cons 10 one-through-four)  ; (10 1 2 3 4)

; 取出元素
(define (list-ref items n)
  (if (= n 0)
      (car items)
      (list-ref (cdr items) (- n 1))))

(define squares (list 1 4 9 16 25))
(list-ref squares 3)        ; 16

;列表长度
(define (length items)
  (if (null? items)
    0
    (+ 1 (length (cdr items)))))
(length squares)               ;5

; append
(define (append list1 list2)
  (if (null? list1)
    list2
    (cons (car list1) (append (cdr list1) list2))))


; 对表的映射
(define (scale-list items factor)
  (if (null? items)
      ()
      (cons (* (car items) factor)
            (scale-list (cdr items) factor))))
(scale-list (list 1 2 3 4 5) 10)