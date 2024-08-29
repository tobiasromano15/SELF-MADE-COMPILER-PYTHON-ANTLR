import AnalizadorLexico.AccionesSemanticas.AccionSemantica as accion
import AnalizadorLexico.Lexico
from AnalizadorLexico.Token import Token

""" Identificadores cuyos nombres pueden tener hasta 20 caracteres de longitud. El primer puede ser una letra o ‟_‟, y
el resto pueden ser letras, dígitos y “_”. Los identificadores con longitud mayor serán truncados y esto se
informará como Warning. Las letras utilizadas en los nombres de identificador sólo pueden ser minúsculas. """

class IdReturnLast(accion.AccionSemantica):
    def __init__(self, lexico: AnalizadorLexico.Lexico.Lexico):
        super().__init__(lexico)

    def ejecutar(self, caracterActual):
        lexema = self.lexico.bufferLexema()
        self.lexico.indice[0] -= 1
        palabras = ["IF", "ELSE", "END_IF", "INT", "ULONG", "FLOAT", "VOID", "PRINT", "CLASS", "<=", ">=", "!!","WHILE","DO","RETURN"]
        if lexema in palabras:
            self.lexico.tokenActual = Token(lexema, self.lexico.nroLinea)
            self.lexico.bufferClear()
            return
        for letra in self.lexico.bufferLexema():
            if letra.isupper():
                self.lexico.tokenActual = Token("error_yacc", self.lexico.nroLinea)
                self.lexico.escribirError("Identificador contiene mayusculas.")
                return
        if len(self.lexico.bufferLexema()) <= 20: #Esperar respuesta de paula a ver que hago con las letras mayusculas
            self.lexico.tokenActual = Token(lexema, self.lexico.nroLinea)
        else:
            self.lexico.tokenActual = Token(lexema[:20], self.lexico.nroLinea)  # Se trunca el lexema
            self.lexico.escribirError("Lexema supera el tamaño máximo de 20")
