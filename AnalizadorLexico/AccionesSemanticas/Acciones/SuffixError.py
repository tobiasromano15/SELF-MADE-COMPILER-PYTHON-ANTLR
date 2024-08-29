import AnalizadorLexico.AccionesSemanticas.AccionSemantica as accion
import AnalizadorLexico.Lexico
from AnalizadorLexico.Token import Token


class SuffixError(accion.AccionSemantica):
    SUFFIX_16BIT = "_i"
    SUFFIX_32BIT = "_ul"
    def __init__(self, lexico: AnalizadorLexico.Lexico.Lexico):
        super().__init__(lexico)

    def ejecutar(self,caracterActual):
        if not (self.lexico.bufferLexema().endswith(self.SUFFIX_32BIT) or self.lexico.bufferLexema().endswith(self.SUFFIX_16BIT)):
            self.lexico.tokenActual = Token("error_yacc", self.lexico.nroLinea)
            self.lexico.escribirError("Entero no contiene Sufijo")

        self.lexico.bufferClear()
