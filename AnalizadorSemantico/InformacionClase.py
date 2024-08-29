import ast


class InformacionClase:
    def __init__(self, simbolo, caracteristicas, uso=None, referencias=None, ambito_de_clase=None, propiedades=None, miembros_de_clase=None, numero_de_herencias=None, clase_herencia=None, tipo=None, tipoparametro=None, nroparametros=None, valor = None, propiedades_heredadas = None, funcion_padre = None,miembros = None):
        self.raw_simbolo = simbolo.replace(":", "_")
        self.simbolo = self.extraer_simbolo(simbolo)
        self.caracteristicas = caracteristicas
        self.uso = uso
        self.tipo = uso if uso == "funcion" else tipo
        self.procesar_caracteristicas()
        self.referencias = referencias
        self.ultimo_ambito = None
        self.procesar_ambito(ambito_de_clase)
        if self.ultimo_ambito is None:
            self.procesar_ambito(simbolo)
        self.propiedades = self.convertir_a_lista(propiedades) if propiedades is not None else None
        self.miembros = self.convertir_a_lista(miembros) if miembros is not None else None
        self.num_herencias = numero_de_herencias
        self.clase_herencia = self.extraer_simbolo(clase_herencia) if clase_herencia is not None else None
        self.tipo_parametro = tipoparametro
        self.nro_parametros = nroparametros
        self.valor = valor
        self.propiedades_heredadas = self.convertir_a_lista(propiedades_heredadas) if propiedades_heredadas is not None else None

        self.funcion_padre = funcion_padre.replace(":","_") if funcion_padre is not None else None
    def convertir_a_lista(self,cadena):
        try:
            lista = ast.literal_eval(cadena)
            if isinstance(lista, list):
                return lista
            else:
                raise ValueError("La cadena no representa una lista válida.")
        except (SyntaxError, ValueError) as e:
            print(f"Error al convertir la cadena a lista: {e}")
            return None

    def procesar_caracteristicas(self):
        if self.caracteristicas:
            key_value = self.caracteristicas.split(":")
            if len(key_value) == 2:
                key = key_value[0].strip().lower()
                value = key_value[1].strip()
                if key == "tipo":
                    self.tipo = value
                elif key == "uso":
                    self.uso = value
                elif key == "tipoparametro":
                    self.tipo_parametro_caracteristicas = value
                elif key == "nroparametros":
                    self.nro_parametros_caracteristicas = value
    def setAmbito(self,ambito):
        self.ultimo_ambito = ambito
    def extraer_simbolo(self,cadena):
        partes = cadena.split(":")
        return partes[0]
    def procesar_ambito(self, ambito):
        if ambito:
            ambito_parts = ambito.split(":")
            self.ultimo_ambito = ambito_parts[-1].strip()

    def __str__(self):
        return (
            f"raw_Simbolo: {self.raw_simbolo}\n"
            f"Simbolo: {self.simbolo}\n"
            f"Caracteristicas: {self.caracteristicas}\n"
            f"Uso: {self.uso}\n"
            f"Referencias: {self.referencias}\n"
            f"Ambito de clase: {self.ultimo_ambito}\n"
            f"Propiedades: {self.propiedades}\n"
            f"Miembros de clase: {self.miembros}\n"
            f"Numero de herencias: {self.num_herencias}\n"
            f"Clase herencia: {self.clase_herencia}\n"
            f"Tipo: {self.tipo}\n"
            f"Tipo Parametro: {self.tipo_parametro}\n"
            f"Nro Parametros: {self.nro_parametros}\n"
            f"Propiedades Heredadas: {self.propiedades_heredadas}\n"
        )