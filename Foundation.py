# Import Dependencies
from Card_Stack import Card_Stack

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
