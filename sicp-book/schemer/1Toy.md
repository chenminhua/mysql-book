# what is atom?

# what is list
()是list吗？  是的

# s表达式
xyz是s表达式吗？    是的，所有atom都是s表达式
(x y z)是s表达式吗？  是的，所有list都是s表达式
((x y) z)是s表达式吗？ 是的

# the law of car
the primitive car is defined only for non-empty lists
what is the car of l where l is (((hotdogs)) (and) (pickle) relish)?   ((hotdogs))
what is (car (car l)) where l is  (((hotdogs)) (and))?                 (hotdogs)

# the law of cdr
the primitive cdr is defined only for non-empty lists. The cdr of any non-empty list is always another list.
what is the cdr of l where l is (a b c)?    (b c)
what is the cdr of l where l is ((a b c) x y x)?     (x y z)
what is (car (cdr l)) where l is ((b) (x y) ((c)))?      (x y)

# the law of cons
the primitive cons takes two arguments, the second argument must be a list. the result is a list
cons接受两个参数，第一个是s表达式，第二个是list
s is (a b (c)), l is (), 那么(cons s l)是？      ((a b (c)))
s is a, l is ((b) c d), 那么(cons s (car l))?    (a b)

# the law of Null?
the primitive null? is defined only for lists
is (null? l) true or false where l is (a b c)?     false
is (atom? s) true or false where s is harry?       true

# the law of Eq?
the primitive eq? takes two arguments. Each must be a non-numeric atom
is (eq? (car l) a) true where l is (Mary had a little lamb chop) and a is Mary?   true