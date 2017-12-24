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



