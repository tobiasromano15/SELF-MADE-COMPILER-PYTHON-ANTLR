Part 1: Overview
This report outlines the design and implementation of a compiler based on the assigned topics. It covers the structure and functionality of the lexical and syntactic analyzers, including additional components used to generate the output.

Assigned Topics (Part 1)
16-bit integers and 32-bit unsigned long integers.
32-bit floating-point numbers.
Arithmetic operator --.
WHILE and DO.
Composition inheritance with named usage.
Method declaration concentration (next stage).
Forward declaration.
Attribute overriding (next stage).
Variable usage checks (next stage).
No conversions.
Single-line comments.
Multi-line strings.
Design and Implementation Decisions
The compiler was developed in Python 3, with the lexical and syntactic analyzers divided into modules. The input program file path is provided via the command line, and output files (output.txt, errors.txt, and symbol_table.txt) are generated in the same directory. The transition to using ANTLR4 from PLY was necessary due to complications with grammar integration, leading to significant adaptation challenges.

Key Components
Lexical Analyzer: Reads character by character, executing semantic actions and generating tokens based on state transitions.
Syntactic Analyzer: ANTLR4 was adapted to work with a custom lexer, with the creation of intermediary modules for token transformation and error handling.
Part 2: Intermediate Code Generation and Assembler
In Part 2, we continued the project by adding semantic checks and generating MASM32 assembler code. The intermediate code was generated using reverse Polish notation, allowing us to manage branching, arithmetic operations, and runtime error handling.

Assigned Topics (Part 2)
Inheritance by composition with method declaration control.
Forward declaration.
Attribute overriding.
Variable usage checks.
Runtime error controls (e.g., division by zero, overflow).
Key Components (Part 2)
Intermediate Code Generation: Implemented with reverse Polish notation and handled by a custom class structure.
Assembler Code Generation: Focused on translating the intermediate code to MASM32, handling operations such as arithmetic, branching, and function calls.
Runtime Error Controls
Errors such as division by zero, floating-point overflow, and unassigned variables are handled during code generation, ensuring robust error checking at runtime.

Conclusion
This project provided significant insights into the challenges of compiler design, particularly in adapting tools like ANTLR4 for Python and generating assembler code. The experience has been invaluable, highlighting both the complexities and rewards of low-level programming and compiler construction.

1- Ejecutar GUI.exe
2- Seleccionar archivo con codigo fuente en la carpeta Pruebas.

------ CASO QUE NO FUNCIONE ------

Version de python 3.10 - 3.11

1) pip install -r requirements.txt
2) python .\main.py .\programa.txt


El Parser de ANTLR4 genera los siguientes archivos:
gramaticaprueba.interp - gramaticaprueba.tokens - gramaticaprueba.py

