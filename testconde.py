#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# github: https://github.com/houm01
# blog: https://houm01.com


import collections


Card = collections.namedtuple('Card', ['rank', 'suit'])


class FrenchDeck:   # 该类表示一张纸牌
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spads diamonds clubs hearts'.split()

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits
                                        for rank in self.ranks]

    def __len__(self):
        return len(self._Cards)

    def __getitem__(self, position):
        return self._Cards[position]


