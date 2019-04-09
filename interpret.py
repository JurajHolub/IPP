#########################################
#   Interpreting XML code               #
#   @file interpret.py                  #
#   @author Diana Barnova, xbarno00     #
#   @date April 2019                    #
#########################################
# !/usr/bin/python

# TODO skontroluj ci uz premenna existuje v frame
# TODO nil
# TODO sort pre instrukcie a aj arg

import argparse
import xml.etree.ElementTree as xml_et
import sys

LocalFrame = {}
GlobalFrame = {}
TemporaryFrame = {}

Init = False
Init_LF = False
tmp_localFrame = []
list_of_root = []
label_stack = {}
data_stack = []
ret_idx = []
calling_idx = 0
input_file = None
jump_now = False


class Command:
    # def __init__(self):
    def Instruction(self, instruction):
        # print(instruction.attrib['opcode'])
        if "CREATEFRAME" in instruction.attrib['opcode'].upper():
            command = CREATEFRAME()
            command.parse(instruction)
        elif "PUSHFRAME" in instruction.attrib['opcode'].upper():
            command = PUSHFRAME()
            command.parse(instruction)
        elif "POPFRAME" in instruction.attrib['opcode'].upper():
            command = POPFRAME()
            command.parse(instruction)
        elif "JUMPIFEQ" in instruction.attrib['opcode'].upper():
            command = JUMPIFEQ()
            command.parse(instruction)
        elif "JUMPIFNEQ" in instruction.attrib['opcode'].upper():
            command = JUMPIFNEQ()
            command.parse(instruction)
        elif "JUMP" in instruction.attrib['opcode'].upper():
            command = JUMP()
            command.parse(instruction)
        elif "RETURN" in instruction.attrib['opcode'].upper():
            command = RETURN()
            command.parse(instruction)
        elif "BREAK" in instruction.attrib['opcode'].upper():
            command = BREAK()
            command.parse(instruction)
        elif "DEFVAR" in instruction.attrib['opcode'].upper():
            command = DEFVAR()
            command.parse(instruction)
        elif "POPS" in instruction.attrib['opcode'].upper():
            command = POPS()
            command.parse(instruction)
        elif "CALL" in instruction.attrib['opcode'].upper():
            command = CALL()
            command.parse(instruction)
        elif "LABEL" in instruction.attrib['opcode'].upper():
            command = LABEL()
            command.parse(instruction)
        elif "PUSHS" in instruction.attrib['opcode'].upper():
            command = PUSHS()
            command.parse(instruction)
        elif "WRITE" in instruction.attrib['opcode'].upper():
            command = WRITE()
            command.parse(instruction)
        elif "EXIT" in instruction.attrib['opcode'].upper():
            command = EXIT()
            command.parse(instruction)
        elif "DPRINT" in instruction.attrib['opcode'].upper():
            command = DPRINT()
            command.parse(instruction)
        elif "MOVE" in instruction.attrib['opcode'].upper():
            command = MOVE()
            command.parse(instruction)
        elif "INT2CHAR" in instruction.attrib['opcode'].upper():
            command = INT2CHAR()
            command.parse(instruction)
        elif "STRLEN" in instruction.attrib['opcode'].upper():
            command = STRLEN()
            command.parse(instruction)
        elif "TYPE" in instruction.attrib['opcode'].upper():
            command = TYPE()
            command.parse(instruction)
        elif "NOT" in instruction.attrib['opcode'].upper():
            command = NOT()
            command.parse(instruction)
        elif "READ" in instruction.attrib['opcode'].upper():
            command = READ()
            command.parse(instruction)
        elif "ADD" in instruction.attrib['opcode'].upper():
            command = ADD()
            command.parse(instruction)
        elif "SUB" in instruction.attrib['opcode'].upper():
            command = SUB()
            command.parse(instruction)
        elif "MUL" in instruction.attrib['opcode'].upper():
            command = MUL()
            command.parse(instruction)
        elif "IDIV" in instruction.attrib['opcode'].upper():
            command = IDIV()
            command.parse(instruction)
        elif "LT" in instruction.attrib['opcode'].upper():
            command = LT()
            command.parse(instruction)
        elif "GT" in instruction.attrib['opcode'].upper():
            command = GT()
            command.parse(instruction)
        elif "EQ" in instruction.attrib['opcode'].upper():
            command = EQ()
            command.parse(instruction)
        elif "AND" in instruction.attrib['opcode'].upper():
            command = AND()
            command.parse(instruction)
        elif "OR" in instruction.attrib['opcode'].upper():
            command = OR()
            command.parse(instruction)
        elif "STRI2INT" in instruction.attrib['opcode'].upper():
            command = STRI2INT()
            command.parse(instruction)
        elif "CONCAT" in instruction.attrib['opcode'].upper():
            command = CONCAT()
            command.parse(instruction)
        elif "GETCHAR" in instruction.attrib['opcode'].upper():
            command = GETCHAR()
            command.parse(instruction)
        elif "SETCHAR" in instruction.attrib['opcode'].upper():
            command = SETCHAR()
            command.parse(instruction)


