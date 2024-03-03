from math import fmod

def TwosCompUndo(num):
    num = num[::-1]
    val = 0
    l = len(num)
    for i in range(l-1):
            val += int(num[i])*(2**int(i))
    
    if num[l-1]=='1': return val-(2**(l-1))
    return val

def printReg(num) :
    num = num[::-1]
    val = 0
    l = len(num)
    for i in range(l):
        val += int(num[i])*(2**int(i))
    return val


# The following are global variables which will be used in the processor stages.
imem = list()
dmem = [0]*200


pc = 0          # For easy memory access, we will implement the instruction memory in words of 32 bits, and increment PC by 1, not 4.
curri = list()
opcode = ''
rs = ''
rt = ''
rd = ''
shamt = ''
funct = ''

imm = 0
aluresult = 0
readdata = 0
zero = 0

itype = ''

regfile = {
    '00000' : 0, '10000' : 0,
    '00001' : 0, '10001' : 0,
    '00010' : 0, '10010' : 0,
    '00011' : 0, '10011' : 0,
    '00100' : 0, '10100' : 0,
    '00101' : 0, '10101' : 0,
    '00110' : 0, '10110' : 0,
    '00111' : 0, '10111' : 0,
    '01000' : 0, '11000' : 0,
    '01001' : 0, '11001' : 0,
    '01010' : 0, '11010' : 0,
    '01011' : 0, '11011' : 0,
    '01100' : 0, '11100' : 0,
    '01101' : 0, '11101' : 0,
    '01110' : 0, '11110' : 0,
    '01111' : 0, '11111' : 0,
    }

#control lines
regwrite = 0
memread = 0
memwrite = 0
memtoreg = 0
aluop = -1                                                       
branch = 0                                                      # regdst and alusrc will both be taken care of by 'itype' 
pcsrc = 0



def IF():
    global imem
    global curri
    global pc

    curri = imem[pc]
    print(f'Instruction number {pc} has been loaded into the processor.')




def ID():
    global itype, curri, rs, rt, rd, shamt, funct, imm, regfile, opcode
    global regwrite, memwrite, memtoreg, aluop, memread, branch, aluresult

    opcode = curri[:6]

    if opcode=='000000' or opcode=='011100':
        print('This is an R-type instruction')
        itype = 'R'
        regwrite = 1
        memtoreg = 0
        
        rs = curri[6:11]
        rt = curri[11:16]
        rd = curri[16:21]
        shamt = curri[21:26]
        funct = curri[26:]                                      # splitting instruction

        branch = 0
        memread = 0
        memtoreg = 0
        memwrite = 0
        regwrite = 1

        if funct=='100000':                                     # add
            aluop = 0                                     

        elif funct=='100010':                                   # sub
            aluop = 1                 

        elif funct=='000010':                                   # mul
            aluop = 2             

        elif funct=='101010':                                   # slt 
            aluop = 3                       

        else: 
            aluop = 4                                         # syscall and jr, skip EX()
            regwrite = 0

    elif (opcode=='000010') or (opcode=='000011'):
        print('This is a J-type instruction')
        itype = 'J'
        imm = curri[6:]
        imm = TwosCompUndo(imm)
        imm = imm*4


    else:
        print('This is an I-type instruction')
        itype = 'I'
        rs = curri[6:11]
        rt = curri[11:16]
        imm = curri[17:]
        imm = TwosCompUndo(imm)


        if opcode=='000100':                                    # beq
            aluop = 5           # checking equality
            branch = 1
            memread = 0
            memtoreg = 0
            memwrite = 0
            regwrite = 0

        elif opcode=='000101':                                  # bne
            aluop = 6           # checking inequality 
            branch = 1
            memread = 0
            memtoreg = 0
            memwrite = 0
            regwrite = 0

        else:            
            if opcode=='001111':                                # lui
                aluop = 7       # left shift by 16
                branch = 0
                memread = 0
                memtoreg = 0
                memwrite = 0
                regwrite = 1

            elif opcode=='100011':                              # lw
                aluop = 0                                     
                branch = 0
                memread = 1
                memtoreg = 1
                memwrite = 0
                regwrite = 1

            elif opcode=='101011':                              # sw
                aluop = 0                                     
                branch = 0
                memread = 0
                memtoreg = 0
                memwrite = 1
                regwrite = 0    

            elif opcode=='001000' or opcode=='001001':
                aluop = 0                                       # addi, addiu
                branch = 0
                memread = 0
                memtoreg = 0
                memwrite = 0
                regwrite = 1

            elif opcode=='001010':                              #slti
                aluop = 3     # checking less than
                branch = 0
                memread = 0
                memtoreg = 0
                memwrite = 0
                regwrite = 1

            else:                                               # ori
                aluop = 8     # or
                branch = 0
                memread = 0
                memtoreg = 0
                memwrite = 0
                regwrite = 1

            print(aluop)





