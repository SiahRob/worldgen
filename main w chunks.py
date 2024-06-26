import tsapp
import time
import world_generation as w


world = w.WorldGeneration(1)
chunks = world.generate_world()
window = tsapp.GraphicsWindow(1670, 682, (200, 200, 255))


def load_chunks(chunkrem, chunkadd):

    for chunk_y in range(len(chunkrem)):
        for chunk_x in range(len(chunkrem[chunk_y])):
            chunkrem[chunk_y][chunk_x].block_has_collision = False
            chunkrem[chunk_y][chunk_x].sprite.visible = False
            chunkrem[chunk_y][chunk_x].sprite.destroy()

    for chunk_y in range(len(chunkadd)):
        for chunk_x in range(len(chunkadd[chunk_y])):
            if not chunkadd[chunk_y][chunk_x].name == "air block":
                chunkadd[chunk_y][chunk_x].block_has_collision = True
            chunkadd[chunk_y][chunk_x].sprite.visible = True
            chunkadd[chunk_y][chunk_x].refresh_sprite()
            window.add_object(chunkadd[chunk_y][chunk_x].sprite)


player = tsapp.Sprite("sprites/player person.png", 0, 0)

player.scale = 0.5
player.center_x = 510
player.center_y = 437


player.y = 0
player.center_x = 535


for i in range(len(chunks[0][0])):
    for y in range(len(chunks[0][0][i])):
        window.add_object(chunks[0][0][i][y].sprite)

current_y_chunk = 0
current_x_chunk = 0
window.add_object(player)
player.y_speed = 300
start = time.time()
block_coll_var = 56
block_right_face_coll = False
block_left_face_coll = False


for y2 in range(len(chunks)):
    for x2 in range(len(chunks[y2])):
        for y in range(int(world.world_height / 10)):
            for x in range(int(world.world_width / 10)):
                pixel = tsapp.Sprite("sprites/pixel sprites/" + chunks[y2][x2][y][x].name + " pixel.png", 0, 0)
                pixel.x = (x * 5) + (x2 * int(world.world_width / 1.9)) + 1100
                pixel.y = (y * 5) + (y2 * int(world.world_height / 1.9))
                window.add_object(pixel)