################


def real_type(value):
    if type(value) is int:
        return 'int'
    elif type(value) is bool:
        return 'bool'
    elif value.isdigit():
        return 'int'
    elif value.upper() is 'TRUE' or value.upper() is 'FALSE':
        return 'bool'
    else:
        return 'string'


def setInit(boolean):
    global Init
    if "True" in boolean:
        Init = True
    elif "False" in boolean:
        Init = False


def exist_localframe(boolean):
    global Init_LF
    if "True" in boolean:
        Init_LF = True
    elif "False" in boolean:
        Init_LF = False


def get_real_type(arg):
    if 'int' in arg.attrib['type']:
        arg.text = int(arg.text)
    elif 'bool' in arg.attrib['type']:
        if 'FALSE' in arg.text.upper():
            arg.text = False
        else:
            arg.text = True
    return arg


def same_type(arg):
    if 'var' in arg[1].attrib['type']:
        arg[1].text = get_value(arg[1].text)
        arg[1].attrib['type'] = real_type(arg[1].text)

    if 'var' in arg[2].attrib['type']:
        arg[2].text = get_value(arg[2].text)
        arg[2].attrib['type'] = real_type(arg[2].text)

    if arg[1].attrib['type'] != arg[2].attrib['type']:
        errors("op_type")
    return arg


def fillFrame(arg_text, value=None):
    if 'GF' in arg_text[:2]:
        GlobalFrame[arg_text[3:]] = value
    elif 'TF' in arg_text[:2]:
        if Init is True:
            TemporaryFrame[arg_text[3:]] = value
        else:
            errors("unknown_frame")
    elif 'LF' in arg_text[:2]:
        if Init_LF is True:
            LocalFrame[arg_text[3:]] = value
        else:
            errors("unknown_frame")
    else:
        errors("wrong_xml_struct")


def get_value(name_var):
    if not is_define(name_var):
        errors("unknown_variable")
    if 'GF' in name_var[:2]:
        return GlobalFrame[name_var[3:]]
    elif 'LF' in name_var[:2]:
        return LocalFrame[name_var[3:]]
    elif 'TF' in name_var[:2]:
        return TemporaryFrame[name_var[3:]]


def real_string(string):
    idx = 0
    str_yield = []
    while idx < len(string):
        if string[idx] == '\\':
            str_yield.append(idx)
        else:
            pass
        idx += 1
    counter = 0
    if len(str_yield) != 0:
        result = string[:str_yield[0]]
    else:
        return string
    while counter < len(str_yield):
        just_backslash = True
        if len(string) >= str_yield[counter] + 4:
            if string[str_yield[counter] + 3].isdigit() and string[str_yield[counter] + 2].isdigit() and string[str_yield[counter] + 1].isdigit():
                num_of_digits = 4
        elif len(string) >= str_yield[counter] + 3:
            if string[str_yield[counter] + 2].isdigit() and string[str_yield[counter] + 1].isdigit():
                num_of_digits = 3
        elif len(string) >= str_yield[counter] + 2:
            if string[str_yield[counter] + 1].isdigit():
                num_of_digits = 2
        else:
            just_backslash = False
            num_of_digits = 1

        if just_backslash:
            char = chr(int(string[str_yield[counter] + 1:str_yield[counter] + num_of_digits]))
            result += char
        else:
            result += '\\'
        if counter + 1 is len(str_yield):
            result += string[str_yield[counter] + num_of_digits:]
        else:
            result += string[str_yield[counter] + num_of_digits:str_yield[counter + 1]]
        counter += 1
    return result


