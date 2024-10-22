import AnalizadorLexico.AccionesSemanticas.AccionSemantica as accion
import AnalizadorLexico.Lexico
from AnalizadorLexico.Token import Token


class SimpleChar(accion.AccionSemantica):
    def __init__(self, lexico: AnalizadorLexico.Lexico.Lexico):
        super().__init__(lexico)

    def ejecutar(self, caracterActual):
        self.lexico.bufferClear()
        self.lexico.bufferAdd(caracterActual)
        self.lexico.tokenActual = Token(self.lexico.bufferLexema(), self.lexico.nroLinea)
        self.lexico.bufferClear()
