import AnalizadorLexico.AccionesSemanticas.Acciones.AddChar as Addchar
import AnalizadorLexico.AccionesSemanticas.Acciones.CadenaEncontrada as CadenaEncontrada
import AnalizadorLexico.AccionesSemanticas.Acciones.CharError as CharError
import AnalizadorLexico.AccionesSemanticas.Acciones.DoubleConst as DoubleConst
import AnalizadorLexico.AccionesSemanticas.Acciones.DoubleError as DoubleError
import AnalizadorLexico.AccionesSemanticas.Acciones.FaltaError as FaltaError
import AnalizadorLexico.AccionesSemanticas.Acciones.IdConsumeLast as IdConsumeLast
import AnalizadorLexico.AccionesSemanticas.Acciones.IdReturnLast as IdReturnLast
import AnalizadorLexico.AccionesSemanticas.Acciones.IgnoreChar as IgnoreChar
import AnalizadorLexico.AccionesSemanticas.Acciones.InitBuffer as InitBuffer
import AnalizadorLexico.AccionesSemanticas.Acciones.IntConst as IntConst
import AnalizadorLexico.AccionesSemanticas.Acciones.SimpleChar as SimpleChar
import AnalizadorLexico.AccionesSemanticas.Acciones.SuffixError as SuffixError
import AnalizadorLexico.Lexico


