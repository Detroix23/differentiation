"""
# Differentiation.
/src/differentiation_detroix23/__main__.py
"""

import math

from differentiation_detroix23.definitions import SIGMOID, show
from differentiation_detroix23 import euler, vector_field

def main() -> None:
	"""
	Differentiation main entry point.
	"""
	run_euler1()

	run_vectors1()

	show()

def run_euler1() -> None:
	"""
	Run an `Euler` differentiator.
	"""
	print("(?) run_euler1() Loading `e1`.")
	e1 = euler.Euler("1.", lambda x: x * (1.0 - x), d=0.03, samples_count=1000, u0=0.1)
	e1.complete()
	e1.plot()

	print("(?) run_euler1() Loading `e2`.")
	e2 = euler.Euler("1.", lambda x: x * (1.0 - x), d=0.01, samples_count=1000, u0=0.3)
	e2.complete()
	e2.plot()

def run_vectors1() -> None:
	"""
	Run a `VectorField` graph.
	"""
	print("(?) run_vectors1() Loading `v1`.")
	v1 = vector_field.VectorField(
		name="1.", 
		f=lambda x: x * (1.0 - x),
		attenuation=SIGMOID,
		sample_position=(-10.0, -10.0),
		sample_size=(20.0, 20.0),
		sample_step=(0.5, 0.5)
	)
	v1.complete()
	v1.plot()

main()
