(deftemplate context
    (slot year (type INTEGER))
    (slot month (type SYMBOL) (allowed-symbols January February March April May June July August September October November December))
    (slot day (type INTEGER))
    (slot day-of-week (type SYMBOL) (allowed-symbols Monday Tuesday Wednesday Thursday Friday Saturday Sunday))

    (slot time-hour (type INTEGER))
    (slot time-minutes (type INTEGER))

    (slot is-public-holiday (type SYMBOL) (allowed-symbols YES NO) (default NO))
    (slot is-class-period (type SYMBOL)(allowed-symbols YES NO) (default YES))
)

(deftemplate school-ocupation
    (slot ocupation (type SYMBOL) (allowed-symbols Zero Low Medium High))
)

(defrule holidays
    ?f1 <- (context (year ?year) (month ?month&July | August) (day ?day) (day-of-week ?day-of-week) (time-hour ?time-hour) (time-minutes ?time-minutes) (is-public-holiday ?is-public-holiday) (is-class-period YES))
    =>
    (retract ?f1)
    (assert (context (year ?year) (month ?month) (day ?day) (day-of-week ?day-of-week) (time-hour ?time-hour) (time-minutes ?time-minutes) (is-public-holiday ?is-public-holiday) (is-class-period NO)))
)

(defrule weekend
    (context (day-of-week ?day&Saturday | Sunday))
    =>
    (assert (school-ocupation (ocupation Zero)))
    (printout t "Occupancy level Zero for being a weekend. Dia de la semana: " ?day crlf)
)

(defrule not-class-period
    (context (is-class-period NO))
    =>
    (assert (school-ocupation (ocupation Zero)))
    (printout t "Occupancy level Zero for not being a class period" crlf)
)

(defrule public-holiday
    (context (is-public-holiday YES))
    =>
    (assert (school-ocupation (ocupation Zero)))
    (printout t "Occupancy level Zero for being a public holiday" crlf)
)

(defrule school-time
    (context    (day-of-week ?day&~Saturday & ~Sunday)
                (is-class-period YES)
                (is-public-holiday NO)
                (time-minutes ?time-minutes)
                (time-hour ?time-hour))

    (test   
        (or     (and (>= ?time-hour 10) (< ?time-hour 14))
                (and (> ?time-hour 8)   (< ?time-hour 10)   (> ?time-minutes 30))
        )
    )
    =>
    (assert (school-ocupation (ocupation Medium)))
    (printout t "Occupancy level Medium. Time: " ?time-hour ":" ?time-minutes crlf)
)

(defrule school-leaving-time
    (context    (day-of-week ?day&~Saturday & ~Sunday)
                (is-class-period YES)
                (is-public-holiday NO)
                (time-minutes ?time-minutes)
                (time-hour ?time-hour&14))

    (test   
        (and (>= ?time-minutes 00)   (< ?time-minutes 30))
    )
    =>
    (assert (school-ocupation (ocupation High)))
    (printout t "Occupancy level High. Time: " ?time-hour ":" ?time-minutes crlf)
)

(defrule school-entry-time
    (context    (day-of-week ?day&~Saturday & ~Sunday)
                (is-class-period YES)
                (is-public-holiday NO)
                (time-minutes ?time-minutes)
                (time-hour ?time-hour&9))

    (test   
        (and (>= ?time-minutes 00)   (< ?time-minutes 30))
    )
    =>
    (assert (school-ocupation (ocupation High)))
    (printout t "Occupancy level High. Time: " ?time-hour ":" ?time-minutes crlf)
)

(defrule not-school-time
    (context    (day-of-week ?day&~Saturday & ~Sunday)
                (is-class-period YES)
                (is-public-holiday NO)
                (time-minutes ?time-minutes)
                (time-hour ?time-hour))

    (test   
        (or     (and (>= ?time-hour 15) (<= ?time-hour 23))
                (and (>= ?time-hour 00) (<= ?time-hour 09))
                (and (> ?time-hour 13)  (< ?time-hour 15)   (> ?time-minutes 30))
        )
    )
    =>
    (assert (school-ocupation (ocupation Zero)))
    (printout t "Occupancy level Zero. Time: " ?time-hour ":" ?time-minutes crlf)
)

; (deffacts contexto
    ; (context (day-of-week Saturday)) ; Zero level --> Weekend
    ; (context (month July)) ; Zero --> there is not class
    ; (context (is-public-holiday YES)) ; Zero --> is public holiday

    ; (context (day-of-week Monday) (is-class-period YES) (is-public-holiday NO) (time-hour 9) (time-minutes 25)) ; Medium (9:30-14:00)
    ; (context (day-of-week Friday) (is-class-period YES) (is-public-holiday NO) (time-hour 14) (time-minutes 16)) ; High (14:00-14:30)
    ; (context (day-of-week Friday) (is-class-period YES) (is-public-holiday NO) (time-hour 9) (time-minutes 09)) ; High (09:00 - 09:30)
    ; (context (day-of-week Wednesday) (is-class-period YES) (is-public-holiday NO) (time-hour 14) (time-minutes 55)) ; High (14:30-09:00)
; )

; (load ../../src/schools_proof_concept.clp)
; (watch facts school-ocupation)
