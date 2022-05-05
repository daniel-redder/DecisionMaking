import pygame
import numpy as np
from GUI.player import Modeledplayer
import json
import time

WIDTH = 1200
HEIGHT = 966
BACKGROUND = (0, 0, 0)


from GUI.logReader import logReader


#all neccesary tools across functions
#-----------------------------------------------
pygame.init()
smallfont = pygame.font.SysFont('Corbel', 35)
smallerfont = pygame.font.SysFont('Corbel',14)
#-----------------------------------------------

#turn parsing function for logs
def parse(turn,player_names=[]):
    #Gameover code
    if "Game over." in turn[-1]:
        return None, False

    if "Start of game" in turn[0]:
        return None, None

    parsed_turn = {}

    parsed_turn["turn_player"] = turn[0].split("turn for ")[1]

    inter = turn[1].split("Cash=")[1].split(", Net Worth=")
    parsed_turn["cash"] = inter[0]
    parsed_turn["networth"] = inter[1]

    move_list = [x for x in turn if "Moved" in x]

    if len(move_list)== 0:
        return None

    opPlayerName=turn[0].split("Start of turn for ")[1].split("\n")[0]
    print(player_names)
    playerChoice = player_names.index(opPlayerName)

    print(move_list[-1])

    #TODO temporary return values
    return ["walk",move_list[-1].split("Moved to ")[1],parsed_turn], playerChoice









#Draws all buttons and display tools
def drawControls(screen,mouse):
    mouse_posit = smallfont.render(f"{mouse[0]},{mouse[1]}",True,(255,255,255))
    screen.blit(mouse_posit, (1039,37))


import json

def handle_events(events,mouse,screen,infinitelist,playerOne:Modeledplayer,playerTwo:Modeledplayer,parsed_turn,next_op):
    if next_op == 0:
        opPlayer = playerOne
    else:
        opPlayer = playerTwo
    if parsed_turn == None: return

    place_dict = ["Go","Vine Street","Community Chest","Coventry Street","Income Tax","Marylebone Station","Leicester Square",
        "Chance","Bow Street","Whitechapel Road","Jail","The Angel Islington","Electric Company","Trafalgar Square","Northumberland Avenue","Fenchurch Street Station"
        ,"Marlborough Street","Community Chest","Fleet Street","Old Kent Road","Free Parking","Whitehall","Chance","Pentonville Road","Pall Mall","Kings Cross Station"
        ,"Bond Street","Strand","Water Works","Regent Street","Go To Jail","Euston Road","Piccadilly","Community Chest","Oxford Street","Liverpool Street Station","Chance","Park Lane"
        ,"Super Tax","Mayfair"]

    if "walk" in parsed_turn[0]:
        if parsed_turn[1] == "Chance":
            p = opPlayer.position+1
            while not "Chance" in place_dict[p]: p+=1
            opPlayer.walk(p)
        elif parsed_turn[1] == "Community Chest":
            p= opPlayer.position+1
            while not "Community" in place_dict[p]:p+=1
            opPlayer.walk(p)

        print(place_dict.index(parsed_turn[1][:-1]))

        opPlayer.walk(place_dict.index(parsed_turn[1][:-1]))

    #elif "trade" in parsed_turn:
        #opPlayer.proposeTrade()


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

    player_one_name = player_one_name
    player_two_name = player_two_name

    parsed_turn, next_op = parse(game_begin,[player_one_name,player_two_name])


    #here the thimble reference is outdated and not used
    player_one = Modeledplayer((255,0,0),player_one_name,"thimble.png",isOne=True)
    player_two = Modeledplayer((0,0,255),player_two_name,"thimble.png",otherPlayer=player_one,isOne=False)
    player_one.addOther(player_two)

    #parsing indicator
    turn_concluded = True

    #TODO deprecated?
    infini_draw_list = []

    #list of text and objects to render prior to looping
    next_button = pygame.Rect(987, 130, 75, 50)
    next_text = smallfont.render("Next",True,(255,255,255))
    back_button = pygame.Rect(1090,130,85,50)
    back_text = smallfont.render("Back",True,(255,255,255))

    console_text = []

    while True:

        #turn begin data collection
        events = pygame.event.get()
        mouse = pygame.mouse.get_pos()



        if player_one.isTurn():
            #TODO implement .isTurn and .check_concluded
            #.isturn returns a boolean indicating whether it is their turn
            #check_concluded indicates whether their turn has finished
            turn_concluded = player_one.check_concluded()
        elif player_two.isTurn():
            turn_concluded = player_two.check_concluded()

        if turn_concluded:
            for event in events:
                if event.type == pygame.MOUSEBUTTONUP:

                    print("booya")
                    turn = log.nextTurn()
                    parsed_turn,next_op = parse(turn,[player_one_name,player_two_name])

                    handle_events(events, mouse, screen, infini_draw_list, player_one, player_two, parsed_turn, next_op)

                    console_text = [smallerfont.render(x[:-1],True,(255,255,255)) for x in turn]





        #background fill
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

        for x in range(len(console_text)): screen.blit(console_text[x],(990,200+20*x))


        #TODO remove only temporary for location drawing
        #for x in infini_draw_list: pygame.draw.rect(screen,x["col"],x["rec"])

        #capture events (used temporarily)



        pygame.display.flip()
        clock.tick(60)







#pass log file name
if __name__ == "__main__":
    main()