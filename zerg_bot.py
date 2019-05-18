import sc2
from sc2.constants import LARVA, ZERGLING, QUEEN, OVERLORD, DRONE, HYDRALISK, HYDRALISKDEN
from sc2.constants import HATCHERY, SPAWNINGPOOL, EXTRACTOR, LAIR
from sc2.constants import RESEARCH_ZERGLINGMETABOLICBOOST, EFFECT_INJECTLARVA, AbilityId

import random
from utils import *

class ZergInfestationStrategyBot(sc2.BotAI):
    def __init__(self):
        self.drone_counter = 0
        self.extractor_started = False
        self.spawning_pool_started = False
        self.moved_workers_to_gas = False
        self.moved_workers_from_gas = False
        self.queeen_started = False
        self.mboost_started = False


    async def on_step(self, iteration):

        self.hq = self.townhalls.random
        self.larvae = self.units(LARVA)

        await self.build_and_distribute_workers()
        await self.explore_the_map()
        await self.launch_attack_if_we_are_ready()
        await self.research_zergling_metabolic_boost_when_possible()
        await self.build_supply_when_necessary()
        await self.try_to_build_hydralisks_quickly()
        await self.try_to_build_zerglings_quickly()
        await self.build_an_expansion()
        await self.build_queens_continously()


    async def build_and_distribute_workers(self):
        await self.distribute_workers()
        if self.hq.assigned_harvesters < self.hq.ideal_harvesters:
            if self.can_afford(DRONE) and self.larvae.amount > 0:
                self.drone_counter += 1
                await self.do(self.larvae.random.train(DRONE))

        if not self.extractor_started:
            if self.can_afford(EXTRACTOR) and self.workers.exists:
                drone = self.workers.random
                target = self.state.vespene_geyser.closest_to(drone.position)
                err = await self.do(drone.build(EXTRACTOR, target))
                if not err:
                    self.extractor_started = True


    async def explore_the_map(self):
        scout_locations = [location for location in self.expansion_locations if
                           location not in self.enemy_start_locations]

        for overlord in self.units(OVERLORD).idle:
            await self.do(overlord.move(random.choice(scout_locations)))

    async def launch_attack_if_we_are_ready(self):
        forces = self.units(ZERGLING) | self.units(HYDRALISK)
        target = self.known_enemy_structures.random_or(self.enemy_start_locations[0]).position

        if self.units(HYDRALISK).amount > 10:
            for unit in forces.idle:
                await self.do(unit.attack(target))

        if self.units(ZERGLING).amount > 50:
            for unit in forces.idle:
                await self.do(unit.attack(target))

    async def research_zergling_metabolic_boost_when_possible(self):
        if self.vespene >= 100:
            sp = self.units(SPAWNINGPOOL).ready
            if sp.exists and self.minerals >= 100 and not self.mboost_started:
                await self.do(sp.first(RESEARCH_ZERGLINGMETABOLICBOOST))
                self.mboost_started = True

    async def build_supply_when_necessary(self):
        if self.supply_left < 2:
            if self.can_afford(OVERLORD) and self.larvae.exists:
                await self.do(self.larvae.random.train(OVERLORD))

    async def try_to_build_zerglings_quickly(self):
        if not self.spawning_pool_started:
            if self.can_afford(SPAWNINGPOOL) and self.workers.exists:
                for d in range(4, 15):
                    pos = self.hq.position.to2.towards(self.game_info.map_center, d)
                    if await self.can_place(SPAWNINGPOOL, pos):
                        drone = self.workers.closest_to(pos)
                        err = await self.do(drone.build(SPAWNINGPOOL, pos))
                        if not err:
                            self.spawning_pool_started = True
                            break

        if self.units(SPAWNINGPOOL).ready.exists:
            if self.larvae.exists and self.can_afford(ZERGLING):
                await self.do(self.larvae.random.train(ZERGLING))


    async def try_to_build_hydralisks_quickly(self):

        if self.units(SPAWNINGPOOL).ready.exists:
            if not self.units(LAIR).exists:
                if self.can_afford(LAIR):
                    await self.do(self.townhalls.first.build(LAIR))

        if self.units(LAIR).ready.exists:
            if not (self.units(HYDRALISKDEN).exists or self.already_pending(HYDRALISKDEN)):
                if self.can_afford(HYDRALISKDEN):
                    await self.build(HYDRALISKDEN, near=self.townhalls.first)

        if self.units(HYDRALISKDEN).ready.exists:
            if self.can_afford(HYDRALISK) and self.larvae.exists:
                await self.do(self.larvae.random.train(HYDRALISK))

    async def build_an_expansion(self):
        scout_locations = [location for location in self.expansion_locations if
                           location not in self.enemy_start_locations]
        if self.minerals > 400 and self.workers.exists:
            #pos = get_closest_expansion_location(scout_locations, self.start_location)
            pos = random.choice(scout_locations)
            if await self.can_place(HATCHERY, pos):
                self.spawning_pool_started = True
                await self.do(self.workers.random.build(HATCHERY, pos))


    async def build_queens_continously(self):
        for queen in self.units(QUEEN).idle:
            abilities = await self.get_available_abilities(queen)
            if AbilityId.EFFECT_INJECTLARVA in abilities:
                await self.do(queen(EFFECT_INJECTLARVA, self.hq))


        if not self.queeen_started and self.units(SPAWNINGPOOL).ready.exists:
            if self.can_afford(QUEEN):
                r = await self.do(self.hq.train(QUEEN))
                if not r:
                    self.queeen_started = True