import random
import battlecode as bc
from Utilities import Utilities as utilities

worker_paths = {}

def replicate(gc, unit, directions):
    for d in directions:
        if gc.can_replicate(unit.id, d):
            gc.replicate(unit.id, d)
            return True
    return False


def build_blueprint(unit, gc, nearby_units):
    for other in nearby_units:
        if gc.can_build(unit.id, other.id):
            gc.build(unit.id, other.id)
            return True
    return False


def place_factory(unit, gc, directions):
    for d in directions:
        tloc = unit.location.map_location().add(d)
        type = bc.UnitType.Factory
        if gc.karbonite() > type.blueprint_cost() and gc.can_blueprint(unit.id, bc.UnitType.Factory, d) and gc.karbonite_at(tloc) == 0 and len(gc.sense_nearby_units_by_type(tloc, 2, type)) == 0:
            gc.blueprint(unit.id, type, d)
            return True
    return False


def find_karbonite(unit, gc, earth_map, mars_map, initialkarbonite):
    loc = unit.location
    if loc.is_on_planet(bc.Planet.Earth):
        karb, dist = utilities.nearest_karbonite(unit, initialkarbonite, gc)
        if not unit.id in worker_paths or not karb == worker_paths[unit.id][-1]:
            worker_paths[unit.id]  = utilities.find_path(loc.map_location(), karb, earth_map, gc)
        if utilities.move(unit, gc, utilities.loc_to_direction(loc.map_location(), worker_paths[unit.id][1])):
            if len(worker_paths[unit.id]) < 2:
                worker_paths.__delitem__(unit.id)
            else:
                (worker_paths[unit.id]).__delitem__(1)
            return True
    return False


def harvest( unit, gc, directions):
    for dir in directions:
        if gc.can_harvest(unit.id, dir):
            gc.harvest(unit.id, dir)
            return True
    return False

class Worker:
    def __init__(self):
        self

    @staticmethod
    def worker(unit, gc, earth_map, mars_map, initialkarbonite, worker_limit):
        # print("unit: " + str(unit.id))
        utilities.try_add_friendly_units(unit)
        num_workers = len(utilities.get_friendly_units(bc.UnitType.Worker))
        nearby = gc.sense_nearby_units(unit.location.map_location(), 2)
        directions = list(bc.Direction)
        if num_workers < worker_limit:
            if replicate(gc, unit, directions):
                return "replicate"
        if build_blueprint(unit, gc, nearby):
            return "build"
        if harvest(unit,gc, directions):
            return "harvest"
        if place_factory(unit, gc, directions):
            return "place"
        if find_karbonite(unit, gc, earth_map, mars_map, initialkarbonite):
            return "find_karbonite"
        return ""
#





