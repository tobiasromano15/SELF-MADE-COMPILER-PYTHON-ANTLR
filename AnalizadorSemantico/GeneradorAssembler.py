from copy import copy

from AnalizadorSemantico.InformacionClase import InformacionClase
from AnalizadorSemantico import PolacaInversa


class DataGenerator:
    def __init__(self):
        self.classes = {}
        self.simboloClase = {}
        self.variables = {}
        self.functions = {}
        self.variablesPolaca = {}
        self.declaraciones = {}
        self.constantes = {}
        self.declaraciones_asm= []
        self.foward = {}

    def procesar_linea(self, linea_texto):
        campos = {}
        partes = linea_texto.split(" - ")
        for parte in partes:
            if ": " in parte:
                clave, valor = parte.split(": ", 1)
                campos[clave.lower().replace(" ", "_")] = valor
        # print(campos)
        return InformacionClase(**campos)

    def generar_declaracion_asm(self, simbolo, tipo, valor = None, uso = None):
        tipos_asm = {"INT": "DW", "FLOAT": "DD", "ULONG": "DD"}  # DD para INT, DQ para FLOAT en MASM32
        clase = None
        if valor == None:
            if (tipos_asm.get(tipo, None)) is None:
                if tipo in self.classes:
                    clase = tipo
                    return f"{simbolo} {clase} <?>"
            else:
                return f"{simbolo} {tipos_asm.get(tipo)} ?"  # Pone '?' si el tipo no se reconoce
        if uso == "constante":
            return f"{simbolo} {tipos_asm.get(tipo)} {valor}"
        if clase == None:
            return None
    def ifClass(self, simbolo: str):
        lexema = simbolo
        partes = lexema.split(':')
        if len(partes) > 2:
            return partes[-1]
        elif len(partes) == 2:
            return partes[1]
        else:
            return None

    def setDatos(self, info: InformacionClase):
        if info.uso == "nombre de clase":
            self.simboloClase[info.simbolo] = info
        elif info.uso == "funcion":
                self.functions[info.raw_simbolo] = info
        elif info.uso == "variable":
            if info.simbolo in self.variables.keys():
                self.variables[info.raw_simbolo] = info
            else:
                self.variables[info.simbolo] = info
            self.variablesPolaca[info.raw_simbolo] = info
        elif info.uso == "auxiliar" or "constante" or "parametro":
            self.variablesPolaca[info.raw_simbolo] = info

    def lookForProperty(self, propiedad) -> InformacionClase:
        aux = copy(self.variables.get(propiedad))
        return aux

    def lookForDeepProperty(self, clase: InformacionClase) -> []:
        list_c = []

        if clase.propiedades is not None:
            for item in clase.propiedades:
                list_c.append(self.lookForProperty(item))
        if clase.clase_herencia is not None:
            aux = self.lookForDeepProperty(copy(self.simboloClase.get(clase.clase_herencia)))
            if len(aux) != 0:
                list_c.extend(aux)
        return list_c

    def procesar_archivo(self, ruta_archivo):
        declaraciones_asm = []
        with open(ruta_archivo, "r") as archivo:
            for linea in archivo:
                if linea.strip():  # Ignorar líneas vacías
                    infoclase = self.procesar_linea(linea)
                    self.setDatos(infoclase)
        for item in self.simboloClase.values():
            if item.simbolo not in self.classes:
                new_struct = StructGen(item.simbolo)
                self.classes[item.simbolo] = new_struct
                #print(item)
                if item.propiedades is not None:
                    for propiedad in item.propiedades:
                        prop = copy(self.lookForProperty(propiedad))
                        self.declaraciones[prop.simbolo + "_main_" + item.simbolo] = prop.tipo
                        #print(self.declaraciones)
                        declaracion = self.generar_declaracion_asm(prop.simbolo, prop.tipo)
                        if declaracion != None:
                            print("hola")
                            new_struct.addField(declaracion)
                            new_struct.aux.append(prop.simbolo)
                        else:
                            print("hola1")
                            new_struct.uses_foward = prop.tipo
                            self.foward[new_struct] = prop

                self.classes[item.simbolo] = new_struct
                if item.clase_herencia is not None:
                    declaracion = self.generar_declaracion_asm(item.clase_herencia+"_", item.clase_herencia)
                    if declaracion != None:
                        new_struct.addField(declaracion)
                        new_struct.aux.append(item.clase_herencia)
                    else:
                        new_struct.uses_foward = item.clase_herencia
                        self.foward[new_struct] = item

                print(new_struct.fields)
                self.classes[item.simbolo] = new_struct

        for item in self.variables.values():
            if item.ultimo_ambito == "main":
                declaracion = self.generar_declaracion_asm(item.raw_simbolo, item.tipo)
                self.declaraciones_asm.append(declaracion)
            elif item.ultimo_ambito in self.functions:
                declaracion = self.generar_declaracion_asm(item.raw_simbolo, item.tipo)
                self.declaraciones_asm.append(declaracion)


        for item in self.variablesPolaca.values():
            if item.uso == "constante":
                declaracion = self.generar_declaracion_asm(item.raw_simbolo,item.tipo,item.valor,item.uso)
                self.declaraciones_asm.append(declaracion)
            elif item.uso == "auxiliares":
                declaracion = self.generar_declaracion_asm(item.raw_simbolo,item.tipo)
                self.declaraciones_asm.append(declaracion)
            elif item.uso == "parametro":
                declaracion = self.generar_declaracion_asm(item.raw_simbolo,item.tipo)
                self.declaraciones_asm.append(declaracion)
            else:
                declaracion = self.generar_declaracion_asm(item.raw_simbolo,item.tipo)
                if declaracion not in self.declaraciones_asm:
                    self.declaraciones_asm.append(declaracion)
            print(self.classes)
            #print(self.declaraciones_asm)
        return self.declaraciones_asm

    def getStruct(self):
        for item,valor in self.foward.items():
            item.addField(self.generar_declaracion_asm(valor.clase_herencia + "_",valor.clase_herencia))

        structures = []
        for a in self.classes.values():
            print(a)
            if a.uses_foward == None:
                structures.append(a.toStr())
        for a in self.classes.values():
            if a.uses_foward != None:
                structures.append(a.toStr())
        return structures


