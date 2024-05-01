import tsapp
import blocks
import random
import math
# from pprint import pp


def _distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def _make_circle(world_list, center_y, center_x, radius, block):
    for y in range(center_y - radius, center_y + radius):
        for x in range(center_x - radius, center_x + radius):
            if _distance(center_y, center_x, y, x) < radius / 1.1:
                world_list[y][x] = block


# While world generation seems complicated, it's actually quite simple.
# Imagine it like you're sculpting. You start off with a base, put material onto it, and then sculpt out the features.
# That's what this program is going to do, and the basis of world generation.
class WorldGeneration:

    # Initialization function. Creates an empty grid, defined by the size that's imputed.
    def __init__(self, size):
        self.world = []
        self.world_width = 110 * int(size)
        self.world_height = 70 * int(size)
        self.window = tsapp.GraphicsWindow()
        for y in range(self.world_height):
            y_list = []
            self.world.append(y_list)
        # pp(self.world)

    def generate_world(self):
        # Fills the entire grid with stone and dirt.
        # Take the world height and divide it by 10, then multiply that number by 2, that's the "surface" layer.
        # Whatever is left, fill it with stone.
        for y in range(self.world_height):
            for x in range(self.world_width):
                if y <= int((self.world_height / 10)) * 2:
                    dirt = tsapp.Sprite("sprites/dirt block.png", 0, 0)
                    block = blocks.Block(dirt, (), "dirt block", True, self.window)
                    self.world[y].append(block)
                elif y > int((self.world_height / 10)) * 2:
                    stone = tsapp.Sprite("sprites/stone block.png", 0, 0)
                    block = blocks.Block(stone, (), "stone block", True, self.window)
                    self.world[y].append(block)

        # Gets the middle of the dirt layer to create the top layer with grass
        value = 0
        for x in range(self.world_width):
            direction = random.choice(("up", "up", "stay", "stay", "stay", "down", "down"))
            if direction == "up" and value >= 1:
                value -= 1
            elif direction == "down" and value <= 1:
                value += 1
            grass = tsapp.Sprite("sprites/grass block.png", 0, 0)
            block = blocks.Block(grass, (), "grass block", True, self.window)
            self.world[int(self.world_height / 10) + value][x] = block

        # Replaces all area above grass with air
        for x in range(self.world_width):
            for y in range(self.world_height):
                if self.world[y][x].name == "grass block":
                    break
                elif self.world[y][x].name != "grass block":
                    air = tsapp.Sprite("sprites/air block.png", 0, 0)
                    block = blocks.Block(air, (), "air block", False, self.window)
                    self.world[y][x] = block

        # Makes the fine line between the stone and dirt layer more "organic"
        for x in range(self.world_width):
            go_down = random.choice((False, False, True))
            if go_down:
                dirt = tsapp.Sprite("sprites/dirt block.png", 0, 0)
                block = blocks.Block(dirt, (), "dirt block", True, self.window)
                self.world[(int((self.world_height / 10)) * 2) + 1][x] = block
        for x in range(self.world_width):
            go_up = random.choice((False, False, True))
            if go_up:
                stone = tsapp.Sprite("sprites/stone block.png", 0, 0)
                block = blocks.Block(stone, (), "stone block", True, self.window)
                self.world[(int((self.world_height / 10)) * 2)][x] = block

        # Adds Patches of Dirt in the Stone Layer.
        dirt = tsapp.Sprite("sprites/dirt block.png", 0, 0)
        block = blocks.Block(dirt, (), "dirt block", True, self.window)
        _make_circle(self.world, 35, 50, 20, block)

    def generate_map(self):
        for y in range(self.world_height):
            for x in range(self.world_width):
                pixel = tsapp.Sprite("sprites/pixel sprites/" + self.world[y][x].name + " pixel.png", 0, 0)
                self.window.add_object(pixel)
                pixel.x = x * 6
                pixel.y = y * 6
                self.window.add_object(pixel)


world = WorldGeneration(1)
world.generate_world()
world.generate_map()
while world.window.is_running:
    world.window.finish_frame()
