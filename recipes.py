import pygame as py
from items import Item, db, SIZE

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
		self.res: Item = result
		self.ings: list[Item | Recipe] = []
		self.notes: dict = {}

	# references to recipe result
	@property
	def x(self) -> int:
		return self.res.x
	@property
	def y(self) -> int:
		return self.res.y
	@property
	def id(self) -> int:
		return self.res.id

	# returns recipe debug notes
	@property
	def notestr(self) -> str:
		return ', '.join(f'{key}: {val}' for key, val in self.notes.items())

	# sets recipe position
	def set(self, x: int, y: int) -> None:
		self.res.x = x
		self.res.y = y

	# shifts item position
	def shift(self, x: int, y: int) -> None:
		self.res.x += x
		self.res.y += y

	# return recipe result index
	@property
	def idx(self) -> int:
		return self.res.i

	# recipe representation
	def __str__(self) -> str:
		ings = ', '.join(db.get(ing.idx)[0] for ing in self.ings)
		return f'[{ings}] = {db.get(self.res.idx)[0]}'

	# get result true position
	def pos(self, offset: tuple[int, int], camera: tuple[int, int], window: tuple[int, int]) -> tuple[int, int]:
		return self.res.pos(offset, camera, window)

	# draws recipe
	def draw(self, offset: tuple[int, int], surface: py.Surface, camera: tuple[int, int], window: tuple[int, int]) -> None:
		res_off = offset[0] + self.res.x, offset[1] + self.res.y

		# get item positions
		rx, ry = center(self.res.pos(offset, camera, window))
		ing_pos = [center(ing.pos(res_off, camera, window)) for ing in self.ings]

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
		res_idx = self.res.draw(offset, surface, camera, window)
		ing_idx = [ing.draw(res_off, surface, camera, window) for ing in self.ings]

		# bind to colliders
		Item.colliders[res_idx]['resof'] = self
		for idx in ing_idx:
			Item.colliders[idx]['ingof'] = self

		# return result collider
		return res_idx