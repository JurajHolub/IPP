<?php

/**
 * @file xml_generator.php
 * @brief Generate XML representation of IPPcode19 with DOMDocument library.
 * @author Juraj Holub <xholub40@stud.fit.vutbr.cz>
 * @date February 2019
 * @project IPP 2018/2019
 */

class XML_Generator {
    public $xml;
    public $inst_cnt;
    public $program;
    function __construct()
    {
        $this->inst_cnt = 1;
        $this->xml = new DOMDocument("1.0", "UTF-8");
        $this->xml->formatOutput = true;
        $this->program = $this->xml->createElement("program");
        $this->program->setAttribute("language", "IPPcode19");
        $this->xml->appendChild($this->program);
    }

    private function get_elem($token)
    {
        $list = explode("@", $token);
        
        if (in_array($list[0], ["nil", "string", "int", "bool"]))
            $elem["type"] = $list[0];
        if (in_array($list[0], ["GF", "LF", "TF"]))
            $elem["type"] = "var";
        if (in_array($list[0], ["nil", "string", "int", "bool"]))
            $elem["arg"] = $list[1];
        if (in_array($list[0], ["GF", "LF", "TF"]))
            $elem["arg"] = $token;
        
        return $elem;
    }


    public function gen_inst_0($tokens)
    {
        //fwrite(STDERR, $tokens[0]->val."\n");

        $inst = $this->xml->createElement("instruction");
        $inst->setAttribute("order", $this->inst_cnt);
        $inst->setAttribute("opcode", $tokens[0]->val);
        $this->program->appendChild($inst);
        $this->inst_cnt += 1;
    }

    public function gen_inst_var($tokens)
    {
        //fwrite(STDERR, $tokens[0]->val."\n");

        $inst = $this->xml->createElement("instruction");
        $inst->setAttribute("order", $this->inst_cnt);
        $inst->setAttribute("opcode", $tokens[0]->val);
        $elem = $this->get_elem($tokens[1]->val);
        $arg1 = $this->xml->createElement("arg1", htmlspecialchars($elem["arg"]));
        $arg1->setAttribute("type", "var");
        $inst->appendChild($arg1);
        $this->program->appendChild($inst);
        $this->inst_cnt += 1;
    }
    
    public function gen_inst_symb($tokens)
    {
        $inst = $this->xml->createElement("instruction");
        $inst->setAttribute("order", $this->inst_cnt);
        $inst->setAttribute("opcode", $tokens[0]->val);
        $elem = $this->get_elem($tokens[1]->val);
        $arg1 = $this->xml->createElement("arg1", htmlspecialchars($elem["arg"]));
        $arg1->setAttribute("type", $elem["type"]);
        $inst->appendChild($arg1);
        $this->program->appendChild($inst);
        $this->inst_cnt += 1;

        //fwrite(STDERR, $tokens[0]->val." ".$elem["type"]. "\n");
    }

    public function gen_inst_label($tokens)
    {
        //fwrite(STDERR, $tokens[0]->val."\n");

        $inst = $this->xml->createElement("instruction");
        $inst->setAttribute("order", $this->inst_cnt);
        $inst->setAttribute("opcode", $tokens[0]->val);
        $arg1 = $this->xml->createElement("arg1", htmlspecialchars($tokens[1]->val));
        $arg1->setAttribute("type", "label");
        $inst->appendChild($arg1);
        $this->program->appendChild($inst);
        $this->inst_cnt += 1;
    }

    public function gen_inst_var_symb($tokens)
    {
        $inst = $this->xml->createElement("instruction");
        $inst->setAttribute("order", $this->inst_cnt);
        $inst->setAttribute("opcode", $tokens[0]->val);
        $arg1 = $this->xml->createElement("arg1", htmlspecialchars($tokens[1]->val));
        $arg1->setAttribute("type", "var");
        $elem = $this->get_elem($tokens[2]->val);
        $arg2 = $this->xml->createElement("arg2", htmlspecialchars($elem["arg"]));
        $arg2->setAttribute("type", htmlspecialchars($elem["type"]));
        $inst->appendChild($arg1);
        $inst->appendChild($arg2);
        $this->program->appendChild($inst);
        $this->inst_cnt += 1;

        //fwrite(STDERR, $tokens[0]->val." ". $elem["arg"]."\n");
    }

    public function gen_inst_var_type($tokens)
    {
        $inst = $this->xml->createElement("instruction");
        $inst->setAttribute("order", $this->inst_cnt);
        $inst->setAttribute("opcode", $tokens[0]->val);
        $arg1 = $this->xml->createElement("arg1", htmlspecialchars($tokens[1]->val));
        $arg1->setAttribute("type", "var");
        $arg2 = $this->xml->createElement("arg2", $tokens[2]->val);
        $arg2->setAttribute("type", "type");
        $inst->appendChild($arg1);
        $inst->appendChild($arg2);
        $this->program->appendChild($inst);
        $this->inst_cnt += 1;

        //fwrite(STDERR, $tokens[0]->val." ". $tokens[2]->val."\n");
    }

    public function gen_inst_var_symb_symb($tokens)
    {
        $inst = $this->xml->createElement("instruction");
        $inst->setAttribute("order", $this->inst_cnt);
        $inst->setAttribute("opcode", $tokens[0]->val);
        $elem1 = $this->get_elem($tokens[1]->val);
        $elem2 = $this->get_elem($tokens[2]->val);
        $elem3 = $this->get_elem($tokens[3]->val);
        $arg1 = $this->xml->createElement("arg1", htmlspecialchars($elem1["arg"]));
        $arg1->setAttribute("type", $elem1["type"]);
        $arg2 = $this->xml->createElement("arg2", htmlspecialchars($elem2["arg"]));
        $arg2->setAttribute("type", $elem2["type"]);
        $arg3 = $this->xml->createElement("arg3", htmlspecialchars($elem3["arg"]));
        $arg3->setAttribute("type", $elem3["type"]);
        $inst->appendChild($arg1);
        $inst->appendChild($arg2);
        $inst->appendChild($arg3);
        $this->program->appendChild($inst);
        $this->inst_cnt += 1;

        //fwrite(STDERR, $tokens[0]->val." ". $elem1["arg"]." ".$elem2["arg"]." ".$elem3["arg"]."\n");
    }

    public function gen_inst_label_symb_symb($tokens)
    {
        $inst = $this->xml->createElement("instruction");
        $inst->setAttribute("order", $this->inst_cnt);
        $inst->setAttribute("opcode", $tokens[0]->val);
        $elem2 = $this->get_elem($tokens[2]->val);
        $elem3 = $this->get_elem($tokens[3]->val);
        $arg1 = $this->xml->createElement("arg1", htmlspecialchars($tokens[1]->val));
        $arg1->setAttribute("type", "label");
        $arg2 = $this->xml->createElement("arg2", htmlspecialchars($elem2["arg"]));
        $arg2->setAttribute("type", $elem2["type"]);
        $arg3 = $this->xml->createElement("arg3", htmlspecialchars($elem3["arg"]));
        $arg3->setAttribute("type", $elem3["type"]);
        $inst->appendChild($arg1);
        $inst->appendChild($arg2);
        $inst->appendChild($arg3);
        $this->program->appendChild($inst);
        $this->inst_cnt += 1;

        //fwrite(STDERR, $tokens[0]->val." ". $tokens[1]->val." ".$elem2["arg"]." ".$elem3["arg"]."\n");
    }

    public function gen_XML()
    {
        echo $this->xml->saveXML();
    }
}

?>
