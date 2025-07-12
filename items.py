import pygame as py
import catalog as cat

# item catalog
db = cat.Catalog()

# item size
SIZE = 48
BORDER = 4

# item object
class Item: pass
class Item:
	colliders = []

	# returns all items at mouse position
	@classmethod
	def get_at(cls, pos: tuple[int, int]) -> tuple[Item]:
		return tuple(map(lambda x: x[4], filter(
			lambda x: (x[0] <= pos[0] < x[2]) and (x[1] <= pos[1] < x[3]),
			cls.colliders
		)))

	# item constructor
	def __init__(self, x: int, y: int, id: int | str):
		# lookup item by name
		if type(id) == str:
			for idx, (name, _, _) in enumerate(db.data):
				if name.lower() == id:
					id = idx
					break
			else:
				raise KeyError(f'failed to find item "{id}"')

		self.x: int = x
		self.y: int = y
		self.i: int = id

	# item representation
	def __str__(self) -> str:
		return f'{db.get(self.i)[0]} @({self.x}, {self.y})'

	# draws item
	def draw(self, surface: py.Surface, camera: tuple[int, int], window: tuple[int, int]) -> None:
		# calculate true position
		# window + size offset makes item at (0, 0) perfectly in the middle of the window
		tx = self.x * 64 - camera[0] + (window[0] - SIZE) // 2
		ty = self.y * 64 - camera[1] + (window[1] - SIZE) // 2

		# draw rects
		_, fill, out = db.get(self.i)
		py.draw.rect(surface, out, (tx, ty, SIZE, SIZE))
		py.draw.rect(surface, fill, (tx + BORDER, ty + BORDER, SIZE - BORDER * 2, SIZE - BORDER * 2))

		# adds item collider
		self.colliders.append((tx, ty, tx + SIZE, ty + SIZE, self))