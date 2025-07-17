from algos import box
from algos import tower
from items import Item, db
from recipes import Recipe
import random

# generates a random item
def random_item() -> Item:
	return random.randrange(db.count)

# generates a random recipe tree
def random_tree(depth: int) -> Recipe:
	# generate an item if exceeded depth or randomly
	if depth <= 0 or random.randrange(depth * 2 + 1) == 0:
		return Item(0, 0, random_item())

	# generate a random recipe
	rec: Recipe = Recipe(Item(0, 0, random_item()))
	if random.uniform(0, 1) < 0.125 and depth >= 3:
		ing_count = random.randrange(2, 6)
	else:
		ing_count = random.randrange(1, 4)
	for _ in range(ing_count):
		rec.ings.append(random_tree(depth - 1))
	return rec

# algorithm index
# [todo]
index = {
	'leaf-l': box.balance_left,
	'leaf-c': box.balance_center,
}