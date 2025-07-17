from items import Item
from recipes import Recipe

# balance recipe tree
# returns recipe bounding box width
def balance_left(rec: Recipe | Item) -> int:
	# balance item
	if type(rec) == Item:
		return 1
	
	# get recipe width & space out ingredients
	width: int = 0
	for ing in rec.ings:
		# set ingredient position
		ing.set(width * 2, 1)

		# update total width
		width += balance_left(ing)
	### log ###
	rec.notes['width'] = width

	# return recipe width
	return width

# balance recipe tree
# returns recipe bounding box width
def balance_center(rec: Recipe | Item) -> int:
	# balance item
	if type(rec) == Item:
		return 1
	
	# get recipe width & space out ingredients
	width: int = 0
	for ing in rec.ings:
		ing_width = balance_center(ing)

		# set ingredient position
		ing.set(width * 2 + ing_width - 1, 1)

		# update total width
		width += ing_width
	### log ###
	rec.notes['width'] = width

	# shift ingredients => center result
	shift: int = width - 1
	for ing in rec.ings:
		ing.shift(-shift, 0)
	### log ###
	rec.notes['shift'] = shift

	# return recipe width
	return width