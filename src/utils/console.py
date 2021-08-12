import os
import ctypes

from colorama import Fore, Style
from datetime import datetime

def time_tag() -> str:
    time = datetime.now().strftime("%H:%M")
    tt = Style.BRIGHT + Fore.BLACK + f"    [{time}]  "
    return tt

class tags:
    default = time_tag() + f"{Fore.WHITE}[ {Fore.YELLOW}anti {Fore.WHITE}]  "
    error = time_tag() + f"{Fore.WHITE}[ {Fore.RED}ERR! {Fore.WHITE}]  "
    okay = time_tag() + f"{Fore.WHITE}[ {Fore.GREEN}OKAY {Fore.WHITE}]  "

def clear():
    """Clears console/terminal"""
    if "nt" in os.name:
        os.system("cls")
    else:
        os.system("clear")

def title(t: str):
    ctypes.windll.kernel32.SetConsoleTitleW(t)
