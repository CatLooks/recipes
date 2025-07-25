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
	selector: int = None
	next_id = 0

	screen_rect = None

	# updates screen rect to include another rect
	@classmethod
	def merge_rect(cls, rect: tuple[int, int, int, int]) -> None:
		if cls.screen_rect == None:
			cls.screen_rect = list(rect)
			return
		cls.screen_rect[0] = min(cls.screen_rect[0], rect[0])
		cls.screen_rect[1] = min(cls.screen_rect[1], rect[1])
		cls.screen_rect[2] = max(cls.screen_rect[2], rect[2])
		cls.screen_rect[3] = max(cls.screen_rect[3], rect[3])

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
		self.notes: dict = {}

		# assign item ID
		self.id = Item.next_id
		Item.next_id += 1

	# returns item debug notes
	@property
	def notestr(self) -> str:
		return '\n'.join(f'{key}: {val}' for key, val in self.notes.items())

	# sets item position
	def set(self, x: int, y: int) -> None:
		self.x = x
		self.y = y

	# shifts item position
	def shift(self, x: int, y: int) -> None:
		self.x += x
		self.y += y

	# return item index
	@property
	def idx(self) -> int:
		return self.i

	# item representation
	def __str__(self) -> str:
		return f'{db.get(self.i)[0]} @({self.x}, {self.y})'

	# calculates true position
	def pos(self, offset: tuple[int, int], camera: tuple[int, int], window: tuple[int, int]) -> tuple[int, int]:
		# scale coordinates
		tx = (self.x + offset[0]) * X_MULT
		ty = (self.y + offset[1]) * Y_MULT

		# window + size offset makes item at (0, 0) perfectly in the middle of the window
		tx += (window[0] - SIZE) // 2 - camera[0]
		ty += (window[1] - SIZE) // 2 - camera[1]
		return tx, ty

	# draws item
	def draw(self, offset: tuple[int, int], surface: py.Surface, camera: tuple[int, int], window: tuple[int, int]) -> int:
		tx, ty = self.pos(offset, camera, window)

		# draw rects
		_, fill, out = db.get(self.i)
		py.draw.rect(surface, out, (tx, ty, SIZE, SIZE))
		py.draw.rect(surface, fill, (tx + BORDER, ty + BORDER, SIZE - BORDER * 2, SIZE - BORDER * 2))

		# draw selector outlines
		if self.id == self.selector:
			py.draw.rect(surface, (255, 255, 255), (tx - 2, ty - 2, SIZE + 4, SIZE + 4), 1)
			py.draw.rect(surface, (255, 255, 255), (tx - 4, ty - 4, SIZE + 8, SIZE + 8), 1)

		# register collider
		collider = {
			'box': (tx, ty, tx + SIZE, ty + SIZE),
			'item': self,
			'resof': None,
			'ingof': None
		}
		self.colliders.append(collider)
		self.merge_rect(collider['box'])
		return len(self.colliders) - 1