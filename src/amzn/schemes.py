from dataclasses import dataclass
from os import link

@dataclass
class amznProduct:
    name: str
    value: str
    link: str