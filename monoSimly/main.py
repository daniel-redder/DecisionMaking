from monoSimly.monopyly import *
from monoSimly.AIs.playerOne import playerOne
from monoSimly.AIs.playerTwo import playerTwo


# True to play a tournament, False to play a single game
# with selected players...
# play_tournament = False

# We find the collection of AIs from the AIs folder...
# ais = load_ais()




# We play a single game with selected players.
#
# This can be useful for testing your AI in a single game without
# having to play a full multi-player tournament.
#
# To test with your own players, change the AI selections below.

# Logging at INFO level shows verbose information about each
# turn in the game...
Logger.add_handler(FileLogHandler("game.log",Logger.INFO))

# # We select specific AIs from the ones loaded...
# sophie_ai = next(ai for ai in ais if ai.get_name() == "Green Devil")
# generous_daddy_ai = next(ai for ai in ais if ai.get_name() == "Generous Sindhi")
# mean_daddy_ai = next(ai for ai in ais if ai.get_name() == "RimpoAI")

playerOne = playerOne()
playerTwo = playerTwo()


# We set up and play a single game...
game = Game()
game.add_player(sophie_One)
game.add_player(playerTwo)
game.play_game()



