<?php

class HTML5_Generator {

    public $tests = array();
    public $succ = 0;
    public $output = "<table>\n".
            "<tr>\n".
            "  <th>Test result</th>\n".
            "  <th>Test name</th>\n".
            "  <th>Expected return value</th>\n".
            "  <th>Test return value</th>\n".
            "</tr>\n";

    public function gen_test($test_name, $success, $ret_val, $expected_ret_val)
    {
        array_push($this->tests, $success);
        if ($success)
        {
            $this->succ += 1;
            $this->output .= "<tr>\n";
            $this->output .= "<td><font color=\"green\">&#10004;</font></td>\n";
            $this->output .= "<td><font color=\"green\">".$test_name."</font></td>\n";
            $this->output .= "<td><font color=\"green\">".$expected_ret_val."</font></td>\n";
            $this->output .= "<td><font color=\"green\">".$ret_val."</font></td>\n";
            $this->output .= "</tr>\n";
        }
        else
        {
            $this->output .= "<tr>\n";
            $this->output .= "<td><font color=\"red\">&#10006;</font></td>\n";
            $this->output .= "<td><font color=\"red\">".$test_name."</font></td>\n";
            $this->output .= "<td><font color=\"red\">".$expected_ret_val."</font></td>\n";
            $this->output .= "<td><font color=\"red\">".$ret_val."</font></td>\n";
            $this->output .= "</tr>\n";
        }
    }

    public function gen_tests()
    {
        $succ = $this->succ;
        $total = count($this->tests);
        $percentage = round($succ / $total * 100);
        print(
            "<!DOCTYPE html>\n".
            "<html>\n".
            "<head>\n".
            "<style>\n".
            "table {\n".
            "  font-family: arial, sans-serif;\n".
            "  border-collapse: collapse;\n".
            "  width: 100%;\n".
            "}\n".
            "\n".
            "td, th {\n".
            "  border: 1px solid #dddddd;\n".
            "  text-align: left;\n".
            "  padding: 8px;\n".
            "}\n".
            "\n".
            "tr:nth-child(even) {\n".
            "  background-color: #dddddd;\n".
            "}\n".
            "</style>\n".
            "</head>\n".
            "<body\n"
        );
        print("<h1><font size='12'>Total tests success ".$succ."/".$total." [".$percentage."%]</font></h1>\n");
        print($this->output);
        print(  "</table>\n".
                "</body>\n".
                "</html>\n");
    }
}

?>
