import pymdp
from pymdp import utils
from pymdp.agent import Agent
from monopyly.monopyly.squares import *

def getProbability(check_property):
    pass



def expected_value(player,check_property: []):

    #syntax check #TODO
    color_set_list = [x.property_set for x in check_property]

    parsed_colors = []

    ev = []

    for i in color_set_list:

        x = color_set_list[i]

        if x in parsed_colors: pass

        #calculate value considering all properties
        elif color_set_list.count(x) > 1:
            num_prop_in_set=x.number_of_properties()
            #TODO get number of properties in set owned by player
            num_prop_owned = 1
            if num_prop_owned + color_set_list.count(x) == num_prop_in_set:
                #TODO potentially add the property to the player then use calculate_rent, need to find out what calculate rent is doing first
                #replace this with calculation of property value across all properties owned and listed here then apply diff for ev
                pass

        #direct value calculation
        else:
            #TODO calculate rent may not be implemented
            #takes parameters "game", "player" look at other ai code
            ev.append( check_property[i].calculate_rent( ) * getProbability(check_property[i]) )

    return ev

