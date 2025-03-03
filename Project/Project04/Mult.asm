// Multiplication assign
// R2 = R1 * R0
@10
D=A
@R0
M=D

@5
D=A
@R1
M=D

@0
D=A
@i
M=D

@0
D=A
@RESULT
M=D

(LOOP)

  @RESULT
  D=M
  @R2
  M=D
  // if (i == n) end the program
  @i
  D=M
  @R1
  D=D-M
  @END
  D;JEQ

  @R0
  D=M
  @RESULT
  D=D+M
  M=D

  @i
  M=M+1

  @LOOP
  0;JMP

(END)
  @END
  0;JMP
