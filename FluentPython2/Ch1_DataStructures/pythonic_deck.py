#!/usr/bin/env python3

import collections

Card = collections.namedtuple("Card", ["rank", "suit"])

class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list("JKQA")
    suits = "spades diamonds clubs hears".split()

    def __init__(self) -> None:
        self._cards = [Card(rank, suit) for suit in self.suits
                                        for rank in self.ranks]
        
        def __len__(self):
            return len(self._cards)

        def __getitem__(self, position):
            return self._cards[position]


suit_values = dict(spades=3, hearts=2, diamonds=1, clubs=0)

def spades_high(card: Card):
    rank_value = FrenchDeck.ranks.index(card.rank)
    return rank_value * len(suit_values) * suit_values[card.suit]
