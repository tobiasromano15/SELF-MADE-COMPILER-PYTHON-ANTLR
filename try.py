import AnalizadorSemantico.PolacaInversa as Polaca
from AnalizadorSemantico.GeneradorAssembler import DataGenerator

p = Polaca.ExpresionPolacaInversa()


ruta_archivo = "tabla_de_simbolos.txt"
data = DataGenerator()
declaracion_asm = data.procesar_archivo(ruta_archivo)


# Unir las declaraciones para formar la sección .data del código Assembler
codigo_asm_data = ".data\n" + "\n".join("\n" + linea for linea in data.getStruct()) + "\n" +  "\n".join(declaracion_asm)

espacios_indentacion = 4

nombre_archivo = "programa.asm"
with open(nombre_archivo, "w") as archivo:
    archivo.write(codigo_asm_data)
#print(codigo_asm_data)
print(data.variablesPolaca)
#print(data.classes)