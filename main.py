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
			if evt.key == py.K_r:
				drag['active'] = False
				camera = 0, 0

			# cycle algorithms
			elif evt.key == py.K_q:
				algo += 1
				algo %= db.algocount
				db.algos[algo][1](rec)

			# generate new tree
			elif evt.key == py.K_g:
				rec = algos.random_tree(depth)
				db.algos[algo][1](rec)

			# change depth
			elif evt.key == py.K_LEFT:
				if depth > 1:
					depth -= 1
			elif evt.key == py.K_RIGHT:
				depth += 1

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
	Recipe.colliders_ing.clear()
	Recipe.colliders_res.clear()

	# draw recipe tree
	rec.draw((0, 0), win, camera, win.get_size())

	# draw camera position
	cam_text = font.render(f'@({camera[0]}, {camera[1]}) (reset with R)', 1, (255, 255, 255))
	win.blit(cam_text, (PAD, PAD))

	# draw current algorithm
	algo_text = font.render(f'Algorithm: {db.algos[algo][0]} (cycle with Q, generate new with G)', 1, (255, 255, 255))
	win.blit(algo_text, (PAD, cam_text.get_height() + PAD))

	# draw current depth
	dep_text = font.render(f'Depth: {depth} (change with < & > arrows)', 1, (255, 255, 255))
	win.blit(dep_text, (PAD, cam_text.get_height() + algo_text.get_height() + PAD))

	# draw framerate
	fps_text = font.render(f'{int(clock.get_fps())} fps', 1, (255, 255, 255))
	win.blit(fps_text, (win.get_width() - fps_text.get_width() - PAD, PAD))

	# draw hovered item info
	hovered_items = Item.get_at(py.mouse.get_pos())
	if hovered_items:
		# item info
		string = str(hovered_items[0]['item'])
		if len(hovered_items) > 1:
			string += f' +{len(hovered_items) - 1}'
		item_text = font.render(string, 1, (255, 255, 255))
		win.blit(item_text, (win.get_width() - item_text.get_width() - PAD, win.get_height() - item_text.get_height() - PAD))

		# recipe debug data
		if hovered_items[0]['resof'] != None:
			dbg_text = font.render(hovered_items[0]['resof'].notestr, 1, (255, 255, 255))
			win.blit(dbg_text, (win.get_width() - dbg_text.get_width() - PAD, win.get_height() - item_text.get_height() - dbg_text.get_height() - PAD))

		# ingredient of
		ingof_text = font.render(f'Used in: {hovered_items[0]["ingof"]}', 1, (255, 255, 255))
		win.blit(ingof_text, (PAD, win.get_height() - ingof_text.get_height() - PAD))

		# result of
		resof_text = font.render(f'Recipe: {hovered_items[0]["resof"]}', 1, (255, 255, 255))
		win.blit(resof_text, (PAD, win.get_height() - resof_text.get_height() - ingof_text.get_height() - PAD))
	
	# wait until next frame
	py.display.flip()
	clock.tick(60)