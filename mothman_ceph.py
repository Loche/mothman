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
    for i in range(num_total - num_lands):
        library.append(Card(CardType.OTHER))
    random.shuffle(library)
    return library

def has_land(cards):
    for card in cards:
        if card.type == CardType.LAND:
            return True
    return False

def ceph_trigger(library, trigger_count):
    print("Milled a land! Mothman triggers, targeting Cephalid. Trigger count: %d" % trigger_count)
    top_three = []
    if len(library) < 3:
        top_three, library = library, []
    else:
        top_three, library = library[:3], library[3:]
    if has_land(top_three):
        return ceph_trigger(library, trigger_count + 1)
    else:
        return library, trigger_count

def ceph_trigger_run():
    lib = generate_library(98, 30)
    lib, triggers = ceph_trigger(lib, 1)
    # print("Cards left in library: %d" % len(lib))
    # print("Ceph triggers: %d" % triggers)
    return triggers


def get_trigger_data(num_runs):
    trigger_counts = {}
    for i in range(num_runs):
        trigger_count = ceph_trigger_run()
        if not trigger_count in trigger_counts:
            trigger_counts[trigger_count] = 0
        else:
            trigger_counts[trigger_count] += 1
    return trigger_counts

# data is a map of ints to other ints
def generate_plot(data):
    x = list(data.keys())
    y = list(data.values())

    plt.plot(x, y, marker="o", linestyle="-", color="blue")
    plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(2))
    plt.title("Ceph trigger likelihood")
    plt.xlabel("Ceph trigger count")
    plt.ylabel("Number of times trigger count occurred")

    plt.savefig("mothman_plot.png")

def main():
    data = get_trigger_data(5000)
    data = {k: data[k] for k in sorted(data)}
    generate_plot(data)


if __name__ == "__main__":
    main()