class StructGen:
    def __init__(self, name):
        self.name = name + " STRUCT"
        self.fields = []
        self.addField("unknown DW ?")
        self.aux = []
        self.end = name + " ENDS"
        self.uses_foward = None

    def addField(self, declaracion: str):
        self.fields.append(declaracion)

    def toStr(self):
        field = self.name
        espacios_indentacion = 4
        structs = "     \n".join(" " * espacios_indentacion + linea for linea in self.fields)
        return field + "\n" + structs + "\n" + self.end + "\n"

class Registros:
    def __init__(self):
        self.EAX = "EAX"
        self.EBX = "EBX"
        self.ECX = "ECX"
        self.EDX = "EDX"


class CodeGenerator:
    def __init__(self, polaca: PolacaInversa, celdaActual = 1, data = DataGenerator(), value = True, pilaOperandos = [],numAux = 1):
        self.polaca = polaca
        self.celdaActual = celdaActual
        self.operadores = ["+", "-", "*", "/", "BI", "BF", "FUNCION", "ret", "=", "<", "<=", ">=", "==", "!!",
                           "CALLFUNC", "PRINT",">","CALLFUNCP"]
        if value:
            self.codigo = ".code\nstart:\n"
        else:
            self.codigo = ""
        self.pilaOperandos = pilaOperandos
        self.Registros = Registros()
        self.registrosDisponibles = {"EAX": True, "EBX": True, "ECX": True, "EDX": True}
        self.tira = polaca.referencias
        self.numAux = numAux
        self.header = ""
        self.tags = []
        self.tipoRegistros = {self.Registros.EAX: "", self.Registros.EBX: "", self.Registros.ECX: "", self.Registros.EDX: ""}
        self.ruta_archivo = "tabla_de_simbolos.txt"
        self.data = data  # Si queres ver si existe una variable,el tipo el ambito, etc. Esta variable
        # tiene 4 diccionarios con clases, funciones, variablesPolaca etc. Si buscas una variable dada por la polaca,
        # busca en variablesPolaca, por ejemplo, variable.raw_simbolo, que es el simbolo Es el simbolo asi:
        # simbolo_main_clase_b
        if value:
            self.declaracion_asm = self.data.procesar_archivo(self.ruta_archivo)
        self.last_texto = ""
        self.codigoFunciones = ""
        self.cadenas = ""
    def getTipo(self, op):
        if op.startswith("f") and (op[1] == "-" or op[1].isdigit()):
            retorno = self.data.variablesPolaca.get(op).tipo if op in self.data.variablesPolaca else "ERROR FLOAT"  # no sabia que poenr ahí
        else:
            if "." in op:  # por si es una clase interfiere con tipo FLOAT
                aux = op.split('.')
                var = aux[0]
                if len(aux) >= 3:
                    var = aux[-1] + "_main_" + aux[1]
                    aux2 = self.data.variablesPolaca.get(var[:-1]).tipo
                else:
                    aux1 = aux[-1] + "_main_" + self.data.variablesPolaca.get(aux[0]).tipo
                    aux2 = self.data.variablesPolaca.get(aux1).tipo

                retorno = aux2
            else:
                retorno = self.data.variablesPolaca.get(op).tipo if op in self.data.variablesPolaca else "funcion"
        return retorno

    def getRegistroExterno(self):
        if self.registrosDisponibles[self.Registros.EAX]:
            return self.Registros.EAX
        elif self.registrosDisponibles[self.Registros.EDX]:
            return self.Registros.EDX
        else:
            self.liberar(self.Registros.EAX, self.tipoRegistros[self.Registros.EAX])
            return self.Registros.EAX

    def getRegistroInterno(self):
        if self.registrosDisponibles[self.Registros.EBX]:
            return self.Registros.EBX
        elif self.registrosDisponibles[self.Registros.ECX]:
            return self.Registros.ECX
        else:
            self.liberar(self.Registros.EBX, self.tipoRegistros[self.Registros.EBX])
            return self.Registros.EBX

    def liberar(self, registro, tipo):
        auxiliar = "@aux" + str(self.numAux)
        self.codigo += "MOV " + auxiliar + ", " + registro + "\n"
        self.last_texto = "MOV " + auxiliar + ", " + registro + "\n"
        if registro == "AX":
            registro = self.Registros.EAX
        if registro == "BX":
            registro = self.Registros.EBX
        if registro == "CX":
            registro = self.Registros.ECX
        if registro == "DX":
            registro = self.Registros.EDX
        self.pilaOperandos.insert(0, auxiliar)
        #self.addData(auxiliar, tipo)
        infoClase = InformacionClase(simbolo=auxiliar, caracteristicas="aux",
                                     tipo=tipo, uso="auxiliar")

        self.data.setDatos(infoClase)
        declaracion = self.data.generar_declaracion_asm(infoClase.raw_simbolo,infoClase.tipo)
        self.data.declaraciones_asm.append(declaracion)
        self.numAux += 1
        self.registrosDisponibles[registro] = True

    def addData(self, dato, tipo):
        if tipo == "INT":
            self.header += dato + " DW ? ; 16bits" + "\n"
        else:
            self.header += dato + " DD ? ; 32bits" + "\n"

    def sumaOResta(self, op):
        op1 = self.pilaOperandos.pop(0)
        op2 = self.pilaOperandos.pop(0)
        if self.getTipo(op1) != self.getTipo(op2):
            self.codigo += "JMP LabelErrorTYPE" + "\n"
            self.last_texto = "JMP ErrorTYPE" + "\n"
        else:
            tipo = self.getTipo(op1)
            registro = self.getRegistroExterno()
            if tipo == "INT":
                if registro == self.Registros.EAX:
                    registro = "AX"
                    self.tipoRegistros[self.Registros.EAX] = "INT"
                else:
                    registro = "DX"
                    self.tipoRegistros[self.Registros.EDX] = "INT"
            elif tipo == "ULONG":
                if registro == self.Registros.EAX:
                    registro = "EAX"
                    self.tipoRegistros[self.Registros.EAX] = "ULONG"
                else:
                    registro = "EDX"
                    self.tipoRegistros[self.Registros.EDX] = "ULONG"
            if tipo != "FLOAT":
                self.codigo += "MOV " + registro + ", " + op2 + "\n"
                self.last_texto = "MOV " + registro + ", " + op2 + "\n"
                if op == "+":
                    self.codigo += "ADD " + registro + ", " + op1 + "\n"
                    self.last_texto = "ADD " + registro + ", " + op1 + "\n"
                else:
                    #print(registro, op1)
                    self.codigo += "SUB " + registro + ", " + op1 + "\n"
                    self.last_texto = "SUB " + registro + ", " + op1 + "\n"
                self.liberar(registro, tipo)
            else:
                self.operacionFlotante(op1,op2,op)
    def multINT(self,registro,op1):
        self.codigo += "IMUL " + registro + ", " + op1 + "\n"
        self.last_texto = "IMUL BX, " + "CX\n"
        self.liberar(registro, self.getTipo(op1))
        self.codigo += "JO LabelErrorOvPE\n"
        self.last_texto = "JO LabelErrorOvPE\n"
    def divINT(self,registro,op1):
        self.codigo += "CMP " + op1 + ", " "0\n"
        self.last_texto = "CMP CX, 0\n"
        self.codigo += "JE LabelErrorDIV0\n"
        self.last_texto = "JE LabelErrorDIV0\n"
        if registro == "BX":
            regis2 = "CX"
            self.codigo += "MOV CX, "+ registro + "\n"
        else:
            regis2 = "BX"
            self.codigo += "MOV BX, " + registro + "\n"

        self.codigo += "IDIV "+ op1 + "\n"
        self.last_texto = "IDIV BX, CX" + "\n"
        self.liberar(regis2, self.getTipo(op1))
    def mul32BIT(self,registro,op1):
        if registro == "EBX":
            regis2 = "ECX"
            self.codigo += "MOV ECX, "+ op1 + "\n"
        else:
            regis2 = "EBX"
            self.codigo += "MOV EBX, " + op1 + "\n"
        self.codigo += "MUL " + registro + "\n"
        self.liberar(regis2, self.getTipo(op1))
        self.codigo += "JO LabelErrorOvPE\n"
        self.last_texto = "JO LabelErrorOvPE\n"
    def div32BIT(self,registro,op1):
        self.codigo += "CMP " + op1 + ", " "0\n"
        self.last_texto = "CMP CX, 0\n"
        self.codigo += "JE LabelErrorDIV0\n"
        self.last_texto = "JE LabelErrorDIV0\n"
        if registro == "EBX":
            regis2 = "ECX"
            self.codigo += "MOV ECX, "+ registro + "\n"
        else:
            regis2 = "EBX"
            self.codigo += "MOV EBX, " + registro + "\n"

        self.codigo += "DIV "+ op1 + "\n"
        self.last_texto = "DIV BX, CX" + "\n"
        self.liberar(regis2, self.getTipo(op1))
    def multODiv(self, op):
        op1 = self.pilaOperandos.pop(0)
        op2 = self.pilaOperandos.pop(0)
        if self.getTipo(op1) != self.getTipo(op2):
            self.codigo += "JMP LabelErrorTYPE" + "\n"
            self.last_texto = "JMP ErrorTYPE" + "\n"
        else:
            registro = self.getRegistroInterno()
            tipo = self.getTipo(op1)
            if tipo == "INT":
                if registro == self.Registros.EBX:
                    registro = "BX"
                    self.tipoRegistros[self.Registros.EBX] = "INT"
                else:
                    registro = "CX"
                    self.tipoRegistros[self.Registros.ECX] = "INT"
                self.codigo += "MOV " + registro + ", " + op2 + "\n"
                if op == "*":
                    self.multINT(registro,op1)
                else:
                    self.divINT(registro,op1)
            elif tipo == "ULONG":
                if registro == self.Registros.EBX:
                    registro = "EBX"
                    self.tipoRegistros[self.Registros.EBX] = "ULONG"
                else:
                    registro = "ECX"
                    self.tipoRegistros[self.Registros.ECX] = "ULONG"
                self.codigo += "MOV " + registro + ", " + op2 + "\n"
                if op == "*":
                    self.mul32BIT(registro,op1)
                else:
                    self.div32BIT(registro,op1)
            elif tipo == "FLOAT":
                self.operacionFlotante(op1,op2,op)
    def operacionFlotante(self, op1, op2, op):
        if op == "+":
            self.codigo += "FLD dword ptr[" + op1 + "]\n"
            self.last_texto = "FLD dword ptr[" + op1 + "]\n"
            self.codigo += "FADD dword ptr[" + op2 + "]\n"
            self.last_texto = "FADD dword ptr[" + op2 + "]\n"
            # ErrorOverflow
            self.codigo += "FCOM dword ptr[MaxFLOAT] \n"
            self.last_texto += "FCOM dword ptr[MaxFLOAT] \n"
            if not self.registrosDisponibles[self.Registros.EAX]:
                self.liberar(self.Registros.EAX, self.tipoRegistros[self.Registros.EAX])
            self.codigo += "FSTSW AX \n"
            self.last_texto += "FSTSW AX \n"
            self.codigo += "SAHF\n"
            self.last_texto += "SAHF\n"
            self.codigo += "JAE LabelErrorOvSF\n"
            self.last_texto += "JAE LabelErrorOvSF\n"
        elif op == "-":
            self.codigo += "FLD dword ptr[" + op2 + "]\n"
            self.last_texto += "FLD dword ptr[" + op2 + "]\n"
            self.codigo += "FSUB dword ptr[" + op1 + "]\n"
            self.last_texto += "FSUB dword ptr[" + op1 + "]\n"
        elif op == "*":
            self.codigo += "FLD dword ptr[" + op1 + "]\n"
            self.last_texto += "FLD dword ptr[" + op1 + "]\n"
            self.codigo += "FMUL dword ptr[" + op2 + "]\n"
            self.last_texto += "FMUL dword ptr[" + op2 + "]\n"
        elif op == "/":
            # error division por 0
            self.codigo += "FLDZ\n"
            self.last_texto += "FLDZ\n"
            self.codigo += "FLD dword ptr[" + op1 + "]\n"
            self.last_texto += "FLD dword ptr[" + op1 + "]\n"
            self.codigo += "FCOM\n"
            self.last_texto += "FCOM\n"
            if not self.registrosDisponibles[self.Registros.EAX]:
                self.liberar(self.Registros.EAX, self.tipoRegistros[self.Registros.EAX])
            self.codigo += "FSTSW AX \n"
            self.last_texto += "FSTSW AX \n"
            self.codigo += "SAHF\n"
            self.last_texto += "SAHF\n"
            self.codigo += "JE LabelErrorDIV0\n"
            self.last_texto += "JE LabelErrorDIV0\n"
            # divido
            self.codigo += "FLD dword ptr[" + op2 + "]\n"
            self.last_texto += "FLD dword ptr[" + op2 + "]\n"
            self.codigo += "FDIV " + op1 + "\n"
            self.last_texto += "FDIV " + op1 + "\n"
        elif op == "=":
            self.codigo += "FLD " + op2 + "\n"
            self.last_texto += "FLD " + op2 + "\n"
            self.codigo += "FSTP " + op1 + "\n"
            self.last_texto += "FSTP " + op1 + "\n"
            self.pilaOperandos.insert(0,op1)

        if op != "=":  # si no fue una asignasion guardo el resultado en un auxiliar y lo pongo en la pila de operandos
            aux = "@aux" + str(self.numAux)
            self.codigo += "FSTP dword ptr[" + aux + "]\n"
            self.last_texto += "FSTP dword ptr[" + aux + "]\n"
            self.pilaOperandos.insert(0, aux)
            infoClase = InformacionClase(simbolo=aux, caracteristicas="aux",
                                         tipo="FLOAT", uso="auxiliar")
            self.data.setDatos(infoClase)
            declaracion = self.data.generar_declaracion_asm(infoClase.raw_simbolo, infoClase.tipo)
            self.data.declaraciones_asm.append(declaracion)
            self.numAux += 1

    def comparacion(self):
        #print(self.pilaOperandos)
        op1 = self.pilaOperandos.pop(0)
        op2 = self.pilaOperandos.pop(0)
        #ajustar texto
        if self.getTipo(op1) != self.getTipo(op2):
            self.codigo += "JMP LabelErrorTYPE\n"  # mejor seria escribir error en el archivo de errores
            self.last_texto = "JMP ErrorTYPE\n"
        else:
            tipo = self.getTipo(op1)
            if tipo == "FLOAT":
                self.codigo += "FLD " + op1 + "\n"
                self.last_texto = "FLD " + op1 + "\n"
                self.codigo += "FCOM " + op2 + "\n"
                self.last_texto = "FCOM " + op2 + "\n"
                if not self.registrosDisponibles[self.Registros.EAX]:
                    self.liberar(self.Registros.EAX, self.tipoRegistros[self.Registros.EAX])
                self.codigo += "FSTSW AX\n"
                self.last_texto = "FSTSW AX\n"
                self.codigo += "SAHF\n"
            else:
                regsitro = self.getRegistroInterno()
                if tipo == "ULONG":
                    self.codigo += "MOV " + str(regsitro) + "," + op2 + "\n"
                    self.last_texto = "MOV " + str(regsitro) + "," + op2 + "\n"
                    self.codigo += "CMP " + op1 + ", " + str(regsitro) + "\n"
                    self.last_texto = "CMP " + op1 + ", " + str(regsitro) + "\n"
                elif tipo == "INT":
                    regsitro = regsitro.split("E")[-1]
                    self.codigo += "MOV " + str(regsitro) + "," + op2 + "\n"
                    self.last_texto = "MOV " + str(regsitro) + "," + op2 + "\n"
                    self.codigo += "CMP " + op1 + ", " + str(regsitro) + "\n"
                    self.last_texto = "CMP " + op1 + ", " + str(regsitro) + "\n"
    def generarCodigoAssembler(self):
        while self.celdaActual <= len(self.tira):
            if self.celdaActual in self.tags:
                if self.tira[self.celdaActual] != "TAG" + str(self.celdaActual):
                    self.codigo += "TAG" + str(self.celdaActual) + ":\n"
                    self.last_texto = "TAG" + str(self.celdaActual) + ":\n"
            celda = self.tira[self.celdaActual]
            if str(celda).startswith("TAG"):
                self.codigo += celda + ":\n"
                self.last_texto = celda + ":\n"
            if celda in self.operadores or str(celda).startswith("FUNCION"):
                if celda == "+":
                    self.sumaOResta(celda)
                elif celda == "-":
                    self.sumaOResta(celda)
                elif celda == "*":
                    self.multODiv(celda)
                elif celda == "/":
                    self.multODiv(celda)
                elif celda == "BI":
                    operando = self.pilaOperandos.pop(0)
                    self.tags.insert(0,operando)
                    self.codigo += "JMP TAG" + str(operando) + "\n" if operando < len(self.tira) else "JMP FIN\n"
                    self.last_texto = "JMP TAG" + str(operando) + "\n" if operando < len(self.tira) else "JMP FIN\n"
                elif celda == "BF":
                    operando1 = self.pilaOperandos.pop(0)
                    if operando1 < len(self.tira):
                        self.tags.insert(0,operando1)
                        self.codigo += "TAG" + str(operando1) + "\n"
                        self.last_texto = "TAG" + str(operando1) + "\n"
                    else:
                        self.codigo += "FIN\n"
                        self.last_texto = "FIN\n"
                elif celda.startswith("FUNCION"):
                    self.codigoFunciones += "TAG" + str(self.celdaActual) + ":\n"
                    aux = self.data.functions.get(celda.split(" ")[-1]).nro_parametros
                    if self.data.functions.get(celda.split(" ")[-1]).nro_parametros == str(1):
                        for item in self.data.variablesPolaca.values():
                            if item.funcion_padre == self.data.functions.get(celda.split(" ")[-1]).raw_simbolo:
                                if item.tipo == "INT":
                                    self.codigoFunciones+= "MOV BX, [esp+4]\n"
                                    self.codigoFunciones+= "MOV " + item.raw_simbolo + ", BX\n"
                                else:
                                    self.codigoFunciones+= "MOV EBX, [esp+4]\n"
                                    self.codigoFunciones+= "MOV " + item.raw_simbolo + ", EBX\n"
                    funcion = CodeGenerator(self.polaca, self.celdaActual + 1, self.data, False,self.pilaOperandos,self.numAux)
                    tupla = funcion.generarCodigoAssembler()
                    self.numAux = funcion.numAux
                    self.codigoFunciones += tupla[0] + "\n"
                    self.celdaActual = tupla[1]
                    if len(tupla) == 5:
                        self.cadenas += tupla[-1]
                    self.pilaOperandos = tupla[2]
                    self.codigoFunciones += tupla[3]
                elif celda == "ret":
                    self.codigo += "ret\n"
                    self.last_texto += "ret\n"
                    return self.codigo, self.celdaActual,self.pilaOperandos,self.codigoFunciones,self.cadenas
                elif celda == "=":
                    operando1 = self.pilaOperandos.pop(0)
                    operando2 = self.pilaOperandos.pop(0)
                    if self.getTipo(operando1) != self.getTipo(operando2):
                        self.codigo += "JMP LabelErrorTYPE" + "\n"
                        self.last_texto = "JMP ErrorTYPE" + "\n"
                    else:
                        if self.getTipo(operando1) == "INT":
                            self.asignacionINT(operando1,operando2)
                        elif self.getTipo(operando1) == "FLOAT":
                            self.operacionFlotante(operando1, operando2, celda)
                        elif self.getTipo(operando1) == "ULONG":
                            self.asignacion32BIT(operando1,operando2)
                elif celda == "<":
                    self.comparacion()
                    self.codigo += "JGE "
                    self.last_texto = "JGE "
                elif celda == "<=":
                    self.comparacion()
                    self.codigo += "JG "
                    self.last_texto = "JG "
                elif celda == ">=":
                    self.comparacion()
                    self.codigo += "JL "
                    self.last_texto = "JL "
                elif celda == "==":
                    self.comparacion()
                    self.codigo += "JNE "
                    self.last_texto = "JNE "
                elif celda == "!!":
                    self.comparacion()
                    self.codigo += "JE "
                    self.last_texto = "JE "
                elif celda == ">":
                    self.comparacion()
                    self.codigo += "JLE "
                    self.last_texto = "JLE "
                elif celda == "CALLFUNC":
                    operando1 = self.pilaOperandos.pop(0)
                    self.codigo += "CALL TAG" + str(operando1) + "\n"
                    self.last_texto = "CALL TAG" + str(operando1) + "\n"
                elif celda == "CALLFUNCP":
                    operando1 = self.pilaOperandos.pop(0)
                    operando2 = self.pilaOperandos.pop(0)
                    registro = self.getRegistroExterno()
                    if self.getTipo(operando2) == "INT":
                        if registro == "EAX":
                            registro = "AX"
                        else:
                            registro = "DX"
                    self.codigo += "MOV " + registro + ", " + operando2 + "\n"
                    self.last_texto += "MOV " + registro + ", " + operando2 + "\n"
                    self.codigo += "PUSH " + registro + "\n"
                    self.last_texto += "PUSH " + registro + "\n"
                    self.codigo += "CALL TAG" + str(operando1) + "\n"
                    self.last_texto += "CALL TAG" + str(operando1) + "\n"
                elif celda == "PRINT":
                    cadena = self.pilaOperandos.pop(0)
                    cadena = str(cadena).removeprefix("%")
                    cadena = cadena.removesuffix("%")
                    self.cadenas += "cadena_" + str(self.celdaActual) + " db \"" + cadena + "\", 0\n"
                    self.codigo += "invoke MessageBox, NULL, addr cadena_" + str(self.celdaActual) + ", addr Imp, MB_OK\n"
                    self.last_texto = "invoke MessageBox, NULL, addr cadena_" + str(self.celdaActual) + ", addr Imp, MB_OK\n"
                elif celda.startswith("TAG"):
                    self.codigo += celda + "\n"
                    self.last_texto = celda + "\n"
            else:
                #print("else", celda)
                self.pilaOperandos.insert(0,celda)
            self.celdaActual += 1
        self.codigo += "JMP FIN\n"
        self.last_texto = "JMP FIN\n"
    def asignacionINT(self,operando1,operando2):
            # self.liberar(self.Registros.EAX, self.tipoRegistros[self.Registros.EAX])
            # print(operando1,operando2)
            self.codigo += "MOV AX, " + operando2 + "\n"
            self.last_texto = "MOV AX, " + operando2 + "\n"
            self.codigo += "MOV " + operando1 + ", AX \n"
            self.last_texto = "MOV " + operando1 + ", AX \n"
    def asignacion32BIT(self,operando1,operando2):
        self.codigo += "MOV EAX, " + operando2 + "\n"
        self.last_texto = "MOV EAX, " + operando2 + "\n"
        self.codigo += "MOV " + operando1 + ", EAX \n"
        self.last_texto = "MOV " + operando1 + ", EAX \n"
    def setHeader(self):
        self.header += "include \\masm32\\include\\masm32rt.inc\n"
        self.header += ".386\n"
        self.header += ".model flat\n"
        self.header += "option casemap :none\n"
        self.header += "include \\masm32\\include\\windows.inc\n"
        self.header += "include \\masm32\\include\\kernel32.inc\n"
        self.header += "include \\masm32\\include\\user32.inc\n"
        self.header += "includelib \\masm32\\lib\\kernel32.lib\n"
        self.header += "includelib \\masm32\\lib\\user32.lib\n"
        self.header += ".data\n"
        self.header += "Error db \"Error\", 0\n"
        self.header += "ErrorOvSF db \"Error: overflow en un suma entre flotantes\", 0\n"
        self.header += "ErrorOvPE db \"Error: overflow en una producto de enteros\", 0\n"
        self.header += "ErrorTYPE db \"Error: Error tipos incomatibles entre operadores\", 0\n"
        self.header += "ErrorDIV0 db \"Error: division por cero\", 0\n"
        self.header += "FINALIZO db \"FINALIZO EL PROGRAMA\", 0\n"
        self.header += "Salida dt ?, 0\n"
        self.header += "Imp db \"Salida por pantalla\", 0\n"
        self.header += "@mem2byte dd ? ; 32 bits\n"
        self.header += "MaxFLOAT dd 3.40282347E38 ; 32 bits \n"

    def setFooter(self):
        self.codigo += "LabelErrorOvSF:\n"
        self.codigo += "invoke MessageBox, NULL, addr ErrorOvSF, addr Error, MB_OK\n"
        self.codigo += "invoke ExitProcess, 0\n"
        self.codigo += "LabelErrorOvPE:\n"
        self.codigo += "invoke MessageBox, NULL, addr ErrorOvPE, addr Error, MB_OK\n"
        self.codigo += "invoke ExitProcess, 0\n"
        self.codigo += "LabelErrorDIV0:\n"
        self.codigo += "invoke MessageBox, NULL, addr ErrorDIV0, addr Error, MB_OK\n"
        self.codigo += "invoke ExitProcess, 0\n"
        self.codigo += "LabelErrorTYPE:\n"
        self.codigo += "invoke MessageBox, NULL, addr ErrorTYPE, addr Error, MB_OK\n"
        self.codigo += "invoke ExitProcess, 0\n"
        self.codigo += "FIN:\n"
        self.codigo += "invoke MessageBox, NULL, addr FINALIZO, addr Error, MB_OK\n"
        self.codigo += "invoke ExitProcess, 0\n"
        self.codigo += "end start"

    def imprimirCodigo(self):
        self.setHeader()
        self.generarCodigoAssembler()
        self.header += self.cadenas
        self.codigo_asm_data = "\n".join("\n" + linea for linea in self.data.getStruct()) + "\n" + "\n".join(self.declaracion_asm)
        self.codigo += self.codigoFunciones + "\n"
        self.setFooter()
        return self.header + "\n" + self.codigo_asm_data + "\n" + self.codigo + "\n"
