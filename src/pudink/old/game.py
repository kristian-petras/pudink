# import pyglet
# from pyglet import gl

# from pudink.utility import collides

# # co chcem vlastne od hry
# # - login screen / register screen
# # - character creation screen
# # - character movement
# # - character interaction with other characters
# # - chat


# def init():
#     window = pyglet.window.Window()

#     gl.glClearColor(0.96, 0.96, 0.75, 1)

#     character_image = pyglet.image.load("assets/character.png")
#     object_image = pyglet.image.load("assets/object.png")

#     # Create object sprite
#     object_sprite = pyglet.sprite.Sprite(object_image)

#     # Set object position
#     object_sprite.x = 100
#     object_sprite.y = 500

#     # Create character sprite
#     character_sprite = pyglet.sprite.Sprite(character_image)

#     # Set character position
#     character_sprite.x = window.width // 2
#     character_sprite.y = window.height // 2

#     # Create a KeyStateHandler object
#     keys = pyglet.window.key.KeyStateHandler()
#     window.push_handlers(keys)


# def update(dt):
#     # Define the movement speed
#     movement_speed = 200 * dt

#     # Calculate the movement in each direction
#     dx = dy = 0
#     if keys[pyglet.window.key.W]:
#         dy += movement_speed
#     if keys[pyglet.window.key.S]:
#         dy -= movement_speed
#     if keys[pyglet.window.key.A]:
#         dx -= movement_speed
#     if keys[pyglet.window.key.D]:
#         dx += movement_speed

#     # Normalize the movement vector
#     length = (dx**2 + dy**2) ** 0.5
#     if length > 0:
#         dx /= length
#         dy /= length

#     # Move the character
#     character_sprite.x += dx * movement_speed
#     character_sprite.y += dy * movement_speed

#     if collides(character_sprite, object_sprite):
#         print("Character has interacted with the object!")


# # Register update function
# pyglet.clock.schedule_interval(update, 1 / 60)


# # Define draw function
# @window.event
# def on_draw():
#     window.clear()
#     character_sprite.draw()
#     object_sprite.draw()  # Draw the object


# # Start the game
# pyglet.app.run()
