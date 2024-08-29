parser grammar gramaticaprueba;
options {
    tokenVocab = Lexico;
}
@parser::header {
import TablaSimbolos as tablasimbolos
from antlr4.Token import Token
import AnalizadorSemantico.PolacaInversa as Polaca
}
@parser::members {
    self.archivo_tabla = open("tabla_de_simbolos.txt", "w")
    self.archivo_errores = open("errores.txt", "a")
    self.simbolos = tablasimbolos.TablaDeSimbolos(self.archivo_tabla)
    self.menos_menos = False
    self.listaVar = []
    self.text = ""
    self.polacaInversa = Polaca.ExpresionPolacaInversa()
    self.aux = 1
    self.elseaux = False
    self.auxIDFunc = ""
    self.auxIDClass = ""
    self.ambitoActual = ":main"
    self.declaracionesVariables = {}
    self.clasesUsadas = {}
    self.clasesDeclaradas = []
    self.inClase = False
    self.inFuncion = False
    self.segundaFuncion = False
    self.auxBorrado = -1
    self.auxAnterior = 0
    self.flag = 0
    self.error = False
    self.errorCondicion = False
    self.flagCondicion = 0
    self.flagFuncion = 0
    self.claseduplicada = False
    self.flagClase = 0
    self.ambitoaux = ""
    self.herenciasFoward = {}
def yyerror(self, texto, linea):
    if linea != 0:
        self.archivo_errores.write(str("ERROR " + texto + " En la linea " + str(linea) + "\n"))
    else:
        self.archivo_errores.write(str("ERROR " + texto) +  "\n")

def getValor(self, texto):
    valor = ""
    for caracter in texto:
        if caracter.isdigit() or caracter in [".", "E", "e", "-"]:
            valor += caracter
    return valor

def reducirAmbito(self):
    self.ambitoActual = self.ambitoActual[:self.ambitoActual.rfind(":")]

def verificarId(self, identificador):  # identificador viene con el ambito
    ambito_id = identificador[identificador.find(":"):]
    id_sin_ambito = identificador[:identificador.find(":")]
    while ambito_id != "":
        if self.simbolos.isKey(id_sin_ambito+ambito_id):
            return id_sin_ambito+ambito_id
        else:
            ambito_id = ambito_id[:ambito_id.rfind(":")]
    return ""

def getAmbitoId(self, identificador):
    return identificador[str(identificador).find(":"):]

def getIdSinAmbito(self, identificador):
    return identificador[:str(identificador).find(":")]
}

programa: '{' cuerpo '}' {
for key in self.declaracionesVariables.keys():
    self.yyerror("SEMANTICO: variable " + key + " no fue asignada en el ambito donde se declaro", self.declaracionesVariables[key])
for clase in self.clasesUsadas.keys():
    if clase not in self.clasesDeclaradas:
        self.yyerror("SEMANTICO: clase " + clase + " fue usada sin declarar", 0)
        list = []

        for item in self.simbolos.simbolos:
            aux = self.simbolos.simbolos[item]
            if "tipo" in aux:
                if self.simbolos.simbolos[item]["tipo"] == clase:
                    list.append(item)
        for a in list:
            del self.simbolos.simbolos[a]

    else:
        referencias = self.clasesUsadas[clase]

self.simbolos.imprimirTabla()
self.archivo_tabla.close()
}
;

cuerpo: cuerpo declaracion
        | cuerpo ejecucion
        | declaracion
        | ejecucion
;

declaracion: declaracion_var  {
for key in self.listaVar:
    if $declaracion_var.t in ["INT","FLOAT","ULONG"]:
        self.declaracionesVariables[key+self.ambitoActual] = $declaracion_var.line
self.listaVar = []
}
            | declaracion_func {
            }
            | declaracion_clase  {
}
;

declaracion_var returns [line, t]: tipo lista_variable ',' {
for key in self.listaVar:
    self.simbolos.addCaracteristica(key + self.ambitoActual, "tipo", $tipo.text)
    self.simbolos.addCaracteristica(key+self.ambitoActual, "uso", "variable")
    $line = $lista_variable.line
    $t = $tipo.text
}
;

lista_variable returns [line]: ID {
self.listaVar.append($ID.text)
$line = $ID.line
}
                | ID ';' lista_variable {
self.listaVar.append($ID.text)
$line = $ID.line
}
;

declaracion_func: {self.flagFuncion = self.polacaInversa.reference_counter} encabezado_funcion {
if self.inFuncion and self.inClase:
    self.segundaFuncion = True
if (not self.inClase) or (not self.inFuncion):
    if $encabezado_funcion.funcion != "":
        self.polacaInversa.addElemento(('FUNCION' + ' ' + $encabezado_funcion.funcion))
} parametro '{' cuerpo_func '}' ',' {
if $encabezado_funcion.funcion != "":
    self.reducirAmbito()
if self.segundaFuncion:
    while self.polacaInversa.reference_counter > self.auxBorrado:
        self.polacaInversa.removeLast()
self.inFuncion = False
if $cuerpo_func.faltaRetorno:
    self.yyerror("SINTACTICO: falta sentencia RETURN en funcion "+$encabezado_funcion.funcion,$encabezado_funcion.line)
if $encabezado_funcion.funcion == "":
    while self.polacaInversa.reference_counter != self.flagFuncion:
        self.polacaInversa.removeLast()
}
;

