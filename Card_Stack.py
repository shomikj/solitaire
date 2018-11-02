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
