from monopyly import *
from testing_utils import *


class GameOverLoggingPlayer(DefaultPlayerAI):
    '''
    A player which logs the game-over event.
    '''
    def __init__(self):
        self.winner = None
        self.maximum_rounds_played = False

    def game_over(self, winner, maximum_rounds_played):
        self.winner = winner
        self.maximum_rounds_played = maximum_rounds_played


def test_maximum_rounds():
    '''
    Tests that the game is over when the maximum number of rounds
    has been played.
    '''
    game = Game()
    player0 = game.add_player(GameOverLoggingPlayer())
    player1 = game.add_player(GameOverLoggingPlayer())

    # We put both players on Free Parking and ensure that all dice
    # are zeros. Player1 has more money, so after the maximum number
    # of rounds, they should win...
    player0.state.square = 20
    player1.state.square = 20
    player0.state.cash = 1000
    player1.state.cash = 1200

    # We play the game...
    game.dice = MockDice(roll_results=[(0, 0)], repeat=True)
    game.maximum_rounds = 20
    game.play_game()

    # We check the winner and the turns played...
    assert game.number_of_rounds_played == game.maximum_rounds
    assert game.winner is player1

    # Did we get the notifications?
    assert player0.ai.winner is player1
    assert player0.ai.maximum_rounds_played is True
    assert player1.ai.winner is player1
    assert player1.ai.maximum_rounds_played is True


def test_maximum_rounds_net_worth_properties():
    '''
    One player has more money at the end of the game, but the other
    has the higher net worth because of properties.
    '''
    game = Game()
    player0 = game.add_player(GameOverLoggingPlayer())
    player1 = game.add_player(GameOverLoggingPlayer())

    # player0 has more money...
    player0.state.cash = 1000
    player1.state.cash = 980

    # But player1 has more valuable properties...
    game.give_property_to_player(player0, Square.Name.BOW_STREET)
    game.give_property_to_player(player0, Square.Name.VINE_STREET)
    game.give_property_to_player(player1, Square.Name.STRAND)
    game.give_property_to_player(player1, Square.Name.FLEET_STREET)
    game.give_property_to_player(player1, Square.Name.TRAFALGAR_SQUARE)

    # We put both players on Free Parking and ensure that all dice
    # are zeros. Player1 has more money, so after the maximum number
    # of rounds, they should win...
    player0.state.square = 20
    player1.state.square = 20

    # We play the game...
    game.dice = MockDice(roll_results=[(0, 0)], repeat=True)
    game.maximum_rounds = 20
    game.play_game()

    # We check the winner and the turns played...
    assert player0.net_worth == 1000 + 90 + 100  # 1190
    assert player1.net_worth == 980 + 110 + 110 + 120  # 1320
    assert game.number_of_rounds_played == game.maximum_rounds
    assert game.winner == player1


def test_maximum_rounds_net_worth_properties_and_houses():
    '''
    One player has more money at the end of the game, the other
    has the higher net worth because of properties, but the first
    player has higher value houses.
    '''
    game = Game()
    player0 = game.add_player(GameOverLoggingPlayer())
    player1 = game.add_player(GameOverLoggingPlayer())

    # player0 has more money...
    player0.state.cash = 1000
    player1.state.cash = 980

    # player1 has more valuable properties...
    bow_street = game.give_property_to_player(player0, Square.Name.BOW_STREET)
    marlborough_street = game.give_property_to_player(player0, Square.Name.MARLBOROUGH_STREET)
    vine_street = game.give_property_to_player(player0, Square.Name.VINE_STREET)
    strand = game.give_property_to_player(player1, Square.Name.STRAND)
    fleet_street = game.give_property_to_player(player1, Square.Name.FLEET_STREET)
    trafaglar_square = game.give_property_to_player(player1, Square.Name.TRAFALGAR_SQUARE)

    # But player0 has more valuable houses...
    bow_street.number_of_houses = 1
    marlborough_street.number_of_houses = 1
    vine_street.number_of_houses = 1
    trafaglar_square.number_of_houses = 1

    # We put both players on Free Parking and ensure that all dice
    # are zeros. Player1 has more money, so after the maximum number
    # of rounds, they should win...
    player0.state.square = 20
    player1.state.square = 20

    # We play the game...
    game.dice = MockDice(roll_results=[(0, 0)], repeat=True)
    game.maximum_rounds = 20
    game.play_game()

    # We check the winner and the turns played...
    assert player0.net_worth == 1000 + 90 + 90 + 100 + 3 * 50  # 1430
    assert player1.net_worth == 980 + 110 + 110 + 120 + 75  # 1395
    assert game.number_of_rounds_played == game.maximum_rounds
    assert game.winner == player0


def test_maximum_rounds_equal_worth():
    '''
    Maximum rounds are played, and it's a draw.
    '''
    game = Game()
    player0 = game.add_player(GameOverLoggingPlayer())
    player1 = game.add_player(GameOverLoggingPlayer())

    # We put both players on Free Parking and ensure that all dice
    # are zeros. Player1 has more money, so after the maximum number
    # of rounds, they should win...
    player0.state.square = 20
    player1.state.square = 20
    player0.state.cash = 1200
    player1.state.cash = 1200

    # We play the game...
    game.dice = MockDice(roll_results=[(0, 0)], repeat=True)
    game.maximum_rounds = 20
    game.play_game()

    # We check the winner and the turns played...
    assert game.number_of_rounds_played == game.maximum_rounds
    assert game.winner is None


def test_all_players_bankrupt_in_same_round():
    '''
    All players go bankrupt in the same round (or at least, they would
    if the game played the whole round).

    We check that the last remaining player wins.
    '''
    game = Game()
    player0 = game.add_player(GameOverLoggingPlayer())
    player1 = game.add_player(GameOverLoggingPlayer())
    player2 = game.add_player(GameOverLoggingPlayer())

    # All players are on Liverpool Street station, and all roll
    # three to land on Super Tax...
    player0.state.square = 35
    player1.state.square = 35
    player2.state.square = 35

    # None of them have enough money to pay the tax...
    player0.state.cash = 20
    player1.state.cash = 20
    player2.state.cash = 20

    # We play a round...
    game.dice = MockDice([(1, 2), (1, 2), (1, 2)])
    game.play_game()

    # Players 0 and 1 should be bankrupt, and player2
    # should be the winner...
    assert player0 not in game.state.players
    assert player1 not in game.state.players
    assert player2 in game.state.players
    assert player0 in game.state.bankrupt_players
    assert player1 in game.state.bankrupt_players
    assert game.winner is player2

    # Did we get the notifications?
    assert player0.ai.winner is player2
    assert player0.ai.maximum_rounds_played is False
    assert player1.ai.winner is player2
    assert player1.ai.maximum_rounds_played is False
    assert player2.ai.winner is player2
    assert player2.ai.maximum_rounds_played is False
