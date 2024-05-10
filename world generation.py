import tsapp
import blocks
import random
import math


# saved block positions
position_tuple = [(50 + (x * 97), 50 + (y * 97)) for y in range(7) for x in range(11)]
position_tuple = tuple(position_tuple)
print(position_tuple)


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
            if direction == "up" and value > -4:
                value -= 1
            elif direction == "down" and value < -1:
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

        # Adds Patches of Dirt in the Stone Layer.
        patches = random.randint(int(self.world_height / 10) * 5, int(self.world_width / 10) * 5)
        for i in range(patches):
            rand_radi = random.randint(int((self.world_height / 10) / 3), int((self.world_height / 10) / 1.69))
            rand_x = random.randint(rand_radi, self.world_width - rand_radi)
            rand_y = random.randint(rand_radi, (self.world_height - int((self.world_height / 10)) * 2) - rand_radi)
            dirt = tsapp.Sprite("sprites/dirt block.png", 0, 0)
            block = blocks.Block(dirt, (), "dirt block", True)
            _make_circle(self.world, rand_y + int((self.world_height / 10)) * 2, rand_x, rand_radi, block)

        # Adds Patches of Air in the Stone Layer.
        patches = random.randint(int(self.world_height / 10) * 5, int(self.world_width / 10) * 5)
        for i in range(patches):
            rand_radi = random.randint(int((self.world_height / 10) / 3), int((self.world_height / 10) / 1.69))
            rand_x = random.randint(rand_radi, self.world_width - rand_radi)
            rand_y = random.randint(rand_radi, (self.world_height - int((self.world_height / 10)) * 2) - rand_radi)
            air = tsapp.Sprite("sprites/air block.png", 0, 0)
            block = blocks.Block(air, (), "air block", False)
            _make_circle(self.world, rand_y + int((self.world_height / 10)) * 2, rand_x, rand_radi, block)

        # Should be the last thing to do, pack the world up into chunks and return them.
        # make sure to make a list with proper values
        chunk = []
        for chunk_y in range(0, self.world_height, int(self.world_height / 10)):
            temp_list1 = []
            for chunk_x in range(0, self.world_width, int(self.world_width / 10)):
                temp_list2 = []
                for y in range(int(self.world_height / 10)):
                    temp_list3 = []
                    for x in range(int(self.world_width / 10)):
                        temp_list3.append(self.world[y + chunk_y][x + chunk_x])
                    temp_list2.append(temp_list3)
                temp_list1.append(temp_list2)
            chunk.append(temp_list1)

        pos = 0
        for chunk_y in range(len(chunk)):
            for chunk_x in range(len(chunk[chunk_y])):
                for y in range(len(chunk[chunk_y][chunk_x])):
                    for x in range(len(chunk[chunk_y][chunk_x][y])):
                        chunk[chunk_y][chunk_x][y][x].position = position_tuple[pos]
                        chunk[chunk_y][chunk_x][y][x].refresh_sprite()
                        if chunk[chunk_y][chunk_x][y][x].name == "air block":
                            chunk[chunk_y][chunk_x][y][x].block_has_collision = False
                        pos += 1
                pos = 0

        return chunk

    # Testing Functions
    def _generate_map(self):
        for y in range(self.world_height):
            for x in range(self.world_width):
                pixel = tsapp.Sprite("sprites/pixel sprites/" + self.world[y][x].name + " pixel.png", 0, 0)
                pixel.x = x * 5
                pixel.y = (y * 5) + 500
                self.window.add_object(pixel)

    def _generate_chunk_map(self, chunk):
        for y2 in range(len(chunk)):
            for x2 in range(len(chunk[y2])):
                for y in range(int(self.world_height / 10)):
                    for x in range(int(self.world_width / 10)):
                        pixel = tsapp.Sprite("sprites/pixel sprites/" + chunk[y2][x2][y][x].name + " pixel.png", 0, 0)
                        pixel.x = (x * 5) + (x2 * int(self.world_width / 2))
                        pixel.y = (y * 5) + (y2 * int(self.world_height / 2))
                        self.window.add_object(pixel)

    # -----------------------


if __name__ == "__main__":
    world = WorldGeneration(1)
    chunk = world.generate_world()





    world._generate_chunk_map(chunk)
    #world._generate_map()
    while world.window.is_running:
        world.window.finish_frame()
