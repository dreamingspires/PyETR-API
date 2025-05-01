__all__ = [
    "view_to_simple",
    "simple_to_view"
]

from functools import cache

import pyparsing as pp
from pyparsing import ParseException, ParserElement

from pyetr.parsing.common import ParsingError
from pyetr.parsing.fol_items import (
    BoolAnd,
    BoolNot,
    BoolOr,
    Falsum,
    Implies,
    Item,
    LogicEmphasis,
    LogicPredicate,
    Truth,
    items_to_view,
    view_to_items
)
from pyetr.parsing.fol_items.items import LogicReal
from pyetr import View
ParserElement.enablePackrat()

pp_left = pp.opAssoc.LEFT
pp_right = pp.opAssoc.RIGHT


@cache
def get_expr() -> pp.Forward:
    """
    Generates the parsing expression

    Returns:
        Forward: the parsing expression
    """
    expr = pp.Forward()

    bool_not = pp.Suppress(pp.Char("~"))
    bool_or = pp.Suppress(pp.oneOf("∨ |"))
    bool_and = pp.Suppress(pp.oneOf("∧ &"))
    implies = pp.Suppress(pp.Char("→"))
    emphasis = pp.Suppress(pp.Char("*"))

    predicate_word = pp.Word(pp.alphas + "_", pp.alphanums + "_").setResultsName(
        "predicate"
    ) | pp.Literal("==")
    predicate = predicate_word.setParseAction(LogicPredicate.from_pyparsing)
    real_word = (
        pp.Optional(pp.Literal("-"))
        + pp.Word(pp.nums)
        + pp.Optional(pp.Literal(".") + pp.Word(pp.nums))
    )
    reals = real_word.setResultsName("reals").setParseAction(LogicReal.from_pyparsing)

    truth = pp.Char("⊤").setParseAction(Truth)
    falsum = pp.Char("⊥").setParseAction(Falsum)
    nested_and = pp.infix_notation(
        predicate | reals | truth | falsum,
        op_list=[
            (predicate_word, 1, pp_right, LogicPredicate.from_pyparsing),
            (emphasis, 1, pp_left, LogicEmphasis.from_pyparsing),
            (bool_not, 1, pp_right, BoolNot.from_pyparsing),
            (bool_and, 2, pp_left, BoolAnd.from_pyparsing),
            (bool_or, 2, pp_left, BoolOr.from_pyparsing),
            (implies, 2, pp_left, Implies.from_pyparsing),
        ],
        lpar=pp.Suppress("("),
        rpar=pp.Suppress(")"),
    )
    expr <<= nested_and
    return expr


def simple_to_items(input_string: str) -> list[Item]:
    expr = get_expr()
    try:
        new_string: list[Item] = expr.parse_string(
            input_string, parseAll=True
        ).as_list()
    except ParseException as e:
        raise ParsingError(e.msg)
    return new_string

def item_to_simple(item: Item) -> str:
    if isinstance(item, BoolOr):
        return "(" + " ∨ ".join([item_to_simple(o) for o in item.operands]) + ")"
    elif isinstance(item, BoolAnd):
        return "(" + " ∧ ".join([item_to_simple(o) for o in item.operands]) + ")"
    elif isinstance(item, BoolNot):
        return "~" + item_to_simple(item.arg)
    elif isinstance(item, LogicEmphasis):
        return item_to_simple(item.arg) + "*"
    elif isinstance(item, LogicPredicate):
        if len(item.args) > 0:
            raise ParsingError("Too many predicate args")
        return item.name
    elif isinstance(item, Implies):
        return item_to_simple(item.left) + "→" + item_to_simple(item.right)
    else:
        return item.to_string()

def items_to_simple(items: list[Item]) -> str:
    return "".join(item_to_simple(item) for item in items)

def view_to_simple(v: View) -> str:
    output = items_to_simple(view_to_items(v))
    if len(output) > 2 and output[0] == "(" and output[-1] == ")":
        return output[1:-1]
    else:
        return output

def simple_to_view(s: str) -> View:
    return View._from_view_storage(items_to_view(simple_to_items(s),[]))
