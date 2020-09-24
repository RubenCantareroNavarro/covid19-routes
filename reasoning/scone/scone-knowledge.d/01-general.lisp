; ;; already in use (new-type {animal} {thing})
; ;; already in use (new-type {person} {thing})
; ;; (new-type {elderly person} {person})
; ;; (new-type {middle-aged person} {person})
; ;; (new-type {young person} {person})
; ;; already in use (new-type {child} {person})

; ;; (new-type {sick person} {person})
; ;; (new-type {person with pathologies} {person})

; (new-type {space} {thing})
; (new-type {building} {space})
; (new-is-a {school} {building})
; (new-type {pub} {building})
; ;; (new-type {rest home} {building})

; ;; (new-type {disease} {thing})
; ;; (new-indv {COVID-19} {disease})

; (new-type {level} {measure})
; (new-type {zero} {level})
; (new-type {low} {level})
; (new-type {medium} {level})
; (new-type {high} {level})	

; (new-type {danger level} {level})
; (new-type {occupancy level} {level})

; (new-extended-relation {is occupied by}
;           :a-inst-of {space}
;           :b-inst-of {person}
; 		  :c-inst-of {occupancy level})


(new-type {elderly person} {person})
(new-type {middle-aged person} {person})
(new-type {young person} {person})
;; already in use (new-type {child} {person})
;; ____________________________________________________

(new-type {space} {thing})
(new-type {building} {space})
(new-type {amenity} {building})
(new-is-a {school} {amenity})
(new-type {pub} {amenity})
(new-type {rest home} {amenity})
;; ____________________________________________________

; (new-type {level} {measure})
; (new-type {zero} {level})
; (new-type {low} {level})
; (new-type {medium} {level})
; (new-type {high} {level})	

; (new-type {danger level} {level})
; (new-type {occupancy level} {level})

(new-relation {is occupied by}
          :a-type-of {space}
          :b-type-of {person})

(new-statement {school} {is occupied by} {child})
(new-statement {rest home} {is occupied by} {elderly person})