def is_define(name_var):
    for definition in list_of_root:
        if 'DEFVAR' in definition.attrib['opcode']:
            for find_var in definition:
                if name_var in find_var.text:
                    return True
    return False


################


class CREATEFRAME:  # 0
    def parse(self, instruction):
        global TemporaryFrame

        if len(list(instruction)) != 0:
            errors("wrong_formated")
        TemporaryFrame.clear()
        setInit("True")


class PUSHFRAME:  # 0
    def parse(self, instruction):
        global LocalFrame
        global TemporaryFrame

        if len(list(instruction)) != 0:
            errors("wrong_formated")
        if not Init:
            errors("unknown_frame")
        for name, value in TemporaryFrame.items():
            tmp_localFrame.insert(len(tmp_localFrame), name)

        exist_localframe("True")
        LocalFrame = TemporaryFrame.copy()
        TemporaryFrame.clear()
        setInit("False")


class POPFRAME:  # 0
    def parse(self, instruction):
        global TemporaryFrame
        global LocalFrame

        if len(list(instruction)) != 0:
            errors("wrong_formated")
        if not Init_LF:
            errors("unknown_frame")
        setInit("True")
        tmp = LocalFrame.popitem()  # last item from local frame pop to var for moving to temp frame
        TemporaryFrame[tmp[0]] = tmp[1]
        if len(LocalFrame.keys()) == 0:
            exist_localframe("False")


class RETURN:  # 0
    def parse(self, instruction):
        global calling_idx
        global jump_now
        if len(list(instruction)) != 0:
            errors("wrong_formated")
        if len(ret_idx) != 0:
            calling_idx = ret_idx.pop()
            jump_now = True
        else:
            errors("missing_value")


class BREAK:  # 0
    def parse(self, instruction):
        global GlobalFrame
        global LocalFrame
        global TemporaryFrame
        global label_stack

        if len(list(instruction)) != 0:
            errors("wrong_formated")
        print("Date stack =", data_stack, file=sys.stderr)
        print("Label stack =", label_stack, file=sys.stderr)
        print("Local Frame =", LocalFrame, file=sys.stderr)
        print("Global Frame =", GlobalFrame, file=sys.stderr)
        print("Temporary Frame =", TemporaryFrame, file=sys.stderr)
        print("This instruction is", instruction.attrib['order'], "in order.", file=sys.stderr)


class DEFVAR:  # 1
    def parse(self, instruction):
        count = 0
        for arg in instruction:
            if 'var' in arg.attrib['type']:
                fillFrame(arg.text)
            else:
                errors("op_type")
            count += 1
        if count != 1:
            errors("wrong_formated")


class CALL:  # 1
    def parse(self, instruction):
        global calling_idx
        global ret_idx
        global jump_now
        for arg in instruction:
            if 'label' in arg.attrib['type']:
                if arg.text in label_stack:
                    calling_idx = label_stack[arg.text]
                    ret_idx.append(instruction.attrib['order'])
                    jump_now = True
                else:
                    errors("missing_value")
            else:
                errors("op_type")


class LABEL:  # 1
    def parse(self, instruction):
        if len(list(instruction)) != 1:
            errors("wrong_formated")


class JUMP:  # 1
    def parse(self, instruction):
        global calling_idx
        global jump_now
        arg = list(instruction)
        if len(arg) != 1:
            errors("wrong_formated")
        if 'label' in arg[0].attrib['type']:
            if arg[0].text in label_stack:
                calling_idx = label_stack[arg[0].text]
                jump_now = True
            else:
                errors("missing_value")
        else:
            errors("op_type")


