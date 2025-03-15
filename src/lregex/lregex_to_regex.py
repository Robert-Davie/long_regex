from .valid_words import ValidWords
import re


class LregexSyntaxException(Exception):
    def __init__(self, message):
        super().__init__(message)


def lregex_to_regex(input_in):
    input_in = re.sub("\\s", " ", input_in)
    input_in = input_in.split(" ")
    pointer = 0
    total = []
    bracket_stack = []
    while pointer < len(input_in):
        current_word = input_in[pointer]
        next_word = None
        if pointer + 1 != len(input_in):
            next_word = input_in[pointer + 1]
        if not current_word:
            pointer += 1
            continue
        if current_word[0] == ValidWords.PERCENT.value:
            temp = current_word[1:]
            for i in ".^$|?*()[]{}+":
                temp = temp.replace(i, "\\" + i)
            total.append(temp)
            pointer += 1
            continue
        if len(current_word) == 6 and current_word[:5] == "group":
            total.append("\\" + current_word[5])
            pointer += 1
            continue
        match current_word:
            case ValidWords.SPACE.value:
                total.append(" ")
            case ValidWords.LITERAL.value:
                temp = []
                pointer += 2
                next_word = input_in[pointer]
                while next_word != ")":
                    temp.append(next_word)
                    pointer += 1
                    next_word = input_in[pointer]
                total.append(" ".join(temp))
            case ValidWords.STRING_START.value:
                total.append("\\A")
            case ValidWords.STRING_END.value:
                total.append("\\Z")
            case ValidWords.ANY_CHAR.value:
                total.append(".")
            case ValidWords.OR.value:
                total.append("|")
            case ValidWords.LOOK_AHEAD.value:
                if next_word == "(":
                    total.append("(?=")
                    pointer += 1
                    bracket_stack.append(")")
            case ValidWords.X_LOOK_AHEAD.value:
                if next_word == "(":
                    total.append("(?!")
                    pointer += 1
                    bracket_stack.append(")")
            case ValidWords.X_CHOICE.value:
                if next_word == "(":
                    total.append("[^")
                    pointer += 1
                    bracket_stack.append("]")
            case ValidWords.MIN0.value:
                total.append("*")
            case ValidWords.MAX1.value:
                total.append("?")
            case ValidWords.MIN1.value:
                total.append("+")
            case ValidWords.START.value:
                total.append("^")
            case ValidWords.END.value:
                total.append("$")
            case ValidWords.BOUNDARY.value:
                total.append("\\b")
            case ValidWords.X_BOUNDARY.value:
                total.append("\\B")
            case ValidWords.DIGIT.value:
                total.append("\\d")
            case ValidWords.X_DIGIT.value:
                total.append("\\D")
            case ValidWords.WHITESPACE.value:
                total.append("\\s")
            case ValidWords.X_WHITESPACE.value:
                total.append("\\S")
            case ValidWords.WORD.value:
                total.append("\\w")
            case ValidWords.X_WORD.value:
                total.append("\\W")
            case ValidWords.REPEAT_EXACTLY.value:
                total.append("{" + next_word + "}")
                pointer += 1
            case ValidWords.AT_LEAST.value:
                total.append("{" + next_word + ",}")
                pointer += 1
            case ValidWords.REPEAT.value:
                if all([next_word == "(", input_in[pointer + 4] == ")"]):
                    total.append(
                        "{" + f"{input_in[pointer + 2]},{input_in[pointer + 3]}" + "}"
                    )
                    pointer += 4
            case ValidWords.RANGE.value:
                if all([next_word == "(", input_in[pointer + 4] == ")"]):
                    total.append(f"{input_in[pointer + 2]}-{input_in[pointer + 3]}")
                    pointer += 4
            case ValidWords.CHOICE.value:
                if next_word == "(":
                    total.append("[")
                    pointer += 1
                    bracket_stack.append("]")
            case ValidWords.CAPTURE.value:
                if next_word == "(":
                    total.append("(")
                    pointer += 1
                    bracket_stack.append(")")
            case ValidWords.X_CAPTURE.value:
                if next_word == "(":
                    total.append("(?:")
                    pointer += 1
                    bracket_stack.append(")")
            case ValidWords.NAMED_CAPTURE.value:
                if next_word == "(":
                    total.append(f"(?P<{input_in[pointer + 2]}>")
                    pointer += 2
                    bracket_stack.append(")")
            case ValidWords.REUSE_CAPTURE.value:
                total.append(f"(?P={next_word})")
                pointer += 1
            case ValidWords.X_GREEDY.value:
                total.append("?")
            case ValidWords.X_BACKTRACK.value:
                total.append("+")
            case ")":
                total.append(bracket_stack.pop())
            case _ as e:
                raise LregexSyntaxException(f"'{e}' is not a valid word in lregex")
        pointer += 1
    res = "".join(total)
    return res
