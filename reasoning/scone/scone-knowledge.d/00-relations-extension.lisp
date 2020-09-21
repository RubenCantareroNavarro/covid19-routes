(defvar *a-rel-element* nil)
(defvar *b-rel-element* nil)
(defvar *c-rel-element* nil)

(setq *a-rel-element*
      (new-indv-role {a-rel-element} {relation} {thing}
      :english '(:no-iname :role)))
(setq *b-rel-element*
      (new-indv-role {b-rel-element} {relation} {thing}
      :english '(:no-iname :role)))
(setq *c-rel-element*
      (new-indv-role {c-rel-element} {relation} {thing}
      :english '(:no-iname :role)))

(defun new-extended-relation (iname &key
							  a
							  a-inst-of
							  a-type-of
							  b
							  b-inst-of
							  b-type-of
							  c
							  c-inst-of
							  c-type-of
							  (parent *relation*)
							  symmetric
							  transitive
							  english
							  inverse)

	(new-relation iname
				  a a-inst-of a-type-of
				  b b-inst-of b-type-of
				  c c-inst-of c-type-of
				  parent symmetric transitive
				  english inverse)
                           
	(if (lookup-element iname)
		;; This node already exists.  See if it is a relation.
		(if (eq :yes (is-x-a-y? iname *relation*))
            ;; Yes, add the role restrictions.
            (progn
                (setq iname (lookup-element iname))
                ;; Add the role restrictions, if any.
                (when a-inst-of
                    (the-x-of-y-is-a-z *a-rel-element* iname a-inst-of))
                (when b-inst-of
                    (the-x-of-y-is-a-z *b-rel-element* iname b-inst-of))
                (when c-inst-of
                    (the-x-of-y-is-a-z *c-rel-element* iname c-inst-of))
            iname)
            ;; No, complain and do nothing else.
            (commentary
            "~&New relation ~S already exists and is not a relation.  Ignoring.~%"
            iname)
        )
    )
)

(defun new-extended-statement (a rel b
							   &key
							   c
							   (context *context*)
							   negate
							   dummy
							   iname
							   english)

	(new-statement a rel b c
				   context negate
				   dummy iname english)

	(let ((e (new-indv nil rel)))
		(when a
			(x-is-the-y-of-z a *a-rel-element* e))
		(when b
			(x-is-the-y-of-z b *b-rel-element* e))
		(when c
			(x-is-the-y-of-z c *c-rel-element* e))
	e)
)