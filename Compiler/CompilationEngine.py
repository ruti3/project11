import os, os.path, re, sys
import Compiler.JackTokenizer as tokenizer
import Compiler.JackGrammar as grammar
import Compiler.SymbolTable as symbol
import Compiler.VMWriter as vmwriter
from collections import deque

# This class does the compilation itself. It reads its input from a JackTokenizer
# and writes its output into a VMWriter. It is organized as a series of
# compilexxx() methods, where xxx is a syntactic element of the Jack language.
# The contract between these methods is that each compilexxx() method should
# read the syntactic construct xxx from the input, advance() the tokenizer
# exactly beyond xxx, and emit to the output VM code effecting the semantics
# of xxx.Thus compilexxx() may only be called if indeed xxx is the next
# syntactic element of the input.If xxx is a part of an expression and thus
# has a value, then the emitted code should compute this value and leave it
# at the top of the VM stack.

#TODO : understand how different from last compiler


NEW_LINE = "\n"


class CompilationEngine(object):
    def __init__(self, input_file, output_file):
        """
        Creates a new compilation engine with the
        given input and output. The next routine
        called must be compileClass().
        :param input_file:
        """
        self.tokenizer = tokenizer.JackTokenizer(input_file, output_file)
        self.symbol_table = symbol.SymbolTable()
        self.vm = vmwriter.VMwriter()
        self.input = input_file  # already open :)
        self.output = output_file  # already open :)
        self.class_name = "" # current class name
        self.current_subroutine_type = 0
        self.current_subroutine_name = ""
        self.type_list = [grammar.K_INT, grammar.K_CHAR, grammar.K_BOOLEAN]
        self.label_counter = 0
        self.if_counter = 0
        self.while_counter = 0
        self.tokenizer.advance()
        self.symbol_tables = []
        self.compile_class()


    def compile_class(self):
        """
        HADAR
        RUTHI

        Compiles a complete class.
        :return:
        """
        if self.tokenizer.current_value != grammar.K_CLASS:
            raise ValueError("No class found in the file")


        #class name
        self.tokenizer.advance()
        # add class type to list of types
        self.type_list.append(self.tokenizer.current_value)
        self.compile_identifier()

        # Create new symbol table
        self.symbol_tables.append(symbol.SymbolTable)

        # {
        self.tokenizer.advance()
        self.checkSymbol("{")

        # classVarDec*
        self.tokenizer.advance()
        if self.tokenizer.current_value in [grammar.K_STATIC, grammar.K_FIELD]:
            while(self.compile_class_var_dec(False)):
                self.tokenizer.advance()

        # subroutineDec*

        if self.tokenizer.current_value in [grammar.K_CONSTRUCTOR,
                                            grammar.K_FUNCTION, grammar.K_METHOD]:
            while(self.compile_subroutine(False)):
                self.tokenizer.advance()

        # }
        self.checkSymbol("}")

        # TODO delete SymbolTable
        self.symbol_tables.pop()


    def compile_class_var_dec(self, raise_error=True):
        """
        HADAR

        ט
        Compiles a static declaration or a field
        declaration.
        :return:
        """
        # Check if there is a classVarDec
        # 'static' or 'field'
        if self.tokenizer.current_value in [grammar.K_STATIC, grammar.K_FIELD]:
            kind = grammar.keyword_2_kind[self.tokenizer.current_value]
        else:
            if raise_error:
                raise ValueError("No 'static' or 'field' found")
            else:
                return False

        self.compile_declaration(kind)


    def compile_subroutine_var_dec(self, raise_error=True):
        """
        HADAR

        :param raise_error:
        :return:
        """
        # 'var'
        if self.tokenizer.current_value == grammar.K_VAR:
            kind = grammar.keyword_2_kind[self.tokenizer.current_value]
        else:
            if raise_error:
                raise ValueError("No 'var' found")
            else:
                return False

        self.compile_declaration(kind)



    def compile_declaration(self, kind):
        """
        HADAR

        :param kind:
        :return:
        """

        #type
        self.tokenizer.advance()
        type = self.compile_type()

        # varName
        self.tokenizer.advance()
        name = self.compile_identifier()

        # add to symbol table
        self.symbol_table.define(name, type, kind) # TODO
        self.symbol_tables[self.last_pos()].define(name, type, kind)


        # (',' varName)*
        more_vars = True
        self.multiple_varNames(more_vars, type, kind)

        # ;
        self.tokenizer.advance()
        self.checkSymbol(";")



    def multiple_varNames(self, more_vars, current_type, kind):
        """
        HADAR

        Compiles all the variables (if there are).
        It is used to represent (',' varName)*

        :param more_vars: more_vars True if there are more varriables, false otherwise
        :param current_type: last var type
        :return:
        """
        #TODO : check if 2 different kinds can be in the same line
        while (more_vars):
            # ','
            if self.tokenizer.get_next()[0] == ",":

                self.tokenizer.advance() # ,

                # type (if applicable)
                if self.tokenizer.get_next()[0] in self.type_list: #new type

                    self.tokenizer.advance()
                    type = self.compile_type(False)
                else:
                    type = current_type

                # varName
                self.tokenizer.advance()
                name = self.compile_identifier()

                # add to symbol table
                self.symbol_table.define(name, type, kind)
                self.symbol_tables[self.last_pos()].define(name, type, kind)

            else:
                more_vars = False



    def compile_type(self, raise_error=True):
        """
        HADAR

        checks that current_value in type list
        :return: type
        """
        if self.tokenizer.current_value in self.type_list:
            return self.tokenizer.current_value
        else:
            if raise_error:
                raise ValueError("No type found")
            else:
                return False



    def compile_expression_list2(self): # TODO I did it in compile_term. Check if something is missing
        """
        Compiles a (possibly empty) comma separated list of expressions.

        ALGORITHM 4: A recursive postfix traversal algorithm for evaluating
        an expression tree by generating commands in a stack-based language.
        Code(exp):
        if exp is a number n then output “push n”
        if exp is a variable v then output “push v”
        if exp = (exp1 op exp2) then Code(exp1); Code(exp2) ; output “op”
        if exp = op(exp1) then Code(exp1) ; output “op”
        if exp = f(exp1 … expN) then Code(exp1) … Code(expN); output “call f”

        :return:
        """



    def compile_identifier(self,raise_error=True):
        """
        checks that current_type is identifier
        :return: current_value
        """
        if self.tokenizer.current_token_type == grammar.IDENTIFIER:
            return self.tokenizer.current_value
        else:
            if raise_error:
                raise ValueError("No identifier found")
            else:
                return False




    def compile_subroutine(self, raise_error=True):
        """
        Compiles a complete method, function, or constructor.

        -A Jack subroutine xxx() in a Jack class Yyy is compiled into a VM
        function called Yyy.xxx.
        - A Jack function or constructor with k arguments is compiled into a
         VM function with k arguments.
        -A Jack method with k arguments is compiled into a VM function with k+1 arguments.
        The first argument (argument number 0) always refers to the this object.
        :return:
        """
        if self.is_subroutine():
            self.current_subroutine_type = self.tokenizer.current_value
        else:
            if raise_error:
                raise ValueError("No keyword found in subroutine")
            else:
                return False

        # void or type
        self.tokenizer.advance()
        type = self.tokenizer.current_value
        if self.current_is_void_or_type():
            return_type = self.tokenizer.current_value
        else:
            if raise_error:
                raise ValueError("No keyword found in subroutine")
            return False

        # subroutine name
        self.tokenizer.advance()
        if self.tokenizer.current_token_type == grammar.IDENTIFIER:
            self.current_subroutine_name = self.tokenizer.current_value
        else:
            if raise_error:
                raise ValueError("No keyword found in subroutine")
            return False

        #open symbol table

        self.symbol_table.start_subroutine() # TODO
        # create new symbol table
        self.symbol_tables.append(symbol.SymbolTable)

        if self.current_subroutine_type == grammar.K_METHOD:
            self.symbol_table.define('this', self.class_name, grammar.K_ARG) # TODO
            self.symbol_tables[self.last_pos()].define('this', self.class_name, grammar.K_ARG)

        # (
        self.tokenizer.advance()
        self.checkSymbol("(")

        # parameterList
        self.tokenizer.advance()
        if self.compile_parameter_list() is not False:
            self.tokenizer.advance()
        else:
            if raise_error:
                raise ValueError("illegal parameter list in subroutine")
            return False

        # )
        self.checkSymbol(")")

        # subroutine body
        self.tokenizer.advance()

        # TODO delete symbolTable
        self.symbol_tables.pop()


    def compile_subroutineBody(self):
        """
        HADAR

        compiles subroutines body
        :return:
        """
        # {
        self.checkSymbol("{")

        # varDecs*
        self.tokenizer.advance()
        more_vars = True
        while (more_vars):
            if self.compile_subroutine_var_dec(False) is False:
                break
            self.tokenizer.advance()

            if self.tokenizer.current_value != "var":
                more_vars = False

        # write function to vm file
        self.write_to_vm_function_dec()

        # statements
        self.compile_statements()

        # }
        self.checkSymbol("}")



    def get_vm_function_name(self):
        """
        HADAR
        A Jack subroutine xxx() in a Jack class Yyy is compiled into a VM
        function called Yyy.xxx.

        :return: vm function name
        """
        return self.class_name+'.'+self.current_subroutine_name



    def write_to_vm_function_dec(self):
        """
        HADAR

        writes "function function_name num_of_vars"
        for example : "function BankAccount.commission 0 "

        loads this pointer according to subroutine type

        :return:
        """

        # TODO symbol table needs to be fixed ?
        self.vm.writeFunction(self.get_vm_function_name(),
                              self.symbol_table.varCount(grammar.K_VAR))

        if self.current_subroutine_type == grammar.K_METHOD:
            self.vm.writePush(grammar.K_ARG, 0) # push argument 0
            self.vm.writePop(grammar.POINTER, 0) # pop pointer 0
        elif self.current_subroutine_type == grammar.K_CONSTRUCTOR:
            # push size of object
            self.vm.writePush(grammar.CONST, self.symbol_table.varCount(grammar.field))
            # call Memory.alloc 1
            self.vm.writeCall('Memory.alloc', 1)
            # pop pointer 0
            self.vm.writePop(grammar.POINTER, 0)



    def compile_statements(self):
        """
        HADAR

        Compiles a sequence of statements, not
        including the enclosing {}.
        :return:
        """
        more_statements = True
        # (statement)*
        while (more_statements):
            # TODO :ask ruthi about there lines
            if self.tokenizer.current_value == "/":
                self.tokenizer.advance()
                self.output.write(self.tokenizer.get_next()[0])

            if self.tokenizer.current_value == "if":
                self.compile_if()
                self.tokenizer.advance()

            elif self.tokenizer.current_value == "let":
                self.compile_let()
                self.tokenizer.advance()

            elif self.tokenizer.current_value == "while":
                self.compile_while()
                self.tokenizer.advance()

            elif self.tokenizer.current_value == "do":
                self.compile_do()
                self.tokenizer.advance()

            elif self.tokenizer.current_value == "return":
                self.compile_return()
                self.tokenizer.advance()
            else:
                more_statements = False




    def get_new_label(self):
        """
        HADAR
        :return: 'Ln' n=counter
        """
        self.label_counter += 1
        return 'L'+str(self.label_counter)

    def current_is_void_or_type(self):

        """
        HADAR

        :return: true if void or type, false otherwise
        """
        return (self.tokenizer.current_value == grammar.K_VOID) or self.tokenizer.current_value in self.type_list



    def is_subroutine(self):
        """
        HADAR

        :return: true if current value is subroutine initial
        """

        return self.tokenizer.current_value in [grammar.K_CONSTRUCTOR, grammar.K_FUNCTION, grammar.K_METHOD]



    def compile_parameter_list(self):
        """
        HADAR

        Compiles a (possibly empty) parameter list,
        not including the enclosing ().

        :return:
        """
        more_parameters = True
        while more_parameters:
            if self.is_type():
                type = self.tokenizer.current_value
                self.tokenizer.advance()
                if self.tokenizer.current_token_type == grammar.IDENTIFIER:
                    name = self.tokenizer.current_value
                    #add to symbol table
                    self.symbol_table.define(name, type, grammar.K_ARG) # TODO
                    self.symbol_tables[self.last_pos()].define(name, type, grammar.K_ARG)
                    self.tokenizer.advance()

                    if self.tokenizer.current_value == ',':
                        self.tokenizer.advance()
                    elif self.tokenizer.current_value == ')':
                        more_parameters = False

            else:
                return False

        return True


    def is_type(self):
        """ Checks if the type of the current type is in the type_list
        """

        return (self.tokenizer.current_value in self.type_list)



    def compile_statements(self):
        """
        Compiles a sequence of statements, not
        including the enclosing {}.
        :return:
        """

    def checkSymbol(self, symbol, raise_error=True):
        """ Check if the symbol is in the current value"""
        if self.tokenizer.current_value == symbol:
            return True
        else:
            if raise_error:
                raise ValueError("No symbol " + symbol + " found")

    def compile_if(self):
        """
        RUTHI

        Compiles an if statement, possibly with a trailing else clause.
        :return:
        """
        self.if_counter += 1

        # (
        self.tokenizer.advance()
        self.checkSymbol("(")

        # expression
        self.tokenizer.advance()
        self.compile_expression(True, True)

        self.vm.WriteArithmetic('neg')
        self.vm.WriteIf("L_" + self.if_counter.__str__() + "_1")

        # )
        self.tokenizer.advance()
        self.checkSymbol(")")

        # {
        self.tokenizer.advance()
        self.checkSymbol("{")

        # statements
        self.tokenizer.advance()
        self.compile_statements()

        self.vm.WriteGoto("L_" + self.if_counter.__str__() + "_2")
        self.vm.WriteLabel("L_" + self.if_counter.__str__() + "_1")

        # }
        self.checkSymbol("}")

        # (else {statement})?
        else_param = False

        if self.tokenizer.get_next()[0] == "else":
            self.tokenizer.advance()
            if self.tokenizer.current_value == "else":
                else_param = True
        if (else_param):
            # {
            self.tokenizer.advance()
            self.checkSymbol("{")

            # statement
            self.tokenizer.advance()
            self.compile_statements()

            # }
            self.checkSymbol("}")

            self.vm.WriteLabel("L_" + self.if_counter.__str__() + "_2")

    def compile_while(self):
        """
        RUTHI

        Compiles a while statement.
        :return:
        """
        self.while_counter += 1

        # (
        self.tokenizer.advance()
        self.checkSymbol("(")
        # expression
        self.tokenizer.advance()

        self.vm.WriteLabel("L_" + self.while_counter.__str__() + "_1")
        self.compile_expression()
        self.vm.WriteArithmetic('neg')
        self.vm.WriteIf("L_" + self.while_counter.__str__() + "_2")

        # )
        self.tokenizer.advance()
        self.checkSymbol(")")

        # {
        self.tokenizer.advance()
        self.checkSymbol("{")

        # statement
        self.tokenizer.advance()
        self.compile_statements()

        self.vm.WriteGoto("L_" + self.while_counter.__str__() + "_1")
        self.vm.WriteLabel("L_" + self.while_counter.__str__() + "_2")

        # }
        self.checkSymbol("}")


    def compile_let(self):
        """
        RUTHI

        Compiles a let statement.
        """

        # varName
        self.tokenizer.advance()
        varName = self.compile_identifier()

        # get varName from SymbolTable
        position = self.last_pos()
        while self.symbol_tables[position].indexOf(varName) == symbol.NO_INDEX:
            position -= 1
        varName_index = self.symbol_tables[position].indexOf(varName)

        # [
        advance_token = False
        self.tokenizer.advance()
        check_expression = False
        if self.checkSymbol("[", False):
            check_expression = True
        if check_expression:
            # expression
            self.tokenizer.advance()
            self.compile_expression(True, True)
            # ]
            self.tokenizer.advance()
            self.checkSymbol("]")
            advance_token = True

        # =
        if (advance_token):
            self.tokenizer.advance()
        self.checkSymbol("=")

        # expression
        self.tokenizer.advance()
        self.compile_expression(True, True)

        # ;
        self.tokenizer.advance()
        self.checkSymbol(";")

        # push varName
        segment = self.symbol_tables[position].kindOf(varName)
        self.vm.writePop(segment, varName_index)

    def compile_term(self, tags=True, check=False):
        """
        Compiles a term. This routine is faced with a slight difficulty when
        trying to decide between some of the alternative parsing rules.
        Specifically, if the current token is an identifier, the routine must
        distinguish between a variable, an array entry, and a subroutine call.
        A single look-ahead token, which may be one of [, (, or .
        suffices to distinguish between the three possibilities.
        Any other token is not part of this term and should not be advanced
        over.
        :return:
        """

        # Integer constant, String constant, keyword constant
        type = self.tokenizer.token_type()
        if (type == grammar.INT_CONST):
            if check:
                return True
            self.vm.writePush(grammar.CONST, "")
        elif (type == grammar.KEYWORD and self.tokenizer.keyword() in grammar.keyword_constant):
            if check:
                return True # TODO what are we suppose to return here?
        elif type == grammar.STRING_CONS:
            if check:
                return True
                # TODO what are we suppose to return here?
        # ( expression )
        elif self.tokenizer.current_value == "(":
            if check:
                return True
            self.checkSymbol("(")
            self.tokenizer.advance()
            self.compile_expression(True, True)
            self.tokenizer.advance()
            self.checkSymbol(")")

        # unaryOp term
        elif self.tokenizer.current_value in grammar.unaryOp:
            if check:
                return True
            op = self.tokenizer.current_value
            self.checkSymbol(self.tokenizer.current_value)
            self.tokenizer.advance()
            self.compile_term()
            # op
            self.vm.output_file.write(op)

        # varName ([ expression ])?
        elif type == grammar.IDENTIFIER:
            if check:
                return True
            # push varName
            self.vm.writePush(self.tokenizer.current_value, "")

            if self.tokenizer.get_next()[0] == "[":
                self.compile_identifier()
                self.tokenizer.advance()

                if self.checkSymbol("[", False):
                    self.tokenizer.advance()
                    self.compile_expression()
                    self.tokenizer.advance()
                    self.checkSymbol("]")
            elif (self.tokenizer.get_next()[0] == "(") or (self.tokenizer.get_next()[0] == "."):
                # subroutineCall
                self.subroutineCall()

        else:
            return False

        return True

    def compile_expression(self, tags=True, term_tag=False, expression_lst=False):
        """
        RUTHI

        Compiles an expression.
        :return:
        """
        expression_counter = 0

        # term
        if self.compile_term(False, True) is False:
            return False
        else:
            if expression_lst:
                return True
            self.compile_term()

        # (op term)*
        while self.tokenizer.get_next()[0] in grammar.operators:
            self.tokenizer.advance()
            self.checkSymbol(self.tokenizer.current_value)
            self.tokenizer.advance()
            self.compile_term()

        return expression_counter

    def compile_expression_list(self):
        """
        Compiles a (possibly empty) comma separated list of expressions.
        :return:
        """

        # expression?
        if self.compile_expression(False, False, True) is not False:
            # (',' expression)*
            self.compile_expression(True, True)
            self.tokenizer.advance()
            while self.tokenizer.current_value == ',':
                self.checkSymbol(",")
                # expression
                self.tokenizer.advance()
                self.compile_expression(True, True)
                self.tokenizer.advance()


    def last_pos(self):
        """
        RUTHI

        :return: position of the last symbol table in the array
        """
        return len(self.symbol_tables) - 1

    def compile_do(self):
        """
        RUTHI

        Compiles a do statement
        :return:
        """

        # subroutineCall
        self.tokenizer.advance()
        self.subroutineCall()

        # ;
        self.tokenizer.advance()
        self.checkSymbol(";")


    def compile_return(self):
        """
        RUTHI

        Compiles a return statement.
        :return:
        """

        # expression?
        if self.tokenizer.get_next()[0] != ";":
            self.tokenizer.advance()
            self.compile_expression()
            self.tokenizer.advance()
            self.checkSymbol(";")
        else:
            # ;
            self.tokenizer.advance()
            self.checkSymbol(";")

        # TODO don't forget abt return 0

