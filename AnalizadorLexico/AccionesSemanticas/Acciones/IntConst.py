import AnalizadorLexico.AccionesSemanticas.AccionSemantica as accion
import AnalizadorLexico.Lexico
from AnalizadorLexico.Token import Token


class IntConst(accion.AccionSemantica):
    CONST_16BIT = 2**15
    SUFFIX_16BIT = "_i"
    CONST_UNSIGNED_32BIT = 2**32 - 1
    SUFFIX_32BIT = "_ul"
    def __init__(self, lexico: AnalizadorLexico.Lexico.Lexico):
        super().__init__(lexico)
    def rango_i(self,numero):
        if (numero >= (self.CONST_16BIT * (-1))) and (numero <= (self.CONST_16BIT)):
            return True
        else:
            return False

    def rango_ul(self, numero):
        if (numero >= 0) and (numero <= self.CONST_UNSIGNED_32BIT):
            return True
        else: return False

    def ejecutar(self,caracterActual):
        self.lexico.bufferAdd(caracterActual)
        parte_numerica = ""

        if self.lexico.bufferLexema()[0] == "-":
            parte_numerica += self.lexico.bufferLexema()[0]

        for caracter in self.lexico.bufferLexema():
            if caracter.isdigit():
                parte_numerica += caracter

        for letra in self.lexico.bufferLexema():
            #Error si el sufijo contiene mayusculas
            if letra.isupper():
                self.lexico.tokenActual = Token("error_yacc", self.lexico.nroLinea)
                self.lexico.escribirError("Sufijo contiene mayusculas.")
                return

        if self.lexico.bufferLexema().endswith(self.SUFFIX_16BIT):
            if not (self.rango_i(int(parte_numerica))):
                self.lexico.tokenActual = Token("error_yacc", self.lexico.nroLinea)
                self.lexico.escribirError("Constante entera INT fuera de rango: " + self.lexico.bufferLexema())
                return
            else:
                lexema = self.lexico.bufferLexema()
                self.lexico.tokenActual = Token(lexema, self.lexico.nroLinea)

        elif self.lexico.bufferLexema().endswith(self.SUFFIX_32BIT):
            if not (self.rango_ul(int(parte_numerica))):
                self.lexico.tokenActual = Token("error_yacc", self.lexico.nroLinea)
                self.lexico.escribirError("Constante entera ULONG fuera de rango: " + self.lexico.bufferLexema())
                return
            else:
                lexema = self.lexico.bufferLexema()
                self.lexico.tokenActual = Token(lexema, self.lexico.nroLinea)





