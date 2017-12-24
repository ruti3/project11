# This class writes VM commands into a file. It encapsulates the VM
# command syntax.

class VMwriter(object):
    """
    Emits VM commands into a file
    """
    def __init__(self, output_file):
        """
        Creates a new file and prepares it for writing VM commands
        :param output_file:
        """

    def writePush(self, segment, index):
        """
        Writes a VM push command
        :param segment:CONST, ARG, LOCAL, STATIC, THIS, THAT, POINTER or TEMP
        :param index:int
        :return:
        """

    def writePop(self, segment, index):
        """
        Writes a VM pop command
        :param segment:CONST, ARG, LOCAL, STATIC, THIS, THAT, POINTER or TEMP
        :param index:int
        :return:
        """

    def WriteArithmetic(self, command):
        """
        Writes a VM arithmetic command
        :param command:ADD, SUB, NEG, EQ, GT, LT, AND, OR, NOT
        :return:
        """

    def WriteLabel(self, label):
        """
        Writes a VM label command

        :param label: string
        :return:
        """


    def WriteGoto(self, label):
        """
        Writes a VM label command?????????????????????????
        :param label:
        :return:
        """

    def WriteIf(self, label):
        """
        Writes a VM If-goto command
        :param label:
        :return:
        """

    def writeCall(self, name, n):
        """
        Writes a VM call command

        :param name: string
        :param n: num of args
        :return:
        """

    def writeFunction(self, name, n):
        """
        Writes a VM function command
        :param name:
        :param n: num of locals
        :return:
        """

    def writeReturn(self):
        """
        Writes a VM return command
        :return:
        """

    def close(self):
        """
        Closes the output file
        :return:
        """

