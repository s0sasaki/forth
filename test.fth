: cr s" \n" type ;

s" testing arithmetics... " type
7 2 + 2 - .  ( 7+2-2)
3 4 * 2 / 1 + .  ( 3*4/2+1)
2 3 drop dup dup 1 + + + 7 dup . . . 
s"  -> 77777" type cr

s" testing variables... " type
variable XXX 
999 XXX ! 
XXX @ .
s"  -> 999" type cr

s" testing functions... " type 
: sq dup * ;
3 sq .
: sqsq sq sq ;
3 sqsq . 
s"  -> 981" type cr

s" testing conditionals... " type
-1  if 1 . then 2 .            ( True is -1, false is 0. )
0 if 4 . then 3 .            
-1  if 7 . else 4 . then 7 .
0 if 4 . else 7 . then 7 . 
-1 if -1 if 1 . then 2 . then 3 .
0 if 4 . else 0 if 4 . else 1 . then 2 . then 3 .
s"  -> 1237777123123" type cr

s" testing comparisons... " type
1 2 < . 
1 0 < .
1 1 <= .
1 0 <= .
2 1 > .
0 1 > .
1 1 >= .
0 1 >= .
1 1 = .
0 1 = .
1 2 <> .
1 1 <> .
s"  -> -10-10-10-10-10-10" type cr

s" testing recursion... " type
: factorial
    dup 1 > if 
    dup 1 - factorial * endif
;
5 factorial .
s"  -> 120" type cr
    
s" done.\n" type