encabezado_funcion returns [funcion, line]: VOID ID {
if self.inClase and self.inFuncion:
    self.yyerror("SEMANTICO: no se puede anidar funciones dentro de una clase", $ID.line)
    self.auxBorrado = self.polacaInversa.reference_counter
    $funcion = ""
else:
    if not self.simbolos.isKey($ID.text + self.ambitoActual):
        self.auxIDFunc = $ID.text + self.ambitoActual
        self.simbolos.addCaracteristica(self.auxIDFunc, "uso", "funcion")
        $funcion = $ID.text + self.ambitoActual
        self.ambitoActual = self.ambitoActual + ":" + $ID.text
    else:
        $funcion = ""
        self.yyerror(" SEMANTICO: variable " + $ID.text + " ya existe en el ambito actual", $ID.line)
$line = $ID.line
}
;

parametro: '(' ')' {
self.simbolos.addCaracteristica(self.auxIDFunc, "nroParametros", "0")
}
            | '(' tipo ID ')' {
self.simbolos.addCaracteristica(self.auxIDFunc, "tipoParametro", $tipo.text)
self.simbolos.addCaracteristica(self.auxIDFunc, "nroParametros", "1")
self.simbolos.addCaracteristica($ID.text + self.ambitoActual, "tipo", $tipo.text)
self.simbolos.addCaracteristica($ID.text + self.ambitoActual, "uso", "parametro")
self.simbolos.addCaracteristica($ID.text + self.ambitoActual, "funcion_padre", self.auxIDFunc)
}
;

cuerpo_func returns[faltaRetorno]: {self.inFuncion = True}cuerpo ejecucion_retorno {
$faltaRetorno = $ejecucion_retorno.faltaRet
}
             | {self.inFuncion = True}ejecucion_retorno {
$faltaRetorno = $ejecucion_retorno.faltaRet
}
;

ejecucion_retorno returns[faltaRet]: RETURN ',' {
self.polacaInversa.addElemento("ret")
$faltaRet = False}  //Agrego BI y una celda vacia. Pero antes de hacer esto esperar respuesta de Paula por multiples cintas.
                    | {
self.polacaInversa.addElemento("ret")
$faltaRet = True}
;


declaracion_clase: {self.flagClase = self.polacaInversa.reference_counter} encabezado_clase '{' componentes_clase '}' ',' {
if self.claseduplicada:
    while self.polacaInversa.reference_counter != self.flagClase:
        self.polacaInversa.removeLast()
    lista = []
    for item in self.simbolos.simbolos.keys():
        if item.endswith("BORRAR_ERROR"):
            lista.append(item)
    for item in lista:
        del self.simbolos.simbolos[item]
    self.ambitoActual = self.ambitoaux
    self.claseduplicada = False
else:
    self.reducirAmbito()
    clase = ""
    if self.getIdSinAmbito(self.auxIDClass) in self.herenciasFoward.values():
        for key in self.herenciasFoward:
            if self.herenciasFoward[key] == self.getIdSinAmbito(self.auxIDClass):
                identificador = key
                herenciasActuales = self.simbolos.getCaracteristica(identificador, "numero de herencias")
                if isinstance(herenciasActuales, int):
                    if herenciasActuales < 2:
                        self.simbolos.aumentarReferencia(identificador)
                        self.simbolos.addCaracteristica(identificador, "numero de herencias", herenciasActuales + 1)
                        self.simbolos.addCaracteristica(identificador, "clase herencia", self.auxIDClass)
                        propiedades = self.simbolos.getCaracteristica(self.auxIDClass, "propiedades")
                        if isinstance(propiedades, list):
                            self.simbolos.addCaracteristica(identificador, "propiedades heredadas", propiedades)
                    else:
                        self.yyerror("SEMANTICO: se exeden los niveles de herencia", $encabezado_clase.line)
                else:
                    self.simbolos.addCaracteristica(identificador, "numero de herencias", 1)
                    self.simbolos.addCaracteristica(identificador, "clase herencia", self.auxIDClass)
                    propiedades = self.simbolos.getCaracteristica(self.auxIDClass, "propiedades")
                    if isinstance(propiedades, list):
                        self.simbolos.addCaracteristica(identificador, "propiedades heredadas", propiedades)
self.inClase = False
}

;

encabezado_clase returns [line]: CLASS ID {
if self.simbolos.isKey($ID.text + self.ambitoActual):
    self.claseduplicada = True
self.auxIDClass = $ID.text + self.ambitoActual
self.clasesDeclaradas.append($ID.text)
self.simbolos.addCaracteristica($ID.text + self.ambitoActual, "uso", "nombre de clase")
self.simbolos.addCaracteristica($ID.text + self.ambitoActual, "ambito de clase", self.ambitoActual + ":" + $ID.text)
if self.claseduplicada:
    self.ambitoaux = self.ambitoActual
    self.ambitoActual = "BORRAR_ERROR"
else:
    self.ambitoActual = self.ambitoActual + ":" + $ID.text
self.inClase = True
$line = $ID.line
}
;

