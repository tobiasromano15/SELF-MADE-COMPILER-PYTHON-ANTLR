import AnalizadorLexico.AccionesSemanticas.AccionSemantica as accion
import AnalizadorLexico.Lexico

class AddChar(accion.AccionSemantica):
    def __init__(self, lexico: AnalizadorLexico.Lexico.Lexico):
        super().__init__(lexico)

    def ejecutar(self,caracterActual):
        #print("addchar buffer:  ", self.lexico.bufferLexema(), "caracterActual addchar", caracterActual)
        #print("----------------------------")
        self.lexico.bufferAdd(caracterActual)
