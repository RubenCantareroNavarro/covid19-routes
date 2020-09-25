;; ____________________________________________________
;; ____________________________________________________
;; ____________________________________________________

(new-type {sick person} {person})
(new-type {person with pathologies} {person})

;; ____________________________________________________

(new-type {elderly person} {person})
(new-type {middle-aged person} {person})
(new-type {young person} {person})

;; ____________________________________________________


(new-type {space} {thing})
(new-type {building} {space})
(new-type {amenity} {building})
(new-is-a {school} {amenity})
(new-type {pub} {amenity})
(new-type {rest home} {amenity})

;; ____________________________________________________


(new-relation {is occupied by}
          :a-type-of {space}
          :b-type-of {person})

(new-statement {school} {is occupied by} {child})
(new-statement {rest home} {is occupied by} {elderly person})

;; ONLY TO TEST
(new-statement {school} {is occupied by} {young person})
