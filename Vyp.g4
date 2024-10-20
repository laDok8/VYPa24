/*
    to generate parser run:
    antlr4 Vyp.g4 -Dlanguage=Python3 -o src/antlr_src
*/

grammar Vyp;

program: (function_def | class_def)+;

function_def: data_type ID param_list code_block;
data_type: INT | VOID | STRING | ID;
param_list: '(' (param (',' param)*)? ')';
param: (data_type ID| VOID);
code_block: '{' (statement)* '}';

statement: (declaration | assignment | expr ';' | ret_stmt | if_else_stmt | while_stmt );

declaration: data_type ID (',' ID)* ';';
assignment: ID '=' expr ';';
ret_stmt: 'return' expr? ';';
if_else_stmt: 'if' '(' expr ')' code_block 'else' code_block;
while_stmt: 'while' '(' expr ')' code_block;

expr
    : '(' data_type ')' expr // type cast
    | '(' expr ')' // parentheses
    | '!' expr
    | expr ('*' | '/') expr
    | expr ('+' | '-') expr
    | expr ('<' | '>' | '<=' | '>=') expr
    | expr ('==' | '!=') expr
    | expr '&&' expr
    | expr '||' expr
    | fun_call
    | instance_creation
    | literal_val
    | ID;

fun_call: ID fun_call_head;
instance_creation: NEW ID fun_call_head;

fun_call_head: '(' expr (',' expr)* ')';

literal_val: INT_LIT | STRING_LIT;

class_def: CLASS ID ':' ID '{' (class_member)* '}';
class_member
    : data_type ID ('=' expr)? ';'
    | function_def;

CLASS: 'class';
NEW: 'new';
INT: 'int';
VOID: 'void';
STRING: 'string';
ID: [a-zA-Z_][a-zA-Z_0-9]*;
INT_LIT: [1-9][0-9]*;
STRING_LIT: '"' (~[\r\n"] | '""')* '"';

//trashing
WS: [ \t\r\n]+ -> skip;
LINE_COMMENT: '//' ~[\r\n]* -> skip;
BLOCK_COMMENT: '/*' .*? '*/' -> skip;
