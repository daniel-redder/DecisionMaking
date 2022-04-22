import pygame
import json



class player:

    """
    color the pygame color to display the token
    position: the integer 0:39 which indicates the position of the piece
    name: the name of the ai playing the piece
    """
    def __init__(self,color,name,pathString,otherPlayer=None,isOne=True):
        self.color = color
        self.otherPlayer = otherPlayer
        with open("formatted_pos.json","r") as fp:
            self.p_pos = json.load(fp)

        #self.image = pygame.image.load(pathString)

        self.position = 0
        self.name = name

        self.turn = False

        #current trip destination
        self.midDestination = None

        #mid travel pos
        self.midDestinationPos = None

        #walk position destination
        self.destination_pos = None
        self.trade_counter = 0
        self.vx = 0.0
        self.smallfont = pygame.font.SysFont('Corbel', 35)
        self.vy = 0.0
        self.isOne = isOne
        self.inTrade = False
        self.inWalk = False
        self.x, self.y = self.teleport(0)

        #time.sleep(100)
        self.walk(39)



    #updates the players position by its velocity per frame
    def update(self):
        self.check_walk()
        self.x += self.vx
        self.y += self.vy



    #draws the player on the board
    def draw(self,screen):
        self.update()

        pygame.draw.rect(screen,self.color,pygame.Rect(self.x,self.y,30,30))



        if self.inTrade: self.drawTrade(screen)


    #Trade Code
    #-------------------------------------------------------------------

    def step(self,nextOp):

        #ends trade if currently in trade
        if self.inTrade: self.inTrade = False





    #internal function to draw a trade
    def drawTrade(self,screen):
        #self.trade_counter+=1
        playerTwo = self.otherPlayer
       # if self.trade_counter > 980:
            #self.inTrade = False
            #return None

        pygame.draw.rect(screen, (100,100,100), pygame.Rect(200,209,563,564))
        screen.blit(self.leftSide,(239,317))
        screen.blit(self.rightSide,(590,317))
        screen.blit(self.title,(239,231))
        self.blit_list(self.properties_from,screen,(590,450),28)
        screen.blit(self.money_from,(625,375))
        screen.blit(self.money_to,(250,375))

    def blit_list(self,lis,screen,position,fontsize):
        font = pygame.font.SysFont("corbel", fontsize)


        label = []
        for line in lis:
            label.append(font.render(line, True, (255,255,255)))


        for line in range(len(label)):
            screen.blit(label[line], (position[0], position[1] + (line * fontsize) + (15 * line)))


    #function called in code to initiate a trade
    def proposeTrade(self,playerTwo,properties_from=["",""],money_from=100,properties_to=["",""],money_to=100,accept_deny=False):
        self.inTrade = True
        self.trade_counter=0
        self.title = self.smallfont.render(f"Trade Proposed By: {playerTwo.name}",True,(255,255,255))
        self.leftSide = self.smallfont.render(f"{self.name}",True,(255,255,255))
        self.rightSide = self.smallfont.render(f"{playerTwo.name}",True,(255,255,255))

        self.money_from = self.smallfont.render(f"${money_from}",True,(255,255,255))
        self.money_to = self.smallfont.render(f"${money_to}",True,(255,255,255))

        properties_from_concat_string = ""
        properties_to_concat_string = ""

        #TODO change when add class for properties (not neccesary right now)


        self.properties_from = properties_from
        self.properties_to = properties_to

        self.accept_deny = self.smallfont.render(f"{accept_deny}",True,(255,255,255))



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
        if tile == self.position: return None

        self.destination_pos = tile
        self.inWalk = True

        self.midDestinationPos = self.position+1
        if self.midDestinationPos == 40: self.midDestinationPos = 0

       # print("middest ",self.midDestinationPos)
        self.midDestination = self.teleport(self.midDestinationPos)

        #initial acceleration calculation
        dx, dy = self.midDestination[0] - self.x, self.midDestination[1] - self.y
        self.vx = dx / 15.
        self.vy = dy / 15.

    # controls when the "walk" is stopped
    def check_walk(self):
        if self.inWalk:
            #ensures proper landing
            if 1 > abs(self.x - self.midDestination[0]) and 1 > abs(self.y - self.midDestination[1]):
                self.x, self.y = self.midDestination
                #print("hiii")
                #base case check
                if self.destination_pos == self.midDestinationPos:
                    #("hi")
                    self.inWalk = False
                    self.position = self.destination_pos
                    self.vx = 0.0
                    self.vy = 0.0
                    return None

                else:

                    #navigate to next square point

                    self.midDestinationPos += 1

                    #reset pos to 0 in case of er
                    if self.midDestinationPos == 40: self.midDestinationPos = 0

                    #reset position/velocity vectors
                    self.midDestination = self.teleport(self.midDestinationPos)

                    #acceleration calculation
                    dx, dy = self.midDestination[0] - self.x, self.midDestination[1] - self.y
                    self.vx = dx / 15.
                    self.vy = dy / 15.



    # returns the x,y float position of the given monopoly tile
    def teleport(self,position):
        if self.isOne:
            #print(self.p_pos["p1"][position]," why why why")
            return self.p_pos["p1"][position]["pos"]
        else:
            #(self.p_pos["p2"][position])
            return self.p_pos["p2"][position]["pos"]


    def addOther(self,other): self.otherPlayer = other
    #----------------------------------------------------------------------
    #used in logger parsing and turn setting

    def isTurn(self):
        return self.turn


    #TODO needs to check if the current process is finished... (general variable for process holding perhaps)
    def check_concluded(self):
        pass