class AccionesSemanticas:
    def __init__(self, lexico: AnalizadorLexico.Lexico.Lexico):
        self.lexico = lexico
        self.AS0 = IgnoreChar.IgnoreChar(self.lexico)
        self.AS1 = InitBuffer.InitBuffer(self.lexico)
        self.AS2 = Addchar.AddChar(self.lexico)
        self.AS3 = IdReturnLast.IdReturnLast(self.lexico)
        self.AS4 = IdConsumeLast.IdConsumeLast(self.lexico)
        self.AS5 = IntConst.IntConst(self.lexico)
        self.AS6 = DoubleConst.DoubleConst(self.lexico)
        self.AS7 = CadenaEncontrada.CadenaEncontrada(self.lexico)
        self.AS8 = SimpleChar.SimpleChar(self.lexico)
        self.E1 = SuffixError.SuffixError(self.lexico)
        self.E2 = CharError.CharError(self.lexico)
        self.E3 = FaltaError.FaltaError(self.lexico)
        self.E4 = DoubleError.DoubleError(self.lexico)

    @property
    def matrizAccionesSemanticas(self):
        self._matrizAccionesSemanticas = [
    #   letra       digito          /          *           +           -            =          <           >           {            }         (          )           ,               ;       .             %           _           u          i          e/E          !        Blc/tab       nl         otro    l      #estado
    [  self.AS1,   self.AS1,   self.AS8,   self.AS1,   self.AS8,   self.AS8,   self.AS1,   self.AS1,   self.AS1,   self.AS8,   self.AS8,   self.AS8,   self.AS8,   self.AS8,   self.AS8,   self.AS1,   self.AS1,   self.AS1,   self.AS1,   self.AS1,   self.AS1,   self.AS1,   self.AS0,   self.AS0, self.E2,self.AS1],  # 0
    [  self.AS2,   self.AS2,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS2,   self.AS2,   self.AS2,   self.AS2,   self.AS3,   self.AS3,   self.AS3, self.E2,self.AS2],  # 1
    [  self.AS2,   self.AS2,   self.AS2,   self.AS2,   self.AS2,   self.AS2,   self.AS2,   self.AS2,   self.AS2,   self.AS2,   self.AS2,   self.AS2,   self.AS2,   self.AS2,   self.AS2,   self.AS2,   self.AS7,   self.AS2,   self.AS2,   self.AS2,   self.AS2,   self.AS2,   self.AS2,   self.AS2, self.E2,self.AS2],  # 2
    [  self.AS3,   self.AS3,   self.AS3,   self.AS2,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3, self.E2,self.AS3],  # 3
    [  self.AS0,   self.AS0,   self.AS0,   self.AS0,   self.AS0,   self.AS0,   self.AS0,   self.AS0,   self.AS0,   self.AS0,   self.AS0,   self.AS0,   self.AS0,   self.AS0,   self.AS0,   self.AS0,   self.AS0,   self.AS0,   self.AS0,   self.AS0,   self.AS0,   self.AS0,   self.AS0,   self.AS0, self.E2,self.AS0],  # 4
    [  self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS4,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3, self.E2,self.AS3],  # 5
    [  self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS4,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3, self.E2,self.AS3],  # 6
    [  self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS4,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3,   self.AS3, self.E2,self.AS3],  # 7
    [   self.E3,    self.E3,    self.E3,    self.E3,    self.E3,    self.E3,    self.E3,    self.E3,    self.E3,    self.E3,    self.E3,    self.E3,    self.E3,    self.E3,    self.E3,    self.E3,    self.E3,    self.E3,    self.E3,    self.E3,    self.E3,   self.AS4,    self.E3,    self.E3, self.E2, self.E3],  # 8
    [   self.E1,   self.AS2,    self.E1,    self.E1,    self.E1,    self.E1,    self.E1,    self.E1,    self.E1,    self.E1,    self.E1,    self.E1,    self.E1,    self.E1,    self.E1,   self.AS2,    self.E1,   self.AS2,    self.E1,    self.E1,    self.E1,    self.E1,    self.E1,    self.E1, self.E2, self.E1],  # 9
    [   self.E1,    self.E1,    self.E1,    self.E1,    self.E1,    self.E1,    self.E1,    self.E1,    self.E1,    self.E1,    self.E1,    self.E1,    self.E1,    self.E1,    self.E1,    self.E1,    self.E1,    self.E1,   self.AS2,   self.AS5,    self.E1,    self.E1,    self.E1,    self.E1, self.E2, self.E1],  # 10
    [   self.E1,    self.E1,    self.E1,    self.E1,    self.E1,    self.E1,    self.E1,    self.E1,    self.E1,    self.E1,    self.E1,    self.E1,    self.E1,    self.E1,    self.E1,    self.E1,    self.E1,    self.E1,    self.E1,    self.E1,    self.E1,    self.E1,    self.E1,    self.E1, self.E2,self.AS5],  # 11
    [  self.AS3,   self.AS2,    self.E4,    self.E4,    self.E4,    self.E4,    self.E4,    self.E4,    self.E4,    self.E4,    self.E4,    self.E4,    self.E4,    self.E4,    self.E4,    self.E4,    self.E4,   self.AS3,   self.AS3,   self.AS3,   self.AS3,    self.E4,    self.E4,    self.E4, self.E2,self.AS3],  # 12
    [  self.AS6,   self.AS2,   self.AS6,   self.AS6,   self.AS6,   self.AS6,   self.AS6,   self.AS6,   self.AS6,   self.AS6,   self.AS6,   self.AS6,   self.AS6,   self.AS6,   self.AS6,   self.AS6,   self.AS6,   self.AS6,   self.AS6,   self.AS6,   self.AS2,   self.AS6,   self.AS6,   self.AS6, self.E2,self.AS6],  # 13
    [   self.E4,    self.E4,    self.E4,    self.E4,   self.AS2,   self.AS2,    self.E4,    self.E4,    self.E4,    self.E4,    self.E4,    self.E4,    self.E4,    self.E4,    self.E4,    self.E4,    self.E4,    self.E4,    self.E4,    self.E4,    self.E4,    self.E4,    self.E4,    self.E4, self.E2, self.E4],  # 14
    [   self.E4,   self.AS2,    self.E4,    self.E4,    self.E4,    self.E4,    self.E4,    self.E4,    self.E4,    self.E4,    self.E4,    self.E4,    self.E4,    self.E4,    self.E4,    self.E4,    self.E4,    self.E4,    self.E4,    self.E4,    self.E4,    self.E4,    self.E4,    self.E4, self.E2, self.E4],  # 15
    [  self.AS6,   self.AS2,   self.AS6,   self.AS6,   self.AS6,   self.AS6,   self.AS6,   self.AS6,   self.AS6,   self.AS6,   self.AS6,   self.AS6,   self.AS6,   self.AS6,   self.AS6,   self.AS6,   self.AS6,   self.AS6,   self.AS6,   self.AS6,   self.AS6,   self.AS6,   self.AS6,   self.AS6, self.E2,self.AS6],  # 16
    ]
        return self._matrizAccionesSemanticas

    def getAccion(self, fila, columna):
        return self.matrizAccionesSemanticas[fila][columna]