class PUSHS:  # 1
    def parse(self, instruction):
        global data_stack
        arg = list(instruction)
        if len(arg) != 1:
            errors("wrong_formated")
        if 'var' in arg[0].attrib['type']:
            arg[0].text = get_value(arg[0].text)
        data_stack.append(arg[0].text)


class POPS:  # 1
    def parse(self, instruction):
        global data_stack
        arg = list(instruction)
        if len(arg) != 1:
            errors("wrong_formated")
        if len(data_stack) == 0:
            errors("missing_value")
        fillFrame(arg[0].text, data_stack.pop())


class WRITE:  # 1
    def parse(self, instruction):
        count = 0
        for arg in instruction:
            if 'bool' in arg.attrib['type']:
                if bool(arg.text) is True:
                    print("true", end="")
                elif bool(arg.text) is False:
                    print("false", end="")
            elif 'int' in arg.attrib['type']:
                print(arg.text, end="")
            elif 'string' in arg.attrib['type']:
                value = real_string(arg.text)
                print(value, end="")
            elif 'var' in arg.attrib['type']:
                value = get_value(arg.text)
                if type(value) == bool:
                    if bool(value) is True:
                        print("true", end="")
                    elif bool(value) is False:
                        print("false", end="")
                elif type(value) == int:
                    print(value, end="")
                elif type(value) == str:
                    value = real_string(value)
                    print(value, end="")
            elif 'nil' in arg.attrib['type']:
                pass  # do nothing
            else:
                errors("op_type")
            count += 1
        if count != 1:
            errors("wrong_formated")


class EXIT:  # 1
    def parse(self, instruction):
        count = 0
        for arg in instruction:
            if 'var' in arg.attrib['type']:
                value = get_value(arg.text)
            else:
                value = arg.text
            if -1 < int(value) < 50:
                exit(int(value))
            else:
                errors("wrong_op_value")
            count += 1
        if count != 1:
            errors("wrong_formated")


class DPRINT:  # 1
    def parse(self, instruction):
        arg = list(instruction)
        if len(arg) != 1:
            errors("wrong_formated")
        if 'var' in arg[0].attrib['type']:
            arg[0].text = get_value(arg[1].text)
        elif 'nil' in arg[0].attrib['type']:
            return  # print nothing
        print(arg[0].text, file=sys.stderr)


class MOVE:  # 2
    def parse(self, instruction):
        arg = list(instruction)
        if len(arg) != 2:
            errors("wrong_formated")
        if 'var' not in arg[0].attrib['type']:
            errors("op_type")
        if not is_define(arg[0].text):
            errors("unknown_variable")
        if 'var' in arg[1].attrib['type']:
            arg[1].text = get_value(arg[1].text)
        arg[1] = get_real_type(arg[1])
        fillFrame(arg[0].text, arg[1].text)


class INT2CHAR:  # 2
    def parse(self, instruction):
        arg = list(instruction)
        if len(arg) != 2:
            errors("wrong_formated")
        if 'var' not in arg[0].attrib['type']:
            errors("op_type")
        if not is_define(arg[0].text):
            errors("unknown_variable")
        if 'var' in arg[1].attrib['type']:
            arg[1].text = get_value(arg[1].text)
        if arg[1].text.find('\\') == -1:
            arg[1].text = '\\' + arg[1].text
        if int(arg[1].text[1:]) > 128:
            errors("wrong_string")

        fillFrame(arg[0].text, real_string(arg[1].text))


class STRLEN:  # 2
    def parse(self, instruction):
        arg = list(instruction)
        if len(arg) != 2:
            errors("wrong_formated")
        if not is_define(arg[0].text):
            errors("unknown_variable")
        if 'var' in arg[1].attrib['type']:
            arg[1].text = get_value(arg[1].text)
        fillFrame(arg[0].text, len(arg[1].text))


class TYPE:  # 2
    def parse(self, instruction):
        arg = list(instruction)
        if len(arg) != 2:
            errors("wrong_formated")
        if not is_define(arg[0].text):
            errors("unknown_variable")
        if 'var' in arg[1].attrib['type']:
            if not is_define(arg[1].text):
                val = ""
            else:
                arg[1].text = get_value(arg[1].text)
        if str == type(arg[1].text):
            val = "string"
        elif int == type(arg[1].text):
            val = "int"
        elif bool == type(arg[1].text):
            val = "bool"
        # elif type(arg[1].text) is Nil:
        #     val = "nil"
        fillFrame(arg[0].text, val)


