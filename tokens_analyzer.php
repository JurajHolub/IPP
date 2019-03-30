<?php

/**
 * @file tokens_analyzer.php
 * @brief Parse input string to tokens which are send to FSM.
 * @author Juraj Holub <xholub40@stud.fit.vutbr.cz>
 * @date February 2019
 * @project IPP 2018/2019
 */

class Tokens_Analyzer {

    var $key_words = array(
        ".IPPCODE19"    =>  "T_IPPCODE19",
        "CREATEFRAME"   =>  "T_INST_0",
        "PUSHFRAME"     =>  "T_INST_0",
        "POPFRAME"      =>  "T_INST_0",
        "RETURN"        =>  "T_INST_0",
        "BREAK"         =>  "T_INST_0",
        "DEFVAR"        =>  "T_INST_VAR",
        "POPS"          =>  "T_INST_VAR",
        "CALL"          =>  "T_INST_LABEL",
        "LABEL"         =>  "T_INST_LABEL",
        "JUMP"          =>  "T_INST_LABEL",
        "PUSHS"         =>  "T_INST_SYMB",
        "WRITE"         =>  "T_INST_SYMB",
        "EXIT"          =>  "T_INST_SYMB",
        "DPRINT"       =>   "T_INST_SYMB",
        "MOVE"          =>  "T_INST_VAR_SYMB",
        "INT2CHAR"      =>  "T_INST_VAR_SYMB",
        "STRLEN"        =>  "T_INST_VAR_SYMB",
        "TYPE"          =>  "T_INST_VAR_SYMB",
        "NOT"           =>  "T_INST_VAR_SYMB",
        "READ"          =>  "T_INST_VAR_TYPE",
        "ADD"           =>  "T_INST_VAR_SYMB_SYMB",
        "SUB"           =>  "T_INST_VAR_SYMB_SYMB",
        "MUL"           =>  "T_INST_VAR_SYMB_SYMB",
        "IDIV"          =>  "T_INST_VAR_SYMB_SYMB",
        "LT"            =>  "T_INST_VAR_SYMB_SYMB",
        "GT"            =>  "T_INST_VAR_SYMB_SYMB",
        "EQ"            =>  "T_INST_VAR_SYMB_SYMB",
        "AND"           =>  "T_INST_VAR_SYMB_SYMB",
        "OR"            =>  "T_INST_VAR_SYMB_SYMB",
        "STRI2INT"      =>  "T_INST_VAR_SYMB_SYMB",
        "CONCAT"        =>  "T_INST_VAR_SYMB_SYMB",
        "GETCHAR"       =>  "T_INST_VAR_SYMB_SYMB",
        "SETCHAR"       =>  "T_INST_VAR_SYMB_SYMB",
        "JUMPIFEQ"      =>  "T_INST_LABEL_SYMB_SYMB",
        "JUMPIFNEQ"     =>  "T_INST_LABEL_SYMB_SYMB"
    );

    public function is_type($token)
    {
        return (in_array($token, ["string", "bool", "int"]));
    }

    public function is_label($token)
    {
        if (strlen($token) == 0)
            return false;
        if (!in_array($token[0], ["_", "-", "$", "&", "%", "*", "!", "?"]) 
        and !ctype_alpha($token[0]))
            return false;

        $arr = str_split($token);
        foreach ($arr as $char)
            if (!ctype_alpha($char) and !ctype_alnum($char) 
            and !in_array($char, ["_", "-", "$", "&", "%", "*", "!", "?"]))
                return false;
        
        return true;
    }

    public function is_variable($token)
    {
        $list = explode("@", $token);

        if (count($list) == 2)
            return in_array($list[0], ["GF", "LF", "TF"]) and $this->is_label($list[1]);
        else
            return false;
    }

    public function is_int_constant($token)
    {
        $list = explode("@", $token);

        if (count($list) == 2)
        {
            return $list[0] === "int" and is_numeric($list[1]);
        }
        else
            return false;
    }

    public function is_bool_constant($token)
    {
        $list = explode("@", $token);
        if (count($list) == 2)
            return $list[0] === "bool" and in_array($list[1], ["true", "false"]);
        else
            return false;
    }

    public function is_string_constant($token)
    {
        //$list = explode("@", $token);
        $list = preg_split("/@/", $token, 2);

        if (count($list) != 2)
            return false;

        $arr = str_split($list[1]);
        foreach ($arr as $i)
            if (ord($i) <= 32 and ord($i) == 35 and ord($i) == 92)
                return false;

        return $list[0] === "string";
    }

    public function is_nil_constant($token)
    {
        return $token === "nil@nil";
    }

    public function is_constant($token)
    {
        return $this->is_int_constant($token) or $this->is_string_constant($token)
            or $this->is_bool_constant($token) or $this->is_nil_constant($token);
    }

    public function is_symbol($token)
    {
        return $this->is_variable($token) or $this->is_constant($token);
    }

    public function is_comment($token)
    {
        return $token === "#";
    }

    public function is_white_space($token)
    {
        return in_array($token, ["\t", " "]);
    }

    public function is_new_line($token)
    {
        return $token === "\n";
    }

    public function is_key_word($token)
    {
        $token = strtoupper($token);
        return array_key_exists($token, $this->key_words);
    }

    public function parse_token($token)
    {
        //echo "Parsed token: \"" . $token . "\"\n";
        $ret = new Token();

        if ($this->is_key_word($token))
        {
            $token = strtoupper($token);
            $ret->id = $this->key_words[$token];
        }
        else if ($this->is_type($token))
        {
            $ret->id = "T_TYPE";
        }
        else if ($this->is_label($token))
        {
            $ret->id = "T_LABEL";
        }
        else if ($this->is_variable($token))
        {
            $ret->id = "T_VAR";
        }
        else if ($this->is_symbol($token))
        {
            $ret->id = "T_SYMB";
        }
        else if ($this->is_new_line($token))
        {
            $ret->id = "T_NEW_LINE";
        }
        else if ($this->is_white_space($token))
        {
            $ret->id = "T_WHITE_SPACE";
        }
        else if ($this->is_comment($token))
        {
            $ret->id = "T_COMMENT";
        }
        else
        {
            $ret->id = "T_ERROR";
        }

        $ret->val = $token;
        return $ret;
    }

    public function get_token()
    {
        $token = "";
        static $curr_char = "";

        if (in_array($curr_char, DELIMETERS))
        {
            $last_char = $curr_char;
            $curr_char = "";
            return $this->parse_token($last_char);
        }

        while (!feof(STDIN))
        {
            $curr_char = fgetc(STDIN);

            if ($curr_char === "#") # eat comment
            {
                while(!feof(STDIN) and !in_array($curr_char, NEW_LINE))
                    $curr_char = fgetc(STDIN);
                if ($token === "")
                {
                    $last_char = $curr_char;
                    $curr_char = "";
                    return $this->parse_token($last_char);
                }
                else
                    return $this->parse_token($token);
            }

            if (in_array($curr_char, DELIMETERS))
            {
                if ($token !== "")
                    return $this->parse_token($token);
            }
            else
            {
                $token .= $curr_char;
            }
        }

        if ($token !== "")
            return $this->parse_token($token);
        $ret = new Token();
        $ret->id = "T_EOF";
        $ret->val = "";
        return $ret;
    }
}

?>
