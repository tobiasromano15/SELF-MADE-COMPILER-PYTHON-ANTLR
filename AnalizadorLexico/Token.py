import numbers
import AnalizadorSintactico.gramaticaprueba as parser

class Token:  # NUMEROS PROVISORIOS (cambian segun lo que asigne el parser)
    IF = parser.gramaticaprueba.IF
    ELSE = parser.gramaticaprueba.ELSE
    END_IF = parser.gramaticaprueba.END_IF
    PRINT = parser.gramaticaprueba.PRINT
    CLASS = parser.gramaticaprueba.CLASS
    VOID = parser.gramaticaprueba.VOID
    INT = parser.gramaticaprueba.INT
    ULONG = parser.gramaticaprueba.ULONG
    FLOAT = parser.gramaticaprueba.FLOAT
    WHILE = parser.gramaticaprueba.WHILE
    DO = parser.gramaticaprueba.DO
    MENORIGUAL = parser.gramaticaprueba.MENORIGUAL
    MAYORIGUAL = parser.gramaticaprueba.MAYORIGUAL
    DISTINTO = parser.gramaticaprueba.DISTINTO
    ID = parser.gramaticaprueba.ID
    ERROR = parser.gramaticaprueba.ERROR
    CADENA = parser.gramaticaprueba.CADENA
    NUM_INT = parser.gramaticaprueba.NUM_INT
    NUM_ULONG = parser.gramaticaprueba.NUM_ULONG
    NUM_FLOAT = parser.gramaticaprueba.NUM_FLOAT
    RETURN = parser.gramaticaprueba.RETURN
    COMPIGUAL = parser.gramaticaprueba.COMPIGUAL
    PUNTO = parser.gramaticaprueba.DOT

    def getToken(self):
        lexema = self.lexema
        if lexema == 'FIN':
            return parser.gramaticaprueba.EOF
        elif lexema == '+':
            return parser.gramaticaprueba.PLUS
        elif lexema == '-':
            return parser.gramaticaprueba.MINUS
        elif lexema == ',':
            return parser.gramaticaprueba.COMMA
        elif lexema == '.':
            return parser.gramaticaprueba.DOT
        elif lexema == '/':
            return parser.gramaticaprueba.DIVIDE
        elif lexema == '*':
            return parser.gramaticaprueba.MULTIPLY
        elif lexema == '(':
            return parser.gramaticaprueba.LEFT_PAREN
        elif lexema == ')':
            return parser.gramaticaprueba.RIGHT_PAREN
        elif lexema == '<':
            return parser.gramaticaprueba.LESS_THAN
        elif lexema == '>':
            return parser.gramaticaprueba.GREATER_THAN
        elif lexema == '{':
            return parser.gramaticaprueba.LEFT_BRACE
        elif lexema == '}':
            return parser.gramaticaprueba.RIGHT_BRACE
        elif lexema == ';':
            return parser.gramaticaprueba.SEMICOLON
        elif lexema == '=':
            return parser.gramaticaprueba.EQUALS
        elif lexema == '<=':
            return self.MENORIGUAL
        elif lexema == '>=':
            return self.MAYORIGUAL
        elif lexema == '!!':
            return self.DISTINTO
        elif lexema == '==':
            return self.COMPIGUAL
        elif lexema == 'IF':
            return self.IF
        elif lexema == 'ELSE':
            return self.ELSE
        elif lexema == 'END_IF':
            return self.END_IF
        elif lexema == 'PRINT':
            return self.PRINT
        elif lexema == 'CLASS':
            return self.CLASS
        elif lexema == 'VOID':
            return self.VOID
        elif lexema == 'INT':
            return self.INT
        elif lexema == 'ULONG':
            return self.ULONG
        elif lexema == 'FLOAT':
            return self.FLOAT
        elif lexema == 'error_yacc':
            return self.ERROR
        elif lexema == 'WHILE':
            return self.WHILE
        elif lexema == 'DO':
            return self.DO
        elif lexema == "RETURN":
            return self.RETURN
        elif str(lexema).startswith("%") and str(lexema).endswith("%"):
            return self.CADENA
        elif str(lexema).endswith("_i"):
            return self.NUM_INT
        elif str(lexema).endswith("_ul"):
            return self.NUM_ULONG
        elif str(lexema).__contains__("."):
            return self.NUM_FLOAT
        else:
            return self.ID

    def __init__(self, lexema, nrolinea):
        self._lineno = nrolinea
        self._lexema = lexema
        self._nro = self.getToken()

    @property
    def lexema(self):
        return self._lexema

    @property
    def value(self):
        return self._lexema

    @property
    def lineno(self):
        return self._lineno

    @lineno.setter
    def lineno(self, nro):
        self.lineno = nro

    @lexema.setter
    def lexema(self, value):
        self._lexema = value
        self._nro = self.getToken()

    @property
    def type(self):
        return self.getToken()

    def getLexema(self):
        return self._lexema

    def print(self):
        print("Token [lexema: '" + str(self.lexema) + "' , nro= " + str(self._nro) + "]")
