"""
# Differentiation.
/src/differentiation_detroix23/euler.py
"""

import numpy
from matplotlib import pyplot

from differentiation_detroix23.definitions import REAL, INTEGER, REAL_FUNCTION, REAL_LIST, INTEGER_LIST

class Euler:
	"""
	# Graph one solution with the `Euler` algorithm.
	Solves:  
	```maths
	y' = f
	```

	Using a recursive sequence:
	```maths
	d → 0, d > 0:
	u(n+1) = u(n) + d * f(u(n))
	```
	"""
	f: REAL_FUNCTION
	d: float
	n: int
	samples_count: int
	x: INTEGER_LIST
	y: REAL_LIST

	def __init__(
		self, 
		f: REAL_FUNCTION, 
		d: float,
		samples_count: int,
		u0: float
	) -> None:
		self.f = f
		self.d = d
		self.n = 0
		self.samples_count = samples_count
		self.y = numpy.zeros((samples_count,), dtype=REAL)
		self.x = numpy.zeros((samples_count,), dtype=INTEGER)
		self.x[0] = 0
		self.y[0] = u0

	def step(self) -> float:
		"""
		Advance the approximation by computing the next number in the recursive sequence.
		"""
		if self.n >= self.samples_count - 1:
			print(f"(!) euler.Euler.step() step max: ({self.n}/ {self.samples_count})")
			return self.y[self.n]

		sequence_last: float = self.y[self.n]
		sequence_next: float = sequence_last + self.d * (self.f)(sequence_last)
		self.y[self.n + 1] = sequence_next
		self.x[self.n + 1] = self.n + 1

		self.n += 1
		return sequence_next

	def complete(self) -> tuple[INTEGER_LIST, REAL_LIST]:
		"""
		Use `step` to reach the `samples_count`.
		"""
		for _ in range(self.samples_count - 1):
			self.step()

		return (self.x, self.y)


	def plot(self) -> None:
		"""
		Plot using `matplotlib`.
		"""
		(figure, axes) = pyplot.subplots()
		axes.plot(self.x, self.y, color="red", marker="o")
		
		axes.set_title(f"Euler method with f, u₀={self.y[0]}, d={self.d}, n={self.n}.")
		axes.set_xlabel("n")
		axes.set_ylabel("y")


		pyplot.show()

		return
	