import AnalizadorLexico.AccionesSemanticas.AccionSemantica as accion
import AnalizadorLexico.Lexico
from AnalizadorLexico.Token import Token


class FaltaError(accion.AccionSemantica):

    def __init__(self, lexico: AnalizadorLexico.Lexico.Lexico):
        super().__init__(lexico)

    def ejecutar(self,caracterActual):
        if not (caracterActual == "!"):
            self.lexico.tokenActual = Token("error_yacc", self.lexico.nroLinea)
            self.lexico.escribirError("Falta !")
        self.lexico.bufferClear()

