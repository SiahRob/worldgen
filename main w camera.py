import tsapp
import pygame
import world_generation as w
import blocks
pygame.init()

world_class = w.WorldGeneration(1)

world = world_class.generate_world()
window = tsapp.GraphicsWindow(1070, 682, (200, 200, 255))

# ideas to spruce up the generation a bit.
# Iron ore, Coal Ore, Gold ore, diamond ore, trees

player = tsapp.Sprite("sprites/player person.png", 0, 0)
player.scale = 0.5
player.center_y = window.height / 2
player.center_x = window.width / 2
window.add_object(player)
rendered_blocks = []
block_coll_var = 56
while window.is_running:
    stored = int(world_class.world[17][0].sprite.y - player.y)
    mouse_x, mouse_y = tsapp.get_mouse_position()

    for i in range(len(world)):
        if -100 < world[i].sprite.center_x < window.width + 100 and -100 < world[i].sprite.center_y < window.height + 100:
            window.add_object(world[i].sprite)
            rendered_blocks.append(world[i])
        if -100 < world[i].sprite.center_x < window.width + 100 and -100 < world[i].sprite.center_y < window.height + 100:
            world[i].sprite.destroy()
            rendered_blocks.remove(world[i])
        if world[i].sprite.is_colliding_point((mouse_x, mouse_y)) and tsapp.was_mouse_pressed():
            air = tsapp.Sprite("sprites/air block.png", world[i].sprite.x, world[i].sprite.y)
            block = blocks.Block(air, (), "air block", False)
            window.add_object(air)
            world[i] = block

    if tsapp.is_key_down(tsapp.K_d):

        for i in range(len(world)):
            block_right_face_coll = world[i].sprite.center_x - block_coll_var <= player.x + player.width <= world[i].sprite.center_x + block_coll_var and (player.y + player.height) > world[i].sprite.y + 16 and player.y < world[i].sprite.y + world[i].sprite.width - 20
            if block_right_face_coll and world[i].block_has_collision:
                move_var = world[i].sprite.x - (player.x + player.width)
                for x in range(len(world)):
                    world[x].sprite.x -= move_var
                break
        else:
            for i in range(len(world)):
                world[i].sprite.x -= 8.5

    if tsapp.is_key_down(tsapp.K_a):
        for i in range(len(world)):
            block_left_face_coll = world[i].sprite.center_x - block_coll_var <= player.x <= world[i].sprite.center_x + block_coll_var and (player.y + player.height) > world[i].sprite.y + 16 and player.y < world[i].sprite.y + world[i].sprite.width - 20
            if block_left_face_coll and world[i].block_has_collision:
                move_var = world[i].sprite.x + world[i].sprite.width - player.x
                for x in range(len(world)):
                    world[x].sprite.x -= move_var
                break
        else:
            for i in range(len(world)):
                world[i].sprite.x += 8.5

    if tsapp.is_key_down(tsapp.K_SPACE):
        for i in range(len(world)):
            if player.is_colliding_rect(world[i].sprite) and world[i].block_has_collision:
                block_bottom_face_coll = world[i].sprite.y + world[i].sprite.width - 100 < player.y < world[i].sprite.y + world[i].sprite.width
                if block_bottom_face_coll and world[i].block_has_collision:
                    move_var = world[i].sprite.y + world[i].sprite.height - (player.y + 33)
                    for y in range(len(world)):
                        world[y].sprite.y -= move_var
                    break
        else:
            for i in range(len(world)):
                world[i].sprite.y += 33

    for i in range(len(world)):
        if player.is_colliding_rect(world[i].sprite) and world[i].block_has_collision:
            block_top_face_coll = world[i].sprite.y + 56 > player.y + player.height > world[i].sprite.y
            if block_top_face_coll and world[i].block_has_collision:
                move_var = world[i].sprite.y - (player.y + player.height - 3)
                for y in range(len(world)):
                    world[y].sprite.y -= move_var
                break
    else:
        for i in range(len(world)):
            world[i].sprite.y -= 16.5

    if world_class.world[int((world_class.world_height / 10)) * 2][0].sprite.y < player.y:
        if stored > int(world_class.world[17][0].sprite.y - player.y):
            r, g, b = window.background_color
            r -= 3
            g -= 3
            b -= 4
            if r <= 69:
                r = 69
            if g <= 69:
                g = 69
            if b <= 69:
                b = 69
            window.background_color = (r, g, b)
    elif world_class.world[int((world_class.world_height / 10)) * 2][0].sprite.y > player.y:
        if stored < int(world_class.world[17][0].sprite.y - player.y):
            r, g, b = window.background_color
            r += 3
            g += 3
            b += 4
            if r >= 200:
                r = 200
            if g >= 200:
                g = 200
            if b >= 255:
                b = 255
            window.background_color = (r, g, b)

    window.finish_frame()
