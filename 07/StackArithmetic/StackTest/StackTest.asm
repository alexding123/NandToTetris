// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// eq
@SP
AM=M-1
D=M
@SP
AM=M-1
D=D-M
@EQ_NOT_2
D;JNE
@SP
A=M
M=-1
@SP
M=M+1
@EQ_END_2
0;JMP
(EQ_NOT_2)
@SP
A=M
M=0
@SP
M=M+1
(EQ_END_2)
@SP
// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 16
@16
D=A
@SP
A=M
M=D
@SP
M=M+1
// eq
@SP
AM=M-1
D=M
@SP
AM=M-1
D=D-M
@EQ_NOT_5
D;JNE
@SP
A=M
M=-1
@SP
M=M+1
@EQ_END_5
0;JMP
(EQ_NOT_5)
@SP
A=M
M=0
@SP
M=M+1
(EQ_END_5)
@SP
// push constant 16
@16
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// eq
@SP
AM=M-1
D=M
@SP
AM=M-1
D=D-M
@EQ_NOT_8
D;JNE
@SP
A=M
M=-1
@SP
M=M+1
@EQ_END_8
0;JMP
(EQ_NOT_8)
@SP
A=M
M=0
@SP
M=M+1
(EQ_END_8)
@SP
// push constant 892
@892
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// lt
@SP
AM=M-1
D=M
@SP
AM=M-1
D=M-D
@LT_11
D;JLT
@SP
A=M
M=0
@SP
M=M+1
@LT_END_11
0;JMP
(LT_11)
@SP
A=M
M=-1
@SP
M=M+1
(LT_END_11)
@SP
// push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 892
@892
D=A
@SP
A=M
M=D
@SP
M=M+1
// lt
@SP
AM=M-1
D=M
@SP
AM=M-1
D=M-D
@LT_14
D;JLT
@SP
A=M
M=0
@SP
M=M+1
@LT_END_14
0;JMP
(LT_14)
@SP
A=M
M=-1
@SP
M=M+1
(LT_END_14)
@SP
// push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// lt
@SP
AM=M-1
D=M
@SP
AM=M-1
D=M-D
@LT_17
D;JLT
@SP
A=M
M=0
@SP
M=M+1
@LT_END_17
0;JMP
(LT_17)
@SP
A=M
M=-1
@SP
M=M+1
(LT_END_17)
@SP
// push constant 32767
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// gt
@SP
AM=M-1
D=M
@SP
AM=M-1
D=M-D
@GT_20
D;JGT
@SP
A=M
M=0
@SP
M=M+1
@GT_END_20
0;JMP
(GT_20)
@SP
A=M
M=-1
@SP
M=M+1
(GT_END_20)
@SP
// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 32767
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
// gt
@SP
AM=M-1
D=M
@SP
AM=M-1
D=M-D
@GT_23
D;JGT
@SP
A=M
M=0
@SP
M=M+1
@GT_END_23
0;JMP
(GT_23)
@SP
A=M
M=-1
@SP
M=M+1
(GT_END_23)
@SP
// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// gt
@SP
AM=M-1
D=M
@SP
AM=M-1
D=M-D
@GT_26
D;JGT
@SP
A=M
M=0
@SP
M=M+1
@GT_END_26
0;JMP
(GT_26)
@SP
A=M
M=-1
@SP
M=M+1
(GT_END_26)
@SP
// push constant 57
@57
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 31
@31
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 53
@53
D=A
@SP
A=M
M=D
@SP
M=M+1
// add
@SP
AM=M-1
D=M
@SP
AM=M-1
M=D+M
@SP
M=M+1
// push constant 112
@112
D=A
@SP
A=M
M=D
@SP
M=M+1
// sub
@SP
AM=M-1
D=M
@SP
AM=M-1
M=M-D
@SP
M=M+1
// neg
@SP
A=M-1
M=-M
// and
@SP
AM=M-1
D=M
@SP
AM=M-1
M=D&M
@SP
M=M+1
// push constant 82
@82
D=A
@SP
A=M
M=D
@SP
M=M+1
// or
@SP
AM=M-1
D=M
@SP
AM=M-1
M=D|M
@SP
M=M+1
// not
@SP
A=M-1
M=!M
