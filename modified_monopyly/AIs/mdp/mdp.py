
import pandas as pd
import numpy as np
import monopyly
from monopyly import *
#only works on 30 maximum turns
import copy
import mdptoolbox
import json
import math

LAMDA = 2.55  # loss aversion coefficient
ALPHA = BETA = 0.88  # power of gains and losses
GAMMA = 0.61  # probability weighting parameter for gains
DELTA = 0.69  # probability weighting parameter for losses

#prospect theory true or false
prospect_theory = True


class mdp():
    def __init__(self,n_states,game_state:monopyly.game.GameState):


        self.build_matrices(n_states,game_state)

        #self.dont_buy_state

        #number of states x number states
        # 168 possible combinations
        # 168 x 168
        #2 x (168 x168) (168 x16)


        #array1 = np.array(self.stateSpace).flatten()
        #array2 = np.array(self.dont_buy_state).flatten()
        #sel.buy_state
        #self.transition = np.array((self.stateSpace,self.dont_buy_state)).reshape(1,4096,4096)



        #print(array1.shape,array2.shape)


        #self.transition = np.zeros((2,))

        print(self.transition.shape)


        print(len(self.stateSpace),"self statespace")

        print(len(self.buy_state),len(self.stateSpace),len(self.dont_buy_state))
        print("state_space")

        testa = np.array(self.stateSpace)
        testb = np.array(self.buy_state)
        testc = np.array(self.dont_buy_state)
        print(testa.shape,"  ",testb.shape,"  ",testc.shape)



        #print(holder_arr.shape,"what")



        #self.transition = self.transition.flatten()

        print(self.transition.shape,"what2")


        print(len(self.reward_list[0][1]))
        print(len(self.reward_list[1][1]))


        rewards = np.column_stack((self.reward_list[0][1],self.reward_list[1][1]))
        self.reward = rewards

        print(self.reward_list)

        print(self.reward.shape,"reward")



        self.mdp = mdptoolbox.mdp.PolicyIteration(
            transitions=self.transition,
            reward = self.reward,
            discount = .9,
        )

        self.mdp.run()

        data_dic = {"policy":self.mdp.policy,"states":self.stateSpace}

        with open("policy_prospect.json","w+") as f:
            json.dump(data_dic,f)



        print(self.mdp.policy)






    def build_matrices(self,n_states,game_state):


        self.game_state = game_state
        # have a list of observations that are equivalent to the states
        n_observ = n_states

        #  0,1  (ignoring houses)
        #we are considering that all properties of the same color have the same rent
        color_set_two_length = 2
        color_set_two_statespace = [color_set_two_length for x in range(2)]


        #  0,1 (three house groups)
        color_set_three_length = 2
        color_set_three_statespace = [color_set_three_length for x in range(6)]


        #0,1
        utilities_length = 2
        utilities_statespace = [utilities_length for x in range(1)]
        station_statespace = [utilities_length for x in range(1)]

        #maximum addresable ammount 600 starting at 0 iter 200
        cash_statespace = 4

        #considers every beginning midpoint near end
        turn_statespace = 4

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
        #print(tot)
        #print(joint_statespace)



        b =  np.zeros( tuple(joint_statespace) )


        stateSpace = []

        for turn in range(b.shape[0]):
            for cash in range(cash_statespace):
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
                                                        state = [turn,cash,a, b, c, d, e, f, g, h, i, j]
                                                        #if state[2:].count(1) == 1:
                                                            #print(state)
                                                        stateSpace.append(state)


        dont_buy_state = copy.deepcopy(stateSpace)

        self.stateSpace = stateSpace

        buy_state = copy.deepcopy(stateSpace)

        print(len(stateSpace)*len(stateSpace)*2)

        self.transition = np.zeros((2,len(stateSpace),len(stateSpace)))
        np.fill_diagonal(self.transition[0], 1.0)
        np.fill_diagonal(self.transition[1], 1.0)
        print(self.transition)


        self.reward_list = [[0,[]],[1,[]]]

        #Test game to generate rewards
        self.gameS = Game()
        testb = Board(gameS)
        testp = Player("Green Demon", 1, testb)
        testb.get_property_set("Utility")
        index_to_property_set = {2:testb.get_property_set("Brown"), 3:testb.get_property_set("Dark blue"),
                                    4:testb.get_property_set("Light blue"), 5:testb.get_property_set("Purple"),
                                    6:testb.get_property_set("Orange"), 7:testb.get_property_set("Red"),
                                    8:testb.get_property_set("Yellow"),9:testb.get_property_set("Green"),10:testb.get_property_set("Utility"),
                                    11:testb.get_property_set("Utility"),12:testb.get_property_set("Station"),13:testb.get_property_set("Station"),
                                    14:testb.get_property_set("Station"),15:testb.get_property_set("Station")}

        #print(action_dimensions)


        print(len(stateSpace), "what is going on")

        #0,1  buy don't buy
        for action in range(action_dimensions):
            if action == 0:
                for state in range(len(stateSpace)):
                            #print(stateSpace[state],state)

                            try:
                                pos = stateSpace[state][2:].index(1)+2
                            except:
                                pos = 3

                            dont_buy_state[state][pos] = 0

                            if not pos == len(index_to_property_set) - 1:
                                prop_enemy_color=[index_to_property_set[x] for x in range(2, pos)] + [index_to_property_set[x] for x in
                                    range(pos + 1, len(index_to_property_set) - 1)]

                            else:
                                prop_enemy_color= [index_to_property_set[x] for x in range(2,pos)]

                            self.reward_list[0][1].append(self.reward_value(player=testp, game_state=gameS.state, cash = stateSpace[state][1], action = action, prop_state = 0
                                                                  ,purchased_prop=index_to_property_set[pos], prop_enemy_color=prop_enemy_color))



                    #print(stateSpace[state])

            elif action == 1:
                for state in range(len(stateSpace)):
                            #print(stateSpace[state],"what")

                            try:
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





                                else:
                                    buy_state[state][pos] = 0
                                    self.reward_list[1][1].append(self.reward_value(player=testp, game_state=gameS.state, cash = stateSpace[state][1], action = action, prop_state = 0
                                                                      ,purchased_prop=index_to_property_set[pos], prop_enemy_color=prop_enemy_color))

                                    temporary_state = stateSpace[state].copy()
                                    temporary_state[pos] = 0

                                    change_pos = stateSpace.index(temporary_state)
                                    print(change_pos)
                                    print(temporary_state, stateSpace[state])

                                    self.transition[1, state, change_pos] = 1
                                    self.transition[1, state, state] = 0

                            except:
                                pos = 3

                                if not pos == len(index_to_property_set) - 1:
                                    prop_enemy_color = [index_to_property_set[x] for x in range(2, pos)] + [
                                        index_to_property_set[x]
                                        for x in
                                        range(pos + 1, len(
                                            index_to_property_set) - 1)]

                                else:
                                    prop_enemy_color = [index_to_property_set[x] for x in range(2, pos)]

                                self.reward_list[1][1].append(
                                    self.reward_value(player=testp, game_state=gameS.state, cash=stateSpace[state][1],
                                                      action=action, prop_state=0
                                                      , purchased_prop=index_to_property_set[pos],
                                                      prop_enemy_color=prop_enemy_color))


        self.dont_buy_state = dont_buy_state
        self.buy_state = buy_state


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



    def avg_expected_value(self,player, game_state: monopyly.game.GameState,
                           property_set_colors: monopyly.PropertySet, current_turn=0):
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
            if prospect_theory:
                return self.prosTheory_value(.5 * (4 * (self.dice_dist())) + .5 * (10 * (self.dice_dist())))

            else:
                return .5 * (4 * (self.dice_dist())) + .5 * (10 * (self.dice_dist()))


        elif color_name == "Station":
            if prospect_theory:
                return self.prosTheory_value((200+100+50+25)/4)
            else:
                return (200 + 100 + 50 + 25) / 4

        # averaged
        if prospect_theory:
            property_values = [self.prosTheory_value(x.rents[0]) for x in property_set]
        else:
            property_values = [x.rents[0] for x in property_set]


        return sum([sum(property_values) / len(property_values) * pow(discount_factor, x) for x in
                    range(maximum_turns - current_turn)])



    def reward_value(self, player, game_state, cash, action, prop_state, purchased_prop:monopyly.PropertySet,
                     prop_enemy_color: [monopyly.PropertySet]):

        if (action == 0 or prop_state == 0):

            if prospect_theory:
                reward = self.prosTheory_value(cash*200) - self.cptValue(player,game_state,prop_enemy_color) - self.cptValue(player,game_state,[purchased_prop])
            else:

                cash_combo = cash*200

                reward = cash_combo - sum(self.avg_expected_value(player, game_state, property_set_colors=x) for x in
                                         prop_enemy_color) - self.avg_expected_value(player, game_state,
                                                                                property_set_colors=purchased_prop)

        else:
            if prospect_theory:
                reward = self.prosTheory_value(cash*200) - self.prosTheory_value(sum([x.price for x in purchased_prop.properties])/ len(
                    purchased_prop.properties)) - self.cptValue(player,game_state,prop_enemy_color) + self.cptValue(player,game_state,[purchased_prop])

            else:

                prob_list = [self.getProbability(x) for x in purchased_prop.properties]
                prob = sum(prob_list) / len(prob_list)

                reward = cash * 200 - (sum([x.price for x in purchased_prop.properties]) / len(
                    purchased_prop.properties)) + prob*self.avg_expected_value(player, game_state,
                                                                     property_set_colors=purchased_prop) - sum(
                    self.avg_expected_value(player, game_state, property_set_colors=x) for x in prop_enemy_color)

        return reward




    def getProbability(self, property: Property):
        # potential issue with calculation in tiles with duplicate names
        # only effects community chest and chance, however could be a problem in functions other than this

        df = pd.read_csv("normalized_prob_n.csv")
        print(property.name)
        output_prob = df[df["prop"] == property.name]

        try:
            print(output_prob)
            return output_prob['prob']

        except Exception as e:
            print(e,"what exception")
            print(f"Exception in getting probabilities {property.name}")





    def expected_value(self, player, game_state, check_property: []):
        maximum_turns = 30
        discount_factor = .9

        # syntax check #TODO
        color_set_list = [x.property_set for x in check_property]

        ev = []

        if len(color_set_list) > 1: color_set_list = set(color_set_list)

        # for each unique color set in check_property
        for color in color_set_list:

            # each property in that colorset
            color_props = [prop for prop in check_property if prop.property_set is color]

            # total number of properties in the set
            total_props = color.number_of_properties

            # all properties owned by the player now
            owned_properties = color.owned_properties(player=player)

            # temporary property val sum
            if len(owned_properties) > 0:
                owned_color_value = sum(
                    [prop.calculate_rent(game_state, player) * self.getProbability(prop) for prop in owned_properties])
            else:
                owned_color_value = 0

            # temporary owner list
            old_owner = []

            # temporary owner setting
            for prop in color_props:
                old_owner.append(prop.owner)
                prop.owner = player

            # temporary property owned #TODO ensure this updates with null sett
            temp_owned_property = color.owned_properties(player)

            # temporary property value
            temp_color_value = sum(
                [prop.calculate_rent(game_state, player) * self.getProbability(prop) for prop in temp_owned_property])

            # calculate difference in cost
            ev.append(temp_color_value - owned_color_value)

            # reset owner to what it was before
            for prop in range(len(color_props)): color_props[prop].owner = old_owner[prop]

        one_round_ev = sum(ev)

        # discount factor determined here
        return sum([one_round_ev * pow(discount_factor, x) for x in range(maximum_turns - player.state.turns_played)])

    def prosTheory_value(self,outcome):
        if (outcome >= 0):
            value = pow(outcome, ALPHA)
        else:
            value = - (LAMDA) * pow(-(outcome), BETA)

        return value

    def prosTheory_weightFunc(self,prob):
        logVal = math.log(prob)
        tempVal = pow(-(logVal), ALPHA)
        expoVal = -(tempVal)
        decisionweightValue = math.exp(expoVal)

        return decisionweightValue

    def cptValue(self,player, game_state, check_property: []):

        if check_property == None: return None

        prosValueList = []
        prosDWValueList = []
        cumulativeProsVal = []

        maximum_turns = 30
        discount_factor = .9

        color_set_list = check_property

        # for each unique color set in check_property
        for color in color_set_list:

            # each property in that colorset
            color_props = color.properties

            # total number of properties in the set
            total_props = color.number_of_properties

            # all properties owned by the player now
            owned_properties = color.owned_properties(player=player)

            # temporary property val sum
            if len(owned_properties) > 0:
                for prop in owned_properties:
                    rentVal = prop.calculate_rent(game_state, player)
                    prob = self.getProbability(prop)
                    prosValueList.append(self.prosTheory_value(rentVal))
                    prosDWValueList.append(self.prosTheory_weightFunc(prob))

                cptValue = sum([x * y for (x, y) in zip(prosValueList, prosDWValueList)])
            else:
                cptValue = 0

            # temporary owner list
            old_owner = []

            # temporary owner setting
            for prop in color_props:
                old_owner.append(prop.owner)
                prop.owner = player

            # temporary property owned #TODO ensure this updates with null sett
            temp_owned_property = color.owned_properties(player)

            # temporary property value
            for prop in temp_owned_property:
                temprentVal = prop.calculate_rent(self.gameS, player)
                #if prop is None: print("nnoooooo")
                tempProb = self.getProbability(prop)
                prosValueList.append(self.prosTheory_value(temprentVal))
                prosDWValueList.append(self.prosTheory_weightFunc(tempProb))

            temp_cptValue = sum([x * y for (x, y) in zip(prosValueList, prosDWValueList)])

            # calculate difference in cost
            cumulativeProsVal.append(temp_cptValue - cptValue)

            # reset owner to what it was before
            for prop in range(len(color_props)): color_props[prop].owner = old_owner[prop]

        one_round_cpt = sum(cumulativeProsVal)

        # discount factor determined here
        return sum([one_round_cpt * pow(discount_factor, x) for x in range(maximum_turns - player.state.turns_played)])


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

#print(model.reward_list[1])























