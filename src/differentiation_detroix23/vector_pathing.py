"""
# Differentiation.
/src/differentiation_detroix23/vector_pathing.py
"""

import numpy
from matplotlib import lines
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from differentiation_detroix23 import vector_field
from differentiation_detroix23.definitions import Real, RealList
from differentiation_detroix23 import vectors

class VectorPathing:
	"""
	# `VectorPathing` in a vector field.
	Step, or _flow_ onto the vector field, and record every step.

	## Plotting.
	Pather:
	- Path: 'blue' line.
	- Start: 'red' point.
	- End: 'green' point.
	"""
	field: 'vector_field.VectorField'
	ready: bool
	step_size: float
	position_start: vectors.Vector
	position: vectors.Vector
	step_counter: int
	sample_count: int
	x: RealList
	y: RealList
	plot_path: list[lines.Line2D]


	def __init__(
		self,
		field: 'vector_field.VectorField', 
		step_size: float,
		start_position: vectors.Vector,
		sample_count: int,
	) -> None:
		"""
		Instantiate a pather `VectorPathing` in a `VectorField`.
		"""
		self.field = field
		self.ready = False
		self.step_size = step_size
		self.position_start = start_position.clone()
		self.position = self.position_start.clone()
		self.step_counter = 0
		self.sample_count = sample_count
		self.x = numpy.zeros((self.sample_count,), dtype=Real)
		self.y = numpy.zeros((self.sample_count,), dtype=Real)
		self.plot_path = []

		return

	def reset(self) -> None:
		"""
		Reset the pather, forget all points and:
		- `position`;
		- `step_counter`;
		- `x`;
		- `y`.
		"""
		self.position = self.position_start.clone()
		self.step_counter = 0
		self.x = numpy.zeros((self.sample_count,), dtype=Real)
		self.y = numpy.zeros((self.sample_count,), dtype=Real)

		return

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
		self.ready = True

		return

	def plot(self) -> None:
		"""
		Plot `VectorPathing` path to the `field` axes.
		"""
		if self.ready:
			self.plot_path: list[lines.Line2D] = self.field.axes.plot(self.x, self.y, color="blue")
			self.field.axes.scatter(self.position_start.x, self.position_start.y, c="red")
			self.field.axes.scatter(self.x[-1], self.y[-1], c="green")
	
		return