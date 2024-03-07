class ColorsFg:
    """
    Special class utilizing ANSI escape sequences to print color output to the console. Foreground color
    Use as ColorsFg.colorname within a Print statement
    Adapted from: <https://www.geeksforgeeks.org/print-colors-python-terminal/>
    """
    black = '\033[30m'
    red = '\033[31m'
    green = '\033[32m'
    orange = '\033[33m'
    blue = '\033[34m'
    purple = '\033[35m'
    cyan = '\033[36m'
    lightgrey = '\033[37m'
    darkgrey = '\033[90m'
    lightred = '\033[91m'
    lightgreen = '\033[92m'
    yellow = '\033[93m'
    lightblue = '\033[94m'
    pink = '\033[95m'
    lightcyan = '\033[96m'
    reset = '\033[0m'


class ColorsBg:
    """
    Special class utilizing ANSI escape sequences to print color output to the console. Background color
    Use as ColorsBg.colorname within a Print statement
    Adapted from: <https://www.geeksforgeeks.org/print-colors-python-terminal/>
    """
    black = '\033[40m'
    red = '\033[41m'
    green = '\033[42m'
    orange = '\033[43m'
    blue = '\033[44m'
    purple = '\033[45m'
    cyan = '\033[46m'
    lightgrey = '\033[47m'