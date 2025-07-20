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
def random_tree(depth: int, boost: float = 1.0) -> Recipe | Item:
	# generate item
	if depth <= 0 or random_chance(0.4 / depth):
		return random_item()
	
	# generate recipe
	rec = Recipe(random_item())
	
	# ingredient count
	dice = random.uniform(0, 1)
	if dice < 0.35:
		count = 1
	elif dice < 0.75:
		count = 2
	elif dice < 0.95:
		count = 3 if random_chance(0.85) else 4
	else:
		count = 3
		if random_chance(0.3):
			count = 4
			if random_chance(0.2):
				count = random.randint(5, 8)

	# biased boosts indices
	biases: list[int] = [random.randrange(count)]
	if random_chance(0.3):
		biases.append(random.randrange(count))

	# generate ingredients
	for idx in range(count):
		boost: float = random.uniform(0.5, 1) if idx in biases else random.uniform(0, 1)
		rec.ings.append(random_tree(depth - 1, boost))
	return rec

# algorithm index
# [todo]
index = {
	'leaf-l': box.balance_left,
	'leaf-c': box.balance_center,
	'tower-0': lambda x: tower.balance(x, 0),
	'tower-2': lambda x: tower.balance(x, 2),
}