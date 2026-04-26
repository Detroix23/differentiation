"""
# Differentiation.
/src/differentiation_detroix23/vector_field.py
"""

import math
import numpy
from matplotlib import pyplot

from differentiation_detroix23.definitions import Real, RealList, RealFunction, Real2Function

class VectorField:
	"""
	# Draw the flow of a differential equation with a `VectorField`. 

	Parameters
	- `name`: `str`, optional identifier,
	- `a`: `(ℝ×ℝ) → ℝ`, compute the `x` displacement,
	- `b`: `(ℝ×ℝ) → ℝ`, compute the `y` displacement,
	"""
	name: str
	a: Real2Function
	b: Real2Function
	attenuation: RealFunction | None
	sample_position: tuple[float, float]
	sample_size: tuple[float, float]
	sample_step: tuple[float, float]
	size: tuple[int, int]
	x: RealList
	"""`x` origin of each vector."""
	y: RealList
	"""`y` origin of each vector."""
	u: RealList
	"""`x` size of each vector."""
	v: RealList
	"""`y` size of each vector."""

	def __init__(
		self,
		name: str,
		a: Real2Function,
		b: Real2Function,
		attenuation: RealFunction | None,
		sample_size: tuple[float, float],
		sample_position: tuple[float, float],
		sample_step: tuple[float, float],
	) -> None:
		self.name = name
		self.a = a
		self.b = b
		self.attenuation = attenuation
		self.sample_size = sample_size
		self.sample_position = sample_position
		self.sample_step = sample_step
		
		self.size = (
			int(math.ceil(self.sample_size[0] / self.sample_step[0])),
			int(math.ceil(self.sample_size[1] / self.sample_step[1])),
		)

		self.x = numpy.zeros((self.size[0] * self.size[1],), dtype=Real)
		self.y = numpy.zeros((self.size[0] * self.size[1],), dtype=Real)
		self.u = numpy.zeros((self.size[0] * self.size[1],), dtype=Real)
		self.v = numpy.zeros((self.size[0] * self.size[1],), dtype=Real)

	def complete(self) -> None:
		"""
		Compute the whole vector field.
		"""
		i: int
		j: int = 0
		x: float
		y: float = self.sample_position[1] + j * self.sample_step[1]
		while j < self.size[1]:
			i = 0
			x = self.sample_position[0] + i * self.sample_step[0]

			while i < self.size[0]:
				index: int = j * self.size[0] + i
				u: float
				v: float
				try:
					u = (self.a)(x, y)
					v = (self.b)(x, y)
				
				except ZeroDivisionError:
					# print(f"(?) vector_field.VectorField.complete() ZeroDivisionError x={x}.")
					u = math.inf * x
					v = math.inf * x

				except Exception as exception:
					print("(X) vector_field.VectorField.complete() Uncaught exception:")
					raise exception

				if self.attenuation is not None:
					length: float = math.sqrt(u * u + v * v)
					if length != 0:
						length_attenuated: float = (self.attenuation)(length)

						u = u / length * length_attenuated
						v = v / length * length_attenuated

				self.x[index] = x
				self.y[index] = y
				self.u[index] = u
				self.v[index] = v

				i += 1
				x = self.sample_position[0] + i * self.sample_step[0]

			j += 1
			y = self.sample_position[1] + j * self.sample_step[1]

	def plot(self) -> None:
		"""
		Plot the vector field. Do not `show` automatically the figure.
		"""
		(figures, axes) = pyplot.subplots()
		
		axes.quiver(self.x, self.y, self.u, self.v)

		axes.set_title(f"""Vector field. `{self.name}` with: 
f, position={self.sample_position}, size={self.sample_size}, step={self.sample_step}.""")
		axes.set_xlabel("x")
		axes.set_ylabel("y")

		return
