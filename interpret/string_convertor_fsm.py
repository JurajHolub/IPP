#!/usr/bin/env python3

"""
@file string_convertor_fsm.py
@brief Convert IPPcode19 string to printable string (e.g. \010 to new line).
@project FIT VUT - IPP interpret
@author Juraj Holub <xholub40>
@date March 2019
"""

class StringConvertorFSM:
    """ Implemented like Finite State Machine"""

    S_BEGIN = 1
    S_BRACKET = 2
    S_NUM1 = 3
    S_NUM2 = 4
    S_NUM3 = 5
    S_END = 6

    def __init__(self):
        self.new_string = list()
        self.state = StringConvertorFSM.S_BEGIN

    def convert(self, string):
        string = list(string)
        string.append("#")
        val = ""
        tmp = ""

        """ string FSM """
        for token in string:
            if self.state == StringConvertorFSM.S_BEGIN:
                if token == "\\":
                    self.state = StringConvertorFSM.S_BRACKET
                    tmp += token
                elif token == "#":
                    pass
                else:
                    self.new_string.append(token)
            elif self.state == StringConvertorFSM.S_BRACKET:
                if token.isdigit():
                    self.state = StringConvertorFSM.S_NUM1
                    val += token
                    tmp += token
                elif token == "\\":
                    self.state = StringConvertorFSM.S_BRACKET
                    self.new_string.append(tmp)
                    tmp = token
                    val = ""
                elif token == "#":
                    self.new_string.append(tmp)
                else:
                    self.state = StringConvertorFSM.S_BEGIN
                    self.new_string.append(tmp)
                    self.new_string.append(token)
                    tmp = ""
                    val = ""
            elif self.state == StringConvertorFSM.S_NUM1:
                if token.isdigit():
                    self.state = StringConvertorFSM.S_NUM2
                    val += token
                    tmp += token
                elif token == "\\":
                    self.state = StringConvertorFSM.S_BRACKET
                    self.new_string.append(tmp)
                    tmp = token
                    val = ""
                elif token == "#":
                    self.new_string.append(tmp)
                else:
                    self.state = StringConvertorFSM.S_BEGIN
                    self.new_string.append(tmp)
                    self.new_string.append(token)
                    tmp = ""
                    val = ""
            elif self.state == StringConvertorFSM.S_NUM2:
                if token.isdigit():
                    self.state = StringConvertorFSM.S_NUM3
                    val += token
                    ord_val = int(val)
                    val = ""
                    tmp = ""
                    self.new_string.append(chr(ord_val))
                elif token == "\\":
                    self.state = StringConvertorFSM.S_BRACKET
                    self.new_string.append(tmp)
                    tmp = token
                    val = ""
                elif token == "#":
                    self.new_string.append(tmp)
                else:
                    self.state = StringConvertorFSM.S_BEGIN
                    self.new_string.append(tmp)
                    self.new_string.append(token)
                    tmp = ""
                    val = ""
            elif self.state == StringConvertorFSM.S_NUM3:
                if token == "\\":
                    self.state = StringConvertorFSM.S_BRACKET
                    self.new_string.append(tmp)
                    tmp = token
                    val = ""
                elif token == "#":
                    self.new_string.append(tmp)
                else:
                    self.state = StringConvertorFSM.S_BEGIN
                    self.new_string.append(tmp)
                    self.new_string.append(token)
                    tmp = ""
                    val = ""

        return "".join(self.new_string)
