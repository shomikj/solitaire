# Import Dependencies
from Card_Stack import Card_Stack

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
