"""
Examples of different dispatch patterns in Python.
Comments are in English as requested.
"""

# ----------------------------------------------------------------------
# 1. Message dispatch (if/elif style)
# A single function checks the incoming "message" and decides what to do.
# ----------------------------------------------------------------------

def make_counter():
    # Local mutable state
    count = 0

    def dispatch(message, value=None):
        nonlocal count
        if message == "increment":
            count += 1
            return count
        elif message == "decrement":
            count -= 1
            return count
        elif message == "reset":
            count = 0
            return count
        elif message == "get":
            return count
        else:
            raise ValueError(f"Unknown message: {message}")

    return dispatch


counter = make_counter()
counter("increment")
counter("increment")
print(counter("get"))  # 2


# ----------------------------------------------------------------------
# 2. Dictionary dispatch
# Instead of if/elif, map messages to handler functions using a dict.
# ----------------------------------------------------------------------

def make_counter_dict():
    state = {"count": 0}

    def increment():
        state["count"] += 1
        return state["count"]

    def decrement():
        state["count"] -= 1
        return state["count"]

    def reset():
        state["count"] = 0
        return state["count"]

    def get():
        return state["count"]

    operations = {
        "increment": increment,
        "decrement": decrement,
        "reset": reset,
        "get": get,
    }

    def dispatch(message):
        handler = operations.get(message)
        if handler is None:
            raise ValueError(f"Unknown message: {message}")
        return handler()

    return dispatch


counter2 = make_counter_dict()
counter2("increment")
counter2("increment")
counter2("increment")
print(counter2("get"))  # 3


# ----------------------------------------------------------------------
# 3. Single dispatch (functools.singledispatch)
# Choose implementation based on the type of ONE argument.
# ----------------------------------------------------------------------

from functools import singledispatch

@singledispatch
def describe(value):
    # Default implementation for unknown types
    return f"Unknown type: {value!r}"

@describe.register
def _(value: int):
    return f"This is an integer: {value}"

@describe.register
def _(value: str):
    return f"This is a string of length {len(value)}"

@describe.register
def _(value: list):
    return f"This is a list with {len(value)} elements"

print(describe(42))         # This is an integer: 42
print(describe("hello"))    # This is a string of length 5
print(describe([1, 2, 3]))  # This is a list with 3 elements


# ----------------------------------------------------------------------
# 4. Single dispatch for methods (functools.singledispatchmethod)
# Same idea, but works with instance methods.
# ----------------------------------------------------------------------

from functools import singledispatchmethod

class Formatter:
    @singledispatchmethod
    def format(self, value):
        return f"Unsupported type: {type(value)}"

    @format.register
    def _(self, value: int):
        return f"Integer: {value:,}"

    @format.register
    def _(self, value: float):
        return f"Float: {value:.2f}"

formatter = Formatter()
print(formatter.format(1000))     # Integer: 1,000
print(formatter.format(3.14159))  # Float: 3.14


# ----------------------------------------------------------------------
# 5. Multiple dispatch
# Choose implementation based on types of SEVERAL arguments.
# Requires the third-party "multipledispatch" package:
#   pip install multipledispatch
# ----------------------------------------------------------------------

try:
    from multipledispatch import dispatch

    @dispatch(int, int)
    def combine(a, b):
        return a + b

    @dispatch(str, str)
    def combine(a, b):
        return a + " " + b

    @dispatch(list, list)
    def combine(a, b):
        return a + b

    print(combine(2, 3))              # 5
    print(combine("hello", "world"))  # hello world
    print(combine([1, 2], [3, 4]))    # [1, 2, 3, 4]

except ImportError:
    print("multipledispatch package is not installed")


# ----------------------------------------------------------------------
# 6. Dynamic dispatch (classic OOP polymorphism)
# The correct method is chosen automatically based on the object's
# actual runtime type, not by any explicit dispatch function.
# ----------------------------------------------------------------------

"""
Dynamic dispatch example.

Idea: We have a general "shape" and several specific shapes
(Circle, Square, Triangle). Each shape knows how to calculate
its OWN area. When we call shape.area(), Python automatically
picks the correct method depending on the REAL type of the object
at runtime -- we never write "if type is Circle: ... elif ...".

This automatic selection of the correct method, based on the
object's actual class, is called DYNAMIC DISPATCH.
"""

class Shape:
    # Base ("parent") class defines a generic method.
    # It exists mostly so every shape has an area() method available.
    def area(self):
        return 0

    def name(self):
        return "Generic shape"


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    # This method OVERRIDES the one in Shape.
    def area(self):
        return 3.14159 * self.radius ** 2

    def name(self):
        return "Circle"


class Square(Shape):
    def __init__(self, side):
        self.side = side

    def area(self):
        return self.side ** 2

    def name(self):
        return "Square"


class Triangle(Shape):
    def __init__(self, base, height):
        self.base = base
        self.height = height

    def area(self):
        return 0.5 * self.base * self.height

    def name(self):
        return "Triangle"


# A list containing DIFFERENT types of objects.
shapes = [
    Circle(radius=3),
    Square(side=4),
    Triangle(base=5, height=6),
]

for shape in shapes:
    # We call the SAME method name "area()" on every object.
    # Python looks at the REAL type of "shape" (Circle, Square, Triangle)
    # and automatically runs the matching version of area().
    # This decision happens at RUNTIME, not before the program runs.
    print(f"{shape.name()}: area = {shape.area()}")

# Output:
# Circle: area = 28.27431
# Square: area = 16
# Triangle: area = 15.0

