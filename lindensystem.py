import re
import numpy.random as rd


def generate_random_lindenmayer(
    num_var: int, num_const: int, max_rule_size: int
) -> dict[str, str]:
    """Generates a dictionary containing the rules of a randomly generated Lindenmayer System.

    Args:
        num_var (int): number of grammar variables.
        num_const (int): maximum number of grammar constants. Actual number between 1 and this
        number.
        max_rule_size (int): maximum length of rule size. Actual between 1 and this number and
        will be different for each variable.

    Returns:
        dict[str, str]: first string representing variable and second string representing
        substitution rule.
    """
    grammar = {}

    for i in range(num_var):
        rule = ""
        for j in range(rd.randint(1, max_rule_size + 1)):
            selector = rd.randint(2)
            char = (
                chr(65 + rd.randint(num_var))
                if selector == 0
                # to help differentiate between variables and constants, constants start from the
                # end of the alphabet.
                else chr(122 - rd.randint(num_const + 1))
            )
            rule += char
        grammar[f"<{chr(i + 65)}>"] = rule

    return grammar


def lind_to_file(rules: dict[str, str], filepath: str):
    """Write lindenmayer system formal grammar rules to a file

    Args:
        rules (dict[str, str]): dictionary containing variables as key and substitution rule as
        value
        filepath (str): file to write rules to
    """

    with open(filepath, "w") as file:
        lines = [variable + " -> " + rules[variable] for variable in rules]
        for line in lines:
            file.write(line + "\n")


def read_lind(filepath: str) -> dict[str, str]:
    """reads an appropriate grammar rules file and returns a dictionary representing it.

    Args:
        filepath (str): file to read grammar rules from.

    Returns:
        dict[str, str]: dictionary containing rules.
    """
    grammar_system = {}
    with open(filepath, "r") as file:
        for line in file.readlines():
            rule = [stage.strip() for stage in line.split("->")]
            grammar_system[rule[0]] = rule[1]
    return grammar_system


def parse_instruction(post: str):
    returner = post

    if returner[:2] == "-r":
        options = [option.strip() for option in post[3:-1].split(",")]
        returner = options[rd.randint(0, len(options))]

    return returner


def iterate_lind(sentence: str, rules: dict[str, str]):
    out = ""
    for x, i in enumerate(sentence):
        new = ""
        keys = list(rules.keys())

        for k in keys:
            back = 0
            forward = 0
            try:
                back = len(k.split(f"<{i}>")[0])
            except:
                pass
            try:
                forward = len(k.split(f"<{i}>")[1])
            except:
                pass
            if k == f"{sentence[x - back:x]}<{i}>{sentence[x + 1:x + 1 + forward]}":
                new = parse_instruction(rules[k])
                break
            else:
                new = i
        out += new
    return out
