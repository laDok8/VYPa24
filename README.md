## VYP compiler
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

# Interpreter
To invoke the interpreter, run the following command:
```bash
java -jar vypint-1.0.jar src.vypcode < input > output
```
# Test automation
To test valid and invalid test cases run the all_test_run.sh bash script
sudo ./all_test_run.sh