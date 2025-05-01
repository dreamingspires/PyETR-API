
from enum import Enum

from pyetr import View
from pyetr.parsing.common import ParsingError
from fastapi import HTTPException, status
from .simple_parser import simple_to_view, view_to_simple

class Mode(Enum):
    fol = "fol"
    simple = "simple"


def string_to_view(input_string: str, mode: Mode) -> View:
    try:
        match mode:
            case Mode.fol:
                return View.from_fol(input_string)
            case Mode.simple:
                return simple_to_view(input_string)
    except ParsingError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


def view_to_string(v: View, mode: Mode) -> str:
    match mode:
        case Mode.fol:
            return v.to_fol()
        case Mode.simple:
            return view_to_simple(v)
