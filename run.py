import random

import sc2
from sc2 import Race, Difficulty
from sc2.player import Bot, Computer

from zerg_bot import ZergInfestationStrategyBot


def main():
    sc2.run_game(sc2.maps.get("AutomatonLE"), [
        Bot(Race.Zerg, ZergInfestationStrategyBot()),
        Computer(Race.Terran, Difficulty.Hard)
    ], realtime=True, save_replay_as="ZvT.SC2Replay")

if __name__ == '__main__':
    main()