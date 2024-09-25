def print_color(text: str, fg_color="green", bg_color="none"):
    """
    Print with colors. Examples:
    print_color("ciao", "orange")
    print_color("miao")
    """
    fg_colors = {
        "black" : '\033[30m',
        "red" : '\033[31m',
        "green" : '\033[32m',
        "orange" : '\033[33m',
        "blue" : '\033[34m',
        "purple" : '\033[35m',
        "cyan" : '\033[36m',
        "lightgrey" : '\033[37m',
        "darkgrey" : '\033[90m',
        "lightred" : '\033[91m',
        "lightgreen" : '\033[92m',
        "yellow" : '\033[93m',
        "lightblue" : '\033[94m',
        "pink" : '\033[95m',
        "lightcyan" : '\033[96m',
    }

    bg_colors = {
        "none" : '',
        "black" : '\033[40m',
        "red" : '\033[41m',
        "green" : '\033[42m',
        "orange" : '\033[43m',
        "blue" : '\033[44m',
        "purple" : '\033[45m',
        "cyan" : '\033[46m',
        "lightgrey" : '\033[47m'        
    }

    if fg_color in fg_colors.keys() and bg_color in bg_colors.keys():
        tmp = fg_colors[fg_color] + " {}"
        #print(tmp.format(text))
        print(fg_colors[fg_color] + text + '\033[0m')

    else:
        print("Error, color not recognized: " + fg_color)