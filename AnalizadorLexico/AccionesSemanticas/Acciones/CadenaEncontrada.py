import AnalizadorLexico.AccionesSemanticas.AccionSemantica as accion
import AnalizadorLexico.Lexico
from AnalizadorLexico.Token import Token


class CadenaEncontrada(accion.AccionSemantica):
    def __init__(self, lexico: AnalizadorLexico.Lexico.Lexico):
        super().__init__(lexico)

    def ejecutar(self, caracterActual):
        self.lexico.bufferAdd(caracterActual)
        lexema = self.lexico.bufferLexema()
        self.lexico.tokenActual = Token(lexema, self.lexico.nroLinea)
        self.lexico.bufferClear()

