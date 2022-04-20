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
        self.inTrade = False
        self.x, self.y = self.teleport(0)

    #updates the players position by its velocity per frame
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.check_walk()


    #draws the player on the board
    def draw(self,other_player,screen):
        self.update()
        oth_pos = other_player.get_posit()

        #coordinated draw
        if oth_pos == self.position:
            pass

        #uncoordinated draw
        else:
           pass

        if self.inTrade:
            self.drawTrade()


    #Trade Code
    #-------------------------------------------------------------------
    #internal function to draw a trade
    def drawTrade(self,screen):
        pass

    #function called in code to initiate a trade
    def trade(self,properties=["",""],money=100,accept_deny=False):
        pass
    #--------------------------------------------------------------------

    #display utilities
    #--------------------------------------------------------------------


    #generic function to display a message
    def display(self,screen,message=""):
        pass

    #---------------------------------------------------------------------

    #walking code
    #--------------------------------------------------------------------

    def get_posit(self):
        return self.position

    # "walks" the user to the specified tile
    def walk(self,tile):
        tile_posit = self.teleport(tile)

    # controls when the "walk" is stopped
    def check_walk(self):
        pass

    # returns the x,y float position of the given monopoly tile
    def teleport(self,position):

        return 0.0, 0.0

    #----------------------------------------------------------------------


#all neccesary tools across functions
#-----------------------------------------------
pygame.init()
smallfont = pygame.font.SysFont('Corbel', 35)

#-----------------------------------------------

#Draws all buttons and display tools
def drawControls(screen,mouse):
    mouse_posit = smallfont.render(f"{mouse[0]},{mouse[1]}",True,(255,255,255))
    screen.blit(mouse_posit, (1039,37))

import json

def handle_events(events,mouse,screen,infinitelist):

    for event in events:
        #currently used for selecting positions of players on field
        if event.type == pygame.MOUSEBUTTONUP:
            out_dict = {"pos":mouse}
            if event.button == 1: out_dict["col"] = (255,0,0)
            if event.button == 3: out_dict["col"] = (0,255,0)
            if event.button == 2:
                print(infinitelist)
                with open("out.json","w+") as wp:
                    li = [{"pos":pl["pos"],"col":pl["col"]} for pl in infinitelist]
                    json.dump(li,wp)
                return infinitelist

            out_dict["rec"] = pygame.Rect(mouse[0],mouse[1],15,15)

            print("test")

            infinitelist.append(out_dict)

    return infinitelist

def main():

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    board = pygame.image.load("monopoly.jpg")

    player_one = player("red","testAIOne")
    player_two = player("blue","testAITwo")
    infini_draw_list = []


    while True:
        events = pygame.event.get()
        mouse = pygame.mouse.get_pos()
        screen.fill(BACKGROUND)
        screen.blit(board, (0, 0))

        #player drawing
        player_one.draw(player_two,screen)
        player_two.draw(player_one,screen)

        #button and control drawing
        drawControls(screen,mouse)


        #TODO remove only temporary for location drawing
        for x in infini_draw_list: pygame.draw.rect(screen,x["col"],x["rec"])

        #capture events
        infini_draw_list = handle_events(events,mouse,screen,infini_draw_list)


        pygame.display.flip()
        clock.tick(60)








if __name__ == "__main__":
    main()