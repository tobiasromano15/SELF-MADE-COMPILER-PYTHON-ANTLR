class TablaDeSimbolos:
    def __init__(self, archivo_tabla):
        self.simbolos = {}
        self.archivo_tabla = archivo_tabla

    def addSimbolo(self, lexema):
        if lexema not in self.simbolos:
            self.simbolos[lexema] = {"referencias": 1}
        else:
            self.simbolos[lexema]["referencias"] = self.simbolos[lexema]["referencias"] + 1

    def addCaracteristica(self, lexema, caracteristica, valor):
        if lexema not in self.simbolos.keys():
            self.simbolos[lexema] = {caracteristica: valor, "referencias": 1}
        else:
            self.simbolos[lexema][caracteristica] = valor

    def aumentarReferencia(self, lexema):
        if lexema in self.simbolos.keys():
            self.simbolos[lexema]["referencias"] = self.simbolos[lexema]["referencias"] + 1
        else:
            self.simbolos[lexema] = {"referencias": 1}

    def reducirReferencia(self, lexema):
        if lexema in self.simbolos.keys():
            self.simbolos[lexema]["referencias"] = self.simbolos[lexema]["referencias"] - 1

    def getSimbolo(self, lexema):
        return self.simbolos.get(lexema)  # retorna el mapa de caracteristicas de ese simbolo

    def getCaracteristica(self, lexema, caracteristica):
        if lexema in self.simbolos.keys():
            if caracteristica in self.simbolos[lexema]:
                return self.simbolos[lexema][caracteristica]
            else:
                return str("ERROR: no existe columna " + caracteristica + " en el simbolo " + lexema)
        else:
            return str("ERROR: no existe el simbolo: " + lexema)

    def removerSimbolo(self, lexema):
        del self.simbolos[lexema]

    def isKey(self, lexema):
        return lexema in self.simbolos

    def keys(self):
        return self.simbolos.keys()

    def remove(self, key):
        self.simbolos.pop(key)

    def imprimirTabla(self):
        for key1, value1 in self.simbolos.items():
            self.archivo_tabla.write(str("Simbolo: {} - Caracteristicas: ").format(key1))
            for key2, value2 in value1.items():
                self.archivo_tabla.write(str("{}: {} - ").format(key2, value2))
            self.archivo_tabla.write(str("\n"))
