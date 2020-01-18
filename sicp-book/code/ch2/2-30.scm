(define (square-tree-map tree)
	(map 
		(lambda (x)
			(if (pair? x)
				(square-tree-map x)
				(square x)
			)
		)
		tree)
)

(square-tree-map (list 1 (list 2 (list 3 4) 5) (list 6 7)))