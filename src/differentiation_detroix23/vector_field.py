"""
# Differentiation.
/src/differentiation_detroix23/vector_field.py
"""

import math
import numpy
from matplotlib import pyplot, figure, axes

from differentiation_detroix23.definitions import Real, RealList, RealFunction, Real2Function
from differentiation_detroix23 import vectors

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
	pather: VectorPathing
	figures: figure.Figure
	axes: axes.Axes

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

		self.pather = VectorPathing(self, 0.01, vectors.Vector(4.0, 5.0), 1000)
		(self.figures, self.axes) = pyplot.subplots()



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
				vector = vectors.Vector(0, 0)
				try:
					vector.x = (self.a)(x, y)
					vector.y = (self.b)(x, y)
				
				except ZeroDivisionError:
					# print(f"(?) vector_field.VectorField.complete() ZeroDivisionError x={x}.")
					vector.x = math.inf * x
					vector.y = math.inf * y

				except Exception as exception:
					print("(X) vector_field.VectorField.complete() Uncaught exception:")
					raise exception

				if self.attenuation is not None and vector.length_squared() != 0:
						length_attenuated: float = (self.attenuation)(vector.length())
						vector.normalize().multiply(length_attenuated)

				self.x[index] = x
				self.y[index] = y
				self.u[index] = vector.x
				self.v[index] = vector.y

				i += 1
				x = self.sample_position[0] + i * self.sample_step[0]

			j += 1
			y = self.sample_position[1] + j * self.sample_step[1]

		self.pather.complete()

		return

	def plot(self) -> None:
		"""
		Plot the vector field. Do not `show` automatically the figure.
		"""
		self.axes.quiver(self.x, self.y, self.u, self.v)
		self.pather.plot()

		self.axes.set_title(f"""Vector field. `{self.name}` with: 
f, position={self.sample_position}, size={self.sample_size}, step={self.sample_step}.""")
		self.axes.set_xlabel("x")
		self.axes.set_ylabel("y")
		self.axes.set_xbound(self.sample_position[0], self.sample_position[0] + self.sample_size[0])
		self.axes.set_ybound(self.sample_position[1], self.sample_position[1] + self.sample_size[1])

		return


class VectorPathing:
	"""
	# `VectorPathing` in a vector field.
	"""
	field: VectorField
	step_size: float
	position_start: vectors.Vector
	position: vectors.Vector
	step_counter: int
	sample_count: int
	x: RealList
	y: RealList

	def __init__(
		self,
		field: VectorField, 
		step_size: float,
		start_position: vectors.Vector,
		sample_count: int,
	) -> None:
		"""
		Instantiate a pather `VectorPathing` in a `VectorField`.
		"""
		self.field = field
		self.step_size = step_size
		self.position_start = start_position.clone()
		self.position = start_position.clone()
		self.step_counter = 0
		self.sample_count = sample_count
		self.x = numpy.zeros((self.sample_count,), dtype=Real)
		self.y = numpy.zeros((self.sample_count,), dtype=Real)

	def step(self) -> vectors.Vector:
		"""
		Advance the pather, _flowing_ down the `field` with the given `step_size`.
		"""
		if self.step_counter > self.sample_count - 1:
			print(f"(!) vector_field.VectorPathing.step() \
Reached step limit ({self.step_counter}/ {self.sample_count} - 1)")
			return self.position
		
		slope: vectors.Vector = vectors.Vector(
			(self.field.a)(self.position.x, self.position.y),
			(self.field.b)(self.position.x, self.position.y),
		)

		self.position.add(slope.multiply(self.step_size))
		self.x[self.step_counter] = self.position.x
		self.y[self.step_counter] = self.position.y
		
		self.step_counter += 1

		return self.position

	def complete(self) -> None:
		"""
		Execute `step` to reach `sample_count`.
		"""
		while self.step_counter < self.sample_count:
			self.step()

	def plot(self) -> None:
		"""
		Plot `VectorPathing` path to the `field` axes.
		"""
		self.field.axes.plot(self.x, self.y, color="blue")
		self.field.axes.scatter(self.position_start.x, self.position_start.y, c="red")
		self.field.axes.scatter(self.x[-1], self.y[-1], c="green")
