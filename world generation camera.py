import tsapp
import blocks
import random
import math


def _distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def _make_circle(world_list, center_y, center_x, radius, name, collision):
    for y in range(center_y - radius, center_y + radius):
        for x in range(center_x - radius, center_x + radius):
            if _distance(center_y, center_x, y, x) < radius / 1.1:
                sprite = tsapp.Sprite("sprites/" + name + ".png", 0, 0)
                block = blocks.Block(sprite, (), name, collision)
                world_list[y][x] = block


# While world generation seems complicated, it's actually quite simple.
# Imagine it like you're sculpting. You start off with a base, put material onto it, and then sculpt out the features.
# That's what this program is going to do, and the basis of world generation.
class WorldGeneration:

    # Initialization function. Creates an empty grid, defined by the size that's imputed.
    def __init__(self, size):
        self.world = []
        self.world_width = int(110 * size)
        self.world_height = int(70 * size)
        self.window = tsapp.GraphicsWindow(1920, 1020, tsapp.WHITE)
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
                    block = blocks.Block(dirt, (), "dirt block", True)
                    self.world[y].append(block)
                elif y > int((self.world_height / 10)) * 2:
                    stone = tsapp.Sprite("sprites/stone block.png", 0, 0)
                    block = blocks.Block(stone, (), "stone block", True)
                    self.world[y].append(block)

        # Gets the middle of the dirt layer to create the top layer with grass
        value = -1
        for x in range(self.world_width):
            direction = random.choice(("up", "up", "up", "stay", "stay", "down", "down", "down"))
            if direction == "up" and value > -2:
                value -= 1
            elif direction == "down" and value < 2:
                value += 1
            grass = tsapp.Sprite("sprites/grass block.png", 0, 0)
            block = blocks.Block(grass, (), "grass block", True)
            self.world[int(self.world_height / 10) + value][x] = block

        # Replaces all area above grass with air
        for x in range(self.world_width):
            for y in range(self.world_height):
                if self.world[y][x].name == "grass block":
                    break
                elif self.world[y][x].name != "grass block":
                    air = tsapp.Sprite("sprites/air block.png", 0, 0)
                    block = blocks.Block(air, (), "air block", False)
                    self.world[y][x].sprite.destroy()
                    self.world[y][x] = block

        # Makes the fine line between the stone and dirt layer more "organic"
        for x in range(self.world_width):
            go_down = random.choice((False, False, True))
            if go_down:
                dirt = tsapp.Sprite("sprites/dirt block.png", 0, 0)
                block = blocks.Block(dirt, (), "dirt block", True)
                self.world[(int((self.world_height / 10)) * 2) + 1][x] = block
        for x in range(self.world_width):
            go_up = random.choice((False, False, True))
            if go_up:
                stone = tsapp.Sprite("sprites/stone block.png", 0, 0)
                block = blocks.Block(stone, (), "stone block", True)
                self.world[(int((self.world_height / 10)) * 2)][x] = block

        # Add some diamond to the Stone Layer.
        patches = random.randint(int(self.world_height * 1.5), int(self.world_width * 1.5))
        for i in range(patches):
            rand_radi = 1
            rand_x = random.randint(rand_radi, self.world_width - rand_radi)
            rand_y = random.randint(rand_radi + 35, (self.world_height - int((self.world_height / 10)) * 2) - rand_radi - 1)
            _make_circle(self.world, rand_y + int((self.world_height / 10)) * 2, rand_x, rand_radi, "diamond ore block", True)

        # Add some gold to the Stone Layer.
        patches = random.randint(int((self.world_height / 10) * 4.5), int((self.world_width / 10) * 4.5))
        for i in range(patches):
            rand_radi = random.randint(1, 2)
            rand_x = random.randint(rand_radi, self.world_width - rand_radi)
            rand_y = random.randint(rand_radi + 30, (self.world_height - int((self.world_height / 10)) * 2) - rand_radi - 5)
            _make_circle(self.world, rand_y + int((self.world_height / 10)) * 2, rand_x, rand_radi, "gold ore block", True)

        # Add some iron to the Stone Layer.
        patches = random.randint(int((self.world_height / 10) * 4), int((self.world_width / 10) * 4))
        for i in range(patches):
            rand_radi = random.randint(int((self.world_height / 10) / 3.5), int((self.world_height / 10) / 2.5))
            rand_x = random.randint(rand_radi, self.world_width - rand_radi)
            rand_y = random.randint(rand_radi + 17, (self.world_height - int((self.world_height / 10)) * 2) - rand_radi - 10)
            _make_circle(self.world, rand_y + int((self.world_height / 10)) * 2, rand_x, rand_radi, "iron ore block", True)

        # Add some coal to the Stone Layer.
        patches = random.randint(int(self.world_height / 10) * 5, int(self.world_width / 10) * 5)
        for i in range(patches):
            rand_radi = random.randint(int((self.world_height / 10) / 3), int((self.world_height / 10) / 2))
            rand_x = random.randint(rand_radi, self.world_width - rand_radi)
            rand_y = random.randint(rand_radi, (self.world_height - int((self.world_height / 10)) * 2) - rand_radi - 30)
            _make_circle(self.world, rand_y + int((self.world_height / 10)) * 2, rand_x, rand_radi, "coal ore block", True)

        # Adds Patches of Dirt in the Stone Layer.
        patches = random.randint(int(self.world_height / 10) * 5, int(self.world_width / 10) * 5)
        for i in range(patches):
            rand_radi = random.randint(int((self.world_height / 10) / 3), int((self.world_height / 10) / 1.69))
            rand_x = random.randint(rand_radi, self.world_width - rand_radi)
            rand_y = random.randint(rand_radi, (self.world_height - int((self.world_height / 10)) * 2) - rand_radi)
            _make_circle(self.world, rand_y + int((self.world_height / 10)) * 2, rand_x, rand_radi, "dirt block", True)

        # Adds Patches of Air in the Stone Layer.
        patches = random.randint(int(self.world_height / 10) * 5 + 1, int(self.world_width / 10) * 5 + 1)
        for i in range(patches):
            rand_radi = random.randint(int((self.world_height / 10) / 3) + 1, int((self.world_height / 10) / 1.69))
            rand_x = random.randint(rand_radi, self.world_width - rand_radi)
            rand_y = random.randint(rand_radi, (self.world_height - int((self.world_height / 10)) * 2) - rand_radi - 1)
            _make_circle(self.world, rand_y + int((self.world_height / 10)) * 2, rand_x, rand_radi, "air block", False)

        # Should be the last thing to do, give the blocks positions.
        world_list = []
        for y in range(self.world_height):
            for x in range(self.world_width):
                world_list.append(self.world[y][x])
                self.world[y][x].position = (50 + (97 * x), 50 + (97 * y))
                self.world[y][x].refresh_sprite()

        return world_list

    # Testing Functions
    def generate_map(self):
        for y in range(self.world_height):
            for x in range(self.world_width):
                pixel = tsapp.Sprite("sprites/pixel sprites/" + self.world[y][x].name + " pixel.png", 0, 0)
                pixel.x = x * 5
                pixel.y = y * 5
                self.window.add_object(pixel)

    # -----------------------


if __name__ == "__main__":
    world = WorldGeneration(1)
    chunk = world.generate_world()
    world.generate_map()
    while world.window.is_running:
        world.window.finish_frame()
