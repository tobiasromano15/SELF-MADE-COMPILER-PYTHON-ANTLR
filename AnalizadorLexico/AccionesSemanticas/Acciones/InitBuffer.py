import AnalizadorLexico.AccionesSemanticas.AccionSemantica as accion
import AnalizadorLexico.Lexico

class InitBuffer(accion.AccionSemantica):
    def __init__(self, lexico: AnalizadorLexico.Lexico.Lexico):
        super().__init__(lexico)

    def ejecutar(self,caracterActual):
        self.lexico.bufferClear()
        self.lexico.bufferAdd(caracterActual)
        #print("initbuffer: ", self.lexico.bufferLexema())
