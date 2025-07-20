import pygame as py
import json5
import catalog
import algos

from items import Item, db
from recipes import Recipe

# load config
try:
	with open('data.json') as file:
		data = json5.load(file)
except Exception as exc:
	print(f'Error when opening "data.json": {exc}')
	raise SystemExit

# load item catalog
try:
	db.load(data, algos)
except catalog.Error as exc:
	print(f'Error when loading item data: {exc}')
	raise SystemExit

# initialize pygame
py.init()
done = False

# create window
size = 1600, 900
win = py.display.set_mode(size, py.RESIZABLE, vsync = 1)
py.display.set_caption('Recipe Tree')

# initialize window related stuff
clock = py.time.Clock()
font = py.font.SysFont('cascadia code', 20)
PAD = 8 # text info pad from borders

# multiline text drawer
def draw_text(text: list[str], *, flip_x: bool, flip_y: bool) -> None:
	# initial position
	pos = [
		win.get_width() - PAD if flip_x else PAD,
		win.get_height() - PAD if flip_y else PAD
	]

	# draw each line
	for line in text:
		text_surface = font.render(line, 1, (255, 255, 255))

		# get text position
		text_pos = (
			pos[0] - text_surface.get_width() if flip_x else pos[0],
			pos[1] - text_surface.get_height() if flip_y else pos[1]
		)

		# draw & calculate next position
		win.blit(text_surface, text_pos)
		if flip_y:
			pos[1] -= text_surface.get_height()
		else:
			pos[1] += text_surface.get_height()

# camera related stuff
camera = 0, 0
drag = {
	'cam': (0, 0),   # camera position at start
	'mouse': (0, 0), # mouse position at start
	'active': False, # whether currently dragging
}

# generator settings
algo = 0
depth = 3

# test recipe
rec: Recipe = Recipe(Item(0, 0, 'gel'))
rec.ings.append(Item(-2, 1, 'iron'))
rec.ings.append(Item( 0, 1, 'gold'))
rec.ings.append(Recipe(Item(2, 1, 'ruby')))
rec.ings[2].ings.append(Item(-1, 1, 'emerald'))
rec.ings[2].ings.append(Item( 1, 1, 'amethyst'))
db.algos[algo][1](rec)

# recipe cursor
cursor: list[int] = []

# returns currently pointed object
def select() -> Recipe | Item:
	now = rec
	for branch in cursor:
		now = now.ings[branch]
	return now

# returns parent of currently pointed object
def parent() -> Recipe | Item:
	now = rec
	for branch in cursor[:-1]:
		now = now.ings[branch]
	return now

# returns parent of parent of currently pointed object
def parent_ex() -> Recipe | Item:
	now = rec
	for branch in cursor[:-2]:
		now = now.ings[branch]
	return now

# main loop
while True:
	# handle events
	for evt in py.event.get():
		# check for window close
		if evt.type == py.QUIT:
			done = True
			break

		# check for drag start
		elif evt.type == py.MOUSEBUTTONDOWN:
			drag['cam'] = camera
			drag['mouse'] = py.mouse.get_pos()
			drag['active'] = True

		# check for drag stop
		elif evt.type == py.MOUSEBUTTONUP:
			drag['active'] = False

		# keyboard events
		elif evt.type == py.KEYDOWN:
			# reset camera position
			if evt.key == py.K_c:
				drag['active'] = False
				camera = 0, 0

			# cycle algorithms
			elif evt.key == py.K_b:
				algo += 1
				algo %= db.algocount
				db.algos[algo][1](rec)

			# generate new tree
			elif evt.key == py.K_g:
				rec = algos.random_tree(depth)
				cursor.clear()
				db.algos[algo][1](rec)

			# change depth
			elif evt.key == py.K_LEFTBRACKET:
				if depth > 1:
					depth -= 1
			elif evt.key == py.K_RIGHTBRACKET:
				depth += 1

			# cursor move controls
			elif evt.key == py.K_LEFT:
				if cursor and cursor[-1] > 0:
					cursor[-1] -= 1
			elif evt.key == py.K_RIGHT:
				if cursor and cursor[-1] < len(parent().ings) - 1:
					cursor[-1] += 1
			elif evt.key == py.K_DOWN:
				current = select()
				if type(current) == Recipe:
					cursor.append((len(current.ings) - 1) // 2)
			elif evt.key == py.K_UP:
				if cursor:
					cursor.pop()
			
			# cursor edit controls
			elif evt.key == py.K_q:
				if cursor:
					parent().ings.insert(cursor[-1], algos.random_item())
				db.algos[algo][1](rec)
			elif evt.key == py.K_w:
				if cursor:
					parent().ings.insert(cursor[-1] + 1, algos.random_item())
				db.algos[algo][1](rec)
			elif evt.key == py.K_r:
				if cursor and type(select()) == Item:
					parent().ings[cursor[-1]] = Recipe(select())
					select().ings.append(algos.random_item())
				db.algos[algo][1](rec)
			elif evt.key == py.K_e:
				if cursor:
					if len(parent().ings) == 1:
						if len(cursor) == 1:
							rec = parent().res
						else:
							parent_ex().ings[cursor[-2]] = parent().res
						cursor.pop()
					else:
						parent().ings.pop(cursor[-1])
						cursor[-1] -= 1
				db.algos[algo][1](rec)

	# quit if window is closed
	if done:
		py.quit()
		break

	# drag camera with mouse
	if drag['active']:
		camera = (
			drag['cam'][0] - (py.mouse.get_pos()[0] - drag['mouse'][0]),
			drag['cam'][1] - (py.mouse.get_pos()[1] - drag['mouse'][1])
		)

	# clear frame
	win.fill((29, 31, 37))

	# reset object colliders
	Item.colliders.clear()

	# draw recipe tree
	Item.selector = select().id
	rec.draw((0, 0), win, camera, win.get_size())

	# top left corner text
	draw_text([
		f'@({camera[0]}, {camera[1]}) (reset with C)',
		f'Algorithm: {db.algos[algo][0]} (cycle with B, generate new with G)',
		f'Depth: {depth} (change with [ and ])',
		'',
		'Navigate recipe tree with arrow keys',
		'Q - add item from right side',
		'W - add item from left side',
		'E - erase item / recipe',
		'R - convert item into a recipe'
	], flip_x = 0, flip_y = 0)

	# text containers
	tr_text: list[str] = []
	bl_text: list[str] = []
	br_text: list[str] = []

	# draw fps
	br_text.append(f'{int(clock.get_fps())} fps')

	# draw hovered item info
	hovered_items = Item.get_at(py.mouse.get_pos())
	if hovered_items:
		# item info
		string = str(hovered_items[0]['item'])
		if len(hovered_items) > 1:
			string += f' +{len(hovered_items) - 1}'
		bl_text.append(string)

		# recipe debug data
		if hovered_items[0]['resof'] != None:
			recipe_debug = hovered_items[0]['resof'].notestr
			if recipe_debug:
				tr_text.append(f'[R] {recipe_debug}')

		# item debug data
		item_debug = hovered_items[0]['item'].notestr
		if item_debug:
			tr_text.append(f'[I] {item_debug}')

		# ingredient & result of
		bl_text.append(f'Used in: {hovered_items[0]["ingof"]}')
		bl_text.append(f'Recipe: {hovered_items[0]["resof"]}')

	# draw text
	draw_text(tr_text, flip_x = 1, flip_y = 0)
	draw_text(bl_text, flip_x = 0, flip_y = 1)
	draw_text(br_text, flip_x = 1, flip_y = 1)
	
	# wait until next frame
	py.display.flip()
	clock.tick(60)