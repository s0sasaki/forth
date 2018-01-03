code = "6 3 + 2 - . 3 4 * 2 / 1 + . 2 3 drop dup dup 1 + + + 7 dup . . ."

def translator(token):
    if token.isdigit():
        print("    pushq $"+token)
    elif token == "+":
        print("    popq %rax")
        print("    addq %rax, (%rsp)")
    elif token == "-":
        print("    popq %rax")
        print("    subq %rax, (%rsp)")
    elif token == "*":
        print("    popq %rax")
        print("    imulq (%rsp), %rax")
        print("    movq %rax, (%rsp)")
    elif token == "/":
        print("    popq %rbx")
        print("    popq %rax")
        print("    cqto")
        print("    idivq %rbx")
        print("    pushq %rax")
    elif token == ".":
        print("    popq %rsi")
        print("    leaq IO, %rdi")
        print("    movq $0, %rax")
        print("    callq printf")
    elif token == "dup":
        print("    movq (%rsp), %rax")
        print("    pushq %rax")
    elif token == "drop":
        print("    addq $8, %rsp")

prologue = """\
    .text
    .globl main
main:
    pushq %rbp
    movq %rsp, %rbp
"""
epilogue = """\
    movq $0, %rax
    leaveq
    retq
    .data
IO:
    .string "%lld"
"""
print(prologue)
tokens = code.split()
for token in tokens:
    translator(token)
print(epilogue)

