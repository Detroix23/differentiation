"""
# Differentiation.
/src/differentiation_detroix23/definitions.py
"""

import math
import numpy
from matplotlib import pyplot
from typing import Callable


Real = numpy.float64
""" ℝ """
Integer = numpy.int64
""" ℕ """
RealFunction = Callable[[float], float]
""" f: ℝ → ℝ """
Real2Function = Callable[[float, float], float]
""" f: (ℝ×ℝ) → ℝ """
RealList = numpy.ndarray[tuple[int], numpy.dtype[Real]]
IntegerList = numpy.ndarray[tuple[int], numpy.dtype[Integer]]

def sign(x: float | int) -> int:
	"""
	Return `-1` if x < 0, `1` if x > 0, `0` else. 
	"""
	return int(abs(x) / x) if x != 0 else 0

def constant(x: float) -> RealFunction:
	"""
	Returns a function that always return `x`.	
	"""
	return lambda _: x

def sigmoid_logistic(x: float) -> float: 
	"""
	Logistic sigmoid: `2 / (1 + e^(-x) - 1)`.
	"""
	return 2.0 / (1.0 + math.exp(-x)) - 1.0 

def ln1pr(x: float) -> float:
	"""
	Natural logarithm of (x+1) over ℝ+.
	"""
	return math.log1p(x)

def show() -> None:
	"""
	Display the `pyplot` figure.
	"""
	pyplot.show()

__all__: list[str] = [
	"Real", "Integer", "RealFunction", "RealList", "IntegerList", 
	"sigmoid_logistic", "ln1pr", "constant",
	"show",
]