componentes_clase: componente_var
                | componente_func
                | componente_herencia
                | componentes_clase componente_var
                | componentes_clase componente_func
                | componentes_clase componente_herencia
;

componente_var: declaracion_var {
if not self.claseduplicada:
    componentesActuales = self.simbolos.getCaracteristica(self.auxIDClass, "propiedades")
    if isinstance(componentesActuales, list):
        for value in self.listaVar:
            componentesActuales.append(value)
    else:
        self.simbolos.addCaracteristica(self.auxIDClass, "propiedades", self.listaVar)
    self.listaVar = []
}
;

componente_func: declaracion_func {
if not self.claseduplicada:
    componentesActuales = self.simbolos.getCaracteristica(self.auxIDClass, "miembros de clase")
    componentesActuales = self.simbolos.getCaracteristica(self.auxIDClass, "miembros")
    if isinstance(componentesActuales, list):
        componentesActuales.append(self.auxIDFunc[:self.auxIDFunc.find(":")])
        componentes = [self.auxIDFunc.replace(":","_")]
    else:
        componentesActuales = [self.auxIDFunc[:self.auxIDFunc.find(":")]]
        componentes = [self.auxIDFunc.replace(":","_")]
        self.simbolos.addCaracteristica(self.auxIDClass, "miembros de clase", componentesActuales)
        self.simbolos.addCaracteristica(self.auxIDClass, "miembros", componentes)
}
;

componente_herencia: ID ',' {
if not self.claseduplicada:
    identificador = self.verificarId($ID.text + self.ambitoActual)
    if identificador != "":
        herenciasActuales = self.simbolos.getCaracteristica(identificador, "numero de herencias")
        if isinstance(herenciasActuales, int):
            if herenciasActuales < 2:
                self.simbolos.aumentarReferencia(identificador)
                self.simbolos.addCaracteristica(self.auxIDClass, "numero de herencias", herenciasActuales + 1)
                self.simbolos.addCaracteristica(self.auxIDClass, "clase herencia", identificador)
                propiedades = self.simbolos.getCaracteristica(identificador, "propiedades")
                if isinstance(propiedades, list):
                    self.simbolos.addCaracteristica(self.auxIDClass, "propiedades heredadas", propiedades)
            else:
                self.yyerror("SEMANTICO: se exeden los niveles de herencia", $ID.line)
        else:
            self.simbolos.addCaracteristica(self.auxIDClass, "numero de herencias", 1)
            self.simbolos.addCaracteristica(self.auxIDClass, "clase herencia", identificador)
            propiedades = self.simbolos.getCaracteristica(identificador, "propiedades")
            if isinstance(propiedades, list):
                self.simbolos.addCaracteristica(self.auxIDClass, "propiedades heredadas", propiedades)
    else:
        simbolo = $ID.text
        if simbolo in self.clasesUsadas.keys():
            self.clasesUsadas[simbolo] += 1
        else:
            self.clasesUsadas[simbolo] = 1
        self.herenciasFoward[self.auxIDClass] = $ID.text
}
;

cuerpo_ejecucion: cuerpo_ejecucion ejecucion
                  | ejecucion
;

ejecucion: asignacion ','
           | invocacion ','
           | seleccion ','
           | print ','
           | while ','
           | ERROR ',' {self.yyerror("SINTACTICO: error en sentencia ejecutable", $ERROR.line)}
;

asignacion: {self.flag = self.polacaInversa.reference_counter} ID '=' expresion {
identificador = self.verificarId($ID.text + self.ambitoActual)
if identificador != "":
    if identificador in self.declaracionesVariables.keys():
        if self.ambitoActual == self.getAmbitoId(identificador):
            self.declaracionesVariables.pop(identificador)
    self.simbolos.aumentarReferencia(identificador)
    self.polacaInversa.addElemento(identificador)
    self.polacaInversa.addElemento("=")
else:
    self.yyerror("SEMANTICO: identificador " + $ID.text + " no declarado en un ambito valido", $ID.line)
if self.error is True:
    while   self.polacaInversa.reference_counter != self.flag:
        self.polacaInversa.removeLast()
    self.error = False
}
        | {self.flag = self.polacaInversa.reference_counter} uso_clase '=' {uso = self.polacaInversa.removeLast()} expresion {
self.polacaInversa.addElemento(uso)
self.polacaInversa.addElemento("=")
if self.error is True:
    while   self.polacaInversa.reference_counter != self.flag:
        self.polacaInversa.removeLast()
    self.error = False
}
;

