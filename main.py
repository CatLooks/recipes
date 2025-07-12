import pygame as py

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

# main loop
while True:
	# handle events
	for evt in py.event.get():
		# check for window close
		if evt.type == py.QUIT:
			done = True
			break

	# quit if window is closed
	if done:
		py.quit()
		break

	# draw new frame
	win.fill((29, 31, 37))

	# draw framerate
	fps_text = font.render(f'{int(clock.get_fps())} fps', 1, (255, 255, 255))
	win.blit(fps_text, (
		win.get_width() - fps_text.get_width(),
		win.get_height() - fps_text.get_height()
	))
	
	# wait until next frame
	py.display.flip()
	clock.tick(60)