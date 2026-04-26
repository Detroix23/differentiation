"""
# Differentiation.
/src/differentiation_detroix23/vector_field.py
"""

import math
import copy

import numpy
from matplotlib import backend_bases, pyplot, figure, axes

from differentiation_detroix23.definitions import Real, RealList, RealFunction, Real2Function
from differentiation_detroix23 import vectors, vector_pathing

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
	sample_position: vectors.Vector
	sample_size: vectors.Vector
	sample_step: vectors.Vector
	size: tuple[int, int]
	x: RealList
	"""`x` origin of each vector."""
	y: RealList
	"""`y` origin of each vector."""
	u: RealList
	"""`x` size of each vector."""
	v: RealList
	"""`y` size of each vector."""
	pather: vector_pathing.VectorPathing
	figures: figure.Figure
	axes: axes.Axes
	connection_mouse_id: int

	def __init__(
		self,
		name: str,
		a: Real2Function,
		b: Real2Function,
		attenuation: RealFunction | None,
		sample_size: vectors.Vector,
		sample_position: vectors.Vector,
		sample_step: vectors.Vector,
	) -> None:
		self.name = name
		self.a = a
		self.b = b
		self.attenuation = attenuation
		self.sample_size = sample_size
		self.sample_position = sample_position
		self.sample_step = sample_step
		
		self.size = (
			int(math.ceil(self.sample_size.x / self.sample_step.x)),
			int(math.ceil(self.sample_size.y / self.sample_step.y)),
		)

		self.x = numpy.zeros((self.size[0] * self.size[1],), dtype=Real)
		self.y = numpy.zeros((self.size[0] * self.size[1],), dtype=Real)
		self.u = numpy.zeros((self.size[0] * self.size[1],), dtype=Real)
		self.v = numpy.zeros((self.size[0] * self.size[1],), dtype=Real)

		self.pather = vector_pathing.VectorPathing(
			field=self, 
			step_size=0.01, 
			start_position=vectors.Vector(4.0, 5.0), 
			sample_count=1000,
		)

		# Matplotlib.
		(self.figures, self.axes) = pyplot.subplots()
		self.axes.autoscale(False)

		self.connection_mouse_id = self.figures.canvas.mpl_connect('button_press_event', self.on_click)

	def __del__(self) -> None:
		"""
		On drop actions.
		"""
		self.figures.canvas.mpl_disconnect(self.connection_mouse_id)

	def on_click(self, event: backend_bases.Event) -> None:
		"""
		Event action, listened by `pyplot`'s `Figure`. 
		
		Use middle mouse button to create a new _pather_ at cursor location.
		"""
		position: vectors.Vector | None
		button: int

		try:
			button = event.button  # pyright: ignore[reportAttributeAccessIssue]
			position = vectors.Vector(float(event.xdata), float(event.ydata))  # pyright: ignore[reportAttributeAccessIssue]
		except:
			button = 0
			position = None

		'''
		print(f"""
Event:
x: {type(event.x)} = {event.x}	
y: {type(event.y)} = {event.y}	
xdata: {type(event.xdata)} = {event.xdata}	
ydata: {type(event.ydata)} = {event.ydata}	
ydata: {type(position_x)} = {position_x}	
ydata: {type(position_y)} = {position_y}	
button={event.button}	
""")
		'''

		if (
			position is not None 
			and position.x is not math.nan 
			and position.y is not math.nan 
			and button == 2
		):
			print(f"(?) VectorField.on_click() {self.name} new 'pather' to ({position})")
			self.pather.position_start = position.clone()
			self.pather.reset()
			self.pather.complete()

			self.pather.plot()
			self.figures.show()


		return

	def complete(self) -> None:
		"""
		Compute the whole vector field.
		"""
		i: int
		j: int = 0
		x: float
		y: float = self.sample_position.y + j * self.sample_step.y
		while j < self.size[1]:
			i = 0
			x = self.sample_position.x + i * self.sample_step.x

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
					print(f"(X) vector_field.VectorField.complete() {self.name} uncaught exception:")
					raise exception

				if self.attenuation is not None and vector.length_squared() != 0:
						length_attenuated: float = (self.attenuation)(vector.length())
						vector.normalize().multiply(length_attenuated)

				self.x[index] = x
				self.y[index] = y
				self.u[index] = vector.x
				self.v[index] = vector.y

				i += 1
				x = self.sample_position.x + i * self.sample_step.x

			j += 1
			y = self.sample_position.y + j * self.sample_step.y

		return

	def plot(self) -> None:
		"""
		Plot the vector field. Do not `show` automatically the figure.
		"""
		self.axes.set_title(f"""Vector field. `{self.name}` with: 
f, position={self.sample_position}, size={self.sample_size}, step={self.sample_step}.""")
		self.axes.set_xlabel("x")
		self.axes.set_ylabel("y")
		self.set_plot_bound()

		self.axes.quiver(self.x, self.y, self.u, self.v)
		self.pather.plot()

		return

	def set_plot_bound(self) -> None:
		"""
		Set the bound respectively to the `samples` parameters.
		"""
		self.axes.set_xbound(self.sample_position.x, self.sample_position.x + self.sample_size.x)
		self.axes.set_ybound(self.sample_position.y, self.sample_position.y + self.sample_size.y)
	