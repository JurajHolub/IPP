#!/usr/bin/env python3

"""
@file argument_parser.py
@brief Parse arguments from command line and decide what to do.
@project FIT VUT - IPP interpret
@author Juraj Holub <xholub40>
@date March 2019
"""

import os

HELP_MESSAGE ="""Script load XML representation of input program and interprete it.
Usage: python3.6 interpret.py [Optionals]
Optionals:
    --help          :   Print this help message.
    --source=<file> :   Input file with IPPcode19 in XML representation. If not set then it is STDIN.
    --input=<file>  :   File with inputs for interpretation of source code. If not set then it is STDIN.
One of <source-file> or <input-file> must be set!"""

class ArgumentParser(object):

    ERROR = 1
    HELP = 2
    INTERPRET = 3

    def __init__(self):
        self.source = None
        self.input = None
        self.help = False
        self.error = False

    @property
    def get_source(self):
        return self.source

    @property
    def get_input(self):
        return self.input

    def parse_args(self, argv):
        for idx, arg in enumerate(argv):
            if arg == argv[0] and idx == 0:
                continue # skip script name
            elif arg == "--help":
                if len(argv) == 2:
                    self.help = True
                else:
                    self.error = True
                return
            elif arg.startswith("--source="):
                file = arg[len("--source="):]
                if os.path.isfile(file):
                    self.source = file
                else:
                    self.error = True
            elif arg.startswith("--input="):
                file = arg[len("--input="):]
                if os.path.isFile(file):
                    self.input = file
                else:
                    self.error = True
            else:
                self.error = True

        if self.source == None and self.input == None:
            self.error = True

    def what_to_do(self):
        if self.error:
            return ArgumentParser.ERROR
        elif self.help:
            return ArgumentParser.HELP
        else:
            return ArgumentParser.INTERPRET
