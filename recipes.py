import pygame as py
from items import Item, SIZE

# returns rounded average
def avg_int(col: list[int]) -> int:
	if type(col) != list:
		col = list(col)
	return round(sum(col) / len(col))

# returns item center
def center(pos: tuple[int, int]) -> tuple[int, int]:
	return pos[0] + SIZE // 2, pos[1] + SIZE // 2

# recipe object
class Recipe:
	# recipe constructor
	def __init__(self, result: Item):
		self.res = result
		self.ings = []

	# get result true position
	def pos(self, camera: tuple[int, int], window: tuple[int, int]) -> tuple[int, int]:
		return self.res.pos(camera, window)

	# draws recipe
	def draw(self, surface: py.Surface, camera: tuple[int, int], window: tuple[int, int]) -> None:
		# get item positions
		rx, ry = center(self.res.pos(camera, window))
		ing_pos = [center(ing.pos(camera, window)) for ing in self.ings]

		# draw horizontal connector
		min_x = min(pos[0] for pos in ing_pos)
		max_x = max(pos[0] for pos in ing_pos)
		hor_y = (avg_int(ing[1] for ing in ing_pos) + ry) // 2
		py.draw.rect(surface, (255, 255, 255), (min_x, hor_y, max_x - min_x, 1))

		# draw vertical connectors
		py.draw.rect(surface, (255, 255, 255), (rx, ry, 1, hor_y - ry))
		for ing in ing_pos:
			py.draw.rect(surface, (255, 255, 255), (ing[0], hor_y, 1, ing[1] - hor_y))

		# draw items
		self.res.draw(surface, camera, window)
		for ing in self.ings:
			ing.draw(surface, camera, window)