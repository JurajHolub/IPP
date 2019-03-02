<?php

/**
 * @file parser.php
 * @brief Analyzator of IPPcode19 (parser) implemented like finite state machine.
 * @author Juraj Holub <xholub40@stud.fit.vutbr.cz>
 * @date February 2019
 * @project IPP 2018/2019
 */

include 'tokens_analyzer.php';
include 'xml_generator.php';

const DELIMETERS = array("\t", " ", "\n");
const WHITE_SPACE = array("\t", " ");
const NEW_LINE = array("\n");
const INST_OP_0 = array("CREATEFRAME", "PUSHFRAME", "POPFRAME", "RETURN", "BREAK");

$help = <<<EOS
Filter script parse.php read input IPPcode19 source code from stdin and check
lexical and syntactical correctnes of code and write XML representation of this
program to stdout.
Usage:
    --help : Print this message.

EOS;

class Token {
    public $id;
    public $val;
}

//handle parameters
if ($argc == 2 and $argv[1] === "--help")
{
    echo($help);
    exit(0);
}
if ($argc > 2)
    exit(10);


$generator = new XML_Generator();
$inst = array();
$token_analyzer = new Tokens_Analyzer();
$state = "S_BEGIN";
$token = $token_analyzer->get_token();
while ($token->id !== "T_EOF")
{
    //fwrite(STDERR, "STATE: " . $state . " \"" . $token->id . "\" \"" . $token->val . "\"\n");

    //TODO FSM
    switch ($state)
    {
        case "S_BEGIN":
            if ($token->id === "T_IPPCODE19")
                $state = "S_WHITE_SPACE";
            else
                $state = "S_BEGIN";
        break;
        case "S_WHITE_SPACE":
            if ($token->id === "T_WHITE_SPACE")
                $state = "S_WHITE_SPACE";
            else if ($token->id === "T_NEW_LINE")
                $state = "S_INST_BEGIN";
            else
                $state = "S_ERROR";
        break;
        case "S_INST_BEGIN":
            $inst = array(); // clear instruction
            if ($token->id === "T_INST_0")
            {
                array_push($inst, $token);
                $generator->gen_inst_0($inst);
                $state = "S_WHITE_SPACE";
            }
            else if ($token->id === "T_WHITE_SPACE")
                $state = "S_INST_BEGIN";
            else if ($token->id === "T_INST_VAR")
            {
                array_push($inst, $token);
                $state = "S_INST_VAR_0";
            }
            else if ($token->id === "T_INST_SYMB")
            {
                array_push($inst, $token);
                $state = "S_INST_SYMB_0";
            }
            else if ($token->id === "T_INST_LABEL")
            {
                array_push($inst, $token);
                $state = "S_INST_LABEL_0";
            }
            else if ($token->id === "T_INST_VAR_SYMB")
            {
                array_push($inst, $token);
                $state = "S_INST_VAR_SYMB_0";
            }
            else if ($token->id === "T_INST_VAR_TYPE")
            {
                array_push($inst, $token);
                $state = "S_INST_VAR_TYPE_0";
            }
            else if ($token->id === "T_INST_VAR_SYMB_SYMB")
            {
                array_push($inst, $token);
                $state = "S_INST_VAR_SYMB_SYMB_0";
            }
            else if ($token->id === "T_INST_LABEL_SYMB_SYMB")
            {
                array_push($inst, $token);
                $state = "S_INST_LABEL_SYMB_SYMB_0";
            }
            else if ($token->id === "T_NEW_LINE")
                $state = "S_INST_BEGIN";
            else
                $state = "S_ERROR_INSTR";
        break;
        case "S_INST_VAR_0":
            if ($token->id === "T_WHITE_SPACE")
                $state = "S_INST_VAR_1";
            else
                $state = "S_ERROR";
        break;
        case "S_INST_VAR_1":
            if ($token->id === "T_VAR")
            {
                array_push($inst, $token);
                $generator->gen_inst_var($inst);
                $state = "S_WHITE_SPACE";
            }
            else if ($token->id === "T_WHITE_SPACE")
                $state = "S_INST_VAR_1";
            else
                $state = "S_ERROR";
        break;
        case "S_INST_SYMB_0":
            if ($token->id === "T_WHITE_SPACE")
                $state = "S_INST_SYMB_1";
            else
                $state = "S_ERROR";
        break;
        case "S_INST_SYMB_1":
            if ($token->id === "T_SYMB" or $token->id === "T_VAR")
            {
                array_push($inst, $token);
                $generator->gen_inst_symb($inst);
                $state = "S_WHITE_SPACE";
            }
            else if ($token->id === "T_WHITE_SPACE")
                $state = "S_INST_SYMB_1";
            else
                $state = "S_ERROR";
        break;
        case "S_INST_LABEL_0":
            if ($token->id === "T_WHITE_SPACE")
                $state = "S_INST_LABEL_1";
            else
                $state = "S_ERROR";
        break;
        case "S_INST_LABEL_1":
            if ($token->id === "T_LABEL")
            {
                array_push($inst, $token);
                $generator->gen_inst_label($inst);
                $state = "S_WHITE_SPACE";
            }
            else if ($token->id === "T_WHITE_SPACE")
                $state = "S_INST_LABEL_1";
            else
                $state = "S_ERROR";
        break;
        case "S_INST_VAR_SYMB_0":
            if ($token->id === "T_WHITE_SPACE")
                $state = "S_INST_VAR_SYMB_1";
            else
                $state = "S_ERROR";
        break;
        case "S_INST_VAR_SYMB_1":
            if ($token->id === "T_VAR")
            {
                array_push($inst, $token);
                $state = "S_INST_VAR_SYMB_2";
            }
            else if ($token->id === "T_WHITE_SPACE")
                $state = "S_INST_VAR_SYMB_1";
            else
                $state = "S_ERROR";
        break;
        case "S_INST_VAR_SYMB_2":
            if ($token->id === "T_WHITE_SPACE")
                $state = "S_INST_VAR_SYMB_3";
            else
                $state = "S_ERROR";
        break;
        case "S_INST_VAR_SYMB_3":
            if ($token->id === "T_WHITE_SPACE")
                $state = "S_INST_VAR_SYMB_3";
            else if ($token->id === "T_SYMB" or $token->id === "T_VAR")
            {
                array_push($inst, $token);
                $generator->gen_inst_var_symb($inst);
                $state = "S_WHITE_SPACE";
            }
            else
                $state = "S_ERROR";
        break;
        case "S_INST_VAR_TYPE_0":
            if ($token->id === "T_WHITE_SPACE")
                $state = "S_INST_VAR_TYPE_1";
            else
                $state = "S_ERROR";
        break;
        case "S_INST_VAR_TYPE_1":
            if ($token->id === "T_VAR")
            {
                array_push($inst, $token);
                $state = "S_INST_VAR_TYPE_2";
            }
            else if ($token->id === "T_WHITE_SPACE")
                $state = "S_INST_VAR_TYPE_1";
            else
                $state = "S_ERROR";
        break;
        case "S_INST_VAR_TYPE_2":
            if ($token->id === "T_WHITE_SPACE")
                $state = "S_INST_VAR_TYPE_3";
            else
                $state = "S_ERROR";
        break;
        case "S_INST_VAR_TYPE_3":
            if ($token->id === "T_WHITE_SPACE")
                $state = "S_INST_VAR_TYPE_3";
            else if ($token->id === "T_TYPE")
            {
                array_push($inst, $token);
                $generator->gen_inst_var_type($inst);
                $state = "S_WHITE_SPACE";
            }
            else
                $state = "S_ERROR";
        break;
        case "S_INST_VAR_SYMB_SYMB_0":
            if ($token->id === "T_WHITE_SPACE")
                $state = "S_INST_VAR_SYMB_SYMB_1";
            else
                $state = "S_ERROR";
        break;
        case "S_INST_VAR_SYMB_SYMB_1":
            if ($token->id === "T_VAR")
            {
                array_push($inst, $token);
                $state = "S_INST_VAR_SYMB_SYMB_2";
            }
            else if ($token->id === "T_WHITE_SPACE")
                $state = "S_INST_VAR_SYMB_SYMB_1";
            else
                $state = "S_ERROR";
        break;
        case "S_INST_VAR_SYMB_SYMB_2":
            if ($token->id === "T_WHITE_SPACE")
                $state = "S_INST_VAR_SYMB_SYMB_3";
            else
                $state = "S_ERROR";
        break;
        case "S_INST_VAR_SYMB_SYMB_3":
            if ($token->id === "T_WHITE_SPACE")
                $state = "S_INST_VAR_SYMB_SYMB_3";
            else if ($token->id === "T_SYMB" or $token->id === "T_VAR")
            {
                array_push($inst, $token);
                $state = "S_INST_VAR_SYMB_SYMB_4";
            }
            else
                $state = "S_ERROR";
        break;
        case "S_INST_VAR_SYMB_SYMB_4":
            if ($token->id === "T_WHITE_SPACE")
                $state = "S_INST_VAR_SYMB_SYMB_4";
            else if ($token->id === "T_SYMB" or $token->id === "T_VAR")
            {
                array_push($inst, $token);
                $generator->gen_inst_var_symb_symb($inst);
                $state = "S_WHITE_SPACE";
            }
            else
                $state = "S_ERROR";
        break;
        case "S_INST_LABEL_SYMB_SYMB_0":
            if ($token->id === "T_WHITE_SPACE")
                $state = "S_INST_LABEL_SYMB_SYMB_1";
            else
                $state = "S_ERROR";
        break;
        case "S_INST_LABEL_SYMB_SYMB_1":
            if ($token->id === "T_LABEL")
            {
                array_push($inst, $token);
                $state = "S_INST_LABEL_SYMB_SYMB_2";
            }
            else if ($token->id === "T_WHITE_SPACE")
                $state = "S_INST_LABEL_SYMB_SYMB_1";
            else
                $state = "S_ERROR";
        break;
        case "S_INST_LABEL_SYMB_SYMB_2":
            if ($token->id === "T_WHITE_SPACE")
                $state = "S_INST_LABEL_SYMB_SYMB_3";
            else
                $state = "S_ERROR";
        break;
        case "S_INST_LABEL_SYMB_SYMB_3":
            if ($token->id === "T_WHITE_SPACE")
                $state = "S_INST_LABEL_SYMB_SYMB_3";
            else if ($token->id === "T_SYMB" or $token->id === "T_VAR")
            {
                array_push($inst, $token);
                $state = "S_INST_LABEL_SYMB_SYMB_4";
            }
            else
                $state = "S_ERROR";
        break;
        case "S_INST_LABEL_SYMB_SYMB_4":
            if ($token->id === "T_WHITE_SPACE")
                $state = "S_INST_LABEL_SYMB_SYMB_4";
            else if ($token->id === "T_SYMB" or $token->id === "T_VAR")
            {
                array_push($inst, $token);
                $generator->gen_inst_label_symb_symb($inst);
                $state = "S_WHITE_SPACE";
            }
            else
                $state = "S_ERROR";
        break;
        case "S_ERROR_INST":
            $state = "S_ERROR_INST"; // syntax or lexical error
        break;
        default:
            $state = "S_ERROR"; // syntax or lexical error
    }
    //TODO FSM

    $token = $token_analyzer->get_token();
}

if ($state === "S_ERROR_INST")
    exit(22);
else if ($state === "S_ERROR")
    exit(23);
else if ($state === "S_BEGIN") // .IPPcode19 missing
    exit(21);
else
    $generator->gen_XML();

?>
