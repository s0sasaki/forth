s" testing C function...\n" type

: call_f
    >rdi >rsi
    call f
    rax>
;
200 100 call_f .

s"  -> 300\n" type

s" done.\n" type

 ( MEMO  SystemV AMD64 ABI
 ( : call_f
 (     >rdi >rsi >rdx >rcx >r8 >r9
 (     call f
 (     rax> rdx>
 ( ;
 ( 6 5 4 3 2 1 call_f drop . cr drop
 )
