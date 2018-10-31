# Simple Solitaire Game

# Import Statements
import random

#############################################################################

# Card Class
# Rank (integer 1 => 13), Str_Rank (for output), Visible (face down/hidden in current game state)
class Card:
    def __init__(self, param_rank):
        self.rank = param_rank
        self.str_rank = ['A  ', '2  ', '3  ', '4  ', '5  ', '6  ', '7  ', '8  ', '9  ', '10 ', 'J  ', 'Q  ', 'K  ']
        self.visible = False

    # print(card_obj) => calls this method
    # takes into account whether card is currently visible for output
    def __str__(self):
        if self.visible:
            return self.str_rank[self.rank-1]
        else:
            return '-  '

    def hide(self):
        self.visible = False

    def show(self):
        self.visible = True

#############################################################################

# Card Stack: Abstract Class
# Framework for Tableaus, Foundations, and Deck
class Card_Stack:
    def __init__(self):
        self.cards = []

    # len(card_stack_obj) => calls this method
    def __len__(self):
        return len(self.cards)

    def top(self):
        if not self.empty():
            return self.cards[-1]
        else:
            return None

    def empty(self):
        return len(self) == 0

#############################################################################

# Deck Class
class Deck(Card_Stack):
    def __init__(self):
        Card_Stack.__init__(self)

        # create 52 cards (4/rank) and add to Deck
        for i in range(0, 4):
            for r in range(1, 14):
                c = Card(r)
                self.cards.append(c)

        self.shuffle()

        # pointer = index to only 1 "viewable" card in deck during game
        self.pointer = 0

    # Shuffle Deck
    def shuffle(self):
        # starting from last element, randomly swap 1 by 1
        # first element will be swapped by default
        for i in range(len(self.cards)-1, 0, -1):
            # pick a random index from 0 to i
            j = random.randint(0, i)

            # swap arr[i] with arr[j]
            self.cards[i],self.cards[j] = self.cards[j],self.cards[i]

    # Note: No add function -- can't add elements to deck (only remove, 1 at a time)

    # Current "viewable" element in Deck
    def top(self):
        return self.cards[self.pointer]

    # Increment pointer: need new viewable card
    def increment(self):
        # hide old card
        self.cards[self.pointer].hide()

        self.pointer += 1
        if (self.pointer >= len(self)):
            self.pointer = 0

        # show new card
        self.cards[self.pointer].show()

    # Remove "viewable" element from deck
    def pop(self):
        answer = self.cards[self.pointer]

        # Delete from deck array, make new "top" visible
        # Note that self.pointer index doesn't change
        del self.cards[self.pointer]
        self.cards[self.pointer].show()

        return answer

#############################################################################

# Tableau Class
class Tableau(Card_Stack):
    def __init__(self):
        Card_Stack.__init__(self)

    # returns boolean: valid to add given cards?
    # (1) cards are visible
    # (2) cards have decreasing rank (1 by 1)
    # (3) first new card 1 less than current bottom of Tableau
    def valid(self, new):
        threshold = 14
        if self.top():
            threshold = self.top().rank

        for c in new:
            if (c.visible) and (c.rank == threshold-1):
                threshold = c.rank
            else:
                return False
        return True

    # Assumes valid is called first!
    def add(self, new):
        for c in new:
            self.cards.append(c)

    # Get copy of cards from index i onwards
    def view_cards(self, i):
        # check valid index
        if (i >= 0) and (i < len(self)):
            return self.cards[i:]
        else:
            return []

    # Remove cards from index i onwards
    # Can only remove visible cards!
    def remove_cards(self, i):
        # check valid index
        if (i >= 0) and (i < len(self)):
            for c in range(i, len(self)):
                if not self.cards[c].visible:
                    return []

            # visible cards => remove!
            answer = self.cards[i:]             # save cards being moved
            self.cards = self.cards[:i]         # modify this tableau

            # make top card visible in new resulting tableau
            if not self.empty():
                self.top().show()

            return answer
        else:
            return []

    # returns whether index == next spot in tableau
    def next_spot(self, i):
        return (i == len(self))

    # returns whether index == last/bottom element in tableau
    def last_spot(self, i):
        return (i == len(self)-1)

    # get "print string" of an element in tableau
    def get_str(self, i):
        if i < len(self.cards):
            return str(self.cards[i])
        else:
            return '   '

#############################################################################

# Foundation Class
class Foundation(Card_Stack):
    def __init__(self):
        Card_Stack.__init__(self)

    # returns boolean: valid to add given card?
    # (1) card must be visible
    # (2) rank must be 1 higher than existing top card
    def valid(self, c):
        threshold = 0
        if self.top():
            threshold = self.top().rank

        return (c.rank == threshold+1)

    # add given card: valid must be called first!
    # only supports adding 1 card at a time
    def add(self, c):
        # hide existing top card
        if not self.empty():
            self.cards[-1].hide()
        self.cards.append(c)

    # print(foundation_obj) => calls this method
    # print top card in tableau
    def __str__(self):
        if self.empty():
            return '-  '
        else:
            return str(self.top())

    # whether foundation contains all cards 1...13
    def full(self):
        # must have 13 cards
        if not (len(self) == 13):
            return False

        # one of each rank, increasing
        for i in range(1,14):
            if not (self.cards[i].rank == i):
                return False

        return True

#############################################################################

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

#############################################################################

# Play Solitaire!

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
