from expected_value import expected_value
import numpy as np
import monopyly.monopyly
from monopyly.monopyly import *
#only works on 30 maximum turns







class mdp():
    def __init__(self,n_states,game_state:monopyly.monopyly.game.GameState):

        n_states = n_states
        #have a list of observations that are equivalent to the states
        n_observ = n_states

        """
        list of states:
        players position, integer 0-39
        
        
        turns_in_jail:
            0-3  (on turn three pays $50)
            
        
        
        mdp 2
        ---------------------------------------------------------------------------------------------
        
        28 properties
        
        players cash integer 0-5000 increments of 100 (if we have to decrease that number we will)
        
        (each property has a unique rent)
        the price of the property (to purchase)
        and the rent given (how many houses) (how many other properties in color set owned)
        
        the action is :buy, :not_buy
        
        state: property to be purchased
        
        
        """




        self.game_state = game_state


        #  0,1,2  (ignoring houses)
        #we are considering that all properties of the same color have the same rent
        color_set_two_length = 3
        color_set_two_statespace = [color_set_two_length for x in range(2)]


        #  0,1,2 (three house groups)
        color_set_three_length = 3
        color_set_three_statespace = [color_set_three_length for x in range(6)]


        #0,1,2
        utilities_length = 3
        utilities_statespace = [utilities_length for x in range(2)]
        station_statespace = [utilities_length for x in range(4)]

        #maximum addresable ammount 600 starting at 0 iter 200
        cash_statespace = 4

        #considers every beginning midpoint near end
        turn_statespace = 3

        #buy or not buy
        action_dimensions = 2

        joint_statespace = []


        #joint_statespace.append(action_dimensions)
        joint_statespace.append(turn_statespace)
        joint_statespace.append(cash_statespace)

        for x in color_set_two_statespace: joint_statespace.append(x)
        for x in color_set_three_statespace: joint_statespace.append(x)
        for x in utilities_statespace: joint_statespace.append(x)
        for x in station_statespace: joint_statespace.append(x)





        tot = 1
        for x in joint_statespace: tot = tot * x
        print(tot)
        print(joint_statespace)

        self.a = np.zeros( (n_states, n_observ) )
        np.fill_diagonal(self.a, 1.0)

        self.b =  np.zeros( tuple(joint_statespace) )

        #self.b.reshape((2,3,6,3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3))

        #for action in range(self.b.shape[0]):
            #every property given a action
            #loop_action = self.b[action]


            #action don't buy
            #if action==0:


        stateSpace = []

        for turn in range(self.b.shape[0]):
            for cash in range(4):
                for a in range(4):
                    for b in range(4):
                        for c in range(4):
                            for d in range(4):
                                for e in range(4):
                                    for f in range(4):
                                        for g in range(4):
                                            for h in range(4):
                                                for i in range(4):
                                                    for j in range(4):
                                                        for k in range(4):
                                                            for l in range(4):
                                                                for m in range(4):
                                                                    for n in range(4):

                                                                        state = [turn,cash,a, b, c, d, e, f, g, h, i, j, k, l, m, n]
                                                                        if state[2:].count(2) > 1:
                                                                            stateSpace.append(state)

        #0,1  buy don't buy
        for action in range(action_dimensions):
            if action == 0:
                for state in range(len(stateSpace)):
                    pos = stateSpace[state].index(2)
                    stateSpace[state][pos] = 0

            elif action == 1:
                for state in range(len(stateSpace)):
                    pos = stateSpace[state].index(2)
                    #we have to consider the cost to purchase the most expensive property from a set
                    price=self.max_price(pos)

                    #accessing the money state
                    if stateSpace[state][1]*200 > price:
                        pass
                    else:
                        stateSpace[state][pos] = 0


    def max_price(self,pos):

        #Browns, Darkblues
        if pos == 2:
            #brown
            return max([x.price for x in self.game_state.board.get_property_set("Brown").properties])

        elif pos == 3:
            #dark blue
            return max([x.price for x in self.game_state.board.get_property_set("Dark blue").properties])
        #Light blue, purple, orange, red, yellow, green

        elif pos == 4:
            #lightblue
            return max([x.price for x in self.game_state.board.get_property_set("Light blue").properties])

        elif pos == 5:
            #purple
            return max([x.price for x in self.game_state.board.get_property_set("Purple").properties])

        elif pos == 6:
            #orange
            return max([x.price for x in self.game_state.board.get_property_set("Orange").properties])
        elif pos == 7:
            #red
            return max([x.price for x in self.game_state.board.get_property_set("Red").properties])
        elif pos == 8:
            #yellow
            return max([x.price for x in self.game_state.board.get_property_set("Yellow").properties])
        elif pos == 9:
            #green
            return max([x.price for x in self.game_state.board.get_property_set("Green").properties])
        #Kings Cross, Marylebone, Fenohil..., Liverpool

        elif pos == 10:
            #kings cross
            return max([x.price for x in self.game_state.board.get_property_set("Station").properties])
        elif pos == 11:
            #Marylebone
            return max([x.price for x in self.game_state.board.get_property_set("Station").properties])
        elif pos == 12:
            #Fenohil
            return max([x.price for x in self.game_state.board.get_property_set("Station").properties])
        elif pos == 13:
            #livepool
            return max([x.price for x in self.game_state.board.get_property_set("Station").properties])
        #Electric, Water

        elif pos == 14:
            #electric
            return max([x.price for x in self.game_state.board.get_property_set("Utility").properties])
        elif pos == 15:
            #water
            return max([x.price for x in self.game_state.board.get_property_set("Utility").properties])


        #print(self.b.shape)



        self.c = ""

        self.d = ""

set = PropertySet("test")
gameS = Game()
testb = Board(gameS)
testp = Player("Green Demon", 1, testb)

test = Property("Go", set, 110)

model = mdp(2,gameS.state)
print(model.max_price(4))