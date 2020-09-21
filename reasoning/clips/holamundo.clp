(deftemplate book
  (slot title
    (type STRING)
    (default "Unknown"))
  (slot author
    (type STRING)
    (default "Unknown"))
  (slot date
    (type INTEGER)
    (default 2001)
    (range 1600 2009)))


(defrule remove-pratas "remove all Prata's books"
  (remove-pratas 1)
  ?which <- (book (title ?t) (author "Stephen Prata") (date ?d))
  =>
    (printout t "Removing book " ?t " from " ?d " year" crlf)
    (retract ?which))


(deffacts books
    (book (title "Clisp book") (author "Giarratano") (date 2001))
    (book (title "Common Lisp") (author "someone") (date 2005))
    (book (title "C++") (author "Stephen Prata") (date 2002))
    (book (title "ANSI C") (author "Stephen Prata") (date 2000)))


; (load ../../src/holamundo.clp)
; (assert (remove-pratas 1))