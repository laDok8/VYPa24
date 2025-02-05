# VYP compiler
Compiler for VYPa class.

Compiler translates from VYPlanguage into VYPcode. 
VYPlanguage is a simple programming language with basic support of object-oriented paradigm inspired in C language and Java.
VYPcode is intermediate code similar to assembly language.

Project site: https://www.fit.vut.cz/study/course/VYPa/public/project/

## Installation
To compile grammar and run the compiler we need antlr4
```bash
pip install -r requirements.txt
```

### Grammar generation
To generate grammar, run the following command:
```bash
antlr4 Vyp.g4 -o src/antlr_src
```

### Running the compiler
To run the compiler, run the following command:
```bash
python3 src/main.py src.vyplang
```

## Interpreter
To invoke the interpreter, run the following command:
```bash
java -jar vypint-1.0.jar src.vypcode < input > output
```
alternatively you can utilize shebang

## Disclaimer
This project is mostly functional, but due to time pressure it's due for a refactor.
Known issues:
- Variable shadowing
- code_gen is due for a refactor 

## Results
```
Lexical analysis (error detection): 73% (157/214)
Syntactical analysis (error detection): 88% (266/301)
Semantic analysis (error detection): 82% (248/300)
Basic code generation (no classes): 93% (373/401)
Code generation (objects and classes): 36% (182/500)
SHORTEVAL: 0% (0/150)
MINUS: 100% (100/100)
FOR: 0% (0/100)
IFONLY: 90% (90/100)
INITVAR: 0% (0/70)
OVERLOAD: 0% (0/200)
FLOAT: 0% (0/100)
VISIBILITY: 0% (0/100)
Total without extensions: 71% (1226/1716)
```
19.8/20
