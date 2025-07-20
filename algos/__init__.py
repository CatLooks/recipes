from algos import box
from algos import tower
from items import Item, db
from recipes import Recipe
import random

# generates a random boolean based on probability rate
def random_chance(rate: float) -> bool:
	return random.uniform(0, 1) < rate

# generates a random item
def random_item() -> Item:
	return Item(0, 0, random.randrange(db.count))

# generates a random recipe tree
def random_tree(depth: int, bias: int = 1) -> Recipe | Item:
	# generate item
	if depth <= 0 or random_chance(0.4 / depth):
		return random_item()
	
	# generate recipe
	rec = Recipe(random_item())
	
	# ingredient count
	count = 1
	if random.randrange(bias) == 0:
		count = random.randint(2, min([2 + depth // 3, 5]))

	# generate ingredients
	for _ in range(count):
		rec.ings.append(random_tree(depth - 1, random.randint(1, 4)))
	return rec

# algorithm index
# [todo]
index = {
	'leaf-l': box.balance_left,
	'leaf-c': box.balance_center,
	'tower-0': lambda x: tower.balance(x, 0),
	'tower-2': lambda x: tower.balance(x, 2),
}