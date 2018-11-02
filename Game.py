# Import Dependencies
from Deck import Deck
from Tableau import Tableau
from Foundation import Foundation

# Game Class!
class Game:
    # Set Up Game, Distribute Cards
    def __init__(self):
        self.tableaus = []
        self.foundations = []
        self.deck = Deck()

        # Create Tableaus
        for i in range(0, 7):
            self.tableaus.append(Tableau())

        # Distribute Cards to Tableaus
        for i in range(7, 0, -1):        # i = number cards to deal
            for j in range(0, i):
                self.tableaus[j].add([self.deck.pop()])
                self.tableaus[j].top().hide()

        # Make Current Card in Deck Visible
        self.deck.top().show()

        # Make Top Card in Each Tableau Visible
        for t in self.tableaus:
            t.top().show()

        # Create Foundations
        for i in range(0, 4):
            self.foundations.append(Foundation())

    # Game Over if all foundations full
    def game_over(self):
        for f in self.foundations:
            if not f.full():
                return False
        return True

    # Input Row Syntax Correct (index checked per individual case)
    # check length and whether begins with 'R'
    def valid_row(self, str):
        if (len(str) == 2) or (len(str) == 3):
            if (str[0] == 'R'):
                return True

        return False # all other invalid, if this point reached

    # Input Column Syntax Correct
    def valid_col(self, str):
        return str in ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'F1', 'F2', 'F3', 'F4', 'D0']

    # Valid Index for Tableaus
    def valid_tableau(self, i):
        return (i >= 0) and (i < len(self.tableaus))

    # Valid Index for Foundations
    def valid_foundation(self, i):
        return (i >= 0) and (i < len(self.foundations))


    # MAIN Move Function!!!
    # (1) New Deck Card
    # (2) Deck to Tableau
    # (3) Tableau to Tableau
    # (4) Deck to Foundation
    # (5) Tableau to Foundation

    def move(self, command):
        sequence = command.split()

        if (len(sequence) != 4):
            print("Invalid Command: format error")
            return False

        from_row = sequence[0]
        from_col = sequence[1]
        to_row = sequence[2]
        to_col = sequence[3]

        # Check Valid Row/Column Names
        if not (self.valid_col(from_col) and self.valid_col(to_col) and self.valid_row(from_row) and self.valid_row(to_row)):
            print("Invalid Command: format error")
            return False

        # Move Type 1: New Deck Card
        if (from_row == 'R0') and (from_col == 'D0') and (to_row == 'R0') and (to_col == 'D0'):
            self.deck.increment()
            return True

        # Move Type 2: Deck to Tableau
        if (from_row == 'R0') and (from_col == 'D0') and ('T' == to_col[0]):
            to_row = int(to_row[1:]) - 1
            to_col = int(to_col[1:]) - 1

            # must be valid tableau
            if not self.valid_tableau(to_col):
                print("Invalid Command: tableau column error")
                return False

            # target row must be at the end of destination tableau
            if not self.tableaus[to_col].next_spot(to_row):
                print("Invalid Command: tableau row error")
                return False

            # look at card to move; move if valid
            move_card = [self.deck.top()]
            if self.tableaus[to_col].valid(move_card):
                self.tableaus[to_col].add([self.deck.pop()])
                return True
            else:
                print("Invalid Command: can't move selected cards")
                return False

        # Move Type 3: Tableau to Tableau
        if ('T' == from_col[0]) and ('T' == to_col[0]):
            from_col = int(from_col[1:]) - 1
            to_col = int(to_col[1:]) - 1
            from_row = int(from_row[1:]) - 1
            to_row = int(to_row[1:]) - 1

            # must be valid tableaus
            if not self.valid_tableau(from_col) or not self.valid_tableau(to_col):
                print("Invalid Command: tableau column error")
                return False

            # target row must be at the end of destination tableau
            if not self.tableaus[to_col].next_spot(to_row):
                print("Invalid Command: destination tableau row error")
                return False

            # source row must be between 0 and num elements in source tableau
            # source tableau cannot be empty
            if (self.tableaus[from_col].empty()) or (from_row < 0) or (from_row >= len(self.tableaus[from_col])):
                print("Invalid Command: source tableau row error")
                return False

            # look at cards to move; move if valid
            move_cards = self.tableaus[from_col].view_cards(from_row)
            if self.tableaus[to_col].valid(move_cards):
                self.tableaus[to_col].add(self.tableaus[from_col].remove_cards(from_row))
                return True
            else:
                print("Invalid Command: can't move selected cards")
                return False

        # Move Type 4: Deck to Foundation
        if (from_row == 'R0') and (from_col == 'D0') and (to_row == 'R0') and ('F' == to_col[0]):
            to_col = int(to_col[1:]) - 1

            # must be valid foundation
            if not self.valid_foundation(to_col):
                print("Invalid Command: foundation column error")
                return False

            # get threshold: destination foundation's top card rank
            move_card = self.deck.top()
            if (self.foundations[to_col].valid(move_card)):
                self.foundations[to_col].add(self.deck.pop())
                return True
            else:
                print("Invalid Command: can't move selected cards")
                return False

        # Move Type 5: Tableau to Foundation
        if (from_col[0] == 'T') and (to_row == 'R0') and ('F' == to_col[0]):
            from_col = int(from_col[1:]) - 1
            to_col = int(to_col[1:]) - 1
            from_row = int(from_row[1:]) - 1

            # must be valid tableau
            if not self.valid_tableau(from_col):
                print("Invalid Command: source tableau column error")
                return False

            # source row must be bottom of tableau
            if not self.tableaus[from_col].last_spot(from_row):
                print("Invalid Command: source tableau row error")
                return False

            # must be valid foundation
            if not self.valid_foundation(to_col):
                print("Invalid Command: destination foundation column error")
                return False

            # get threshold: destination foundation's top card rank
            move_card = self.tableaus[from_col].top()
            if (self.foundations[to_col].valid(move_card)):
                move_card = self.tableaus[from_col].remove_cards(from_row)
                move_card = move_card[0]
                self.foundations[to_col].add(move_card)
                return True
            else:
                print("Invalid Command: can't move selected cards")
                return False

    # print(game_obj) => calls this method
    # print current game state
    def __str__(self):
        # Header Row = Top Card in Deck
        spot = '   '

        header = spot + 'D0 ' + spot + spot + 'F1 ' + 'F2 ' + 'F3 ' + 'F4 ' + '\n'

        header_cards = 'R0 ' + str(self.deck.top()) + spot + spot
        for f in self.foundations:
            header_cards += str(f)
        header_cards += '\n' + '\n'

        tableau_header = spot
        for i in range(0, 7):
            tableau_header += 'T' + str(i+1) + ' '
        tableau_header += '\n'

        tableau_str = ''
        max_len = max([len(i) for i in self.tableaus])
        for r in range(0, max_len+1):
            tableau_str += 'R' + str(r+1)
            if r < 9:
                tableau_str += ' '
            for t in self.tableaus:
                tableau_str += t.get_str(r)
            tableau_str += '\n'

        return header + header_cards + tableau_header + tableau_str
