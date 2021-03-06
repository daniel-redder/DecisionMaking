from .square import Square
from ..utility import Logger


class Go(Square):
    '''
    Represents the Go square.
    '''
    def __init__(self):
        '''
        The 'constructor'.
        '''
        super().__init__(Square.Name.GO)

    async def landed_on(self, game, player):
        '''
        When a player lands on Go they get £200.
        '''
        await Logger.log("{0} landed on Go and gets £200".format(player.name))
        await game.give_money_to_player(player, 200)

