import AnalizadorLexico.Lexico as lexico
from AnalizadorSintactico.Sintactico import Sintactico
def main_function(filepath):
    with open(filepath, 'r') as file:
        contenido_str = file.read()
        archivo_salida = open("salida.txt", "w")
        archivo_errores = open("errores.txt", "w")

    sintactico = Sintactico(contenido_str, archivo_errores, archivo_salida)
    sintactico.start()
    archivo_salida.close()
    archivo_errores.close()

    print("Generacion de token finalizada")
    print(sintactico)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        main_function(filepath)
