class PilaReferencias:
    def __init__(self):
        self.pila = []

    def push(self, referencia):
        self.pila.append(referencia)

    def pop(self):
        if self.pila:
            return self.pila.pop()
        return None

class ExpresionPolacaInversa:
    def __init__(self):
        self.expresion = []
        self.referencias = {}
        self.reference_counter = 1
        self.pila_referencias = PilaReferencias()

    def addElemento(self, elemento):
        # Agregar un operando a la pila
        self.expresion.append((elemento.replace(":","_") if elemento != None and not isinstance(elemento, (int, float)) else elemento, self.reference_counter))
        # Asociar el elemento con un número de referencia

        self.referencias[self.reference_counter] = elemento.replace(":","_") if elemento != None and not isinstance(elemento, (int, float)) else elemento

        self.reference_counter += 1
    def setElemento(self,number):
        self.referencias[number] = self.reference_counter

    def addPendingStep(self, referencia):
        self.pila_referencias.push(referencia)
    def getLastPendingStep(self):
        return self.pila_referencias.pop()

    def getAllOperando(self):
        return self.expresion.copy()

    def getOperandoRef(self, referencia):
        print(referencia)
        if ":" in referencia:
            print(referencia)
            referencia = referencia.replace(":","_")
        for elem, ref in self.expresion:
            if ref == referencia:
                return elem
        return None

    def getReferenciaOp(self, elemento):
        if ":" in elemento:
            print(elemento)
            elemento = elemento.replace(":","_")

        for elem, ref in self.expresion:
            if elem == elemento:
                return ref
        return None
    def getAmbitoOp(self,elem,ref):
        op = self.referencias[ref]

    def removeLast(self):
        aux = self.referencias.pop(self.reference_counter-1)
        self.reference_counter -= 1
        return aux
