from monoSimly.monopyly import *
import random
from ..bot import sendDM
import discord
import asyncio
import itertools
import time

class playerTwo(PlayerAIBase):
    '''
    An AI that plays like Sophie.

    She only buys the stations and Mayfair and Park Lane, and
    will enter into fairly generous deals to get hold of them.
    '''
    def __init__(self,client:discord.client,member:discord.Member,bot:discord.ext.commands.bot):
        '''
        The 'constructor'.
        '''
        self.member = member
        self.client = client
        self.bot = bot
        self.tired = False



    async def passToBot(self,message):
        self.client.loop.create_task(self.member.send(message))

        time.sleep(1)

        output = await self.bot.wait_for('message',check=(lambda context: context.author == self.member),
                                         timeout=None)


        return output.content

    async def messager(self,message=""):
        self.client.loop.create_task(self.member.send(message))


    def get_name(self):
        '''
        Returns this AI's name.
        '''
        return "playerOne"

    async def landed_on_unowned_property(self, game_state, player, property):
        '''
        Called when we land on an unowned property.

        If it is a station or Mayfair or Park Lane, we'll buy it.
        '''
        self.tired=False
        buy = await self.passToBot(f"Do you want to buy {property.name}, for {property.price}. Respond yes or no")

        if buy=="yes":
            await self.messager("attempting to purchase")
            return PlayerAIBase.Action.BUY

        else:
            await self.messager("not purchasing")
            return PlayerAIBase.Action.DO_NOT_BUY


    async def start_of_turn(self, game_state, player):
        self.tired=False



    async def propose_deal(self, game_state, player):
        '''
        We have the opportunity to propose a deal.

        If any other player has one of the properties we want, we
        offer them 2x the price for it.
        '''
        deal_proposal = DealProposal()

        hold_dic = []

        if self.tired: return []


        for x in Square.Name.hold_dic:
            val =  game_state.board.get_square_by_name(x)
            hold_dic.append(val)

        properties_owned_us = [x for x in hold_dic if x.owner is player]
        properties_owned = [x for x in hold_dic if not x.owner is None and not x.owner is player]

        out_string = "The Opponent Owns: "
        for x in range(len(properties_owned)): out_string= out_string + f"\n {x}: {properties_owned[x]}"
        out_string = out_string+"\n You own:"
        for y in range(len(properties_owned_us)): out_string= out_string +f"\n {y}: {properties_owned_us[y]}"

        out_string= out_string+"\n \n You will be given 3 chances to propose a trade with the opponent."

        print(out_string)
        await self.messager("what the fuck")
        await self.messager(out_string)

        tradeFor = await self.passToBot("Please enter a comma seperated list of the index of properties you want to trade for none if you don't want to trade for a property, or stop if you don't want to trade")

        if "stop" in tradeFor.lower():
            self.tired = True
            return None

        moneyFor = await self.passToBot("Please enter a integer ammount of cash you want to trade for (ie recieve), or none:")

        tradeTo = await self.passToBot("Please enter a comma seperated list of the index of properties you want to trade with (give), or none:")

        moneyTo = await self.passToBot("Please enter a integer ammount of cash you want to trade with  (ie give), or none:")

        try:
            if "none" in moneyFor.lower(): moneyFor = 0
            else: moneyFor = int(moneyFor)
            if "none" in moneyTo.lower(): moneyTo = 0
            else: moneyTo = int(moneyTo)
        except:
            print("issue calculating money to-from in trade")

        try:
            if "none" in tradeFor: tradeFor = []
            elif "," in tradeFor: tradeFor = [int(x) for x in tradeFor.split(",")]
            else: tradeFor = [int(tradeFor)]

            if "none" in tradeTo: tradeTo = []
            if "," in tradeTo: tradeTo = [int(x) for x in tradeTo.split(",")]
            else: tradeTo = [int(tradeTo)]
        except:
            print("error in trade for int conv")
            return None


        self.tired = False

        return DealProposal(
            properties_wanted=[x for x in properties_owned if properties_owned.index(x) in tradeFor],
            properties_offered=[x for x in properties_owned_us if properties_owned_us.index(x) in tradeTo],
            minimum_cash_wanted=moneyFor,
            maximum_cash_offered=moneyTo,
            propose_to_player=properties_owned[0].owner
        )



        # # We check to see if any of the properties we like is owned
        # # by another player...
        # for property_name in self.properties_we_like:
        #     property = game_state.board.get_square_by_name(property_name)
        #     if(property.owner is player or property.owner is None):
        #         # The property is either not owned, or owned by us...
        #         continue
        #
        #     # The property is owned by another player, so we make them an
        #     # offer for it...
        #     price_offered = property.price * 2
        #     if player.state.cash > price_offered:
        #         return DealProposal(
        #             properties_wanted=[property],
        #             maximum_cash_offered=price_offered,
        #             propose_to_player=property.owner)
        #
        # # We do not want to propose a deal...
        # return None


#not implemented for the moment
    async def build_houses(self, game_state, player):
        '''
        Sophie always tries to build houses if she can.
        '''

        buildable = []

        for owned_set in player.state.owned_unmortgaged_sets:
            if owned_set.can_build_houses:
                buildable.append(owned_set)


        #
        #
        # if player.state.cash < 1000:
        #     return []
        #
        # for owned_set in player.state.owned_unmortgaged_sets:
        #     if not owned_set.can_build_houses:
        #         continue
        #     return [(p, 1) for p in owned_set.properties]

        return []


    async def mortgage_properties(self, game_state, player):
        '''
        Sophie mortgages if she is short of cash.
        '''
        test = await self.passToBot("Do you wish to mortgage properties respond: yes, or no")

        if "no" in test.lower(): return []

        unmort_prop = [p for p in player.state.properties if p.is_mortgaged is False]

        out_string = ""
        for x in range(len(unmort_prop)): out_string = out_string + f"\n {x}: {unmort_prop[x]}"
        self.messager(out_string)
        choicer = await self.passToBot("Please enter a comma seperated list of properties to mortgage.")

        if "," in choicer:
            choicer = [unmort_prop[int(x)] for x in choicer.split(",")]
        else: choicer = [unmort_prop[int(choicer)]]

        return choicer


    async def unmortgage_properties(self, game_state, player):
        '''
        Sophie unmortgages if she is flush with cash.
        '''
        test = await self.passToBot("Do you wish to unmortgage properties respond: yes, or no")

        if "no" in test.lower(): return []

        unmort_prop = [p for p in player.state.properties if p.is_mortgaged]

        out_string = ""
        for x in range(len(unmort_prop)): out_string = out_string + f"\n {x}: {unmort_prop[x]}"
        self.messager(out_string)
        choicer = await self.passToBot("Please enter a comma seperated list of properties to unmortgage.")

        if "," in choicer:
            choicer = [unmort_prop[int(x)] for x in choicer.split(",")]
        else:
            choicer = [unmort_prop[int(choicer)]]

        return choicer





    async def players_birthday(self):
        '''
        Sophie is polite.
        '''
        return "Happy Birthday!"