class NOT:  # 2
    def parse(self, instruction):
        arg = list(instruction)
        if len(arg) != 2:
            errors("wrong_formated")
        if 'var' not in arg[0].attrib['type']:
            errors("op_type")
        if not is_define(arg[0].text):
            errors("unknown_variable")
        if 'var' in arg[1].attrib['type']:
            arg[1].text = get_value(arg[1].text)
        arg[1] = get_real_type(arg[1])
        fillFrame(arg[0].text, bool(arg[1].text))


class READ:  # 2 --input
    def parse(self, instruction):
        arg = list(instruction)
        if len(arg) != 2:
            errors("wrong_formated")
        if 'var' not in arg[0].attrib['type'] or 'type' not in arg[1].attrib['type']:
            errors("op_type")
        if not is_define(arg[0].text):
            errors("unknown_variable")

        if input_file is not None:
            try:
                open(input_file, 'r')
            except Exception:
                errors("source_input_file")
            #TODO pri novom read citat to iste alebo novy riadok??
            from_stdin = open(input_file).readline()
            from_stdin = from_stdin[:len(from_stdin)-1]
        else:
            from_stdin = input()

        if 'int' in arg[1].text:
            if from_stdin.strip().isdigit():
                fillFrame(arg[0].text, int(from_stdin.strip()))
            else:
                fillFrame(arg[0].text, 0)
        elif 'bool' in arg[1].text:
            if from_stdin.strip().upper() == "TRUE":
                fillFrame(arg[0].text, True)
            else:
                fillFrame(arg[0].text, False)
        elif 'string' in arg[1].text:
            fillFrame(arg[0].text, from_stdin)
        else:
            errors("semantic_mistake")


class ADD:  # 3,
    def parse(self, instruction):
        if len(list(instruction)) != 3:
            errors("wrong_formated")
        for arg in instruction:
            print(arg.tag, arg.attrib, arg.text)


class SUB:  # 3,
    def parse(self, instruction):
        if len(list(instruction)) != 3:
            errors("wrong_formated")
        for arg in instruction:
            print(arg.tag, arg.attrib, arg.text)


class MUL:  # 3,
    def parse(self, instruction):
        if len(list(instruction)) != 3:
            errors("wrong_formated")
        for arg in instruction:
            print(arg.tag, arg.attrib, arg.text)


class IDIV:  # 3,
    def parse(self, instruction):
        if len(list(instruction)) != 3:
            errors("wrong_formated")
        for arg in instruction:
            print(arg.tag, arg.attrib, arg.text)


class LT:  # 3
    def parse(self, instruction):
        arg = list(instruction)
        if len(arg) != 3:
            errors("wrong_formated")
        if 'nil' in arg[1].attrib['type'] or 'nil' in arg[2].attrib['type']:
            errors("op_type")
        if not is_define(arg[0].text):
            errors("unknown_variable")

        arg = same_type(arg)
        arg[1] = get_real_type(arg[1])
        arg[2] = get_real_type(arg[2])
        fillFrame(arg[0].text, arg[1].text < arg[2].text)


class GT:  # 3
    def parse(self, instruction):
        arg = list(instruction)
        if len(arg) != 3:
            errors("wrong_formated")
        if 'nil' in arg[1].attrib['type'] or 'nil' in arg[2].attrib['type']:
            errors("op_type")
        if not is_define(arg[0].text):
            errors("unknown_variable")

        arg = same_type(arg)
        arg[1] = get_real_type(arg[1])
        arg[2] = get_real_type(arg[2])
        fillFrame(arg[0].text, arg[1].text > arg[2].text)


class EQ:  # 3
    def parse(self, instruction):
        arg = list(instruction)
        if len(arg) != 3:
            errors("wrong_formated")
        if not is_define(arg[0].text):
            errors("unknown_variable")

        arg = same_type(arg)
        arg[1] = get_real_type(arg[1])
        arg[2] = get_real_type(arg[2])
        fillFrame(arg[0].text, arg[1].text == arg[2].text)


