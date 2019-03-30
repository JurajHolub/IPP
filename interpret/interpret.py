#!/usr/bin/env python3

"""
@file interpret.py
@brief Main body of program + implementation of interpret it self.
@project FIT VUT - IPP interpret
@author Juraj Holub <xholub40>
@date March 2019
"""

import sys
import xml_parser
import argument_parser
import string_convertor_fsm
from xml_parser import *
from error_handle import *

class Nil:
    """ Represent nil type of IPPcode19 """
    def __eq__(self, other):
        if type(other) is Nil:
            return True
        else:
            return False

    def __ne__(self, other):
        if type(other) is Nil:
            return False
        else:
            return True

class Stack:
    """ Simple stack implementation. Used in interpret local, global, temporary frame and data stack for push/pop. """
    def __init__(self, error_handle):
        self.stack = []
        self.error_handle = error_handle

    def pop(self, inst_idx):
        try:
            self.stack.pop(0)
        except:
            raise self.error_handle(inst_idx)

    def push(self, item):
        self.stack.insert(0, item)

    def top(self, inst_idx):
        try:
            return self.stack[0]
        except:
            raise self.error_handle(inst_idx)

    def debug_print(self):
        for item in self.stack:
            print(item)

class Interpret(object):
    """ Implementation of interpret it self. For every instruction there is one function."""

    SEMANTIC_ERR = 52
    RUNTIME_ERR_WRONG_OPERANDS_TYPE = 53
    RUNTIME_ERR_UNDEF_VAR = 54
    RUNTIME_ERR_NONEXIST_FRAME = 55
    RUNTIME_ERR_MISSING_VALUE = 56
    RUNTIME_ERR_WRONG_OPERAND_VALUE = 57
    RUNTIME_ERR_STRING = 58

    CONST_SYMBOLS = ["int", "bool", "string"]

    def __init__(self):
        self.global_frame = dict()
        self.temporary_frame = None
        self.local_frame_stack = Stack(RuntimeErrorNonExistFrame)
        self.data_stack = Stack(RuntimeErrorMissingValue)
        self.inst_idx = 1
        self.label_position = dict()
        self.call_stack =Stack(RuntimeErrorMissingValue)

    def inc_idx(self):
        self.inst_idx += 1

    def get_line(self):
        return str(self.inst_idx)

    def save_label(self, inst, idx):
        if inst.attrib["opcode"].upper() == "LABEL":
            label_type, label_name = interpret.get_argument(inst, 1)
            if label_name in self.label_position:
                raise SemanticError(idx)
            else:
                self.label_position[label_name] = idx

    def add_global_variable(self, var_name, var_val):
        if var_name in self.global_frame:
            self.global_frame[var_name] = var_val
            return True
        else:
            return False

    def get_argument(self, inst, idx):
        arg = inst.find("arg" + str(idx))

        if arg is not None and "type" in arg.attrib:
            type = arg.attrib["type"]
            value = arg.text
        else:
            raise XMLOperandError(self.inst_idx, "arg" + str(idx), inst.attrib["opcode"], "None", "type")

        if type == "int":
            if not XMLParser.is_int_constant(value):
                raise XMLOperandError(self.inst_idx, "arg" + str(idx), inst.attrib["opcode"], value, "int")
            value = int(value)
        elif type == "bool":
            if not XMLParser.is_bool_constant(value):
                raise XMLOperandError(self.inst_idx, "arg" + str(idx), inst.attrib["opcode"], value, "bool")
            value = value.title()  # Capitalize first letter of true, false => python compatibility
            if value.title() == "False":
                value = False
            else:
                value = True
        elif type == "string":
            if not XMLParser.is_string_constant(value):
                raise XMLOperandError(self.inst_idx, "arg" + str(idx), inst.attrib["opcode"], value, "string")
            if value is None:
                value = ""
            value = str(value)
        elif type == "nil":
            if not XMLParser.is_nil_constant(value):
                raise XMLOperandError(self.inst_idx, "arg" + str(idx), inst.attrib["opcode"], value, "nil")
            value = Nil()
        elif type == "label":
            if not XMLParser.is_label(value):
                raise XMLOperandError(self.inst_idx, "arg" + str(idx), inst.attrib["opcode"], value, "label")
        elif type == "type":
            if not XMLParser.is_type(value):
                raise XMLOperandError(self.inst_idx, "arg" + str(idx), inst.attrib["opcode"], value, "type")
        elif type == "var":
            if not XMLParser.is_variable(value):
                raise XMLOperandError(self.inst_idx, "arg" + str(idx), inst.attrib["opcode"], value, "var")
        else:
            raise XMLOperandError(self.inst_idx, "arg" + str(idx), inst.attrib["opcode"], value,
                                  "some supported symbol")

        return type, value

    def get_variable(self, var):
        var = var.split("@")
        if var[0] == "GF" and var[1] in self.global_frame:
            return self.global_frame[var[1]]
        elif var[0] == "TF" and var[1] in self.temporary_frame:
            return self.temporary_frame[var[1]]
        elif var[0] == "LF" and var[1] in self.local_frame_stack.top(self.get_line()):
            return self.local_frame_stack.top(self.get_line())[var[1]]
        else:
            raise RuntimeErrorUndefVar(self.inst_idx, var[0], var[1])

    def set_variable(self, var, val):
        var = var.split("@")
        if var[0] == "GF" and var[1] in self.global_frame:
            self.global_frame[var[1]] = val
        elif var[0] == "TF" and var[1] in self.temporary_frame:
            self.temporary_frame[var[1]] = val
        elif var[0] == "LF" and var[1] in self.local_frame_stack.top(self.get_line()):
            self.local_frame_stack.top(self.get_line())[var[1]] = val
        else:
            raise RuntimeErrorUndefVar(self.inst_idx, var[0], var[1])

    def create_variable(self, var):
        var = var.split("@")
        if var[0] == "GF":
            self.global_frame[var[1]] = None
        elif var[0] == "TF":
            self.temporary_frame[var[1]] = None
        elif var[0] == "LF":
            self.local_frame_stack.top(self.get_line())[var[1]] = None
        else:
            raise RuntimeErrorUndefVar(self.inst_idx, var[0], var[1])

    def get_symbol(self, type, value):
        if type == "var":
            return self.get_variable(value)
        else:
            return value

    def CREATEFRAME(self, inst):
        self.temporary_frame = dict()

    def PUSHFRAME(self, inst):
        self.local_frame_stack.push(self.temporary_frame)

    def POPFRAME(self, inst):
        self.temporary_frame = self.local_frame_stack.top(self.get_line())
        self.local_frame_stack.pop(self.get_line())

    def PUSHS(self, inst):
        type, name = self.get_argument(inst, 1)
        self.data_stack.push((type, name))

    def POPS(self, inst):
        var_type, var_name = self.get_argument(inst, 1)
        if var_type == "var":
            symb_type, symb_value = self.data_stack.top(self.get_line())
            self.data_stack.pop(self.get_line())
            self.set_variable(var_name, symb_value)
        else:
            raise RuntimeErrorUndefVar(self.get_line, "unknown", var_name)

    def DEFVAR(self, inst):
        """ DEFVAR <var>"""
        type, name = self.get_argument(inst, 1)

        if type != "var":
            raise RuntimeErrorWrongOperandsType(self.get_line)

        self.create_variable(name)

    def MOVE(self, inst):
        """ MOVE <var> <symb>"""
        var_type, var_name = self.get_argument(inst, 1)
        symb_type, symb_value = self.get_argument(inst, 2)

        self.set_variable(var_name, symb_value)

    def WRITE(self, inst):
        """ WRITE <symb>"""
        symb_type, symb_value = self.get_argument(inst, 1)
        if symb_type == "var" or symb_type in Interpret.CONST_SYMBOLS:
            symb_value = self.get_symbol(symb_type, symb_value)
            if type(symb_value) is str:
                convertor = string_convertor_fsm.StringConvertorFSM()
                symb_value = convertor.convert(symb_value)
            print(symb_value, end="")
        elif symb_type == "nil":
            pass  # print nothing
        else:
            raise SemanticError(self.get_line)  # todo return value?

    def binary_operation(self, inst, op):
        type1, value1 = self.get_argument(inst, 1)
        type2, value2 = self.get_argument(inst, 2)
        type3, value3 = self.get_argument(inst, 3)

        val1 = self.get_symbol(type2, value2)
        val2 = self.get_symbol(type3, value3)

        if op in ["+", "-", "*", "//"] and type(val1) is int and type(val2) is int:
            res = eval("val1 " + op + " val2")
        elif op in ["and", "or"] and type(val1) is bool and type(val2) is bool:
            res = eval("val1 " + op + " val2")
        elif op in [">", "==", "<"] and \
                (type(val1) is bool and type(val2) is bool or \
                 type(val1) is int and type(val2) is int or \
                 type(val1) is str and type(val2) is str):
            res = eval("val1 " + op + " val2")
        elif op == "CONCAT" and type(val1) is str and type(val2) is str:
            res = val1 + val2
        else:
            raise RuntimeErrorWrongOperandValue(self.inst_idx, val1, val2, op)

        self.set_variable(value1, res)

    def ADD(self, inst):
        """ ADD <var> <symb> <symb>"""
        self.binary_operation(inst, "+")

    def SUB(self, inst):
        """ SUB <var> <symb> <symb>"""
        self.binary_operation(inst, "-")

    def MUL(self, inst):
        """ MUL <var> <symb> <symb>"""
        self.binary_operation(inst, "*")

    def IDIV(self, inst):
        """ IDIV <var> <symb> <symb>"""
        self.binary_operation(inst, "//")

    def AND(self, inst):
        """ AND <var> <symb> <symb>"""
        self.binary_operation(inst, "and")

    def OR(self, inst):
        """ OR <var> <symb> <symb>"""
        self.binary_operation(inst, "or")

    def LT(self, inst):
        """ LT <var> <symb> <symb>"""
        self.binary_operation(inst, "<")

    def GT(self, inst):
        """ GT <var> <symb> <symb>"""
        self.binary_operation(inst, ">")

    def EQ(self, inst):
        """ EQ <var> <symb> <symb>"""
        self.binary_operation(inst, "==")

    def NOT(self, inst):
        """ NOT <var> <symb> """
        type1, value1 = self.get_argument(inst, 1)
        type2, value2 = self.get_argument(inst, 2)

        val1 = self.get_symbol(type2, value2)

        if type(val1) is bool:
            res = not val1
        else:
            raise RuntimeErrorWrongOperandValue(self.inst_idx, val1, "NOT EXIST", "NOT")

        self.set_variable(value1, res)

    def CONCAT(self, inst):
        """ CONCAT <var> <symb> <symb>"""
        self.binary_operation(inst, "CONCAT")

    def INT2CHAR(self, inst):
        """ INT2CHAR <var> <symb>"""
        var_type, var_name = self.get_argument(inst, 1)
        symb_type, symb_value = self.get_argument(inst, 2)
        symb_value = self.get_symbol(symb_type, symb_value)

        if var_type != "var" or type(symb_value) is not int:
            raise RuntimeErrorWrongOperandsType(self.get_line())

        try:
            ordinary_value = chr(symb_value)
        except ValueError:
            raise RuntimeErrorString(self.get_line())

        symb_value = str(ordinary_value)

        self.set_variable(var_name, symb_value)

    def STRI2INT(self, inst):
        """ STRI2INT <var> <symb> <symb>"""
        var_type, var_name = self.get_argument(inst, 1)
        symb_type1, symb_value1 = self.get_argument(inst, 2)
        symb_type2, symb_value2 = self.get_argument(inst, 3)

        symb_value1 = self.get_symbol(symb_type1, symb_value1)
        symb_value2 = self.get_symbol(symb_type2, symb_value2)

        if var_type != "var" or type(symb_value1) is not str or type(symb_value2) is not int:
            raise RuntimeErrorWrongOperandsType(self.get_line())

        try:
            ordinary_value = ord(symb_value1[symb_value2])
        except IndexError:
            raise RuntimeErrorString(self.get_line())

        self.set_variable(var_name, ordinary_value)

    def CONCAT(self, inst):
        """ CONCAT <var> <symb> <symb>"""
        var_type, var_name = self.get_argument(inst, 1)
        symb_type1, symb_value1 = self.get_argument(inst, 2)
        symb_type2, symb_value2 = self.get_argument(inst, 3)

        symb_value1 = self.get_symbol(symb_type1, symb_value1)
        symb_value2 = self.get_symbol(symb_type2, symb_value2)

        if var_type != "var" or type(symb_value1) is not str or type(symb_value2) is not str:
            raise RuntimeErrorWrongOperandsType(self.get_line())

        self.set_variable(var_name, symb_value1 + symb_value2)

    def STRLEN(self, inst):
        """ STRLEN <var> <symb>"""
        var_type, var_name = self.get_argument(inst, 1)
        symb_type, symb_value = self.get_argument(inst, 2)

        symb_value = self.get_symbol(symb_type, symb_value)
        if var_type != "var" or type(symb_value) is not str:
            raise RuntimeErrorWrongOperandsType(self.get_line())

        self.set_variable(var_name, len(symb_value))

    def GETCHAR(self, inst):
        """ GETCHAR <var> <symb> <symb>"""
        var_type, var_name = self.get_argument(inst, 1)
        symb_type1, symb_value1 = self.get_argument(inst, 2)
        symb_type2, symb_value2 = self.get_argument(inst, 3)

        symb_value1 = self.get_symbol(symb_type1, symb_value1)
        symb_value2 = self.get_symbol(symb_type2, symb_value2)

        if var_type != "var" or type(symb_value1) is not str or type(symb_value2) is not int:
            raise RuntimeErrorWrongOperandsType(self.get_line())

        try:
            char = symb_value1[symb_value2]
        except IndexError:
            raise RuntimeErrorString(self.get_line())
        self.set_variable(var_name, char)

    def SETCHAR(self, inst):
        """ SETCHAR <var> <symb> <symb>"""
        var_type, var_name = self.get_argument(inst, 1)
        symb_type1, symb_value1 = self.get_argument(inst, 2)
        symb_type2, symb_value2 = self.get_argument(inst, 3)

        var_value = self.get_symbol(var_type, var_name)
        symb_value1 = self.get_symbol(symb_type1, symb_value1)
        symb_value2 = self.get_symbol(symb_type2, symb_value2)

        if var_type != "var" and type(var_value) is not str or type(symb_value1) is not int or type(
                symb_value2) is not str:
            raise RuntimeErrorWrongOperandsType(self.get_line())

        try:
            var_value = var_value[:symb_value1] + symb_value2[0] + var_value[symb_value1 + 1:]
        except IndexError or TypeError:
            raise RuntimeErrorString(self.get_line())

        self.set_variable(var_name, var_value)

    def TYPE(self, inst):
        """ TYPE <var> <symb>"""
        var_type, var_name = self.get_argument(inst, 1)
        symb_type, symb_value = self.get_argument(inst, 2)

        symb_value = self.get_symbol(symb_type, symb_value)
        if type(symb_value) is int:
            var_value = "int"
        elif type(symb_value) is str:
            var_value = "string"
        elif type(symb_value) is bool:
            var_value = "bool"
        elif type(symb_value) is Nil:
            var_value = "nil"

        self.set_variable(var_name, var_value)

    def JUMP(self, inst):
        """ JUMP <label>"""
        label_type, label_name = self.get_argument(inst, 1)
        if label_name in self.label_position:
            self.inst_idx = self.label_position[label_name]
        else:
            raise SemanticError(self.get_line())

    def LABEL(self, inst):
        """ LABEL <label>"""
        label_type, label_name = self.get_argument(inst, 1)

    def JUMPIFNEQ(self, inst):
        """ JUMPIFNEQ <label> <symb> <symb>"""
        label_type, label_name = self.get_argument(inst, 1)
        symb_type1, symb_name1 = self.get_argument(inst, 2)
        symb_type2, symb_name2 = self.get_argument(inst, 3)

        symb_value1 = self.get_symbol(symb_type1, symb_name1)
        symb_value2 = self.get_symbol(symb_type2, symb_name2)

        if type(symb_value1) != type(symb_value2):
            raise RuntimeErrorWrongOperandsType(self.get_line())

        if symb_value1 != symb_value2:
            if label_name in self.label_position:
                self.inst_idx = self.label_position[label_name]
            else:
                raise SemanticError(self.get_line())

    def JUMPIFEQ(self, inst):
        """ JUMPIFEQ <label> <symb> <symb>"""
        label_type, label_name = self.get_argument(inst, 1)
        symb_type1, symb_name1 = self.get_argument(inst, 2)
        symb_type2, symb_name2 = self.get_argument(inst, 3)

        symb_value1 = self.get_symbol(symb_type1, symb_name1)
        symb_value2 = self.get_symbol(symb_type2, symb_name2)

        if type(symb_value1) != type(symb_value2):
            raise RuntimeErrorWrongOperandsType(self.get_line())

        if symb_value1 == symb_value2:
            if label_name in self.label_position:
                self.inst_idx = self.label_position[label_name]
            else:
                raise SemanticError(self.get_line())

    def CALL(self, inst):
        """ CALL <label> """
        label_type, label_name = self.get_argument(inst, 1)

        if label_name in self.label_position:
            self.call_stack.push(self.inst_idx)
            self.inst_idx = self.label_position[label_name]
        else:
            raise SemanticError(self.get_line())

    def RETURN(self, inst):
        """ RETURN """
        self.inst_idx = self.call_stack.top(self.get_line())

    def EXIT(self, inst):
        """ EXIT <symb>"""
        symb_type, symb_name = self.get_argument(inst, 1)
        symb_value = self.get_symbol(symb_type, symb_name)
        if type(symb_value) is int and 0 <= symb_value <= 49:
            raise ExitInstruction(symb_value)
        else:
            raise RuntimeErrorWrongOperandValue(self.get_line(), str(symb_value), "NOT EXIST", "EXIT")

    def DPRINT(self, inst):
        """ DPRINT <symb>"""
        symb_type, symb_value = self.get_argument(inst, 1)
        if symb_type == "var" or symb_type in Interpret.CONST_SYMBOLS:
            symb_value = self.get_symbol(symb_type, symb_value)
            if type(symb_value) is str:
                convertor = string_convertor_fsm.StringConvertorFSM()
                symb_value = convertor.convert(symb_value)
            sys.stderr.write(symb_value)
        elif symb_type == "nil":
            pass  # print nothing

    def BREAK(self, inst):
        """ BREAK """
        sys.stderr.write("Line:" + self.get_line() + "\n")

    def READ(self, inst):
        """ READ <var> <type>"""
        var_type, var_name = self.get_argument(inst, 1)
        symb_type, symb_value = self.get_argument(inst, 2)
        symb_value = self.get_symbol(symb_type, symb_value)

        if var_type != "var":
            raise RuntimeErrorWrongOperandsType(self.get_line())

        input_value = input()

        if symb_type == "type" and symb_value == "int":
            try:
                input_value = int(input_value)
            except ValueError:
                input_value = 0
        elif symb_type == "type" and symb_value == "string":
            pass
        elif symb_type == "type" and symb_value == "bool":
            if input_value.lower() == "true":
                input_value = True
            else:
                input_value = False
        else:
            raise RuntimeErrorWrongOperandsType(self.get_line())

        self.set_variable(var_name, input_value)

