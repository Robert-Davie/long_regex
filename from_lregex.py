def from_lregex(input_in):
    input_in = input_in.split(" ")
    pointer = 0
    total = []
    bracket_stack = []
    while pointer < len(input_in):
        current_word = input_in[pointer]
        if not current_word:
            pointer += 1
            continue
        if current_word[0] == "%":
            temp = current_word[1:]
            for i in ".":
                temp = temp.replace(i, "\\" + i )
            total.append(temp)
        if len(current_word) == 6 and current_word[:5] == "group":
            total.append("\\" + current_word[5])
        match current_word:
            case "stringStart":
                total.append("\\A")
            case "stringEnd":
                total.append("\\Z")
            case "anyChar":
                total.append(".")
            case "or":
                total.append("|")
            case "lookAhead":
                if input_in[pointer + 1] == "(":
                    total.append("(?=")
                    pointer += 1
                    bracket_stack.append(")")
            case "xLookAhead":
                if input_in[pointer + 1] == "(":
                    total.append("(?!")
                    pointer += 1
                    bracket_stack.append(")")
            case "xOption":
                if input_in[pointer + 1] == "(":
                    total.append("[^")
                    pointer += 1
                    bracket_stack.append("]")
            case "min0":
                total.append("*")
            case "max1":
                total.append("?")
            case "min1":
                total.append("+")
            case "start":
                total.append("^")
            case "end":
                total.append("$")
            case "boundary":
                total.append("\\b")
            case "xBoundary":
                total.append("\\B")
            case "digit":
                total.append("\\d")
            case "xDigit":
                total.append("\\D")
            case "space":
                total.append("\\s")
            case "xSpace":
                total.append("\\S")
            case "word":
                total.append("\\w")
            case "xWord":
                total.append("\\W")
            case "repeatExactly":
                total.append("{" + input_in[pointer + 1] + "}")
                pointer += 1
            case "atLeast":
                total.append("{" + input_in[pointer + 1] + ",}")
                pointer += 1
            case "repeat":
                if all([
                    input_in[pointer + 1] == "(",
                    input_in[pointer + 4] == ")"
                ]):
                    total.append("{" + f"{input_in[pointer + 2]},{input_in[pointer + 3]}" + "}")
                    pointer += 4
            case "range":
                if all([
                    input_in[pointer + 1] == "(",
                    input_in[pointer + 4] == ")"
                ]):
                    total.append(f"{input_in[pointer + 2]}-{input_in[pointer + 3]}")
                    pointer += 4
            case "option":
                if input_in[pointer + 1] == "(":
                    total.append("[")
                    pointer += 1
                    bracket_stack.append("]")
            case "capture":
                if input_in[pointer + 1] == "(":
                    total.append("(")
                    pointer += 1
                    bracket_stack.append(")")
            case "xCapture":
                if input_in[pointer + 1] == "(":
                    total.append("(?:")
                    pointer += 1
                    bracket_stack.append(")")
            case "namedCapture":
                if input_in[pointer + 1] == "(":
                    total.append(f"(?P<{input_in[pointer + 2]}>")
                    pointer += 2
                    bracket_stack.append(")")
            case "reuseCapture":
                total.append(f"(?P={input_in[pointer + 1]})")
                pointer += 1
            case "nonGreedy":
                total.append("?")
            case "xBacktrack":
                total.append("+")
            case ")":
                total.append(bracket_stack.pop())
        pointer += 1
    res = "".join(total)
    return res