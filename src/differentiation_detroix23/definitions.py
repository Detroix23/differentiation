"""
# Differentiation.
/src/differentiation_detroix23/definitions.py
"""

import math
import numpy
from matplotlib import pyplot
from typing import Callable


Real = numpy.float64
Integer = numpy.int64
RealFunction = Callable[[float], float]
RealList = numpy.ndarray[tuple[int], numpy.dtype[Real]]
IntegerList = numpy.ndarray[tuple[int], numpy.dtype[Integer]]

SIGMOID: RealFunction = lambda x: 2.0 / (1.0 + math.exp(-x)) - 1.0 
"""Logistic sigmoid: `2 / (1 + e^(-x) - 1)`"""

def show() -> None:
	"""
	Display the `pyplot` figure.
	"""
	pyplot.show()

__all__: list[str] = ["Real", "Integer", "RealFunction", "RealList", "IntegerList", "SIGMOID"]
