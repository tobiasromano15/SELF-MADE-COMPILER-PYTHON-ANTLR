import importlib

from AnalizadorLexico.Token import Token


class Lexico:
    FINAL = 99
    ERROR = 100
    termino = False
    erroresLex = 0
    matrizDeTransiciones = [
        # letra digito    /      *      +      -     =      <       >      {      }      (      )      ,      ;      .     %      _      u      i     e/E     !   Blc/tab   nl    otro    l  #estado
        [    1,     9, FINAL,     3, FINAL, FINAL,     7,     5,     6, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL,    12,     2,     1,     1,     1,     1,     8,     0,     0, ERROR,     1],  # 0
        [    1,     1, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL,     1,     1,     1,     1, FINAL, FINAL, FINAL, ERROR,     1],  # 1
        [    2,     2,     2,     2,     2,     2,     2,     2,     2,     2,     2,     2,     2,     2,     2,     2, FINAL,     2,     2,     2,     2,     2,     2,     2, ERROR,     2],  # 2
        [FINAL, FINAL, FINAL,     4, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, ERROR, FINAL],  # 3
        [    4,     4,     4,     4,     4,     4,     4,     4,     4,     4,     4,     4,     4,     4,     4,     4,     4,     4,     4,     4,     4,     4,     4, FINAL, ERROR,     4],  # 4
        [FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, ERROR, FINAL],  # 5
        [FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, ERROR, FINAL],  # 6
        [FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, ERROR, FINAL],  # 7
        [ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, FINAL, ERROR, ERROR, ERROR, ERROR],  # 8
        [ERROR,     9, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR,    13, ERROR,    10, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR],  # 9
        [ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR,    11, FINAL, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR],  # 10
        [ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, FINAL],  # 11
        [FINAL,    13, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, FINAL, FINAL, FINAL, FINAL, ERROR, ERROR, ERROR, ERROR, FINAL],  # 12
        [FINAL,    13, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL,    14, FINAL, FINAL, FINAL, ERROR, FINAL],  # 13
        [ERROR, ERROR, ERROR, ERROR,    15,    15, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR],  # 14
        [ERROR,    16, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR, ERROR],  # 15
        [FINAL,    16, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL, FINAL],  # 16
    ]

    columna = {
        '/': 2,
        '*': 3,
        '+': 4,
        '-': 5,
        '=': 6,
        '<': 7,
        '>': 8,
        '{': 9,
        '}': 10,
        '(': 11,
        ')': 12,
        ',': 13,
        ';': 14,
        '.': 15,
        '%': 16,
        '_': 17,
        '!': 21,
    }

    # habria que ver como funcionaría con tab nl y espacio
    def getColumna(self, caracter):
        ascii = ord(caracter)
        #print(caracter, ascii)
        if ascii == 69 or ascii == 101:  # e/E
            return 20
        elif ascii == 117:  # u
            return 18
        elif ascii == 105:  # i
            return 19
        elif ascii == 108:
            return 25
        elif 64 < ascii < 91 or 96 < ascii < 123:  # letras restantes
            return 0
        elif 47 < ascii < 58:  # numeros
            return 1
        elif ascii == 32 or ascii == 9:  # espacio/tab
            return 22
        elif ascii == 10 or ascii == 13:  # new line/carriage return
            return 23
        else:
            return self.columna.get(caracter, 24)  # resto de simbolos

    def __init__(self, programa, archivo_errores):
        self._programa = programa
        self._tokenActual = None
        self._indice = [0]
        self._nroLinea = 1
        self._bufferLexema = ""
        self._archivo_errores = archivo_errores
    def bufferAdd(self,caracterActual):
        self._bufferLexema += caracterActual
    def bufferClear(self):
        self._bufferLexema = ""
    @property
    def tokenActual(self):
        return self._tokenActual

    @tokenActual.setter
    def tokenActual(self, value):
        self._tokenActual = value

    @tokenActual.getter
    def tokenActual(self):
        return self._tokenActual

    @property
    def nroLinea(self):
        return self._nroLinea

    @nroLinea.setter
    def nroLinea(self, value):
        self._nroLinea = value

    @property
    def indice(self):
        return self._indice

    @indice.setter
    def indice(self, value):
        self._indice = value

    def bufferLexema(self):
        return self._bufferLexema

    def setBufferLexema(self, value):
        self._bufferLexema = value

    def escribirError(self, error):
        self._archivo_errores.write("Error lexico : " + error + ", en linea nro " + str(self.nroLinea) + "\n")

    def yyLex(self):
        self.tokenActual = None
        import AnalizadorLexico.AccionesSemanticas.Acciones_Semanticas as acc
        #print(self._indice[0], len(programa))
        if self._indice[0] == len(self._programa):
            return Token("FIN", self.nroLinea)
        estado = 0
        while self.tokenActual is None:
            caracter_actual = self._programa[self._indice[0]]
            if ord(caracter_actual) == 10:
                self.nroLinea += 1
            estado_sig = self.matrizDeTransiciones[estado][self.getColumna(caracter_actual)]
            acciones = acc.AccionesSemanticas(self)
            accion = acciones.getAccion(estado, self.getColumna(caracter_actual))
            accion.ejecutar(caracter_actual)
            estado = estado_sig
            self._indice[0] += 1
            if self._indice[0] >= len(self._programa):
                if self._indice[0] == len(self._programa):
                    if estado == 2:
                        self.escribirError("Cadena no cerrada")
                        return Token("error_yac", self.nroLinea)
                    return self.tokenActual
                return Token("FIN", self.nroLinea)
            if estado_sig == self.FINAL or estado_sig == self.ERROR:
                break
        return self.tokenActual
