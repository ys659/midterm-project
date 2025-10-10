from colorama import init, Fore, Style
init(autoreset=True)

def success(msg: str) -> str:
    return f"{Fore.GREEN}{msg}{Style.RESET_ALL}"

def error(msg: str) -> str:
    return f"{Fore.RED}{msg}{Style.RESET_ALL}"

def info(msg: str) -> str:
    return f"{Fore.CYAN}{msg}{Style.RESET_ALL}"

def value(msg: str) -> str:
    return f"{Fore.YELLOW}{msg}{Style.RESET_ALL}"
