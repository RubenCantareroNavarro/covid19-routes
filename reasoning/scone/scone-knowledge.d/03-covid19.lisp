;; Knowledge to work with the level of danger of potential transmitters:
;; A sick person is more dangerous than normal people. Therefore, a space
;; with a level of occupancy {low} with sick people can be more dangerous than
;; a space with a medium level of occupancy with normal people.

;; (new-type {potential COVID-19 transmitter} {thing})
;; (new-is-a {potential COVID-19 transmitter} {dangerous thing})
;; (new-is-a {person} {potential COVID-19 transmitter})
;; (new-is-not-a {animal} {potential COVID-19 transmitter})

;; (new-type {person with COVID-19} {sick person})
;; (x-is-the-y-of-z {high} {danger level} {person with COVID-19})

;; Knowledge to know the people that can be affected by COVID-19
;; This can be use to avoid rest homes, for example (the danger is their
;; healty, not yours).

;; (new-type {at risk for COVID-19} {person})
;; (new-is-a {elderly person} {at risk for COVID-19})
;; (new-is-a {sick person} {at risk for COVID-19})
;; (new-is-a {person with pathologies} {at risk for COVID-19})
;; ____________________________________________________

; (new-type {potential COVID-19 transmitter} {thing})
; (new-is-a {potential COVID-19 transmitter} {dangerous thing})


; (new-extended-relation {}
;           :a-inst-of {}
;           :b-inst-of {}
; 		  :c-inst-of {danger level})

; (new-type-role {} {} {})


; (new-is-a {child} {potential COVID-19 transmitter})


; ;; ____________________________________________________

; ;; Working only with occupancy:
; (new-type-role {COVID-19 danger level} {space} {danger level})

; (x-is-the-y-of-z
;     (the-x-role-of-y {c-rel-element} {is occupied by})
;     {COVID-19 danger level}
;     (the-x-role-of-y {a-rel-element} {is occupied by}))

; (x-is-a-y-of-z
;     (the-x-role-of-y {c-rel-element} {is occupied by})
;     {COVID-19 danger level}
;     (the-x-role-of-y {a-rel-element} {is occupied by}))


;; ____________________________________________________
;; ____________________________________________________
;; ____________________________________________________

(new-type {potential COVID-19 transmitter} {thing})
(new-is-a {potential COVID-19 transmitter} {dangerous thing})
(new-is-a {person} {potential COVID-19 transmitter})
(new-is-not-a {animal} {potential COVID-19 transmitter})


; (new-type-role {transmission risk} {potential COVID-19 transmitter} {level})

; (x-is-the-y-of-z
;     {high}
;     {transmission risk}
;     {child} ; (the-x-role-of-y {b-rel-element} {is occupied by})
; )

; (x-is-the-y-of-z {low} {transmission risk} {elderly person})

; (new-type-role {COVID-19 vulnerability level} {person} {level})
; (x-is-the-y-of-z {low} {COVID-19 vulnerability level} {child})
; (x-is-the-y-of-z {high} {COVID-19 vulnerability level} {elderly person})


;; ____________________________________________________

(new-measurable-quality {risk level})
(new-unit {risk level unit} {risk level} nil 1)

(new-indv {transmission risk measure} {intangible})
(new-type-role {transmission risk level} {potential COVID-19 transmitter} {transmission risk measure})
(x-is-the-y-of-z 
    (new-measure 1 {risk level unit})
    {transmission risk level} 
    {elderly person})

(x-is-the-y-of-z 
    (new-measure 10 {risk level unit})
    {transmission risk level} 
    {child})

;; ____________________________________________________

(new-measurable-quality {vulnerability level})
(new-unit {vulnerability level unit} {vulnerability level} nil 1)

(new-indv {vulnerability measure} {intangible})
(new-type-role {COVID-19 vulnerability level} {person} {vulnerability measure})
(x-is-the-y-of-z 
    (new-measure 10 {vulnerability level unit})
    {COVID-19 vulnerability level} 
    {elderly person})

(x-is-the-y-of-z 
    (new-measure 1 {vulnerability level unit})
    {COVID-19 vulnerability level} 
    {child})


; (the-x-of-y {COVID-19 vulnerability level} {child})
; (the-x-of-y {measure magnitude} (the-x-of-y {COVID-19 vulnerability level} {child}))
; (the-x-of-y {measure unit} (the-x-of-y {COVID-19 vulnerability level} {child}))

;; ____________________________________________________

(new-measurable-quality {occupation})
(new-unit {occupation unit} {occupation} nil 1)

(new-indv {occupation level measure} {intangible})
(new-type-role {occupation level} {space} {occupation level measure})
(x-is-the-y-of-z 
    (new-measure 10 {occupation unit})
    {occupation level} 
    {school})

(x-is-the-y-of-z 
    (new-measure 1 {occupation unit})
    {occupation level} 
    {rest home})