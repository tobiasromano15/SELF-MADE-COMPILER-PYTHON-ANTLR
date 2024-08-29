include \masm32\include\masm32rt.inc
.386
.model flat
option casemap :none
include \masm32\include\windows.inc
include \masm32\include\kernel32.inc
include \masm32\include\user32.inc
includelib \masm32\lib\kernel32.lib
includelib \masm32\lib\user32.lib
.data
Error db "Error", 0
ErrorOvSF db "Error: overflow en un suma entre flotantes", 0
ErrorOvPE db "Error: overflow en una producto de enteros", 0
ErrorTYPE db "Error: Error tipos incomatibles entre operadores", 0
ErrorDIV0 db "Error: division por cero", 0
FINALIZO db "FINALIZO EL PROGRAMA", 0
Salida dt ?, 0
Imp db "Salida por pantalla", 0
@mem2byte dw ? ; 32 bits
MaxF32 dw 3.40282347E38 ; 32 bits 
cadena_24 db "B, AUMENTANDOO", 0
cadena_44 db "A, RESTANDOO", 0


clase_c STRUCT
    property1 DD ?     
    propertyc2 DD ?
clase_c ENDS

c1_main clase_c <?>
b_main DW ?
a_main DW ?
i_5 DW 5
i_6 DW 6
i_10 DW 10
i_1 DW 1
@aux1 DW ?
@aux2 DW ?
@aux3 DW ?
.code
start:
MOV AX, i_5
MOV a_main, AX 
MOV AX, i_5
MOV b_main, AX 
MOV BX,b_main
CMP i_6, BX
JNE TAG29
TAG12:
MOV BX,b_main
CMP i_10, BX
JE TAG27
MOV AX, b_main
ADD AX, i_1
MOV @aux1, AX
MOV AX, @aux1
MOV b_main, AX 
invoke MessageBox, NULL, addr cadena_24, addr Imp, MB_OK
JMP TAG12
TAG27:
JMP TAG47
TAG29:
MOV BX,a_main
CMP i_1, BX
JE TAG47
MOV AX, a_main
SUB AX, i_1
MOV @aux2, AX
MOV AX, @aux2
MOV a_main, AX 
MOV AX, a_main
MOV a_main, AX 
invoke MessageBox, NULL, addr cadena_44, addr Imp, MB_OK
JMP TAG29
TAG47:
MOV AX, b_main
MOV a_main, AX 
MOV AX, b_main
ADD AX, i_1
MOV @aux3, AX
MOV AX, @aux3
MOV b_main, AX 
JMP FIN
LabelErrorOvSE:
invoke MessageBox, NULL, addr ErrorOvSF, addr Error, MB_OK
invoke ExitProcess, 0
LabelErrorOvPF:
invoke MessageBox, NULL, addr ErrorOvPE, addr Error, MB_OK
invoke ExitProcess, 0
LabelErrorDIV0:
invoke MessageBox, NULL, addr ErrorDIV0, addr Error, MB_OK
invoke ExitProcess, 0
LabelErrorTYPE:
invoke MessageBox, NULL, addr ErrorTYPE, addr Error, MB_OK
invoke ExitProcess, 0
FIN:
invoke MessageBox, NULL, addr FINALIZO, addr Error, MB_OK
invoke ExitProcess, 0
end start
