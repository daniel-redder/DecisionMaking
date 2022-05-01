
import random
from monopyly import *
from monopyly.monopyly import PlayerAIBase

"""
We move (we roll out dice)



----------------------------- actions

if we land on a property
do we buy the property


"""




"""
partial order

[ [state_1, state_2] [decisions], [state_3,stat_4] [decision 2]  ]

"""






"""
MDP models

1)  mdp for determining how to acquire a given amount of money
    
    is it going to look at the expected value of all properties you own
    It will compare the rent gained from owning a house and the cost of buying a house / selling 
    against the loss from mortgaging the property
    against a potential proposal 
    
    input: proposal ( certain amount of cash, and or a certain number of properties in exchange for cash)
    
    if its greater than the value of the money that you are looking for then its just the value
    if its less then it is very low
    
    
    
2) mdp buying a property  (consider cash on hand)

    looks at expected value gained from property vs initial cost
    
    
3) mdp for accepting declining a proposal
    
    is going to consider whether to accept or decline a proposal which is given as input. 
    it is going to consider the money exchanged and the expected value exchanged (which is really just one state)

4) mdp which runs at the beginning of the round (consider cash on hand)

   has 3 actions: 
       if you are in jail do you pay to leave
        (has the jail state)
       do you unmortgage properties
       do you build houses


"""


def figureMoney():





class mdpAristocrat(PlayerAIBase):
    def __init(self):
        pass


    def get_name(self):
        return "mdp Aristocrat"



    def propose_deal(self, game_state, player):
        """Deal generation (the agent proposing a deal)

        Either randomly, or heuristically generate deals, then pass them to the "deals/proposal mdp" which will decide whether to accept or decline
        3 deals that are accepted from the list of generated deals will be passed to the opponenet to decide on.

        If 3 deals are not accepted it will pass as many that are as possible otherwise no deal.


        deal_proposal = DealProposal()

        random.shuffle(self.properties_we_like)

        # We check to see if any of the properties we like is owned
        # by another player...
        for property_name in self.properties_we_like:
            property = game_state.board.get_square_by_name(property_name)
            if(property.owner is player or property.owner is None):
                # The property is either not owned, or owned by us...
                continue

            # The property is owned by another player, so we make them an
            # offer for it...
            price_offered = property.price * 2
            if player.state.cash > price_offered:
                return DealProposal(
                    properties_wanted=[property],
                    maximum_cash_offered=price_offered,
                    propose_to_player=property.owner)



        """
        pass




    def landed_on_unowned_property(self, game_state, player, property):
        """
            return PlayerAIBase.Action.BUY
            return Action.DO_NOT_BUY
        """

        pass




    def build_houses(self, game_state, player):

        """
        usefull attributes
        player.state.owned_unmortgaged_sets (owned_set)
        owned_set.can_build_houses (True if can build houses in set)
        owned_set.properties  (returns property objects)

        example code:
                if player.state.cash < 1000:
            return []

        for owned_set in player.state.owned_unmortgaged_sets:
            if not owned_set.can_build_houses:
                continue
            return [(p, 1) for p in owned_set.properties]

        return []
        """


    def mortgage_properties(self,game_state, player):
        """
        player.state.cash
        attribute of properties.is_mortgaged

        example code:
                if player.state.cash < 500:
            return [p for p in player.state.properties if p.is_mortgaged is False]
        """





    def unmortgage_properties(self, game_state, player):
        """
        return list of mortgaged properties to unmortgage
        """