class AND:  # 3
    def parse(self, instruction):
        arg = list(instruction)
        if len(arg) != 3:
            errors("wrong_formated")
        if not is_define(arg[0].text):
            errors("unknown_variable")
        arg = same_type(arg)
        if 'bool' not in arg[1].attrib['type']:
            errors("op_type")
        arg[1] = get_real_type(arg[1])
        arg[2] = get_real_type(arg[2])
        fillFrame(arg[0].text, arg[1].text and arg[2].text)


class OR:  # 3
    def parse(self, instruction):
        arg = list(instruction)
        if len(arg) != 3:
            errors("wrong_formated")
        if not is_define(arg[0].text):
            errors("unknown_variable")
        arg = same_type(arg)
        if 'bool' not in arg[1].attrib['type']:
            errors("op_type")
        arg[1] = get_real_type(arg[1])
        arg[2] = get_real_type(arg[2])
        fillFrame(arg[0].text, arg[1].text or arg[2].text)


class STRI2INT:  # 3
    def parse(self, instruction):
        arg = list(instruction)
        if len(arg) != 3:
            errors("wrong_formated")
        if not is_define(arg[0].text):
            errors("unknown_variable")
        if 'var' in arg[1].attrib['type']:
            arg[1].text = get_value(arg[1].text)
        if 'var' in arg[2].attrib['type']:
            arg[2].text = get_value(arg[2].text)
        arg[1].text = real_string(arg[1].text)
        arg[2] = get_real_type(arg[2])
        if len(arg[1].text) < int(arg[2].text):
            errors("wrong_string")
        fillFrame(arg[0].text, ord(arg[1].text[arg[2].text]))


class CONCAT:  # 3
    def parse(self, instruction):
        arg = list(instruction)
        if len(arg) != 3:
            errors("wrong_formated")
        if 'var' in arg[1].attrib['type']:
            arg[1].text = get_value(arg[1].text)
        if 'var' in arg[2].attrib['type']:
            arg[2].text = get_value(arg[2].text)
        if type(arg[1].text) != type(arg[1].text):
            errors("semantic_mistake")
        fillFrame(arg[0].text, (arg[1].text + arg[2].text))


class GETCHAR:  # 3
    def parse(self, instruction):
        arg = list(instruction)
        if len(arg) != 3:
            errors("wrong_formated")
        if not is_define(arg[0].text):
            errors("unknown_variable")
        if 'var' in arg[1].attrib['type']:
            arg[1].text = get_value(arg[1].text)
        if 'var' in arg[2].attrib['type']:
            arg[2].text = get_value(arg[2].text)
        if not arg[2].text.isdigit():
            errors("op_type")
        if len(arg[1].text) < int(arg[2].text):
            errors("wrong_string")
        fillFrame(arg[0].text, arg[1].text[int(arg[2].text)])


class SETCHAR:  # 3
    def parse(self, instruction):
        arg = list(instruction)
        if len(arg) != 3:
            errors("wrong_formated")
        str_to_modif = get_value(arg[0].text)
        if 'var' in arg[1].attrib['type']:
            arg[1].text = get_value(arg[1].text)
        if 'var' in arg[2].attrib['type']:
            arg[2].text = get_value(arg[2].text)
        if arg[2].text == '':
            errors("wrong_string")
        if len(arg[0].text) < int(arg[1].text):
            errors("wrong_string")
        str_to_modif = str_to_modif[:int(arg[1].text)] + arg[2].text[0] + str_to_modif[int(arg[1].text)+1:]
        fillFrame(arg[0].text, str_to_modif)


class JUMPIFEQ:  # 3
    def parse(self, instruction):
        global calling_idx
        global jump_now
        arg = list(instruction)
        if len(arg) != 3:
            errors("wrong_formated")
        arg = same_type(arg)
        if arg[1].text == arg[2].text:
            if 'label' in arg[0].attrib['type']:
                if arg[0].text in label_stack:
                    calling_idx = label_stack[arg[0].text]
                    jump_now = True
                else:
                    errors("missing_value")
            else:
                errors("op_type")


