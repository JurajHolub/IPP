<?php

class HTML5_Generator {

    public $tests = array();
    public $succ = 0;

    public function gen_test($test_name, $success)
    {
        array_push($this->tests, $success);
        if ($success)
        {
            $this->succ += 1;
            print("  <li>".$test_name." : SUCCESS</li>\n");
        }
        else
            print("  <li>".$test_name." : FAIL</li>\n");
    }

    public function gen_header()
    {
        print(  "<!DOCTYPE html>\n".
                "<html>\n".
                "<head>\n".
                "<meta charset=\"UTF-8\">\n".
                "<title>IPP tests</title>\n".
                "</head>\n".
                "<body>\n");
        print("<ul>\n");

    }

    public function gen_end()
    {
        $succ = $this->succ;
        $total = count($this->tests);
        $percentage = round($succ / $total * 100);
        print("<ul>\n");
        print("<h1>Total tests success ".$succ."/".$total." [".$percentage."%]</h1>\n");
        print(  "</body>\n".
                "</html>\n");
    }
}

?>