invocacion: {self.flag = self.polacaInversa.reference_counter} ID '(' expresion ')' {
identificador = self.verificarId($ID.text + self.ambitoActual)
if identificador != "":
    if self.simbolos.getCaracteristica(identificador, "uso") == "funcion":
        if self.simbolos.getCaracteristica(identificador, "nroParametros") == "1":
            self.simbolos.aumentarReferencia(identificador)
            aux = self.polacaInversa.getReferenciaOp('FUNCION' + ' ' + identificador)
            self.polacaInversa.addElemento(aux)
            self.polacaInversa.addElemento("CALLFUNCP")
        else:
            self.yyerror("SEMANTICO: numero incorrecto de parametros", $ID.line)
    else:
        self.yyerror("SEMANTICO: identificador no es una funcion", $ID.line)
else:
    self.yyerror("SEMANTICO: funcion no declarada en un ambito valido", $ID.line)
if self.error is True:
    while   self.polacaInversa.reference_counter != self.flag:
        self.polacaInversa.removeLast()
    self.error = False
}
            | {self.flag = self.polacaInversa.reference_counter} ID '(' ')' {
identificador = self.verificarId($ID.text + self.ambitoActual)
if identificador != "":
    if self.simbolos.getCaracteristica(identificador, "uso") == "funcion":
        if self.simbolos.getCaracteristica(identificador, "nroParametros") == "0":
            self.simbolos.aumentarReferencia(identificador)
            aux = self.polacaInversa.getReferenciaOp('FUNCION' + ' ' + identificador)
            self.polacaInversa.addElemento(aux)
            self.polacaInversa.addElemento("CALLFUNC")
        else:
            self.yyerror("SEMANTICO: numero incorrecto de parametros", $ID.line)
    else:
        self.yyerror("SEMANTICO: identificador no es una funcion", $ID.line)
else:
    self.yyerror("SEMANTICO: funcion no declarada en un ambito valido", $ID.line)
if self.error is True:
    while   self.polacaInversa.reference_counter != self.flag:
        self.polacaInversa.removeLast()
    self.error = False
}
            | {self.flag = self.polacaInversa.reference_counter} clase=ID '.' funcion=ID '(' ')' {
simbolo = self.verificarId($clase.text + self.ambitoActual)
if  simbolo != "":
    self.simbolos.aumentarReferencia(simbolo)
    claseAmbito = self.verificarId(self.simbolos.getCaracteristica(simbolo, "tipo") + self.ambitoActual)
    miembros = self.simbolos.getCaracteristica(claseAmbito, "miembros de clase")
    if $funcion.text in miembros:
        ambitoClase = self.simbolos.getCaracteristica(claseAmbito, "ambito de clase")
        simboloFuncion = self.verificarId($funcion.text + ambitoClase)
        if self.simbolos.getCaracteristica(simboloFuncion, "nroParametros") == "0":
            self.simbolos.aumentarReferencia(simboloFuncion)
            aux = self.polacaInversa.getReferenciaOp('FUNCION' + ' ' + simboloFuncion)
            self.polacaInversa.addElemento(aux)
            self.polacaInversa.addElemento("CALLFUNC")
        else:
            self.yyerror("SEMANTICO: numero incorrecto de parametros en la funcion " + $funcion.text, $funcion.line)
    else:
        self.yyerror("SEMANTICO: " + $funcion.text + " no encontrado en clase " + claseAmbito, $clase.line)
else:
    self.yyerror("SEMANTICO: variable " + $clase.text + "no fue declarada en un ambito valido", $clase.line)
if self.error is True:
    while   self.polacaInversa.reference_counter != self.flag:
        self.polacaInversa.removeLast()
    self.error = False
}
            | {self.flag = self.polacaInversa.reference_counter} clase=ID '.' funcion=ID '(' expresion ')' {
simbolo = self.verificarId($clase.text + self.ambitoActual)
if  simbolo != "":
    self.simbolos.aumentarReferencia(simbolo)
    claseAmbito = self.verificarId(self.simbolos.getCaracteristica(simbolo, "tipo") + self.ambitoActual)
    miembros = self.simbolos.getCaracteristica(claseAmbito, "miembros de clase")
    if $funcion.text in miembros:
        ambitoClase = self.simbolos.getCaracteristica(claseAmbito, "ambito de clase")
        simboloFuncion = self.verificarId($funcion.text + ambitoClase)
        if self.simbolos.getCaracteristica(simboloFuncion, "nroParametros") == "1":
            self.simbolos.aumentarReferencia(simboloFuncion)
            aux = self.polacaInversa.getReferenciaOp('FUNCION' + ' ' + simboloFuncion)
            self.polacaInversa.addElemento(aux)
            self.polacaInversa.addElemento("CALLFUNCP")
        else:
            self.yyerror("SEMANTICO: numero incorrecto de parametros en la funcion " + $funcion.text, $funcion.line)
    else:
        self.yyerror("SEMANTICO: " + $funcion.text + " no encontrado en clase " + claseAmbito, $clase.line)
else:
    self.yyerror("SEMANTICO: variable " + $clase.text + "no fue declarada en un ambito valido", $clase.line)
if self.error is True:
    while   self.polacaInversa.reference_counter != self.flag:
        self.polacaInversa.removeLast()
    self.error = False
}
        | {self.flag = self.polacaInversa.reference_counter} clase=ID '.' herencia=ID '.' funcion=ID '(' ')' {
simbolo = self.verificarId($clase.text + self.ambitoActual)
if  simbolo != "":
    self.simbolos.aumentarReferencia(simbolo)
    claseAmbito = self.verificarId(self.simbolos.getCaracteristica(simbolo, "tipo") + self.ambitoActual)
    claseHerencia = self.simbolos.getCaracteristica(claseAmbito, "clase herencia")
    if $herencia.text == self.getIdSinAmbito(claseHerencia):
        miembros = self.simbolos.getCaracteristica(claseHerencia, "miembros de clase")
        if $funcion.text in miembros:
            ambitoClase = self.simbolos.getCaracteristica(claseHerencia, "ambito de clase")
            simboloFuncion = self.verificarId($funcion.text + ambitoClase)
            if self.simbolos.getCaracteristica(simboloFuncion, "nroParametros") == "0":
                self.simbolos.aumentarReferencia(simboloFuncion)
                aux = self.polacaInversa.getReferenciaOp('FUNCION' + ' ' + simboloFuncion)
                self.polacaInversa.addElemento(aux)
                self.polacaInversa.addElemento("CALLFUNC")
            else:
                self.yyerror("SEMANTICO: numero incorrecto de parametros en la funcion " + $funcion.text, $funcion.line)
        else:
            self.yyerror("SEMANTICO: " + $funcion.text + " no encontrado en clase " + $herencia.text, $clase.line)
    else:
        self.yyerror("SEMANTICO: " + $clase.text + " no hereda de " + $herencia.text, $clase.line)
else:
    self.yyerror("SEMANTICO: variable " + $clase.text + "no fue declarada en un ambito valido", $clase.line)
if self.error is True:
    while   self.polacaInversa.reference_counter != self.flag:
        self.polacaInversa.removeLast()
    self.error = False
}
        | {self.flag = self.polacaInversa.reference_counter} clase=ID '.' herencia=ID '.' funcion=ID '(' expresion ')' {
simbolo = self.verificarId($clase.text + self.ambitoActual)
if  simbolo != "":
    self.simbolos.aumentarReferencia(simbolo)
    claseAmbito = self.verificarId(self.simbolos.getCaracteristica(simbolo, "tipo") + self.ambitoActual)
    claseHerencia = self.simbolos.getCaracteristica(claseAmbito, "clase herencia")
    if $herencia.text == self.getIdSinAmbito(claseHerencia):
        miembros = self.simbolos.getCaracteristica(claseHerencia, "miembros de clase")
        if $funcion.text in miembros:
            ambitoClase = self.simbolos.getCaracteristica(claseHerencia, "ambito de clase")
            simboloFuncion = self.verificarId($funcion.text + ambitoClase)
            if self.simbolos.getCaracteristica(simboloFuncion, "nroParametros") == "1":
                self.simbolos.aumentarReferencia(simboloFuncion)
                aux = self.polacaInversa.getReferenciaOp('FUNCION' + ' ' + simboloFuncion)
                self.polacaInversa.addElemento(aux)
                self.polacaInversa.addElemento("CALLFUNCP")
            else:
                self.yyerror("SEMANTICO: numero incorrecto de parametros en la funcion " + $funcion.text, $funcion.line)
        else:
            self.yyerror("SEMANTICO: " + $funcion.text + " no encontrado en clase " + $herencia.text, $clase.line)
    else:
        self.yyerror("SEMANTICO: " + $clase.text + " no hereda de " + $herencia.text, $clase.line)
else:
    self.yyerror("SEMANTICO: variable " + $clase.text + "no fue declarada en un ambito valido", $clase.line)
if self.error is True:
    while   self.polacaInversa.reference_counter != self.flag:
        self.polacaInversa.removeLast()
    self.error = False
}
        | {self.flag = self.polacaInversa.reference_counter} clase=ID '.' herencia1=ID '.' herencia2=ID '.' funcion=ID '(' ')' {
simbolo = self.verificarId($clase.text + self.ambitoActual)
if  simbolo != "":
    self.simbolos.aumentarReferencia(simbolo)
    claseAmbito = self.verificarId(self.simbolos.getCaracteristica(simbolo, "tipo") + self.ambitoActual)
    claseHerencia = self.simbolos.getCaracteristica(claseAmbito, "clase herencia")
    if $herencia1.text == self.getIdSinAmbito(claseHerencia):
        claseHerencia = self.simbolos.getCaracteristica(claseHerencia, "clase herencia")
        if $herencia2.text == self.getIdSinAmbito(claseHerencia):
            miembros = self.simbolos.getCaracteristica(claseHerencia, "miembros de clase")
            if $funcion.text in miembros:
                ambitoClase = self.simbolos.getCaracteristica(claseHerencia, "ambito de clase")
                simboloFuncion = self.verificarId($funcion.text + ambitoClase)
                if self.simbolos.getCaracteristica(simboloFuncion, "nroParametros") == "0":
                    self.simbolos.aumentarReferencia(simboloFuncion)
                    aux = self.polacaInversa.getReferenciaOp('FUNCION' + ' ' + simboloFuncion)
                    self.polacaInversa.addElemento(aux)
                    self.polacaInversa.addElemento("CALLFUNC")
                else:
                    self.yyerror("SEMANTICO: numero incorrecto de parametros en la funcion " + $funcion.text, $funcion.line)
            else:
                self.yyerror("SEMANTICO: funcion " + $funcion.text + " no encontrada en " + $herencia2.text, $clase.line)
        else:
            self.yyerror("SEMANTICO: " + $herencia1.text + " no hereda de " + $herencia2.text, $clase.line)
    else:
        self.yyerror("SEMANTICO: " + $clase.text + " no hereda de " + $herencia1.text, $clase.line)
else:
    self.yyerror("SEMANTICO: variable " + $clase.text + "no fue declarada en un ambito valido", $clase.line)
if self.error is True:
    while   self.polacaInversa.reference_counter != self.flag:
        self.polacaInversa.removeLast()
    self.error = False
}
        | {self.flag = self.polacaInversa.reference_counter} clase=ID '.' herencia1=ID '.' herencia2=ID '.' funcion=ID '(' expresion ')' {
simbolo = self.verificarId($clase.text + self.ambitoActual)
if  simbolo != "":
    self.simbolos.aumentarReferencia(simbolo)
    claseAmbito = self.verificarId(self.simbolos.getCaracteristica(simbolo, "tipo") + self.ambitoActual)
    claseHerencia = self.simbolos.getCaracteristica(claseAmbito, "clase herencia")
    if $herencia1.text == self.getIdSinAmbito(claseHerencia):
        claseHerencia = self.simbolos.getCaracteristica(claseHerencia, "clase herencia")
        if $herencia2.text == self.getIdSinAmbito(claseHerencia):
            miembros = self.simbolos.getCaracteristica(claseHerencia, "miembros de clase")
            if $funcion.text in miembros:
                ambitoClase = self.simbolos.getCaracteristica(claseHerencia, "ambito de clase")
                simboloFuncion = self.verificarId($funcion.text + ambitoClase)
                if self.simbolos.getCaracteristica(simboloFuncion, "nroParametros") == "1":
                    self.simbolos.aumentarReferencia(simboloFuncion)
                    aux = self.polacaInversa.getReferenciaOp('FUNCION' + ' ' + simboloFuncion)
                    self.polacaInversa.addElemento(aux)
                    self.polacaInversa.addElemento("CALLFUNCP")
                else:
                    self.yyerror("SEMANTICO: numero incorrecto de parametros en la funcion " + $funcion.text, $funcion.line)
            else:
                self.yyerror("SEMANTICO: funcion " + $funcion.text + " no encontrada en " + $herencia2.text, $clase.line)
        else:
            self.yyerror("SEMANTICO: " + $herencia1.text + " no hereda de " + $herencia2.text, $clase.line)
    else:
        self.yyerror("SEMANTICO: " + $clase.text + " no hereda de " + $herencia1.text, $clase.line)
else:
    self.yyerror("SEMANTICO: variable " + $clase.text + "no fue declarada en un ambito valido", $clase.line)
if self.error is True:
    while   self.polacaInversa.reference_counter != self.flag:
        self.polacaInversa.removeLast()
    self.error = False
}
;

