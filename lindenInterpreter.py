import time
from lindensystem import *
import os
import colorsys


def generate_palette(num_colors, brightness, base_hue_offset=0.7):
    colors = []
    for i in range(num_colors):
        hue = (i / num_colors + base_hue_offset) % 1.0
        rgb = colorsys.hsv_to_rgb(hue, brightness, brightness)
        scaled_rgb = [int(x * 255) for x in rgb]
        colors.append(scaled_rgb)
    return colors


upper_palette = generate_palette(26, 1)
lower_palette = generate_palette(26, 0.6, 0.5)

grammar_dir = "grammars"
num_rules = len(os.listdir(grammar_dir))


# user commands use generic args argument to use easily with user input:
def remove_grammar(args: list[str]):
    """Remove grammar from list."""
    if args[0] + ".gmo" in os.listdir(grammar_dir):
        os.remove(f"{grammar_dir}/{args[0]}.gmo")
    elif args[0] == "all":
        for file in os.listdir(grammar_dir):
            os.remove(f"{grammar_dir}/{file}")
    else:
        raise ValueError


def list_grammars(args: list[str]):
    for x, i in enumerate(os.listdir(grammar_dir)):
        print(f"{x}.\t{i[:-4]}")


def view_grammar(args: list[str]):
    if args[0] + ".gmo" in os.listdir(grammar_dir):
        with open(f"{grammar_dir}/{args[0]}.gmo", "r") as file:
            for line in file.readlines():
                print(f"\t{line.strip()}")
    else:
        raise ValueError


def store_random_grammar(args: list[str]):
    base_grammar_name = f"{grammar_dir}/rand.gmo"
    grammar_name = base_grammar_name

    num_grammars = 0
    if os.path.isfile(base_grammar_name):
        grammar_name = base_grammar_name[:-4] + str(num_grammars) + ".gmo"
        while os.path.isfile(grammar_name):
            num_grammars += 1
            grammar_name = base_grammar_name[:-4] + str(num_grammars) + ".gmo"

    lind_to_file(generate_random_lindenmayer(26, 10, 5), grammar_name)


def run_grammar(args: list[str]):
    iterations = 5
    seed = "A"
    masked = False
    if len(args) == 2:
        iterations = int(args[1])
    elif len(args) == 3:
        seed = args[1]
        iterations = int(args[2])
    elif len(args) == 4:
        masked = bool(int(args[3]))

    sentence = seed

    def draw_sentence():
        if not masked:
            printable = ""
            for i in sentence:
                rgb = [0, 0, 0]
                if i.isupper():
                    rgb = upper_palette[ord(i) - 65]
                else:
                    rgb = lower_palette[ord(i) - 97]
                printable += (
                    f"\033[38;2;{int(rgb[0])};{int(rgb[1])};{int(rgb[2])}m{i}\033[0m"
                )
            print(printable)
            time.sleep(0.15)

    draw_sentence()

    for i in range(iterations):
        rules = read_lind(f"{grammar_dir}/{args[0]}.gmo")
        sentence = iterate_lind(sentence, rules)

        draw_sentence()


def add_to(args):
    rules = {}
    while True:
        rule = input("\t")
        if rule == "":
            break
        rule_list = rule.split(" -> ")
        rules[rule_list[0].strip()] = rule_list[1].strip()
    name = ""
    if len(args) == 1:
        name = args[0]
    else:
        name = input("name: ")
    lind_to_file(rules, grammar_dir + "/" + name + ".gmo")


def list_commands(args: list[str]):
    for x, command in enumerate(commands):
        print(f"\t{command}: {command_help[x]}")
    print(f"\tq: quit program.")


command_help = [
    "displays information about commands.",
    "lists names of all currently stored formal grammar rules.",
    "rm <grammar_name> removes the grammar specified from the list.",
    "v <grammar_name> displays the formal grammar rules for specified grammar name.",
    "adds a randomly generated formal grammar to the list.",
    "run <grammar_name> or run <grammar_name> <iterations> or run <grammar_name> <seed> <iterations> runs and displays iterations of applying the formal grammar rule to a seed. If iterations or seed arguments are not passed then defaults are 5 and A respectively.",
    "add <name> or leave empty -> <A -> rule> ... q",
]
commands = {
    "h": list_commands,
    "ls": list_grammars,
    "rm": remove_grammar,
    "v": view_grammar,
    "rdg": store_random_grammar,
    "run": run_grammar,
    "add": add_to,
}


def main():
    print("\n Welcome to the Lindenmayer system explorer. Press h for help.\n")
    while True:
        command = input("[>>")
        if command == "q":
            break
        else:
            cmd_args = command.split(" ")
            if cmd_args[0] in commands.keys():
                commands[cmd_args[0]]([arg.strip() for arg in cmd_args[1:]])
            else:
                print(
                    f"Invalid command '{cmd_args[0]}' entered. Type 'h' for valid command list."
                )


if __name__ == "__main__":
    main()
