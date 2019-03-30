<?php

/**
 * @file test_cmd_args.php
 * @brief Parser of test.php script input command line arguments.
 * @author Juraj Holub <xholub40@stud.fit.vutbr.cz>
 * @date February 2019
 * @project IPP 2018/2019
 */

function startsWith($pattern, $str)
{
    return substr($str, 0, strlen($pattern)) === $pattern;
}

function endsWith($pattern, $str)
{
    if (strlen($pattern) == 0)
        return true;

    return substr($str, -strlen($pattern)) === $pattern;
}

class TestCmdArgs {
    public $help;
    public $directory;
    public $recursive;
    public $parse_script;
    public $parse_script_file;
    public $int_script;
    public $int_script_file;
    public $parse_only;
    public $int_only;
    public $unknown;
    public $xml;
    public $xml_file;

    function __construct($argv, $argc)
    {
        $this->argv = $argv;
        $this->argc = $argc;
        $this->help = "NOT_SET";
        $this->dir = "NOT_SET";
        $this->dir_path = "./";
        $this->recursive = "NOT_SET";
        $this->parse_script = "NOT_SET";
        $this->parse_script_file = "parse.php";
        $this->int_script = "NOT_SET";
        $this->int_script_file = "interpret.py";
        $this->parse_only = "NOT_SET";
        $this->int_only = "NOT_SET";
        $this->unknown = "NOT_SET";
        $this->xml = "NOT_SET";
        $this->xml_file = "/pub/courses/ipp/jexamxml/jexamxml.jar";
    }

    public function parse_args()
    {
        foreach ($this->argv as $arg)
        {
            if ($arg === "test.php")
                continue; // skip script name

            if ($arg === "--help")
                $this->help = "SET";
            else if (startsWith("--directory=", $arg))
                $this->parse_directory($arg); 
            else if ($arg === "--recursive")
                $this->recursive = "SET";
            else if (startsWith("--parse-script=", $arg))
                $this->parser_file($arg);
            else if (startsWith("--int-script=", $arg))
                $this->int_file($arg);
            else if ($arg === "--parse-only")
                $this->parse_only = "SET";
            else if ($arg === "--int-only")
                $this->int_only = "SET";
            else if (startsWith("--xml=", $arg))
                $this->parse_xml($arg);
            else
                $this->unknown = "ERROR_SET";
        }
    }

    public function parse_directory($arg)
    {
        $list = explode("=", $arg);
        if (count($list) == 2 and is_dir($list[1]))
        {
            $this->dir_path = $list[1];    
            $this->dir = "SET";
        }
        else
            $this->dir = "ERROR_SET";    
    }

    public function int_file($arg)
    {
        $list = explode("=", $arg);
        if (count($list) == 2 and is_file($list[1]))
        {
            $this->int_script = "SET";    
            $this->int_script_file = $list[1];    
        }
        else
            $this->int_script = "ERROR_SET";    
    }

    public function parse_file($arg)
    {
        $list = explode("=", $arg);
        if (count($list) == 2 and is_file($list[1]))
        {
            $this->parse_script = "SET";    
            $this->parse_script_file = $list[1];    
        }
        else
            $this->parse_script = "ERROR_SET";    
    }

    public function parse_xml($arg)
    {
        $list = explode("=", $arg);
        if (count($list) == 2 and is_file($list[1]))
        {
            $this->xml = "SET";    
            $this->xml_file = $list[1];    
        }
        else
            $this->xml = "ERROR_SET";    
    }

    public function what_to_do()
    {
        $this->parse_args();
        if ($this->argc == 1)
            return "ERROR";
        if ($this->unknown == "ERROR_SET")
            return "ERROR";
        if ($this->help === "SET" and $this->argc != 2)
            return "ERROR";
        if ($this->directory === "ERROR_SET" or $this->int_script === "ERROR_SET"
            or $this->parse_script === "ERROR_SET")
            return "ERROR";
        if ($this->parse_script === "SET" and $this->int_only === "SET")
            return "ERROR";
        if ($this->int_script === "SET" and $this->parse_only === "SET")
            return "ERROR";
        if ($this->int_only === "SET" and $this->parse_only === "SET")
            return "ERROR";
        if ($this->xml === "ERROR_SET")
            return "ERROR";
        
        if ($this->help === "SET")
            return "HELP";
        if ($this->int_only === "SET")
            return "TEST_INT_ONLY";
        if ($this->parse_only === "SET")
            return "TEST_PARSE_ONLY";
        
        return "TEST_BOTH";
    }
}

?>
