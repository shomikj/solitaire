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
