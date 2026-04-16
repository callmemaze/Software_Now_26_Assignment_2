import os
import re

# ---------------- CONFIG ---------------- #

DEBUG = False  # set True for internal debug logs


def debug(*args):
    if DEBUG:
        print("[DEBUG]:", *args)


# ---------------- TOKENIZER ---------------- #

NUMBER_REGEX = re.compile(r"""
    (\d+(\.\d*)?|\.\d+)      # normal decimal
    ([eE][+-]?\d+)?          # optional scientific notation
""", re.VERBOSE)


def tokenize(expr):
    tokens = []
    i = 0
    n = len(expr)

    while i < n:
        c = expr[i]

        if c.isspace():
            i += 1
            continue

        # number (supports scientific notation)
        match = NUMBER_REGEX.match(expr, i)
        if match:
            num_str = match.group(0)
            tokens.append(("NUM", num_str))
            i += len(num_str)
            continue

        if c in "+-*/":
            tokens.append(("OP", c))
            i += 1
            continue

        if c == "(":
            tokens.append(("LPAREN", c))
            i += 1
            continue

        if c == ")":
            tokens.append(("RPAREN", c))
            i += 1
            continue

        raise ValueError(f"Invalid character: '{c}'")

    tokens.append(("END", ""))
    debug("Tokens:", tokens)
    return tokens


# ---------------- PARSER ---------------- #

def parse(tokens):
    pos = 0

    def peek():
        return tokens[pos]

    def consume(expected_type=None, expected_value=None):
        nonlocal pos
        tok = tokens[pos]

        if expected_type and tok[0] != expected_type:
            raise ValueError(f"Expected {expected_type}, got {tok}")

        if expected_value and tok[1] != expected_value:
            raise ValueError(f"Expected '{expected_value}', got {tok}")

        pos += 1
        return tok

    # Grammar:
    # expr   = term ((+|-) term)*
    # term   = factor ((*|/) factor | implicit_mul)*
    # factor = '-' factor | primary
    # primary= NUM | '(' expr ')'

    def parse_expr():
        node = parse_term()

        while True:
            tok = peek()
            if tok[0] == "OP" and tok[1] in "+-":
                op = consume()[1]
                right = parse_term()
                node = ("bin", op, node, right)
            else:
                break

        return node

    def parse_term():
        node = parse_factor()

        while True:
            tok = peek()

            # explicit operators
            if tok[0] == "OP" and tok[1] in "*/":
                op = consume()[1]
                right = parse_factor()
                node = ("bin", op, node, right)
                continue

            # implicit multiplication
            if tok[0] in ("NUM", "LPAREN"):
                right = parse_factor()
                node = ("bin", "*", node, right)
                continue

            break

        return node

    def parse_factor():
        tok = peek()

        if tok[0] == "OP":
            if tok[1] == "-":
                consume("OP", "-")
                operand = parse_factor()
                return ("neg", operand)

            if tok[1] == "+":
                raise ValueError("Unary + is not allowed")

        return parse_primary()

    def parse_primary():
        tok = peek()

        if tok[0] == "NUM":
            consume("NUM")
            return ("num", float(tok[1]))

        if tok[0] == "LPAREN":
            consume("LPAREN")
            node = parse_expr()

            if peek()[0] != "RPAREN":
                raise ValueError("Missing closing parenthesis")

            consume("RPAREN")
            return node

        raise ValueError(f"Unexpected token: {tok}")

    tree = parse_expr()

    if peek()[0] != "END":
        raise ValueError("Unexpected trailing input")

    debug("Parse tree:", tree)
    return tree


# ---------------- TREE STRING ---------------- #

def format_number(val):
    if float(val).is_integer():
        return str(int(val))
    return str(round(val, 4))


def tree_to_string(node):
    t = node[0]

    if t == "num":
        return format_number(node[1])

    if t == "neg":
        return f"(neg {tree_to_string(node[1])})"

    if t == "bin":
        op, left, right = node[1], node[2], node[3]
        return f"({op} {tree_to_string(left)} {tree_to_string(right)})"


# ---------------- EVALUATION ---------------- #

def eval_tree(node):
    t = node[0]

    if t == "num":
        return node[1]

    if t == "neg":
        return -eval_tree(node[1])

    if t == "bin":
        op = node[1]
        l = eval_tree(node[2])
        r = eval_tree(node[3])

        if op == "+":
            return l + r
        if op == "-":
            return l - r
        if op == "*":
            return l * r
        if op == "/":
            if r == 0:
                raise ZeroDivisionError("Division by zero")
            return l / r

    raise ValueError("Invalid node")


# ---------------- TOKEN STRING ---------------- #

def tokens_to_string(tokens):
    result = []
    for ttype, val in tokens:
        if ttype == "END":
            result.append("[END]")
        else:
            result.append(f"[{ttype}:{val}]")
    return " ".join(result)


# ---------------- MAIN FUNCTION ---------------- #

def evaluate_file(input_path: str) -> list[dict]:
    import os

    results = []
    output_path = os.path.join(os.path.dirname(input_path), "output.txt")

    with open(input_path, "r") as f:
        lines = f.readlines()

    with open(output_path, "w") as out:
        for idx, raw_line in enumerate(lines):
            expr = raw_line.rstrip("\n")

            # ---------------- PARSING STAGE ---------------- #
            try:
                tokens = tokenize(expr)
                tree = parse(tokens)

                tree_str = tree_to_string(tree)
                tokens_str = tokens_to_string(tokens)

            except Exception:
                results.append({
                    "input": expr,
                    "tree": "ERROR",
                    "tokens": "ERROR",
                    "result": "ERROR"
                })

                out.write(f"Input: {expr}\n")
                out.write("Tree: ERROR\n")
                out.write("Tokens: ERROR\n")
                out.write("Result: ERROR\n")

                if idx != len(lines) - 1:
                    out.write("\n")

                continue  

            # ---------------- EVALUATION STAGE ---------------- #
            try:
                value = eval_tree(tree)

                formatted_result = (
                    int(value) if float(value).is_integer()
                    else round(value, 4)
                )

                result_value = float(value)

            except Exception:
                formatted_result = "ERROR"
                result_value = "ERROR"

            results.append({
                "input": expr,
                "tree": tree_str,
                "tokens": tokens_str,
                "result": result_value
            })

            out.write(f"Input: {expr}\n")
            out.write(f"Tree: {tree_str}\n")
            out.write(f"Tokens: {tokens_str}\n")
            out.write(f"Result: {formatted_result}\n")

            if idx != len(lines) - 1:
                out.write("\n")

    return results


if __name__ == "__main__":
    evaluate_file("sample_input.txt")