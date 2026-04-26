"""
# Differentiation.
/src/differentiation_detroix23/vectors.py
"""

import math
from typing import Self

class Vector:
	"""
	# 2 dimension `float` `Vector`.
	"""
	x: float
	y: float
	
	def __init__(self, x: float, y: float) -> None:
		"""
		Create a vector of coordinate (`x`; `y`).
		"""
		self.x = x
		self.y = y

	def __str__(self) -> str:
		return f"({self.x}; {self.y})"

	def __repr__(self) -> str:
		return f"Vector(x={self.x}, y={self.y})"

	def __mul__(self, other: object) -> Vector:
		if isinstance(other, float) or isinstance(other, int):
			return Vector(self.x * other, self.y * other)
		else:
			return NotImplemented

	def clone(self) -> 'Vector':
		"""
		Clone the `Vector` and return an identical unlinked copy.
		"""
		return Vector(self.x, self.y)

	def add(self, value: 'float | int | Vector') -> Self:
		"""
		Add to it`self` the real or `Vector` `value`. Return `Self` for chaining.
		"""
		if isinstance(value, Vector):
			self.x += value.x
			self.y += value.y
		else:
			self.x += value
			self.y += value
		return self

	def subtract(self, value: 'float | int | Vector') -> Self:
		"""
		Subtract to it`self` the real or `Vector` `value`. Return `Self` for chaining.
		"""
		if isinstance(value, Vector):
			self.x -= value.x
			self.y -= value.y
		else:
			self.x -= value
			self.y -= value
		return self

	def multiply(self, factor: float | int) -> Self:
		"""
		Multiply it`self` by the real `factor`. Return `Self` for chaining.
		"""
		self.x *= factor
		self.y *= factor
		return self

	def divide(self, factor: float | int) -> Self:
		"""
		Divide it`self` by the real `factor`. Return `Self` for chaining.
		"""
		self.x /= factor
		self.y /= factor
		return self

	def length_squared(self) -> float:
		"""
		Return the length of vector `v` without doing a square root.

		Uses a simple pythagorean distance: `|v|^2 = x^2 + y^2`
		"""
		return self.x * self.x + self.y * self.y

	def length(self) -> float:
		"""
		Return the length, or absolute value of the vector `v`.

		Uses a simple pythagorean distance: `|v| = sqrt(x^2 + y^2)`
		"""
		return math.sqrt(self.length_squared())

	def normalize(self) -> Self:
		"""
		Transform the `Vector` such as |v| = 1. Return `Self` for chaining.
		"""
		return self.divide(self.length())
	