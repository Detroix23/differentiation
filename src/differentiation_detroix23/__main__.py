"""
# Differentiation.
/src/differentiation_detroix23/__main__.py
"""

from differentiation_detroix23.definitions import REAL_FUNCTION
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
	f: REAL_FUNCTION = lambda x: -1 * x + 2

	e = euler.Euler(f, d=0.01, samples_count=100, u0=1)
	e.complete()
	print(e.x)
	e.plot()

main()
