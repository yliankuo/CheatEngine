# Import dependencies (modules/classes we'll need in our main function)

import battlecode as bc
import random
import sys
import traceback
from Factory import Factory as factory
from Utilities import Utilities as utilities
from Worker import Worker as worker
# from Knight import Knight as Knight
# from Mage import Mage as Mage
from Ranger import Ranger as ranger
# from Healer import Healer as Healer

# Import dependencies end


print("pystarted")

# It's a good idea to try to keep your bots deterministic, to make debugging easier.
# determinism isn't required, but it means that the same things will happen in every thing you run,
# aside from turns taking slightly different amounts of time due to noise.
random.seed(6137)


# Obtain value end

#Define Variables that we will call within the method
# Obtain game values to reduce module calls
# A GameController is the main type that you talk to the game with.
# Its constructor will connect to a running game.
init = False
gc = bc.GameController()
gm = bc.GameMap
# orbit_pattern = bc.OrbitPattern()
directions = list(bc.Direction)
my_team = gc.team()
earth_map = gc.starting_map(bc.Planet.Earth)
mars_map = gc.starting_map(bc.Planet.Mars)
asteroid_pattern = gm.asteroids
unit_paths = {}
initial_deposits = utilities.initial_karbonite(earth_map)
sortedf = {}
sortede = {}
enem = []
# sortedf, sortede, enem = utilities.sort_units(earth_map.initial_units, sortedf, sortede, enem, gc)
worker_lim = 20
p_counter = utilities.pcounter_reset()
# Define variables end

# Define Functions that we will call within the method


def resolve_unit(unit):
    temp_path = []
    action = ""
    type = unit.unit_type
    if type == bc.UnitType.Factory:
        utype = bc.UnitType.Ranger
        action = factory.factory(unit, gc, utype)
        if action == "produce":
            p_counter[utype] = p_counter[utype] + 1

    if type == bc.UnitType.Worker:
        # print(sortedf)
        action= worker.worker(unit, gc, earth_map, mars_map, initial_deposits, worker_lim)
        if action == "replicate":
            p_counter[type] = p_counter[type] + 1

    if type == bc.UnitType.Ranger:
        action = ranger.ranger(unit,gc,earth_map,mars_map)
    # print(str(unit.id) + ": " + str(action))

# let's start off with some research!
# we can queue as much as we want.


gc.queue_research(bc.UnitType.Worker)
gc.queue_research(bc.UnitType.Rocket)
gc.queue_research(bc.UnitType.Knight)


while True:
    # We only support Python 3, which means brackets around print()

    # frequent try/catches are a good idea
    try:
        if gc.planet() == bc.Planet.Earth:
            print('pyround:', gc.round())
            print("Time Left:" + str(gc.get_time_left_ms()))
        # if init:
        #     # print(gc.units())
        #     sortedf = utilities.clean_units(sortedf, gc)
        #     sortedf, sortede, enem = utilities.sort_units(gc.units(), sortedf, sortede, enem, gc)
        # else:
        #     init = True
        # print(sorted)
        # print(gc.karbonite())
        # walk through our units:
        for unit in gc.my_units():

            # first, factory logic
            resolve_unit(unit)

            # first, let's look for nearby blueprints to work on
            # location = unit.location
            # if location.is_on_map():
            #     for other in nearby:
            #         if unit.unit_type == bc.UnitType.Worker and gc.can_build(unit.id, other.id):
            #             gc.build(unit.id, other.id)
            #             print('built a factory!')
            #             # move onto the next unit
            #             continue
            #         if other.team != my_team and gc.is_attack_ready(unit.id) and gc.can_attack(unit.id, other.id):
            #             print('attacked a thing!')
            #             gc.attack(unit.id, other.id)
            #             continue

            # okay, there weren't any dudes around
            # pick a random direction:


            # or, try to build a factory:

            # and if that fails, try to move

    except Exception as e:
        print('Error:', e)
        # use this to show where the error was
        traceback.print_exc()

    # send the actions we've performed, and wait for our next turn.
    gc.next_turn()
    p_counter = utilities.pcounter_reset()
    # these lines are not strictly necessary, but it helps make the logs make more sense.
    # it forces everything we've written this turn to be written to the manager.
    sys.stdout.flush()
    sys.stderr.flush()