seleccion: {self.flagCondicion = self.polacaInversa.reference_counter
} if_condicion bloque_control posible_else END_IF {
if self.elseaux is False:
    number = self.polacaInversa.getLastPendingStep()
    self.polacaInversa.setElemento(number)
else:
    self.elseaux = False
if self.errorCondicion is True:
    while   self.polacaInversa.reference_counter != self.flagCondicion:
        self.polacaInversa.removeLast()
    self.errorCondicion = False
}
 //Agrego valor que sigue de la cinta en la celdad el tope de la Pila. Y desapilo
;
posible_else: else bloque_control {
number = self.polacaInversa.getLastPendingStep()
self.polacaInversa.setElemento(number)
} //Agrego valor que sigue de la cinta en la celda del tope de la pila. Y desapilo
             |
;
else: ELSE {
self.elseaux = True
number = self.polacaInversa.getLastPendingStep()
self.polacaInversa.addPendingStep(self.polacaInversa.reference_counter)
self.polacaInversa.addElemento(" ")
self.polacaInversa.addElemento("BI")
self.polacaInversa.setElemento(number)
} // agrego celda vacia(y agrego en la pila) y BI
;

if_condicion: IF '(' condicion ')' {
self.polacaInversa.addPendingStep(self.polacaInversa.reference_counter)
self.polacaInversa.addElemento(" ")
self.polacaInversa.addElemento("BF")
} //Agrego celda vacia, apilo, y agrego BF
;

