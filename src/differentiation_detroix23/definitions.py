"""
# Differentiation.
/src/differentiation_detroix23/definitions.py
"""

from typing import Callable

import numpy
from matplotlib import pyplot

REAL = numpy.float64
INTEGER = numpy.int64
REAL_FUNCTION = Callable[[float], float]
REAL_LIST = numpy.ndarray[tuple[int], numpy.dtype[REAL]]
INTEGER_LIST = numpy.ndarray[tuple[int], numpy.dtype[INTEGER]]

def show() -> None:
	pyplot.show()

__all__: list[str] = ["REAL", "INTEGER", "REAL_FUNCTION", "REAL_LIST", "INTEGER_LIST"]
