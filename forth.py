import sys

jump_label_id = 0
jump_label_stack = []
label_id = 0
varnames = []
strlist  = []
funcdict = {}

text_header = """\
    .text
    .globl main
main:
    pushq %rbp
    movq %rsp, %rbp
    movq %rbp, %r15
    subq $1024, %r15"""
main_return = """\
    movq $0, %rax
    leaveq
    retq"""
data_header = """\
    .data
IO:
    .string "%lld" """
varinit = """:
    .int 0
    .align 8"""

def translator(tokens):
    global label_id
    global jump_label_id
    token = tokens.pop(0)
    if token.isdigit() or (token[0] in "-+" and token[1:].isdigit()):
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
    elif token == "variable":
        varnames.append(tokens.pop(0))
    elif token in varnames:
        print("    pushq $"+token)
    elif token == "@":
        print("    popq %rax")
        print("    pushq (%rax)")
    elif token == "!":
        print("    popq %rax")
        print("    popq (%rax)")
    elif token[:4] == "_str":
        print("    pushq $"+token)
        strid = int(token[4:])
        strlen = len(strlist[strid])-2
        print("    pushq $"+str(strlen)) 
    elif token == "type":
        print("    addq $8, %rsp")          
        print("    popq %rdi")
        print("    movq $0, %rax")
        print("    callq printf")
    elif token == ":":
        func_name = tokens.pop(0)
        func = []
        while token != ";":
            token = tokens.pop(0)
            func.extend([token])
        funcdict[func_name] = func
    elif token in funcdict.keys():
        print("    addq $8, %r15")
        print("    leaq (_L"+str(label_id)+"), %rax")
        print("    movq %rax, (%r15)")
        print("    jmp "+token)
        print("_L"+str(label_id)+":")
        print("    subq $8, %r15")
        label_id += 1
    elif token == ";":
        print("    movq (%r15), %rax")
        print("    jmp *%rax")
    elif token == "if":
        jump_label = "_J"+str(jump_label_id)
        jump_label_stack.extend([jump_label])
        jump_label_id += 1
        print("    popq %rax")
        print("    cmpq $-1, %rax")
        print("    jne "+jump_label)
    elif token == "else":
        jump_label = jump_label_stack.pop()
        jump_label_x = jump_label+"x"
        jump_label_stack.extend([jump_label_x])
        print("    jmp "+jump_label_x)
        print(jump_label+":")
    elif token in ["then", "endif"]:
        jump_label = jump_label_stack.pop()
        print(jump_label+":")
    elif token == "<":  emit_bool("jl")
    elif token == "<=": emit_bool("jle")
    elif token == ">":  emit_bool("jg")
    elif token == ">=": emit_bool("jge")
    elif token == "=":  emit_bool("je")
    elif token == "<>": emit_bool("jne")
    elif token == "call":
        print("    callq "+tokens.pop(0))
    elif token == "rax>": print("    pushq %rax")
    elif token == "rdx>": print("    pushq %rdx")
    elif token == ">rax": print("    popq %rax")
    elif token == ">rdi": print("    popq %rdi")
    elif token == ">rsi": print("    popq %rsi")
    elif token == ">rdx": print("    popq %rdx")
    elif token == ">rcx": print("    popq %rcx")
    elif token == ">r8":  print("    popq %r8")
    elif token == ">r9":  print("    popq %r9")

def emit_bool(jmp_instr):
    print("    popq %rax")
    print("    popq %rbx")
    print("    cmpq %rax, %rbx")
    print("    movq $-1, %rax")
    print("    "+jmp_instr+" 1f")
    print("    movq $0, %rax")
    print("1:")
    print("    pushq %rax")

def remove_str(code):
    strid = 0
    code2 = ""
    while code != "":
        c, code = code[0], code[1:]
        if c =="s" and code[:2]=="\" ":
            code = code[2:]
            ss = "\""
            while c != "\"":
                c, code = code[0], code[1:]
                ss += c
            strlist.append(ss.replace("\n","\\n"))
            c = "_str"+str(strid)
            strid += 1
        code2 += c
    return code2

def remove_comment(code):
    code += "   "
    code2 = ""
    while len(code) > 3:
        c, code = code[0], code[1:]
        if (c in [" ","\n"]) and code[:2] == "( ":
            while c != ")":
                c, code = code[0], code[1:]
        code2 += c
    return code2
        
filename = sys.argv[1]
with open(filename, "r") as f:
    code = f.read()
code = remove_str(code)
code = remove_comment(code)
tokens = code.split()

print(text_header)
while tokens != []:
    translator(tokens)
print(main_return)

for funcname, tokens in funcdict.items():
    print(funcname+":")
    while tokens != []:
        translator(tokens)

print(data_header)
for varname in varnames:
    print(varname+varinit)
for k,v in enumerate(strlist):
    print("_str"+str(k)+":")
    print("    .string "+v)