class JUMPIFNEQ:  # 3
    def parse(self, instruction):
        global calling_idx
        global jump_now
        arg = list(instruction)
        if len(arg) != 3:
            errors("wrong_formated")
        arg = same_type(arg)
        if not arg[1].text == arg[2].text:
            if 'label' in arg[0].attrib['type']:
                if arg[0].text in label_stack:
                    calling_idx = label_stack[arg[0].text]
                    jump_now = True
                else:
                    errors("missing_value")
            else:
                errors("op_type")


def main():
    global list_of_root
    global input_file
    global jump_now
    parser = argparse.ArgumentParser()
    parser.add_argument("--source")
    parser.add_argument("--input")

    try:
        args = parser.parse_args()
    except SystemExit:
        # if in args is help and other args do just help and do it successfully
        if sys.exc_info()[1].code != 0:
            errors("wrong_param")
        exit(0)

    if args.source is not None:
        if not open(args.source):
            errors("source_input_file")

    if args.input is not None:
        input_file = args.input

    try: #todo source nie je - cita so z input()
        tree = xml_et.parse(args.source)
    except Exception:
        errors("wrong_formated")

    root = tree.getroot()
    if root.tag != "program" or root.attrib['language'] != "IPPcode19":  # OK
        errors("wrong_xml_struct")

    list_of_root = list(root)

    for child in root:
        if 'LABEL' in child.attrib['opcode']:
            for arg in child:
                if arg.text in label_stack:
                    errors("semantic_mistake")  # redefinice
                label_stack[arg.text] = child.attrib['order']

    counter = 0
    while counter < len(list_of_root):
        if "instruction" not in list_of_root[counter].tag[:11] and len(list_of_root[counter].tag) != 11:
            errors("wrong_formated")

        jump_now = False
        function = Command()
        function.Instruction(list_of_root[counter])
        if ('CALL' in list_of_root[counter].attrib['opcode'] or \
                'RETURN' in list_of_root[counter].attrib['opcode'] or \
                'JUMP' in list_of_root[counter].attrib['opcode']) and jump_now:
            counter = int(calling_idx)
            # print(counter)
        else:
            counter += 1
        # print(counter)
        # print(list(child))

        # print(child.attrib['order'])
        # print("Global:", GlobalFrame)
        # print("Local:", LocalFrame)
        # print("Temp:", TemporaryFrame)
        # print("init Temp:", Init)
        # print("init Local:", Init_LF)
        # print("-----------------------------")
    print("Global:", GlobalFrame)
    # print("Temp:", TemporaryFrame)

    exit(0)


def errors(er_msg):
    if er_msg == "wrong_param":
        exit(10)  # zle parametre skriptu
    elif er_msg == "source_input_file":
        exit(11)  # chyba při otevírání vstupních souborů
    elif er_msg == "output_file":
        exit(12)  # chyba při otevření výstupních souborů pro zápis
    elif er_msg == "wrong_formated":
        exit(31)  # chybný XML formát ve vstupním souboru
    elif er_msg == "wrong_xml_struct":
        exit(32)  # neočekávaná struktura XML
    elif er_msg == "semantic_mistake":
        exit(52)  # sémantických kontrolách vstupního kódu v IPPcode19
    elif er_msg == "op_type":
        exit(53)  # špatné typy operandů
    elif er_msg == "unknown_variable":
        exit(54)  # přístup k neexistující proměnné
    elif er_msg == "unknown_frame":
        exit(55)  # rámec neexistuje
    elif er_msg == "missing_value":
        exit(56)  # chybějící hodnota (v proměnné, na datovém zásobníku, nebo v zásobníku volání)
    elif er_msg == "wrong_op_value":
        exit(57)  # špatná hodnota operandu (dělení nulou, špatná návratová hodnota instrukce EXIT,..)
    elif er_msg == "wrong_string":
        exit(58)  # chybná práce s řetězcem
    elif er_msg == "internal":
        exit(99)  # interní chyba


if __name__ == '__main__':
    main()
