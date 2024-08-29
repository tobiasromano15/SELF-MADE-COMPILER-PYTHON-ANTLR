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
@mem2byte dd ? ; 32 bits
MaxFLOAT dd 3.40282347E38 ; 32 bits 
cadena_3 db "metodo de clase_foward", 0


clase_foward STRUCT
    unknown DW ?     
    propoerty_foward DW ?
clase_foward ENDS


test_clase STRUCT
    unknown DW ?     
    clase_foward_ clase_foward <?>
test_clase ENDS

a_main test_clase <?>
propoerty_foward_main_clase_foward DW ?
.code
start:
CALL TAG1
JMP FIN
TAG1:
invoke MessageBox, NULL, addr cadena_3, addr Imp, MB_OK
ret


LabelErrorOvSF:
invoke MessageBox, NULL, addr ErrorOvSF, addr Error, MB_OK
invoke ExitProcess, 0
LabelErrorOvPE:
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
