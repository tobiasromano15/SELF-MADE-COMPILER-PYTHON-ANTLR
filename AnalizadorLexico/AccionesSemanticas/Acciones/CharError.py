import AnalizadorLexico.AccionesSemanticas.AccionSemantica as accion
import AnalizadorLexico.Lexico
from AnalizadorLexico.Token import Token


class CharError(accion.AccionSemantica):

    def __init__(self, lexico: AnalizadorLexico.Lexico.Lexico):
        super().__init__(lexico)

    def ejecutar(self,caracterActual):
        if (not caracterActual.isalpha()) and not (caracterActual in self.lexico.columna.keys()):
            self.lexico.tokenActual = Token("error_yacc", self.lexico.nroLinea)
            self.lexico.escribirError("Caracter no soportado")
        self.lexico.bufferClear()

