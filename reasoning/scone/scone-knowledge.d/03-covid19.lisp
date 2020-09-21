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

;; Working only with occupancy:
(new-type-role {COVID-19 danger level} {space} {danger level})

(x-is-the-y-of-z
    (the-x-role-of-y {c-rel-element} {is occupied by})
    {COVID-19 danger level}
    (the-x-role-of-y {a-rel-element} {is occupied by}))

(x-is-a-y-of-z
    (the-x-role-of-y {c-rel-element} {is occupied by})
    {COVID-19 danger level}
    (the-x-role-of-y {a-rel-element} {is occupied by}))