bloque_control: '{' cuerpo_ejecucion '}'
;

condicion: expresion comparador expresion {
self.polacaInversa.addElemento($comparador.text)
if self.error is True:
    self.errorCondicion = True
    self.error = False
}
;

comparador: '<'
            | '>'
            | MENORIGUAL
            | MAYORIGUAL
            | DISTINTO
            | COMPIGUAL
;

print: PRINT '(' CADENA ')'{
self.polacaInversa.addElemento($CADENA.text)
self.polacaInversa.addElemento("PRINT")
}
;
while: {self.flagCondicion = self.polacaInversa.reference_counter} while_condicion bloque_control {
number = self.polacaInversa.getLastPendingStep()
self.polacaInversa.addElemento(self.aux)
self.polacaInversa.addElemento("BI")
self.aux = self.auxAnterior
self.polacaInversa.setElemento(number)
if self.errorCondicion is True:
    while   self.polacaInversa.reference_counter != self.flagCondicion:
        self.polacaInversa.removeLast()
    self.errorCondicion = False
}

;

while_condicion:{self.auxAnterior = self.aux
self.aux = self.polacaInversa.reference_counter
} WHILE {self.polacaInversa.addElemento("TAG"+str(self.aux))} '(' condicion ')' DO{
self.polacaInversa.addPendingStep(self.polacaInversa.reference_counter)
self.polacaInversa.addElemento(" ")
self.polacaInversa.addElemento("BF")
}

