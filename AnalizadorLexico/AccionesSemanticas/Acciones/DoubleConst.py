import AnalizadorLexico.AccionesSemanticas.AccionSemantica as accion
import AnalizadorLexico.Lexico
from AnalizadorLexico.Token import Token


class DoubleConst(accion.AccionSemantica):
    CONST_HIGHEXP = 38
    CONST_LOWEXP = -38
    CONST_LOWDEC = 1.17549435 * (10 ** CONST_LOWEXP)
    CONST_HIGHDEC = 3.40282347 * (10 ** CONST_HIGHEXP)

    def __init__(self, lexico: AnalizadorLexico.Lexico.Lexico):
        super().__init__(lexico)

    def ejecutar(self, caracterActual):
        self.lexico.indice[0] -= 1
        exponente = 0
        entero_decimal = 0
        if "E" in self.lexico.bufferLexema():
            numero = self.lexico.bufferLexema().split("E")
            exponente = int(numero[1])
            entero_decimal = float(numero[0])
        elif "e" in self.lexico.bufferLexema():
            numero = self.lexico.bufferLexema().split("e")
            exponente = int(numero[1])
            entero_decimal = float(numero[0])
        else:
            entero_decimal = float(self.lexico.bufferLexema())

        if abs(exponente) > self.CONST_HIGHEXP:
            self.lexico.tokenActual = Token("error_yacc", self.lexico.nroLinea)
            self.lexico.escribirError("Constante de tipo flotante FLOAT con exponente fuera de rango")
        else:
            exponencial = float(10 ** exponente)
            resultado = float(entero_decimal * exponencial)
            if resultado == 0.0:
                lexema = self.lexico.bufferLexema()
                self.lexico.tokenActual = Token(lexema, self.lexico.nroLinea)
            else:
                if resultado <= self.CONST_LOWDEC:
                    self.lexico.tokenActual = Token("error_yacc", self.lexico.nroLinea)
                    self.lexico.escribirError("Constante de tipo FLOAT: " + str(resultado) + " fuera de rango")
                elif resultado >= self.CONST_HIGHDEC:
                    self.lexico.tokenActual = Token("error_yacc", self.lexico.nroLinea)
                    self.lexico.escribirError("Constante de tipo FLOAT: " + str(resultado) + " fuera de rango")
                else:
                    lexema = self.lexico.bufferLexema()
                    self.lexico.tokenActual = Token(lexema, self.lexico.nroLinea)

