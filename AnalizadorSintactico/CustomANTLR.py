from antlr4.CommonTokenFactory import CommonTokenFactory
from antlr4.Lexer import TokenSource
import AnalizadorLexico.Lexico as lexico
from antlr4.Token import Token

from AnalizadorSintactico.gramaticaprueba import gramaticaprueba


class CustomTokenSource(TokenSource):
    def __init__(self,contenido_str,archivo_errores):
        self.contenido_str = contenido_str
        self.lex = lexico.Lexico(contenido_str, archivo_errores)
        self._factory = CommonTokenFactory.DEFAULT

    def nextToken(self):
        # Usa tu lexer personalizado para obtener el próximo token
        self.current_token = self.lex.yyLex()
        token = Token()
        self._tokenFactorySourcePair = (None, None)
        if self.current_token.getLexema() != "FIN":
            t = self._factory.create(self._tokenFactorySourcePair, self.current_token.getToken(), self.current_token.getLexema(), Token.DEFAULT_CHANNEL,
                                     0,
                                     0, self.current_token.lineno, 0)
        else:
            t = self._factory.create(self._tokenFactorySourcePair, Token.EOF, None, Token.DEFAULT_CHANNEL,
                                     0,
                                     0, self.current_token.lineno, 0)

        return t
    def getSourceName(self):
        return "UNKNOWN"
"""La clase CustomTokenSource si bien no es lo mas efectivo es necesaria para poder trabajar con ANTLR ya que el parser utiliza su propia clase TOKEN """

from antlr4.error.ErrorStrategy import DefaultErrorStrategy
from antlr4 import Parser

class CustomErrorStrategy(DefaultErrorStrategy):
    def setParserGen(self,GenParser: gramaticaprueba):
        self.GenParser = GenParser

    def writeErrorFILE(self,tokentext,line,regla,estructura):
        txt = "Error en sentencia " + regla + " " + estructura
        self.GenParser.yyerror(txt,line)

    def getMissingSymbol(self, recognizer:Parser):
        currentSymbol = recognizer.getCurrentToken()
        expecting = self.getExpectedTokens(recognizer)
        expectedTokenType = expecting[0] # get any element
        if expectedTokenType==Token.EOF:
            tokenText = "<missing EOF>"
        else:
            name = None
            if expectedTokenType < len(recognizer.literalNames):
                name = recognizer.literalNames[expectedTokenType]
            if name is None and expectedTokenType < len(recognizer.symbolicNames):
                name = recognizer.symbolicNames[expectedTokenType]
            tokenText = "<missing " + str(name) + ">"
        current = currentSymbol
        self.writeErrorFILE(tokenText, recognizer.getCurrentToken().line, recognizer.getRuleInvocationStack()[0],recognizer.getTokenErrorDisplay(current) )
        lookback = recognizer.getTokenStream().LT(-1)
        if current.type==Token.EOF and lookback is not None:
            current = lookback
        return recognizer.getTokenFactory().create(current.source,
            expectedTokenType, tokenText, Token.DEFAULT_CHANNEL,
            -1, -1, current.line, current.column)