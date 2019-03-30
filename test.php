<?php

/**
 * @file test.php
 * @brief Test script of parser an interpret.
 * @author Juraj Holub <xholub40@stud.fit.vutbr.cz>
 * @date February 2019
 * @project IPP 2018/2019
 */

include 'test_cmd_args.php';
include 'html5_generator.php';

$TEST_HELP = <<<EOS
Script test.php automtaicly test applications parse.php and interpret.py. Script
automaticly search given directory with tests and validate functionality of both
application and generate summary in HTML 5 to stdout.
Usage:
    --help                  : Print this help message.
    --directory=<path>      : Directory where scritp search tests. Implicit value is
                             actual directory.
    --recursive             : Script search in given directory recursively.
    --parse-script=<file>   : Script in php7.3 whitch analyze IPPcode19. Implicit 
                             value is parse.php.
    --int-script=<file>     : Script in python3.6 whitch interpret XML reprezentation
                              of IPPcode19.
                              Implicit value is interpret.py.
    --parse-only            : Testing only script for analyze IPPcode19. Cant't be 
                             combinated with --int-script.
    --int-only              : Testing only script for interpret XML reprezentation
                              of IPPcode19. Can't be combinated with --parse-script.
    --xml=<jar-file>        : Jar file A7Soft JExamXML used for comparing XML. 
                              Imlicit value "/pub/courses/ipp/jexamxml/jexamxml.jar"

EOS;

class AllTests {
    public $tests = array();

    public function search_test_files($dir, $recursive)
    {
        if ($recursive == "SET")
            $dir_iter = new RecursiveIteratorIterator(new RecursiveDirectoryIterator($dir));
        else
            $dir_iter = new RecursiveDirectoryIterator($dir);
        foreach ($dir_iter as $file)
        {
            $parse_file = preg_split("/\.(?=[^\.]*$)/", $file);
            if (count($parse_file) == 2 and $parse_file[1] === "src")
            {
                array_push($this->tests, $parse_file[0]);
            }
        }
    }
}

$cmd_args = new TestCmdArgs($argv, $argc);
switch ($cmd_args->what_to_do())
{
    case "ERROR":
        exit(10);
    break;
    case "HELP":
        echo $TEST_HELP;
    break;
    case "TEST_INT_ONLY":
        $tests = new AllTests();
        $tests->search_test_files($cmd_args->dir_path, $cmd_args->recursive);
        $html_gen = new HTML5_Generator();

        $html_gen->gen_header();
        foreach ($tests->tests as $test)
        {
            $src = $test . ".src";
            $in = $test . ".in";
            $out = $test . ".out";
            $rc = $test . ".rc";

            if (!file_exists($in))
                exec("touch ".$in);
            if (!file_exists($out))
                exec("touch ".$out);

            $interpret = "python3.6 ".$cmd_args->int_script_file.
                " --source=" . $src ." --input=". $in . " < " . $in;
            exec($interpret, $my_output, $int_ret_val);
            $my_output = implode("\n", $my_output);

            $expected_output = file_get_contents($out);

            if (is_readable($rc))
            {
                $expected_rc = fopen($rc, "r");
                fscanf($expected_rc,"%d", $expected_int_ret_val);
                fclose($expected_rc);
            }
            else
                $expected_int_ret_val = 0;


            if ($int_ret_val == $expected_int_ret_val)
            {
                if ($int_ret_val == 0)
                {
                    if ($expected_output !== $my_output)
                        $html_gen->gen_test($test, False);
                    else
                        $html_gen->gen_test($test, True);
                }
                else
                    $html_gen->gen_test($test, True);
            }
            else
                $html_gen->gen_test($test, False);
        }
        $html_gen->gen_end();
    break;
    case "TEST_PARSE_ONLY":

        //execute parser
        $tests = new AllTests();
        $tests->search_test_files($cmd_args->dir_path, $cmd_args->recursive);
        $html_gen = new HTML5_Generator();

        $html_gen->gen_header();
        foreach ($tests->tests as $test)
        {
            $src = $test . ".src";
            $in = $test . ".in";
            $out = $test . ".out";
            $my_out = $test . ".my_out";
            $rc = $test . ".rc";

            $parse = "php7.3 ".$cmd_args->parse_script_file.
            " <" . $src .">". $my_out;
            exec($parse, $dump, $parse_ret_val);

            $jexamxml = "java -jar ". $cmd_args->xml_file . " " . $out . " " . $my_out;
            exec($jexamxml, $dump, $jexam_ret_val);

            if (is_readable($rc))
            {
                $expected_rc = fopen($rc, "r");
                fscanf($expected_rc,"%d", $expected_parse_ret_val);
                fclose($expected_rc);
            }
            else
                $expected_parse_ret_val = 0;

            if ($parse_ret_val != $expected_parse_ret_val)
                if (in_array($parse_ret_val, [21,22,23]) and in_array($expected_parse_ret_val, [21,22,23]))
                    $html_gen->gen_test($test, True);
                else
                    $html_gen->gen_test($test, False);
            else
            {
                if ($parse_ret_val != 0)
                    $html_gen->gen_test($test, True);
                else if ($parse_ret_val == 0 and $jexam_ret_val == 0)
                    $html_gen->gen_test($test, True);
                else
                    $html_gen->gen_test($test, False);
            }

            //exec("rm ".$my_out);
        }
        $html_gen->gen_end();

    break;
    case "TEST_BOTH":
        echo "interpret.py not implemented yet.";
    break;
}


?>
