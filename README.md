# MIPS-Processor

The MIPS Processor (written in python) takes in a binary file dumped by the [MARS assembler](https://courses.missouristate.edu/kenvollmar/mars/download.htm) and runs it using the terminal as output.

The following instructions have been implemented in the processor:


I-fomat:

lui     op-001111

lw      op-100011

sw      op-101011

addi    op-001000

addiu   op-001001

beq     op-000100

bne     op-000101

slti    op-001010

ori     op-001101


R-format:

slt     op-000000 func-101010

add     op-000000 func-100000

sub	    op-000000 func-100010

mul     op-011100 func-000010

syscall op-000000 func-001100

jr      op-000000 func-001000


J-format:

j       op-000010

jal     op-000011

--------------------------------------------------------------------------------------------------------------------------


The following registers are being stored.

Registers:

zero -0

at -1

v0 -2

v1 -3

a0 -4

a1 -5

a2 -6

a3 -7

t0 -8

t1 -9

t2 -10

t3 -11

t4 -12

t5 -13

t6 -14

t7 -15

s0 -16

s1 -17

s2 -18

s3 -19

s4 -20

s5 -21

s6 -22

s7 -23

t8 -24

t9 -25

k0 -26

k1 -27

gp -28

sp -29

fp -30

ra -31

