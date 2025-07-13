import pygame as py
import catalog as cat

# item catalog
db = cat.Catalog()

# item size
SIZE = 48
BORDER = 4

# coordinate scalers
# if x = 2, then there should be half of SIZE between items
X_MULT = SIZE * 3 // 4
# separate ingredient layers by 1 item height
Y_MULT = SIZE * 2

# item object
class Item: pass
class Recipe: pass
class Item:
	colliders = []

	# returns all items at mouse position
	@classmethod
	def get_at(cls, pos: tuple[int, int]) -> tuple[dict]:
		return tuple(filter(
			lambda x: (x['box'][0] <= pos[0] < x['box'][2]) and (x['box'][1] <= pos[1] < x['box'][3]),
			cls.colliders
		))

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

	# return item index
	@property
	def idx(self) -> int:
		return self.i

	# item representation
	def __str__(self) -> str:
		return f'{db.get(self.i)[0]} @({self.x}, {self.y})'

	# calculates true position
	def pos(self, camera: tuple[int, int], window: tuple[int, int]) -> tuple[int, int]:
		# scale coordinates
		tx = self.x * X_MULT
		ty = self.y * Y_MULT

		# window + size offset makes item at (0, 0) perfectly in the middle of the window
		tx += (window[0] - SIZE) // 2 - camera[0]
		ty += (window[1] - SIZE) // 2 - camera[1]
		return tx, ty

	# draws item
	def draw(self, surface: py.Surface, camera: tuple[int, int], window: tuple[int, int]) -> int:
		tx, ty = self.pos(camera, window)

		# draw rects
		_, fill, out = db.get(self.i)
		py.draw.rect(surface, out, (tx, ty, SIZE, SIZE))
		py.draw.rect(surface, fill, (tx + BORDER, ty + BORDER, SIZE - BORDER * 2, SIZE - BORDER * 2))

		# register collider
		# min x, min y, max x, max y, item reference, result of, ingredient of
		collider = {
			'box': (tx, ty, tx + SIZE, ty + SIZE),
			'item': self,
			'resof': None,
			'ingof': None
		}
		self.colliders.append(collider)
		return len(self.colliders) - 1