;

tipo: INT
       | ULONG
       | FLOAT
       | ID {
identificador = self.verificarId($ID.text + self.ambitoActual)
if identificador != "":
    self.simbolos.aumentarReferencia(identificador)
else:
    simbolo = $ID.text
    if simbolo in self.clasesUsadas.keys():
        self.clasesUsadas[simbolo] += 1
    else:
        self.clasesUsadas[simbolo] = 1
}
;

expresion:  expresion '+' termino {self.polacaInversa.addElemento("+")}
            | expresion '-' termino {self.polacaInversa.addElemento("-")}
            | termino
;

termino: termino '*' factor {self.polacaInversa.addElemento("*")}
        | termino '/' factor {self.polacaInversa.addElemento("/")}
        | factor
;

factor: referencia
        | '-' NUM_INT {
text = "_".join(reversed($NUM_INT.text.split("_")))
key = text
if key in self.simbolos.keys():
    if self.simbolos.getCaracteristica(key, "referencias") == 1:
        self.simbolos.remove(key)
    else:
        self.simbolos.reducirReferencia(key)
self.simbolos.addSimbolo("-" + text)
self.simbolos.addCaracteristica("-" + text, "tipo", "INT")
self.simbolos.addCaracteristica("-" + text, "valor", self.getValor("-" + text))
self.simbolos.addCaracteristica("-" + text, "uso","constante")
self.polacaInversa.addElemento(text)
}
        | NUM_ULONG {
texto = $NUM_ULONG.text
text = "_".join(reversed(texto.split("_")))
self.simbolos.addCaracteristica(text, "tipo", "ULONG")
self.simbolos.addCaracteristica(text, "valor", self.getValor(text))
self.simbolos.addCaracteristica(text, "uso","constante")
self.polacaInversa.addElemento(text)
}
        | NUM_FLOAT {
guion = $NUM_FLOAT.text.replace(".","_")
guion = guion.replace("+","")
self.simbolos.addCaracteristica("f"+guion, "tipo", "FLOAT")
self.simbolos.addCaracteristica("f"+guion, "uso","constante")
aux = float($NUM_FLOAT.text)
self.simbolos.addCaracteristica("f"+guion, "valor",str(aux).replace("+",""))
self.polacaInversa.addElemento("f"+guion)
}
        | '-' NUM_FLOAT {
key = $NUM_FLOAT.text
if key in self.simbolos.keys():
    if self.simbolos.getCaracteristica(key, "referencias") == 1:
        self.simbolos.remove(key)
    else:
        self.simbolos.reducirReferencia(key)
guion = $NUM_FLOAT.text.replace(".","_")
guion = guion.replace("-","_")
self.simbolos.addSimbolo("f_" + guion)
aux = float($NUM_FLOAT.text)
self.simbolos.addCaracteristica("f_" + guion, "valor","-" + str(aux))
self.simbolos.addCaracteristica("f_" + guion, "tipo", "FLOAT")
self.polacaInversa.addElemento("f_"+guion)
}
        | NUM_INT {
text = "_".join(reversed($NUM_INT.text.split("_")))
if text == "i_32768":
    self.yyerror("LEXICO: INT fuera de rango",$NUM_INT.line)
else:
    texto = text
    self.simbolos.addCaracteristica(texto, "tipo", "INT")
    self.simbolos.addCaracteristica(texto, "valor", self.getValor(texto))
    self.simbolos.addCaracteristica(texto, "uso","constante")
    self.polacaInversa.addElemento(texto)
}
        | ERROR {self.yyerror("SINTACTICO: se espera una constante o id",$ERROR.line)}
;

referencia: ID {
identificador = self.verificarId($ID.text + self.ambitoActual)
if identificador != "":
    self.polacaInversa.addElemento(identificador)} posible_guion_doble {
identificador = self.verificarId($ID.text + self.ambitoActual)
if identificador != "":
    self.simbolos.aumentarReferencia(identificador)
    if (self.menos_menos is True):
        aux = self.simbolos.getCaracteristica(identificador,"tipo")
        if aux == "INT":
            text = "_".join(reversed("1_i".split("_")))
            self.simbolos.addSimbolo(text)
            self.polacaInversa.addElemento(text)
            self.simbolos.addCaracteristica(text, "tipo", "INT")
            self.simbolos.addCaracteristica(text, "valor", 1)
            self.simbolos.addCaracteristica(text, "uso","constante")
        elif aux == "ULONG":
            text = "_".join(reversed("1_ul".split("_")))
            self.simbolos.addSimbolo(text)
            self.polacaInversa.addElemento(text)
            self.simbolos.addCaracteristica(text, "tipo", "ULONG")
            self.simbolos.addCaracteristica(text, "valor", 1)
            self.simbolos.addCaracteristica(text, "uso","constante")
        elif aux == "FLOAT":
            text = "1.0"
            self.simbolos.addSimbolo(text)
            self.polacaInversa.addElemento(text)
            self.simbolos.addCaracteristica(text, "tipo", "FLOAT")
            self.simbolos.addCaracteristica(text, "valor", 1.0)
            self.simbolos.addCaracteristica(text, "uso","constante")

        self.polacaInversa.addElemento("-")
        self.polacaInversa.addElemento(identificador)
        self.polacaInversa.addElemento('=')
        self.polacaInversa.addElemento(identificador)
        self.menos_menos = False
else:
    self.yyerror("SEMANTICO: id " + $ID.text + " no existe en un ambito valido", $ID.line)
    self.error = True

}
            | uso_clase
