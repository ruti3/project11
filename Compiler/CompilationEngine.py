import os, os.path, re, sys
import Compiler.JackTokenizer as tokenizer
import Compiler.JackGrammar as grammar
import Compiler.SymbolTable as symbol

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
        self.input = input_file  # already open :)
        self.output = output_file  # already open :)
        self.current_class = 0 # class name
        self.type_list = [grammar.K_INT, grammar.K_CHAR, grammar.K_BOOLEAN] #TODO: do we need??
        self.tokenizer.advance()

        self.compile_class()


    def compile_class(self):
        """
        Compiles a complete class.
        :return:
        """

    def compile_class_var_dec(self, raise_error=True):
        """
        Compiles a static declaration or a field
        declaration.
        :return:
        """

    def compile_expression_list(self):
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

    def compile_identifier(self):
        """

        :return:
        """



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
            current_subroutine = self.tokenizer.current_value
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
            subroutine_name = self.tokenizer.current_value
        else:
            if raise_error:
                raise ValueError("No keyword found in subroutine")
            return False

        #open symbol table
        self.symbol_table.start_subroutine()
        if current_subroutine == grammar.K_METHOD:
            self.symbol_table.define('this', self.current_class, grammar.K_ARG)

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


    def compile_subroutineBody(self):
        """
        compiles subroutines body
        :return:
        """
        # {
        self.checkSymbol("{")





    def current_is_void_or_type(self):
        if (self.tokenizer.current_value == grammar.K_VOID) or self.tokenizer.current_value in self.type_list:
            return True


    def is_subroutine(self):

        return ((self.tokenizer.current_value == grammar.K_CONSTRUCTOR) or (self.tokenizer.current_value == grammar.K_FUNCTION)
        or (self.tokenizer.current_value == grammar.K_METHOD))



    def compile_parameter_list(self):
        """
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

                    self.symbol_table.define(name, type, grammar.K_ARG)
                    self.tokenizer.advance()

                    if self.tokenizer.current_value == ',':
                        self.tokenizer.advance()
                    elif self.tokenizer.current_value == ')':
                        more_parameters = False

            else:
                return False

        return True















    def compile_var_dec(self, raise_error=True):
        """
        Compiles a var declaration.
        :param raise_error: raises error if True, returns otherwise
        :return:
        """

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
















