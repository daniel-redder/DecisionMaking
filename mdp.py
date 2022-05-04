from expected_value import expected_value
import numpy as np
import monopyly.monopyly
from monopyly.monopyly import *
#only works on 30 maximum turns
import copy






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


        #  0,1  (ignoring houses)
        #we are considering that all properties of the same color have the same rent
        color_set_two_length = 2
        color_set_two_statespace = [color_set_two_length for x in range(2)]


        #  0,1 (three house groups)
        color_set_three_length = 2
        color_set_three_statespace = [color_set_three_length for x in range(6)]


        #0,1
        utilities_length = 2
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
                for a in range(2):
                    for b in range(2):
                        for c in range(2):
                            for d in range(2):
                                for e in range(2):
                                    for f in range(2):
                                        for g in range(2):
                                            for h in range(2):
                                                for i in range(2):
                                                    for j in range(2):
                                                        for k in range(2):
                                                            for l in range(2):
                                                                for m in range(2):
                                                                    for n in range(2):

                                                                        state = [turn,cash,a, b, c, d, e, f, g, h, i, j, k, l, m, n]
                                                                        if state[2:].count(1) == 1:
                                                                            #print(state)
                                                                            stateSpace.append(state)


        dont_buy_state = copy.deepcopy(stateSpace)




        buy_state = copy.deepcopy(stateSpace)

        self.reward_list = [[0,[]],[1,[]]]

        #Test game to generate rewards
        gameS = Game()
        testb = Board(gameS)
        testp = Player("Green Demon", 1, testb)
        testb.get_property_set("Utility")
        index_to_property_set = {2:testb.get_property_set("Brown"), 3:testb.get_property_set("Dark blue"),
                                    4:testb.get_property_set("Light blue"), 5:testb.get_property_set("Purple"),
                                    6:testb.get_property_set("Orange"), 7:testb.get_property_set("Red"),
                                    8:testb.get_property_set("Yellow"),9:testb.get_property_set("Green"),10:testb.get_property_set("Utility"),
                                    11:testb.get_property_set("Utility"),12:testb.get_property_set("Station"),13:testb.get_property_set("Station"),
                                    14:testb.get_property_set("Station"),15:testb.get_property_set("Station")}

        print(action_dimensions)

        #0,1  buy don't buy
        for action in range(action_dimensions):
            if action == 0:
                for state in range(len(stateSpace)):
                    print(stateSpace[state],state)
                    pos = stateSpace[state][2:].index(1)+2
                    dont_buy_state[state][pos] = 0

                    if not pos == len(index_to_property_set) - 1:
                        prop_enemy_color=[index_to_property_set[x] for x in range(2, pos)] + [index_to_property_set[x] for x in
                            range(pos + 1, len(index_to_property_set) - 1)]

                    else:
                        prop_enemy_color= [index_to_property_set[x] for x in range(2,pos)]

                    self.reward_list[0][1].append(self.reward_value(player=testp, game_state=gameS.state, cash = stateSpace[state][1], action = action, prop_state = 0
                                                          ,purchased_prop=index_to_property_set[pos], prop_enemy_color=prop_enemy_color))



                    print(stateSpace[state])

            elif action == 1:
                for state in range(len(stateSpace)):
                    print(stateSpace[state],"what")
                    pos = stateSpace[state][2:].index(1)+2
                    #we have to consider the cost to purchase the most expensive property from a set
                    price=self.max_price(pos)

                    if not pos == len(index_to_property_set) - 1:
                        prop_enemy_color = [index_to_property_set[x] for x in range(2, pos)] + [index_to_property_set[x]
                                                                                                for x in
                                                                                                range(pos + 1, len(
                                                                                                    index_to_property_set) - 1)]

                    else:
                        prop_enemy_color = [index_to_property_set[x] for x in range(2, pos)]


                    #accessing the money state
                    if stateSpace[state][1]*200 > price:
                        self.reward_list[1][1].append(self.reward_value(player=testp, game_state=gameS.state, cash = stateSpace[state][1], action = action, prop_state = 1
                                                          ,purchased_prop=index_to_property_set[pos], prop_enemy_color=prop_enemy_color))
                        pass
                    else:
                        buy_state[state][pos] = 0
                        self.reward_list[1][1].append(self.reward_value(player=testp, game_state=gameS.state, cash = stateSpace[state][1], action = action, prop_state = 0
                                                          ,purchased_prop=index_to_property_set[pos], prop_enemy_color=prop_enemy_color))


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

        else:
            print(pos," pos what")

        #print(self.b.shape)

    def dice_dist(self):
        return 2 * 1 / 36 + 3 * 1 / 18 + 4 * 3 / 36 + 5 * 1 / 9 + 6 * (1 / 9 + 1 / 36) + 7 * 1 / 6 + 8 * (
                    1 / 9 + 1 / 36) + 9 * 1 / 9 + 10 * (3 / 36) + 11 * 1 / 18 + 12 * 1 / 36



    def avg_expected_value(self,player, game_state: monopyly.monopyly.game.GameState,
                           property_set_colors: monopyly.monopyly.PropertySet, current_turn=0):
        # default value for max turns in monopoly ai competition
        maximum_turns = 30

        # value we choose
        discount_factor = .9

        # for every color in color_set_list
        # for every property in color append to list
        # for every property get property.rent[0] avg()

        color_name = property_set_colors.set_enum
        property_set = property_set_colors.properties

        # non averaged
        if color_name == "Utility":
            return .5 * (4 * (self.dice_dist())) + .5 * (10 * (self.dice_dist()))


        elif color_name == "Station":
            return (200 + 100 + 50 + 25) / 4

        # averaged
        property_values = [x.rents[0] for x in property_set]
        return sum([sum(property_values) / len(property_values) * pow(discount_factor, x) for x in
                    range(maximum_turns - current_turn)])



    def reward_value(self, player, game_state, cash, action, prop_state, purchased_prop: monopyly.monopyly.PropertySet,
                     prop_enemy_color: [monopyly.monopyly.PropertySet]):

        if (action == 0 or prop_state == 0):

            reward = cash * 200 - sum(self.avg_expected_value(player, game_state, property_set_colors=x) for x in
                                      prop_enemy_color) - self.avg_expected_value(player, game_state,
                                                                             property_set_colors=purchased_prop)

        else:

            reward = cash * 200 - (sum([x.price for x in purchased_prop.properties]) / len(
                purchased_prop.properties)) + self.avg_expected_value(player, game_state,
                                                                 property_set_colors=purchased_prop) - sum(
                self.avg_expected_value(player, game_state, property_set_colors=x) for x in prop_enemy_color)

        return reward


"""
Reward function
(S,A)
look at all the states
if action is do not buy:
calculate  the averaged discounted expected value across all (0) state properties which is all properties & the reward is:  cash - expected value

there is a cash state 
that state * 200 = cash  (0-3)

if action is do buy:
check if there exists a property with state 1 (you own the property)
if so: reward is: cash - price + expected value of that property - all other expected values
else: reward is: cash - all expected values

"""



gameS = Game()
testb = Board(gameS)
testp = Player("Green Demon", 1, testb)





model = mdp(2,gameS.state)
print(model.max_price(7))

print(model.reward_list[1])























