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

        self.type_list = [grammar.K_INT, grammar.K_CHAR, grammar.K_BOOLEAN] #TODO: do we need??
        self.tokenizer.advance()

        self.compile_class()


















