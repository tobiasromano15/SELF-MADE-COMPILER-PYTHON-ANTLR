from abc import ABC,abstractmethod
import AnalizadorLexico.Lexico
class AccionSemantica(ABC):
    def __init__(self, lexico: AnalizadorLexico.Lexico.Lexico):
        self.lexico = lexico

    @abstractmethod
    def ejecutar(self,caracterActual):
        pass

