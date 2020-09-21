(new-context {morning} {general})
(in-context {morning})
(new-extended-statement {school} {is occupied by} {child} :c {high})
(new-extended-statement {pub} {is occupied by} {person} :c {low})
;; _____________________________________________________________________

(new-context {afternoon} {general})
(in-context {afternoon})
(new-extended-statement {school} {is occupied by} {child} :c {medium})
(new-extended-statement {pub} {is occupied by} {person} :c {medium})
;; _____________________________________________________________________

(new-context {evening} {general})
(in-context {evening})
(new-extended-statement {school} {is occupied by} {child} :c {zero})
(new-extended-statement {pub} {is occupied by} {person} :c {high})
;; _____________________________________________________________________

(in-context {general})

;; (in-context {morning})
;; (list-all-x-of-y {COVID-19 danger level} {school})
;; (is-x-a-y? (the-x-role-of-y {COVID-19 danger level} {school}) {high})
;; (the-x-of-y {COVID-19 danger level} {school})
;; (a-x-of-y {COVID-19 danger level} {school})