def EX():
    global rs, rt, imm, itype, regfile
    global aluop, aluresult, pc, zero

    if itype=='I':
        if aluop==7: aluresult = imm*(2**16)                    # lui
        elif aluop==0: aluresult = imm + regfile[rs]            # lw, sw, addi, addi
        elif aluop==3: aluresult = regfile[rt] < imm            # slti
        elif aluop==5: zero = regfile[rs] == regfile[rt]        # beq
        elif aluop==6: zero = regfile[rs] != regfile[rt]        # bne
        else: aluresult = regfile[rs]

    elif itype=='R':
        if aluop==0: aluresult = regfile[rs] + regfile[rt]
        elif aluop==1: aluresult = regfile[rs] - regfile[rt]
        elif aluop==2: aluresult = regfile[rt] * regfile[rs]
        elif aluop==3: aluresult = regfile[rs] < regfile[rt]

    print(f'Zero flag: {zero} \t ALU Result: {aluresult}')



def MEM():
    global rs, rt, imm, itype, regfile, dmem, readdata
    global memwrite, memtoreg, memread

    if memread: 
        readdata = dmem[ int((aluresult - 268500992)/4) ]
        print(f'Data read from memory location {aluresult}')

    if memwrite:
        dmem[ int((aluresult - 268500992)/4) ] = regfile[rt]
        print(f'Data written from register ${int(rt, 2)} to memory location {aluresult}')



def WB():
    global rs, rt, imm, itype, pc, opcode
    global regfile, memtoreg, regwrite, branch, aluresult, zero

    if memtoreg & regwrite: 
        if itype == 'I':
            regfile[rt] = readdata
            #print(f'reg: {printReg(rt)}', 'val:', str(readdata) )
        elif itype == 'R':
            regfile[rd] = readdata
            #print(f'reg: {printReg(rd)}', 'val:', str(readdata) )

    elif (not memtoreg) & regwrite:
        if itype == 'I':
            regfile[rt] = aluresult
            #print(f'reg: {printReg(rt)}', 'val:', str(aluresult) )
        elif itype == 'R':
            regfile[rd] = aluresult
            #print(f'reg: {printReg(rd)}', 'val:', str(aluresult) )


    if branch and zero: 
       pc += 1 + imm

    elif opcode=='000011':                                          #jal
        regfile['11111'] = pc
        pc = int((imm-4194304)/4)

    elif opcode=='000010': pc = int((imm-4194304)/4)                   # j

    elif opcode=='000000' and funct=='001000': pc = regfile['11111'] + 1              # jr

    else: pc += 1                                                 # pc increment

    print(f'PC targeted to instruction {pc} \n')








currf = 'diff_binary.txt'
file = open('diff_binary.txt', 'r')
lines = file.readlines()
for l in lines:
    imem.append(l.rstrip('\n'))
print(imem)

while imem[pc]!='00000000000000000000000000001100':
    IF()
    ID()
    EX()
    MEM()
    WB()



print('''registers

zero -00000
at -00001
v0 -00010
v1 -00011
a0 -00100
a1 -00101
a2 -00110
a3 -00111
t0 -01000
t1 -01001
t2 -01010
t3 -01011
t4 -01100
t5 -01101
t6 -01110
t7 -01111
s0 -10000
s1 -10001
s2 -10010
s3 -10011
s4 -10100
s5 -10101
s6 -10110
s7 -10111
t8 -11000
t9 -11001
k0 -11010
k1 -11011
gp -11100
sp -11101
fp -11110
ra -11111''')

regtoprint = ''

while(True):
    regtoprint = input('Register to be printed (type \'exit\' to exit): ')
    if regtoprint == 'exit':
        break
    else:
        print(f'register {regtoprint}: ' + str(regfile[regtoprint]) )