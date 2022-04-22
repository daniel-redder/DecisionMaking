import pygame
import numpy as np
from player import player
import json
import time

WIDTH = 1200
HEIGHT = 966
BACKGROUND = (0, 0, 0)


from logReader import logReader


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

def handle_events(events,mouse,screen,infinitelist,playerOne,playerTwo):

    for event in events:
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1: playerOne.walk(10)
            if event.button == 2: playerOne.proposeTrade(playerTwo)



        #deprecated code only used for dev
        #currently used for selecting positions of players on field
    #     if event.type == pygame.MOUSEBUTTONUP:
    #         out_dict = {"pos":mouse}
    #         if event.button == 1: out_dict["col"] = (255,0,0)
    #         if event.button == 3: out_dict["col"] = (0,255,0)
    #         if event.button == 2:
    #             print(infinitelist)
    #             with open("out.json","w+") as wp:
    #                 li = [{"pos":pl["pos"],"col":pl["col"]} for pl in infinitelist]
    #                 json.dump(li,wp)
    #             return infinitelist
    #
    #         out_dict["rec"] = pygame.Rect(mouse[0],mouse[1],15,15)
    #
    #         print("test")
    #
    #         infinitelist.append(out_dict)
    #
    # return infinitelist

def main(logName="game.log"):

    #define pygame components
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    #initialize board
    board = pygame.image.load("monopoly.jpg")

    #start log reader
    log = logReader("game.log")

    game_begin = log.nextTurn()
    print(game_begin)

    #here begins the assumption we are using only two players
    assert len(game_begin)==3, "Warning this implementation of GUI is only implemented for two players"
    player_one_name = game_begin[1].split("- ")[1].split("\n")[0]
    player_two_name = game_begin[2].split("- ")[1].split("\n")[0]

    #here the thimble reference is outdated and not used
    player_one = player((255,0,0),player_one_name,"thimble.png",isOne=True)
    player_two = player((0,0,255),player_two_name,"thimble.png",otherPlayer=player_one,isOne=False)
    player_one.addOther(player_two)

    #TODO deprecated?
    infini_draw_list = []

    #list of text and objects to render prior to looping
    next_button = pygame.Rect(987, 130, 75, 50)
    next_text = smallfont.render("Next",True,(255,255,255))
    back_button = pygame.Rect(1090,130,85,50)
    back_text = smallfont.render("Back",True,(255,255,255))


    while True:
        events = pygame.event.get()
        mouse = pygame.mouse.get_pos()
        screen.fill(BACKGROUND)
        screen.blit(board, (0, 0))

        #player drawing
        player_one.draw(screen)
        player_two.draw(screen)

        #button and control drawing
        drawControls(screen,mouse)
        pygame.draw.rect(screen,(100,100,100),next_button)
        screen.blit(next_text,(990,140))
        pygame.draw.rect(screen,(100,100,100),back_button)
        screen.blit(back_text,(1100,140))


        #TODO remove only temporary for location drawing
        #for x in infini_draw_list: pygame.draw.rect(screen,x["col"],x["rec"])

        #capture events (used temporarily)
        handle_events(events,mouse,screen,infini_draw_list,player_one,player_two)


        pygame.display.flip()
        clock.tick(60)







#pass log file name
if __name__ == "__main__":
    main()