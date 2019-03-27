import xml.dom.minidom
import xml.etree.ElementTree
import sys
from error_handle import *

class XMLParser(object):

    NOT_WELL_FORMED_XML = 31
    UNSUPPORTED_XML_ELEMENT = 32
    PARSE_SUCCES = 0

    def __init__(self, cmd_args):
        self.cmd_args = cmd_args
        self.instructions = []

    def error_xml_header(self):
        dom = xml.dom.minidom.parse(self.cmd_args.source)
        if dom.encoding == "UTF-8" and dom.version == "1.0":
            return True
        else:
            return False

    def get_instructions(self):
        return self.instructions

    def parse(self):
        if self.error_xml_header():
            return XMLParser.NOT_WELL_FORMED_XML
        try:
            tree = xml.etree.ElementTree.parse(self.cmd_args.source)
            root = tree.getroot()
        except:
            return XMLParser.NOT_WELL_FORMED_XML

        if root.tag == "program" and "language" in root.attrib and str.lower(root.attrib["language"]) == "ippcode19":
            if len(root.attrib) == 2 and ("description" not in root.attrib and "name" not in root.attrib):
                return XMLParser.UNSUPPORTED_XML_ELEMENT
            elif len(root.attrib) == 3 and ("description" not in root.attrib) or ("name" not in root.attrib):
                return XMLParser.UNSUPPORTED_XML_ELEMENT
        else:
            return XMLParser.UNSUPPORTED_XML_ELEMENT

        for xml_inst in root:
            if xml_inst.tag == "instruction":
                if "order" not in xml_inst.attrib and "opcode" not in xml_inst.attrib:
                    return XMLParser.UNSUPPORTED_XML_ELEMENT
                try:
                    order = int(xml_inst.attrib["order"])
                except ValueError:
                    return XMLParser.UNSUPPORTED_XML_ELEMENT
                self.instructions.append((xml_inst, order))
            else:
                return XMLParser.UNSUPPORTED_XML_ELEMENT

        return XMLParser.PARSE_SUCCES

    @staticmethod
    def is_label(label):
        if label[0][0] not in ["_", "-", "$", "&", "%", "*", "!", "?"] and not label[0][0].isalpha():
            return False
        for char in label:
            if char not in ["_", "-", "$", "&", "%", "*", "!", "?"] and not char.isalnum() and not char.isalpha():
                return False
        return True

    @staticmethod
    def is_type(type):
        return type in ["string", "bool", "int"]

    @staticmethod
    def is_variable(var):
        var = var.split("@")
        if len(var) != 2:
            return False
        else:
            return var[0] in ["GF", "LF", "TF"] and XMLParser.is_label(var[1])

    @staticmethod
    def is_int_constant(symb):
        try:
            int(symb)
        except TypeError:
            return False

        return True

    @staticmethod
    def is_bool_constant(symb):
        if symb in ["true", "false"]:
            return True

        return False

    @staticmethod
    def is_string_constant(symb):

        if symb is None:
            return True

        for char in symb:
            if ord(char) <= 32 and ord(char) == 35 and ord(char) == 92:
                return False

        return True

    @staticmethod
    def is_nil_constant(symb):
        return symb == "nil"

    @staticmethod
    def is_constant(symb):
        return XMLParser.is_int_constant(symb) or XMLParser.is_bool_constant(symb) or \
        XMLParser.is_string_constant(symb) or XMLParser.is_nil_constant(symb)

    @staticmethod
    def is_symbol(symb):
        return XMLParser.is_variable(symb) or XMLParser.is_constant(symb)
