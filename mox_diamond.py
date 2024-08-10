#!/usr/bin/env python3

from enum import Enum
import random
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

class CardType(Enum):
    OTHER = 0
    LAND = 1

class Card:
    def __init__(self, type):
        self.type = type


def generate_library(num_total, num_lands):
    library = []
    for i in range(num_lands):
        library.append(Card(CardType.LAND))
    for i in range(num_total - num_lands - 1):
        library.append(Card(CardType.OTHER))
    random.shuffle(library)
    return library

def get_land_count(hand):
    num_lands = 0
    for card in hand:
        if card.type is CardType.LAND:
            num_lands += 1
    return num_lands

def main():
    for land_count in range(15, 40):
        online_count = 0
        offline_count = 0
        mise_count = 0
        library = None
        for x in range(10000):
            if not library:
                # Mox Diamond is always drawn for this experiment.
                library = generate_library(97, land_count)
                random.shuffle(library)
                library.insert(0, Card(CardType.OTHER))
            else:
                mox_diamond, rest_of_library = library[0], library[1:]
                random.shuffle(rest_of_library)
                rest_of_library.insert(0, mox_diamond)
                library = rest_of_library

            hand = library[0:7]
            num_lands = get_land_count(hand)
            if num_lands >= 2:
                online_count += 1
            else:
                offline_count += 1
                if library[7].type == CardType.LAND and num_lands == 1:
                    mise_count += 1
        print("--Land count: %d" % land_count)
        print("Online: %d" % online_count)
        print("Offline: %d" % offline_count)
        print("Topdeck the second land: %d" % mise_count)


if __name__ == "__main__":
    main()
