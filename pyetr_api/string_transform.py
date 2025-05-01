
from enum import Enum

from pyetr import View


class Mode(Enum):
    fol = "fol"

def string_to_view(input_string: str, mode: Mode = Mode.fol) -> View:
    match mode:
        case Mode.fol:
            return View.from_fol(input_string)


def view_to_string(v: View, mode: Mode = Mode.fol) -> str:
    match mode:
        case Mode.fol:
            return v.to_fol()
