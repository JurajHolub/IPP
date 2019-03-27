#!/usr/bin/env python3

"""
@file error_handle.py
@brief Definition of error classes for interpret runtime exception handling.
@project FIT VUT - IPP interpret
@author Juraj Holub <xholub40>
@date March 2019
"""

class Error(Exception):
    pass

class XMLOperandError(Error):

    def __init__(self, line, arg, inst, wrong_operand, expected_operand):
        self.line = str(line)
        self.arg = str(arg)
        self.inst = str(inst)
        self.wrong_operand = str(wrong_operand)
        self.expected_operand = str(expected_operand)

class RuntimeErrorUndefVar(Error):
    def __init__(self, line, frame, variable):
        self.line = str(line)
        self.frame = str(frame)
        self.variable = str(variable)

class RuntimeErrorWrongOperandValue(Error):
    def __init__(self, line, op1, op2, operator):
        self.line = str(line)
        self.op1 = str(op1)
        self.op2 = str(op2)
        self.operator = str(operator)

class RuntimeErrorNonExistFrame(Error):
    def __init__(self, line):
        self.line = str(line)

class RuntimeErrorMissingValue(Error):
    def __init__(self, line):
        self.line = str(line)

class RuntimeErrorString(Error):
    def __init__(self, line):
        self.line = str(line)

class SemanticError(Error):
    def __init__(self, line):
        self.line = str(line)

class RuntimeErrorWrongOperandsType(Error):
    def __init__(self, line):
        self.line = str(line)
