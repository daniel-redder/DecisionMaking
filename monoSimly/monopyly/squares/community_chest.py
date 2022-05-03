from .square import Square


class CommunityChest(Square):
    '''
    Represents one of the Community Chest squares.
    '''
    def __init__(self):
        '''
        The 'constructor'.
        '''
        super().__init__(Square.Name.COMMUNITY_CHEST)

    async def landed_on(self, game, player):
        '''
        Called when a player has landed on Community Chest.
        '''
        await game.state.board.community_chest_deck.take_card(game, player)
