from pyetr import View
from pyetr_api.simple_parser import simple_to_view, view_to_simple
v = simple_to_view("A | B")
print(view_to_simple(v))