import pymdp
from pymdp import utils
from pymdp.agent import Agent
import pandas as pd

import monopyly
import monopyly.monopyly.squares
from monopyly.monopyly import *

#probabilities from https://faculty.math.illinois.edu/~bishop/monopoly.pdf
# n column
def getProbability(property:Property):
    df = pd.read_csv("prob.csv")
    print(df)



def expected_value(player,game_state,check_property: []):

    #syntax check #TODO
    color_set_list = [x.property_set for x in check_property]

    ev = []

    #for each unique color set in check_property
    for color in set(color_set_list):

        #each property in that colorset
        color_props = [prop for prop in check_property if prop.property_set is color]

        #total number of properties in the set
        total_props = color.number_of_properties()

        #all properties owned by the player now
        owned_properties = color.owned_properties(player)

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

    return sum(ev)


dfo = pd.read_csv("hol.csv")
df = pd.read_csv("prob.csv")
print(df)
df['prob'] = dfo['prob']
df['prob'] = df['prob'] / df['prob'].sum()
print(df.sum())
df.to_csv("normalized_prob_n.csv")