# Draw a rectangle to the screen:
pygame.draw.rect(screen, BLACK, pygame.Rect(0, 0, 100, 100))



# Patterns for different game states
# 1. Draw all the "base" stuff first, that appears for every game state, then draw the state-specific stuff in indentend if game_state == state blocks.


# To animate a sprite, create an Animation class that holds a sequence of images. Give it an update method that increments the timer
# and then increments the index in the image list if the timer hits it's max. Give it a draw method to draw to the screen. See Part 12, 24:53.

# If a sprite has different animations, create on Animation for each one, and then have a dictionary that maps the sprite state to the sprite animation.
# You can then just update and draw using that one.