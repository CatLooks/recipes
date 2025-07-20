from items import Item
from recipes import Recipe
from itertools import zip_longest

# balance recipe tree
# returns a list of ingredient layer bounds relative to recipe result
def balance(rec: Recipe | Item, spacing: int) -> list[tuple[int, int]]:
	rec.notes.clear()

	# balance item
	if type(rec) == Item:
		return []

	# collect ingredient bounds
	bounds: list[list[tuple[int, int]]] = [balance(ing, spacing) for ing in rec.ings]

	# space out ingredients
	for i, ing in enumerate(rec.ings):
		# first ingredient is used as reference point
		if i == 0:
			ing.set(0, 1)
			continue
		prev = rec.ings[i - 1]

		# set minimal padding
		ing.set(prev.x + 2, 1)

		# get space between ingredient results
		diff: int = ing.x - prev.x

		# get minimal padding
		pads: list[int] = []
		for (_, ar), (bl, _) in zip(bounds[i - 1], bounds[i]):
			pads.append((
				(bl + diff) - ar - 2,
				ar, bl, diff
			))

		# pad ingredient
		if pads:
			pad = -min(p[0] for p in pads)
			ing.shift(pad, 0)
			### log ###
			ing.notes['pad'] = f'{pad}\n' + '\n'.join(f'* {p[1]}, {p[2]} + {p[3]}) = {p[0]}' for p in pads)

	# center recipe result
	x = rec.ings[-1].x // 2
	for ing in rec.ings:
		ing.shift(-x, 0)
	### log ###
	rec.notes['offset'] = x	

	# get ingredient layer bounds
	layers: list[tuple[int, int]] = [
		(rec.ings[0].x, rec.ings[-1].x)
	]
	for layer in zip_longest(*bounds):
		# find leftmost ingredient layer
		for i, bound in enumerate(layer):
			if bound != None:
				l_idx = i
				break

		# find rightmost ingredient layer
		for i, bound in reversed(list(enumerate(layer))):
			if bound != None:
				r_idx = i
				break

		# merge layers
		al = layer[l_idx][0] + rec.ings[l_idx].x
		br = layer[r_idx][1] + rec.ings[r_idx].x
		layers.append((al, br))
	### log ###
	rec.notes['layers'] = '\n' + '\n'.join(f'* {l}' for l in layers)

	return layers