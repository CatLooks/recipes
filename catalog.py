import pygame as py

# base error
class Error(Exception):
	# error constructor
	def __init__(self, text: str = ""):
		self.text = text

	# error representation
	def __str__(self) -> str:
		return self.text
	
# adds text to raised error
def hookup(f: any, text: str) -> any:
	try:
		return f()
	except Error as exc:
		exc.text += text
		raise exc
	
# returns dictionary field while checking its type
def get_field(data: dict, field: str, field_type: type) -> None:
	if field not in data:
		raise Error(f'field "{field}" is missing')
	if type(data[field]) != field_type:
		raise Error(f'type of "{field}" must be {field_type.__name__}, not {type(data[field]).__name__}')
	return data[field]

# parses a hexadecimal number
def parse_hex(text: str) -> int:
	try:
		return int(text, 16)
	except ValueError:
		raise Error(f'"{text}" is not a valid hex number')

# parses a color string
def parse_color_raw(color: str) -> py.Color:
	if not color.startswith('#'):
		raise Error(f'color string does not start with "#"')
	if len(color) == 7:
		r = parse_hex(color[1:3])
		g = parse_hex(color[3:5])
		b = parse_hex(color[5:7])
		return py.Color(r, g, b)
	if len(color) == 4:
		r = parse_hex(color[1]) * 0x11
		g = parse_hex(color[2]) * 0x11
		b = parse_hex(color[3]) * 0x11
		return py.Color(r, g, b)
	raise Error(f'invalid color string length (expected 4 or 7, got {len(color)})')

# parses a color string
def parse_color(color: str) -> py.Color:
	return hookup(lambda: parse_color_raw(color), f' while parsing color "{color}"')

# item database
class Catalog:
	# catalog constructor
	def __init__(self):
		self.data: list[str, py.Color, py.Color] = []
		self.algos: list[str, any] = []
		self.border = 0

	# loads item catalog from json data
	def load(self, data: dict, algos: __module__) -> None:
		# load item data
		for i, item in enumerate(get_field(data, 'items', list)):
			self.data.append((
				hookup(lambda: get_field(item, 'name', str), f' while parsing item {i}'),
				parse_color(get_field(item, 'a', str)),
				parse_color(get_field(item, 'b', str))
			))

		# load algorithm data
		for i, algo in enumerate(get_field(data, 'algorithms', list)):
			path = get_field(algo, 'func', str)
			if path not in algos.index:
				raise Error(f'algorithm "{path}" not found')
			self.algos.append((
				get_field(algo, 'name', str),
				algos.index[path]
			))

		# load image border
		self.border = get_field(data, 'border', int)

	# returns total item count
	@property
	def count(self):
		return len(self.data)
	
	# returns total item count
	@property
	def algocount(self):
		return len(self.algos)

	# returns item data
	def get(self, id: int) -> tuple[str, py.Color, py.Color]:
		return self.data[id]