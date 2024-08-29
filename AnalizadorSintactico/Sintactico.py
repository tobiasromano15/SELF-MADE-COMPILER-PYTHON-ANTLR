from antlr4 import CommonTokenStream
from AnalizadorSintactico.CustomANTLR import CustomTokenSource
from AnalizadorSintactico.CustomANTLR import CustomErrorStrategy
from AnalizadorSintactico.gramaticaprueba import gramaticaprueba
from AnalizadorSemantico.GeneradorAssembler import CodeGenerator


class Sintactico:
    def __init__(self,contenido_str,archivo_errores,archivo_salida):
        self.contenido_str = contenido_str
        self.archivo_errores = archivo_errores
        self.archivo_salida = archivo_salida
        self.polaca = None

    def start(self):
            token_source = CustomTokenSource(self.contenido_str,self.archivo_errores)
            token_stream = CommonTokenStream(token_source)
            parser = gramaticaprueba(token_stream)
            customErrorHandler = CustomErrorStrategy()
            customErrorHandler.setParserGen(parser)
            parser._errHandler = customErrorHandler
            tree = parser.programa()
            self.polaca = parser.polacaInversa
            #print(parser.polacaInversa.referencias)
            for clave, valor in parser.polacaInversa.referencias.items():
                self.archivo_salida.write(f"{clave}: {valor}\n")
            self.archivo_salida.close()
            generadorAsembler = CodeGenerator(self.polaca)
            codigo = generadorAsembler.imprimirCodigo()
            nombre_archivo = "programa.asm"
            with open(nombre_archivo, "w") as archivo:
                archivo.write(codigo)
