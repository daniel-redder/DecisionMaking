import pymdp
from pymdp import utils
from pymdp.agent import Agent
import pandas as pd

import monopyly
import monopyly.monopyly.squares
from monopyly.monopyly import *

AMMOUNT_IN_WALLET = 500







#probabilities from https://faculty.math.illinois.edu/~bishop/monopoly.pdf
# n column
def getProbability(property:Property):

    #potential issue with calculation in tiles with duplicate names
    #only effects community chest and chance, however could be a problem in functions other than this

    df = pd.read_csv("normalized_prob_n.csv")
    print(property.name)
    output_prob = df[df["prop"]==property.name]

    try:
        return output_prob['prob'][0]

    except:
        print(f"Exception in getting probabilities {property.name}")

def expected_value(player,game_state,check_property: []):

    #default value for max turns in monopoly ai competition
    maximum_turns = 500

    #value we choose
    discount_factor = .9


    #syntax check #TODO
    color_set_list = [x.property_set for x in check_property]

    ev = []

    if len(color_set_list) > 1: color_set_list = set(color_set_list)

    #for each unique color set in check_property
    for color in color_set_list:

        #each property in that colorset
        color_props = [prop for prop in check_property if prop.property_set is color]

        #total number of properties in the set
        total_props = color.number_of_properties

        #all properties owned by the player now
        owned_properties = color.owned_properties(player=player)

        #temporary property val sum
        if len(owned_properties) > 0: owned_color_value = sum([prop.calculate_rent(game_state, player) * getProbability(prop) for prop in owned_properties])
        else: owned_color_value = 0

        #temporary owner list
        old_owner = []

        #temporary owner setting
        for prop in color_props:
            old_owner.append(prop.owner)
            prop.owner = player

        #temporary property owned #TODO ensure this updates with null sett
        temp_owned_property = color.owned_properties(player)

        #temporary property value
        temp_color_value = sum([prop.calculate_rent(game_state,player) * getProbability(prop) for prop in temp_owned_property])

        #calculate difference in cost
        ev.append( temp_color_value - owned_color_value )

        #reset owner to what it was before
        for prop in range(len(color_props)): color_props[prop].owner = old_owner[prop]

    one_round_ev = sum(ev)

    #discount factor determined here
    return sum([one_round_ev*pow(discount_factor, x) for x in range(maximum_turns-player.state.turns_played)])





set = PropertySet("test")
gameS = Game()
testb =Board(gameS)
testp = Player("Green Demon",1,testb)

test = Property("Go",set,110)
print(getProbability(test))
print(expected_value(player=testp,game_state=gameS,check_property = [test]))
