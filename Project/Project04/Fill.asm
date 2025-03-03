// Program to make the screen turn pixel black
// HACK ASSEMBLY
// 
// Algorithm
//
// check if any key is pressed
//    if yes 
//          turn pixels black (write -1 to the screen rom)
//    if no 
//          turn pixels white (write zero to the screen rom)

// for (i = 0; i<n; i++) {
//    arr[i] = -1
// }
//
// screen - 16384 (ROM start address)
@SCREEN
D=A
@pixels
M=D

// n = 10
@8000
D=A
@n
M=D

(LOOP)
  // initialize i = 0
  @i
  M=0

  // if keyboard is pressed
  @KBD
  D=M
  @BLACK
  D;JGT

  (WHITE)
  // if (i == n) goto END
  @i
  D=M
  @n
  D=D-M
  @LOOP
  D;JEQ

  // RAM[screen+i] = -1
  @pixels
  D=M
  @i
  A=D+M
  M=0

  // i++
  @i
  M=M+1

  @WHITE
  0;JMP

(BLACK)
  // if (i == n) goto END
  @i
  D=M
  @n
  D=D-M
  @LOOP
  D;JEQ

  // RAM[screen+i] = -1
  @pixels
  D=M
  @i
  A=D+M
  M=-1

  // i++
  @i
  M=M+1

  @BLACK
  0;JMP
