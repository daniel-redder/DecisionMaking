import pygame
import numpy as np

WIDTH = 1200
HEIGHT = 966
BACKGROUND = (0, 0, 0)



class player:

    """
    color the pygame color to display the token
    position: the integer 0:39 which indicates the position of the piece
    name: the name of the ai playing the piece
    """
    def __init__(self,color,name):
        self.color = color
        self.position = 0
        self.name = name
        self.destination = None
        self.vx = 0.0
        self.vy = 0.0
        self.x, self.y = self.teleport(0)

    #updates the players position by its velocity per frame
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.checkWalk()


    #draws the player on the board
    def draw(self,other_player,):
        self.update()
        oth_pos = other_player.get_posit()

        #coordinated draw
        if oth_pos == self.position:
            pass

        #uncoordinated draw
        else:
           pass


    def get_posit(self):
        return self.position

    # "walks" the user to the specified tile
    def walk(self,tile):
        tile_posit = self.teleport(tile)

    # controls when the "walk" is stopped
    def check_walk(self):
        pass

    # returns the x,y float position of the given monopoly tile
    def teleport(self):

        return 0.0, 0.0




def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    board = pygame.image.load("monopoly.jpg")

    while True:
        events = pygame.event.get()
        screen.fill(BACKGROUND)
        screen.blit(board, (0, 0))

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()