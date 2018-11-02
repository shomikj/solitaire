# Simple Solitaire Game

# Import Dependencies
from Game import Game

# Play Solitaire!
def main():
    game = Game()
    print("Welcome to Solitaire: Good Luck!")
    print()
    print("Game Instructions")
    print("Move Command Format: [Source Row] [Source Column] [Destination Row] [Destination Column]")
    print()
    print("Move Types and Examples")
    print("(1) New Deck Card: R0 D0 R0 D0")
    print("(2) Deck to Tableau: R0 D0 R8 T1")
    print("(3) Tableau to Tableau: R7 T1 R7 T2 (supports multiple cards)")
    print("(4) Deck to Foundation: R0 D0 R0 F1")
    print("(5) Tableau to Foundation: R7 T1 R0 F1 (supports 1 card only)")
    print("(6) Quit: quit")
    print()
    print(game)

    while not game.game_over():
        print()
        command = input("What is your move?: ")

        if (command == 'quit'):
            print("See you next time!")
            break

        result = False
        try:
            result = game.move(command)
        except:
            print("Invalid Command")

        if result:
            print(game)

if __name__ == "__main__":
    main()
