/*
    to generate parser run:
    antlr4 Vyp.g4 -o src/antlr_src
*/
grammar Vyp;
options {
    language = Python3;
}

program: (function_def | class_def)+;

function_def: ret_type ID '(' f_param_list ')' code_block;
var_type: INT | STRING | ID;
ret_type: var_type | VOID;
f_param_list: (param (',' param)*|VOID) ;
f_call_list: (expr (',' expr)*)? ;
param: var_type ID;
code_block
    : '{' statement* '}'
    | '{' code_block '}';

statement
    : declaration ';'
    | var_assign ';'
    | instance_assign ';'
    | expr ';'
    | ret_stmt ';'
    | if_else_stmt
    | while_stmt
    | ';';

declaration: var_type ID (',' ID)*;
var_assign: ID '=' expr;
instance_assign: instance_expr '=' expr;
ret_stmt: 'return' expr?;
if_else_stmt: 'if' '(' expr ')' code_block 'else' code_block;
while_stmt: 'while' '(' expr ')' code_block;

expr
    : '(' var_type ')' expr #cast_expr
    | '(' expr ')' #brace_expr
    | '!' expr  #not_expr
    | expr op=('*' | '/') expr #mul_div_expr
    | expr op=('+' | '-') expr #add_sub_expr
    | expr op=('<' | '>' | '<=' | '>=') expr #rel_expr
    | expr op=('==' | '!=') expr #eq_expr
    | expr op='&&' expr #and_expr
    | expr op='||' expr #or_expr
    | fun_call #fun_call_expr
    | instance_creation #instance_creation_expr
    | literal_val #literal_expr
    | instance_expr #invocation_expr
    | ID #id_expr;

fun_call: ID '(' f_call_list ')';
instance_creation: NEW ID ('(' f_call_list ')')?;

literal_val: INT_LIT | STRING_LIT;

first_instance_ref: ref=(SUPER | THIS | ID) | fun_call;
instance_expr: first_instance_ref '.' nested_invocation;
nested_invocation: (fun_call | ID) ('.' nested_invocation)?;

class_def: CLASS ID ':' ID '{' (class_member)* '}';
class_member
    : declaration ';'
    | function_def;

CLASS: 'class';
NEW: 'new';
INT: 'int';
VOID: 'void';
STRING: 'string';
MULT: '*';
DIV: '/';
ADD: '+';
SUB: '-';
SUPER:'super';
THIS:'this';
ID: [a-zA-Z_][a-zA-Z_0-9]*;
INT_LIT: '0'|[1-9][0-9]*;
STRING_LIT: '"' ( '\\' [nt\\"] | '\\x' [0-9a-fA-F]{6} | ~[\r\n"\\] )* '"';

//trashing
WS: [ \t\r\n]+ -> skip;
LINE_COMMENT: '//' ~[\r\n]* -> skip;
BLOCK_COMMENT: '/*' .*? '*/' -> skip;
