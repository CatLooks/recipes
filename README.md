# Recipes Viewer
Displays efficiently packed recipe tree.

Each recipe is defined as a list of ingredient items and a resulting item.

# Items
Items are randomly pulled from `data.json`.

# Balancing Algorithms
Balancing algorithms are stored in `algos/` folder.

Algorithm index is defined in `algos/__init__.py`.

# Controls
| Button | Action |
|--------|--------|
| LMB | Mouse camera movement |
| C | Resets camera position |
| B | Cycle balancing algorithm |
| G | Generate a new random recipe tree |
| [ | Decrease maximum depth |
| ] | Increase maximum depth |
| Left & Right Arrow | Move to neighboring ingredient |
| Up Arrow | Select recipe result |
| Down Arrow | Select middle ingredient of selected recipe |
| Q | Insert a random item before selected ingredient |
| W | Insert a random item after selected ingredient |
| E | Erase recipe or item |
| R | Replaces an item by a recipe with a single ingredient |
| CTRL + S | Save current recipe tree as an image (saved to `./recipe.png`) |