#################################################################
########################### MAIN BODY ###########################
#################################################################

cmd_args = argument_parser.ArgumentParser()
cmd_args.parse_args(sys.argv)

if cmd_args.what_to_do() == argument_parser.ArgumentParser.ERROR:
    sys.exit(10)
elif cmd_args.what_to_do() == argument_parser.ArgumentParser.HELP:
    print(argument_parser.HELP_MESSAGE)
    sys.exit(0)

parser = xml_parser.XMLParser(cmd_args)
result = parser.parse()

if result != XMLParser.PARSE_SUCCES:
    exit(result)

instructions = parser.get_instructions()
instructions.sort(key=lambda tup: tup[1])
interpret = Interpret()

idx = 1
for inst, order in instructions:
    if order != idx:
        exit(XMLParser.UNSUPPORTED_XML_ELEMENT)
    interpret.save_label(inst, idx)
    idx += 1

i = 0
while i < len(instructions):
    inst, order = instructions[i]
    try:
        instruction_to_parse = getattr(interpret, inst.attrib["opcode"].upper())
        instruction_to_parse(inst) # execute one instruction
        interpret.inc_idx()
        i = interpret.inst_idx - 1
    except AttributeError:
        sys.stderr.write(str(idx-1)+": Instruction \""+ inst.attrib["opcode"]+"\" not exist!\n")
        exit(XMLParser.UNSUPPORTED_XML_ELEMENT)
    except XMLOperandError as e:
        sys.stderr.write(e.line+": "+e.inst + " "+e.arg+" has wrong argument \"" + e.wrong_operand + "\" (\""+e.expected_operand+"\" expected).")
        exit(XMLParser.UNSUPPORTED_XML_ELEMENT)
    except SyntaxError as e:
        sys.stderr.write(interpret.get_line()+": \""+inst.attrib["opcode"] + "\" not supported instruction.")
        print(interpret.get_argument(inst, 1))
        print(interpret.get_argument(inst, 2))
        print(interpret.get_argument(inst, 3))
        exit(XMLParser.UNSUPPORTED_XML_ELEMENT)
    except RuntimeErrorUndefVar as e:
        sys.stderr.write(e.line+": "+"Undefined variable \""+ e.variable +"\" in frame \""+ e.frame +"\"")
        exit(Interpret.RUNTIME_ERR_UNDEF_VAR)
    except RuntimeErrorWrongOperandValue as e:
        sys.stderr.write(interpret.get_line()+": Wrong operand type for operator \""+e.operator+"\": op1=\""+ e.op1 +"\", op2=\""+ e.op2 +"\"")
        exit(Interpret.RUNTIME_ERR_UNDEF_VAR)
    except RuntimeErrorNonExistFrame as e:
        sys.stderr.write(e.line+": Nonexisting frame!")
        exit(Interpret.RUNTIME_ERR_NONEXIST_FRAME)
    except RuntimeErrorMissingValue as e:
        sys.stderr.write(e.line+": Missing value!")
        exit(Interpret.RUNTIME_ERR_MISSING_VALUE)
    except RuntimeErrorString as e:
        sys.stderr.write(e.line+": String error!")
        exit(Interpret.RUNTIME_ERR_STRING)
    except RuntimeErrorWrongOperandsType as e:
        sys.stderr.write(e.line+": Wrong operands type!")
        exit(Interpret.RUNTIME_ERR_WRONG_OPERANDS_TYPE)
    except SemanticError as e:
        sys.stderr.write(e.line+": Semantic error!")
        exit(Interpret.SEMANTIC_ERR)
    except ExitInstruction as e:
        exit(e.ret_code)
exit(XMLParser.PARSE_SUCCES)