while window.is_running:

    seconds_passed = time.time() - start
    mouse_x, mouse_y = tsapp.get_mouse_position()
    for y in range(len(chunks[current_y_chunk][current_x_chunk])):
        for x in range(len(chunks[current_y_chunk][current_x_chunk][y])):

            if player.is_colliding_rect(chunks[current_y_chunk][current_x_chunk][y][x].sprite) and \
                    chunks[current_y_chunk][current_x_chunk][y][x].block_has_collision:

                if tsapp.was_key_pressed(tsapp.K_SPACE):
                    start = time.time()
                    player.y -= 10
                    player.y_speed = -300
                    break

                elif chunks[current_y_chunk][current_x_chunk][y][x].sprite.y + 15 > player.y + player.height > \
                        chunks[current_y_chunk][current_x_chunk][y][x].sprite.y and \
                        chunks[current_y_chunk][current_x_chunk][y][x].block_has_collision:
                    player.y_speed = 0
                    player.y = chunks[current_y_chunk][current_x_chunk][y][x].sprite.y - player.height

                elif chunks[current_y_chunk][current_x_chunk][y][x].sprite.y + \
                        chunks[current_y_chunk][current_x_chunk][y][x].sprite.width - 15 < player.y < \
                        chunks[current_y_chunk][current_x_chunk][y][x].sprite.y + \
                        chunks[current_y_chunk][current_x_chunk][y][x].sprite.width and \
                        chunks[current_y_chunk][current_x_chunk][y][x].block_has_collision:
                    player.y_speed = 0
                    player.y = chunks[current_y_chunk][current_x_chunk][y][x].sprite.y + \
                               chunks[current_y_chunk][current_x_chunk][y][x].sprite.width

            elif seconds_passed > 0.425:
                player.y_speed = 300
        else:
            continue
        break

    if tsapp.is_key_down(tsapp.K_d):
        for y in range(len(chunks[current_y_chunk][current_x_chunk])):
            for x in range(len(chunks[current_y_chunk][current_x_chunk][y])):
                block_right_face_coll = chunks[current_y_chunk][current_x_chunk][y][x].sprite.center_x - block_coll_var <= player.x + player.width <= chunks[current_y_chunk][current_x_chunk][y][x].sprite.center_x + block_coll_var and (player.y + player.height) > chunks[current_y_chunk][current_x_chunk][y][x].sprite.y + 15 and player.y < chunks[current_y_chunk][current_x_chunk][y][x].sprite.y + chunks[current_y_chunk][current_x_chunk][y][x].sprite.width
                if block_right_face_coll and chunks[current_y_chunk][current_x_chunk][y][x].block_has_collision:
                    player.x_speed = 0
                    player.x = chunks[current_y_chunk][current_x_chunk][y][x].sprite.x - player.width
                    break
                elif not block_right_face_coll:
                    player.x_speed = 200
            else:
                continue
            break

    elif tsapp.is_key_down(tsapp.K_a):
        for y in range(len(chunks[current_y_chunk][current_x_chunk])):
            for x in range(len(chunks[current_y_chunk][current_x_chunk][y])):
                block_left_face_coll = chunks[current_y_chunk][current_x_chunk][y][x].sprite.center_x - block_coll_var <= player.x <= chunks[current_y_chunk][current_x_chunk][y][x].sprite.center_x + block_coll_var and (player.y + player.height) > chunks[current_y_chunk][current_x_chunk][y][x].sprite.y + 15 and player.y < chunks[current_y_chunk][current_x_chunk][y][x].sprite.y + chunks[current_y_chunk][current_x_chunk][y][x].sprite.width
                if block_left_face_coll and chunks[current_y_chunk][current_x_chunk][y][x].block_has_collision:
                    player.x_speed = 0
                    player.x = chunks[current_y_chunk][current_x_chunk][y][x].sprite.x + chunks[current_y_chunk][current_x_chunk][y][x].sprite.width
                    break
                elif not block_left_face_coll:
                    player.x_speed = -200
            else:
                continue
            break

    else:
        player.x_speed = 0

    if player.center_x < 0:
        if not current_x_chunk == 0:
            load_chunks(chunks[current_y_chunk][current_x_chunk], chunks[current_y_chunk][current_x_chunk - 1])
            current_x_chunk -= 1
            player.center_x = 1070
            for y in range(int(world.world_height / 10)):
                if not chunks[current_y_chunk][current_x_chunk][y][-1].name == "air block" and current_y_chunk < 1:
                    player.y = chunks[current_y_chunk][current_x_chunk][y][-1].sprite.y - player.height - 1
                    break
        elif player.x_speed < 0:
            player.x_speed = 0
    elif player.center_x > 1070:
        if not current_x_chunk == len(chunks) - 1:
            load_chunks(chunks[current_y_chunk][current_x_chunk], chunks[current_y_chunk][current_x_chunk + 1])
            current_x_chunk += 1
            player.center_x = 0
            for y in range(int(world.world_height / 10)):
                if not chunks[current_y_chunk][current_x_chunk][y][0].name == "air block" and current_y_chunk < 1:
                    player.y = chunks[current_y_chunk][current_x_chunk][y][0].sprite.y - player.height - 1
                    break
        elif player.x_speed > 0:
            player.x_speed = 0

    if player.center_y > 714:
        player.center_y = 0
        load_chunks(chunks[current_y_chunk][current_x_chunk], chunks[current_y_chunk + 1][current_x_chunk])
        current_y_chunk += 1
    elif player.center_y < 0:
        player.center_y = 714
        load_chunks(chunks[current_y_chunk][current_x_chunk], chunks[current_y_chunk - 1][current_x_chunk])
        current_y_chunk -= 1


    for y in range(len(chunks[current_y_chunk][current_x_chunk])):
        for x in range(len(chunks[current_y_chunk][current_x_chunk][y])):
            if chunks[current_y_chunk][current_x_chunk][y][x].sprite.is_colliding_point((mouse_x, mouse_y)) and tsapp.was_mouse_pressed() and not chunks[current_y_chunk][current_x_chunk][y][x].name == "air block":
                chunks[current_y_chunk][current_x_chunk][y][x].name = "air block"
                chunks[current_y_chunk][current_x_chunk][y][x].block_has_collision = False
                chunks[current_y_chunk][current_x_chunk][y][x].refresh_sprite()
                break
        else:
            continue
        break

    window.finish_frame()