;

posible_guion_doble: '-' '-' {
self.menos_menos = True
}
                  |
;

uso_clase: clase=ID '.' atributo=ID {
idClase = self.verificarId($clase.text + self.ambitoActual)
if idClase != "":
    self.simbolos.aumentarReferencia(idClase)
    ambitoClase = self.verificarId(self.simbolos.getCaracteristica(idClase, "tipo") + self.ambitoActual)
    if $atributo.text in self.simbolos.getCaracteristica(ambitoClase, "propiedades"):
        atributo = $atributo.text + self.simbolos.getCaracteristica(ambitoClase, "ambito de clase")
        if atributo != "":
            self.simbolos.aumentarReferencia(atributo)
            clase = $clase.text + self.ambitoActual + "." + $atributo.text
            self.polacaInversa.addElemento(str(clase))
    else:
        self.yyerror("SEMANTICO: propiedad " + $atributo.text + " no encontrada en clase " + idClase, $clase.line)
        self.error = True
else:
    self.yyerror("SEMANTICO: variable " + $clase.text + "no fue declarada en un ambito valido", $clase.line)
    self.error = True
}
        | clase=ID '.' herencia= ID '.' atributo=ID {
idClase = self.verificarId($clase.text + self.ambitoActual)
if idClase != "":
    self.simbolos.aumentarReferencia(idClase)
    ambitoClase = self.verificarId(self.simbolos.getCaracteristica(idClase, "tipo") + self.ambitoActual)
    claseHerencia = self.simbolos.getCaracteristica(ambitoClase, "clase herencia")
    if $herencia.text == self.getIdSinAmbito(claseHerencia):
        if $atributo.text in self.simbolos.getCaracteristica(claseHerencia, "propiedades"):
            atributo = $atributo.text + self.simbolos.getCaracteristica(claseHerencia, "ambito de clase")
            self.simbolos.aumentarReferencia(atributo)
            clase = $clase.text + self.ambitoActual + "." + $herencia.text + "_" + "." + $atributo.text
            self.polacaInversa.addElemento(str(clase))
        else:
            self.yyerror("SEMANTICO: propiedad " + $atributo.text + " no encontrada en clase " + claseHerencia, $clase.line)
            self.error = True
    else:
        self.yyerror("SEMANTICO: clase " + idClase + " no hereda de " + $herencia.text, $clase.line)
        self.error = True
else:
    self.yyerror("SEMANTICO: variable " + $clase.text + "no fue declarada en un ambito valido", $clase.line)
    self.error = True
}
        | clase=ID '.' herencia1= ID '.' herencia2= ID '.' atributo=ID {
idClase = self.verificarId($clase.text + self.ambitoActual)
if idClase != "":
    self.simbolos.aumentarReferencia(idClase)
    ambitoClase = self.verificarId(self.simbolos.getCaracteristica(idClase, "tipo") + self.ambitoActual)
    claseHerencia = self.simbolos.getCaracteristica(ambitoClase, "clase herencia")
    if $herencia1.text == self.getIdSinAmbito(claseHerencia):
        claseHerencia = self.simbolos.getCaracteristica(claseHerencia, "clase herencia")
        if $herencia2.text == self.getIdSinAmbito(claseHerencia):
            if $atributo.text in self.simbolos.getCaracteristica(claseHerencia, "propiedades"):
                atributo = $atributo.text + self.simbolos.getCaracteristica(claseHerencia, "ambito de clase")
                self.simbolos.aumentarReferencia(atributo)
                clase = $clase.text + self.ambitoActual + "." + $herencia1.text + "_" + "." + $herencia2.text + "_" + "." + $atributo.text
                self.polacaInversa.addElemento(str(clase))
            else:
                self.yyerror("SEMANTICO: propiedad " + $atributo.text + " no encontrada en clase " + claseHerencia, $clase.line)
                self.error = True
        else:
            self.yyerror("SEMANTICO: clase " + $herencia1.text + " no hereda de " + $herencia2.text, $clase.line)
            self.error = True
    else:
        self.yyerror("SEMANTICO: clase " + idClase + " no hereda de " + $herencia1.text, $clase.line)
        self.error = True
else:
    self.yyerror("SEMANTICO: variable " + $clase.text + "no fue declarada en un ambito valido", $clase.line)
    self.error = True
}
;
