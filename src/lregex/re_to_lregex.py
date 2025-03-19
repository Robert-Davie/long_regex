from string import punctuation, ascii_letters, digits
from .lregex_to_regex import LregexSyntaxException


METACHARACTERS = r".|*+?()[]{}^$-"
NON_METACHARACTERS = "".join([i for i in ascii_letters + digits + punctuation if i not in (METACHARACTERS + "\\")])


def re_to_lregex(string_in: str) -> str:
    pointer = 0
    iteration_counter = 0  # prevent infinite loop
    res = []
    choice_mode = False
    while pointer < len(string_in):
        if iteration_counter > pointer:
            raise Exception("LRegex Failure: infinite loop detected")
        iteration_counter += 1
        current_letter = string_in[pointer]
        if choice_mode and current_letter == '-':
            if res[-1][0] == "%":
                temp = res[-1][-1]
                res[-1] = res[-1][:-1]
                if res[-1] == "%":
                    res.pop()
                res.append("range")
                res.append("(")
                res.append(temp)
                res.append(string_in[pointer + 1])
                res.append(")")
                pointer += 2
        if current_letter in NON_METACHARACTERS:
            temp = f"%{current_letter}"
            pointer += 1
            while pointer < len(string_in) and string_in[pointer] in NON_METACHARACTERS:
                temp = temp + string_in[pointer]
                pointer += 1
            res.append(temp)
            continue
        match string_in[pointer]:
            case '*' | '?' | '+':
                # single character quantifiers
                if string_in[pointer] == '*':
                    res.append("min0")
                elif string_in[pointer] == '?':
                    res.append("max1")
                else:
                    res.append('min1')
                pointer += 1
                if pointer < len(string_in):
                    if string_in[pointer] == "?":
                        res.append("x_greedy")
                        pointer += 1
                    elif string_in[pointer] == "+":
                        res.append("x_backtrack")
                        pointer += 1
            case ' ':
                res.append("space")
                pointer += 1
            case '.':
                res.append("any_char")
                pointer += 1
            case '|':
                res.append("or")
                pointer += 1
            case '^':
                res.append("start")
                pointer += 1
            case '$':
                res.append("end")
                pointer += 1
            case '{':
                pointer += 1
                temp = ""
                while string_in[pointer] != "}":
                    temp = temp + string_in[pointer]
                    pointer += 1
                if "," in temp:
                    if len(temp) >= 1 and temp[-1] == ',':
                        res.append("repeat_min")
                        res.append(temp[:-1])
                    else:
                        t = temp.split(',')
                        res.append("repeat_between")
                        res.append("(")
                        res.append(t[0])
                        res.append(t[1])
                        res.append(")")
                else:
                    res.append("repeat_exactly")
                    res.append(temp)
                pointer += 1
            case '(':
                if string_in[pointer + 1] == '?':
                    match string_in[pointer + 2]:
                        case ':':
                            res.append("x_capture")
                            res.append("(")
                            pointer += 3
                        case '=':
                            res.append("look_ahead")
                            res.append("(")
                            pointer += 3
                        case '!':
                            res.append("x_look_ahead")
                            res.append("(")
                            pointer += 3
                        case 'P':
                            if string_in[pointer + 3] == '=':
                                pointer += 4
                                group_name = ""
                                while string_in[pointer] != ')':
                                    group_name = group_name + string_in[pointer]
                                    pointer += 1
                                res.append("reuse_capture")
                                res.append(group_name)
                                pointer += 1
                            elif string_in[pointer + 3] == '<':
                                pointer += 4
                                group_name = ""
                                while string_in[pointer] != '>':
                                    group_name = group_name + string_in[pointer]
                                    pointer += 1
                                res.append("capture")
                                res.append(group_name)
                                res.append('(')
                                pointer += 1
                else:
                    res.append("capture")
                    res.append("(")
                    pointer += 1
            case ')':
                res.append(')')
                pointer += 1
            case '[':
                if string_in[pointer + 1] == '^':
                    pointer += 2
                    res.append("x_choice")
                    res.append("(")
                else:
                    pointer += 1
                    res.append("choice")
                    res.append("(")
                choice_mode = True
            case ']':
                res.append(')')
                choice_mode = False
                pointer += 1
            case '\\':
                pointer += 1
                if string_in[pointer] in "123456789":
                    res.append(f"group{string_in[pointer]}")
                    pointer += 1
                    continue
                if string_in[pointer] in METACHARACTERS:
                    if res and res[-1][0] == "%":
                        res[-1] = res[-1] + string_in[pointer]
                    else:
                        res.append(f"%{string_in[pointer]}")
                    pointer += 1
                    continue
                match string_in[pointer]:
                    case 'A':
                        res.append("string_start")
                        pointer += 1
                    case 'b':
                        res.append("boundary")
                        pointer += 1
                    case 'B':
                        res.append("x_boundary")
                        pointer += 1
                    case 'd':
                        res.append("digit")
                        pointer += 1
                    case 'D':
                        res.append("x_digit")
                        pointer += 1
                    case 's':
                        res.append("whitespace")
                        pointer += 1
                    case 'S':
                        res.append("x_whitespace")
                        pointer += 1
                    case 'w':
                        res.append("word")
                        pointer += 1
                    case 'W':
                        res.append("x_word")
                        pointer += 1
                    case 'Z':
                        res.append("string_end")
                        pointer += 1
                    case _:
                        if res and res[-1][0] == "%":
                            res[-1] = res[-1] + "\\"
                        else:
                            res.append(r"%\\")
                        pointer += 1
            case _ as e:
                raise LregexSyntaxException(message=f"{e} appears to be invalid")
    return " ".join(res)
