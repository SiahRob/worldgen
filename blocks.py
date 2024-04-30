import tsapp


class Block:

    def __init__(self, sprite, position, name, collision, window):
        self.sprite = sprite
        self.position = position
        self.name = name
        self.collision = collision
        self.window = window

    @property
    def block_has_collision(self):
        return self.collision

    @block_has_collision.setter
    def block_has_collision(self, boolean):
        self.collision = boolean

    def refresh_sprite(self):
        self.sprite.destroy()
        refreshed_sprite = tsapp.Sprite("sprites/" + self.name + ".png", 0, 0)
        refreshed_sprite.center_x = self.position[0]
        refreshed_sprite.center_y = self.position[1]
        self.sprite = refreshed_sprite
