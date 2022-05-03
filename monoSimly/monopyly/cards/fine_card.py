from .card import Card
import asyncio

class FineCard(Card):
    '''
    Manages cards that fine the player who picks them up.
    For example: Speeding fine pay £15.
    '''
    def __init__(self, fine):
        '''
        The 'constructor'
        '''
        self.fine = fine

    async def play(self, game, current_player):
        '''
        Takes the fine from the player.
        '''

        await game.take_money_from_player(current_player, self.fine)



