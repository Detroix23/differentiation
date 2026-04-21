"""
# Differentiation.
/src/differentiation_detroix23/__main__.py
"""

from differentiation_detroix23.definitions import REAL_FUNCTION, show
from differentiation_detroix23 import euler

def main() -> None:
	"""
	Differentiation main entry point.
	"""
	run_euler1()

def run_euler1() -> None:
	"""
	Run an `Euler` differentiator.
	"""
	e1 = euler.Euler("1.", lambda x: (1.0 - x) / x, d=0.03, samples_count=1000, u0=0.1)
	e1.complete()
	e1.plot()

	e2 = euler.Euler("2.", lambda x: x * (1.0 - x), d=0.01, samples_count=1000, u0=0.3)
	e2.complete()
	e2.plot()

	show()

main()
