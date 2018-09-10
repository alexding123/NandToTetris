// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// some constants
@8192
D=A
@TOTAL
M=D

// listens to keyboard
(listen)
    // initialize counter
    @addr
    M=0

    @KBD
    D=M

    @fillBlack
    D;JNE
    @fillWhite
    D;JEQ

(fillBlack)
    @addr // if addr==TOTAL, jump to listen
    D=M
    @TOTAL
    D=D-M
    @listen
    D;JEQ

    @addr // fill with 1's
    D=M
    @SCREEN
    A=A+D
    M=-1
    @addr
    M=M+1

    @fillBlack
    0;JMP

(fillWhite)
    @addr // if addr==TOTAL, jump to listen
    D=M
    @TOTAL
    D=D-M
    @listen
    D;JEQ

    @addr // fill with 0's
    D=M
    @SCREEN
    A=A+D
    M=0
    @addr
    M=M+1

    @fillWhite
    0;JMP
