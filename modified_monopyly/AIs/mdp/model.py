
import random


from monopyly import *
from monopyly import PlayerAIBase
import monopyly
from .mdp import mdp
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
    
    not pay everything
        or is impossible to do like selling a house on a property that doesn't have houses
    
    1 action: 
    (avoid making a false decision) ie you cannot make a decision where it will 
        
    
    
        0: selling a house, 1: mortgaging a property, 2: making a trade 3: I can't do anything
    
    
    if we mortgage a property
    look at the   properties who are not mortgaged who argmax( mortgage funds gained - (expected value of the properties + the 10% cost to mortgage) )
    
    
2) mdp buying a property  (consider cash on hand)

    looks at expected value gained from property vs initial cost
    the reward function for this model if you decide not to buy must subtract the expected value of the property
    
    0: don't buy, 1: buy
    
    this agent doesn't bet
    

3) mdp for accepting declining a proposal
    
    is going to consider whether to accept or decline a proposal which is given as input. 
    it is going to consider the money exchanged and the expected value exchanged (which is really just one state)

    0: decline, 1: accept

4)  subset mdps which runs at the beginning of the round (consider cash on hand)

   has 3 actions: 
        mdp
           if you are in jail do you pay to leave
            (has the jail state)
            
            (0 occurs when they are not in jail)
            0: does nothing, 1: pay to leave jail, 2: don't pay
        
        
           do you unmortgage properties
           0: do not unmortgage, 2: unmortgage 
           (provided with candidate properties)
           
           get_unmortgage_cost()
           0: no, 1: yes 
        
        
           do you build houses
            0: no, 1: yes
            (if you can't build a house the model won't run)
            
            provide candidate properties which can be built upon
        
        loops until both actions are no
"""

gameS = Game()
testb = Board(gameS)
testp = Player("Green Demon", 1, testb)

minimum_money = 300
unmortgage_bound = 250

buy_mdp = mdp(1,gameS.state)



buy_policy = buy_mdp.mdp.policy
buy_policy_states = buy_mdp.stateSpace

property_sets = [PropertySet.BROWN,PropertySet.DARK_BLUE,PropertySet.LIGHT_BLUE,PropertySet.PURPLE,PropertySet.ORANGE,PropertySet.RED,
PropertySet.YELLOW,PropertySet.GREEN,PropertySet.UTILITY,PropertySet.UTILITY,PropertySet.STATION,PropertySet.STATION,PropertySet.STATION,PropertySet.STATION]







class mdpAristocrat(PlayerAIBase):
    def __init(self):

        pass

    def get_name(self):
        return "mdp Aristocrat human"



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

#Accepting /Declining Deals
    def deal_proposed(self, game_state, player, deal_proposal):
        pass



    def landed_on_unowned_property(self, game_state:monopyly.game.GameState, player, property):
        """
            return PlayerAIBase.Action.BUY
            return Action.DO_NOT_BUY
        """
        pos = property_sets.index(property.property_set.set_enum)

        cash = player.state.cash

        cashrat = cash / 200

        cash_states = [0,1,2,3]

        x_cash = [abs(x-cashrat) for x in cash_states].index(min([abs(x-cashrat) for x in cash_states]))

        cash_state = cash_states[x_cash]

        state = [0 for x in property_sets]
        state.insert(0,cash_state)
        state.insert(0,1)
        state[pos] = 1


        try:
            decision = buy_policy[buy_policy_states.index(state)]
        except:
            decision = 1

        if decision == 0:
            return PlayerAIBase.Action.DO_NOT_BUY
        elif decision == 1:
            return PlayerAIBase.Action.BUY
        else:
            print("what")
            return PlayerAIBase.Action.DO_NOT_BUY



        pass


#Pay / stay jail

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


    def mortgage_properties(self,game_state:monopyly.game.GameState, player:monopyly.game.Player):

        unmort_prop = player.state.owned_unmortgaged_sets
        unmort_proper = [x.properties for x in unmort_prop]

        unmort_prop = []

        for x in unmort_prop:
            for y in x:
                unmort_prop.append(y)


        print(unmort_prop,"unmort prop")
        cash = player.state.cash

        if len(unmort_prop) == 0: return []

        value_list = [buy_mdp.expected_value(player, game_state, [x]) for x in unmort_prop]


        ticker = 0
        mortgage_list = []

        if player.state.cash < 300:
            while cash < 300:
                cash += min(value_list).mortgage_value
                mortgage_list.append(unmort_prop[value_list.index(min(value_list))])
                value_list.remove(value_list.index(min(value_list)))
                ticker +=1
                if ticker >= 24:
                    return unmort_prop

            return mortgage_list

        else:
            return []






    def unmortgage_properties(self, game_state, player:monopyly.Player):

        mortgaged_sets = [p for p in player.state.properties if p.is_mortgaged]

        if len(mortgaged_sets) == 0: return []

        value_list = [self.buy_mdp.expected_value(player, game_state, [x]) for x in mortgaged_sets]

        cash = player.state.cash
        mortgage_list = []
        ticker = 0
        if player.state.cash > 300 +250:
            while cash> 300+250:
                cash -= max(value_list).get_unmortgage_cost()
                mortgage_list.append(mortgaged_sets[value_list.index(max(value_list))])
                value_list.remove(value_list.index(max(value_list)))
                ticker += 1
                if ticker >= 24:
                    return mortgaged_sets

            return mortgage_list

        else: return []


