;; Knowledge to work with the level of danger of potential transmitters:
;; A sick person is more dangerous than normal people. Therefore, a space
;; with a level of occupancy {low} with sick people can be more dangerous than
;; a space with a medium level of occupancy with normal people.

;; ____________________________________________________
;; ____________________________________________________
;; ____________________________________________________

(new-type {potential COVID-19 transmitter} {thing})
(new-is-a {potential COVID-19 transmitter} {dangerous thing})
(new-is-a {person} {potential COVID-19 transmitter})
(new-is-not-a {animal} {potential COVID-19 transmitter})

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

(x-is-the-y-of-z 
    (new-measure 5 {risk level unit})
    {transmission risk level} 
    {young person})

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

(x-is-the-y-of-z 
    (new-measure 1 {vulnerability level unit})
    {COVID-19 vulnerability level} 
    {young person})


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