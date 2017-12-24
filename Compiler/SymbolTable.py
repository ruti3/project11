# This module provides services for creating, populating, and using a symbol
# table. Recall that each symbol has a scope from which it is visible
# in the source code. In the symbol table, each symbol is given a running
# number (index) within the scope, where the index starts at 0 and is
# reset when starting a new scope.

# TODO :you will probably need to use two separate hash tables to implement the symbol
# table: one for the class-scope and another one for the subroutine-scope. When a new subroutine
# is started, the subroutine-scope table should be cleared.

class SymbolTable(object):

    """
    A symbol table that associates names with information needed for Jack
    compilation: type, kind, and running index. The symbol table has 2
    nested scopes (class/subroutine).
    """
    def __init__(self):
        """
        Creates a new empty symbol table
        """


    def startSubroutine(self):
        """
        Starts a new subroutine scope (i.e. erases
        all names in the previous subroutine’s scope.)
        :return:
        """

    def define(self, name, type, kind):
        """
        Defines a new identifier of a given name, type, and kind and assigns
        it a running index. STATIC and FIELD identifiers have a class scope,
        while ARG and VAR identifiers have a subroutine scope.

        :param name: string
        :param type: string
        :param kind:(STATIC,FIELD, ARG, or VAR)
        :return:
        """

    def varCount(self, kind):
        """
        Returns the number of variables of the given kind already defined in
        the current scope.
        :param kind:STATIC,FIELD, ARG, or VAR
        :return: int
        """

    def kindOf(self, name):
        """
        Returns the kind of the named identifier in the current scope.
        Returns NONE if the identifier is unknown in the current scope
        :param name:string
        :return:kind:STATIC,FIELD, ARG, or VAR
        """

    def typeOf(self, name):
        """
        Returns the type of the named identifier in the current scope.
        :param name:string
        :return:string
        """

    def indexOf(self, name):
        """
        Returns the index assigned to named identifier.
        :param name:string
        :return:int
        """

