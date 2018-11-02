# Import Dependencies
from Card_Stack import Card_Stack
from Card import Card
from random import randint

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
            j = randint(0, i)

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
