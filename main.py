import pygame as py
import json5
import items, catalog

from items import Item, db

# load config
try:
	with open('data.json') as file:
		data = json5.load(file)
except Exception as exc:
	print(f'Error when opening "data.json": {exc}')
	raise SystemExit

# load item catalog
try:
	db.load(data)
except catalog.Error as exc:
	print(f'Error when loading item data: {exc}')
	raise SystemExit

# initialize pygame
py.init()
done = False

# create window
size = 1600, 900
win = py.display.set_mode(size, py.RESIZABLE)
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

# test item
item: Item = Item(0, 0, 'gel')

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

	# draw recipe tree
	Item.colliders.clear()
	item.draw(win, camera, win.get_size())
	item.draw(win, camera, win.get_size())

	# draw camera position
	cam_text = font.render(f'@({camera[0]}, {camera[1]}) (reset with R)', 1, (255, 255, 255))
	win.blit(cam_text, (PAD, PAD))

	# draw framerate
	fps_text = font.render(f'{int(clock.get_fps())} fps', 1, (255, 255, 255))
	win.blit(fps_text, (win.get_width() - fps_text.get_width() - PAD, PAD))

	# draw hovered item info
	hovered_items = Item.get_at(py.mouse.get_pos())
	if hovered_items:
		string = str(hovered_items[0])
		if len(hovered_items) > 1:
			string += f' +{len(hovered_items) - 1}'
		item_text = font.render(string, 1, (255, 255, 255))
		win.blit(item_text, (win.get_width() - item_text.get_width() - PAD, win.get_height() - item_text.get_height() - PAD))
	
	# wait until next frame
	py.display.flip()
	clock.tick(60)