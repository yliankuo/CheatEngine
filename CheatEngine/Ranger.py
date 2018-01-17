import random
import battlecode as bc
from Utilities import Utilities as utilities

ranger_paths = {}
def kite(unit, gc, directions):
    team = bc.Team.Red
    loc = unit.location.map_location()
    if unit.team == team:
        team = bc.Team.Blue
    enemies = utilities.sense_nearby_units(unit.location.map_location(), 30, team, bc.UnitType, gc)
    if len(enemies) > 0:
        min_dist = 100000
        enemy = enemies[0]
        for enem in enemies:
            type = enem.unit_type
            dist = loc.distance_squared_to(enem.location.map_location())
            if not type == bc.UnitType.Worker and dist < min_dist:
                min_dist = dist
                enemy = enem
        min_dist = 0
        dir = bc.Direction.Center
        for d in directions:
            nloc = loc.add(d)
            dist = nloc.distance_squared_to(enem.location.map_location())
            if dist > min_dist  and gc.can_move(unit.id, dir):
                min_dist = dist
                dir = d
        return utilities.move(unit,gc,dir)
    return False

def attack(unit, gc):
    team = bc.Team.Red
    loc = unit.location.map_location()
    if unit.team == team:
        team = bc.Team.Blue
    enemies = utilities.sense_nearby_units(unit.location.map_location(), 50, team, bc.UnitType, gc)
    if len(enemies) > 0:
        min_dist = 100000
        enemy = unit
        for enem in enemies:
            type = enem.unit_type
            dist = loc.distance_squared_to(enem.location.map_location())
            if min_dist > 35 and type == bc.UnitType.Healer:
                enemy = enem
                break
            if not type == bc.UnitType.Worker and dist < min_dist:
                min_dist = dist
                enemy = enem
        if not enemy == unit and gc.can_attack(unit.id, enemy.id) and gc.is_attack_ready(unit.id):
            gc.attack(unit.id, enemy.id)
            print("attacked")
            return True
    return False

def hunt(unit, gc, enem, earth_map):
    enemy, dist = utilities.nearest_unit(unit,enem,gc,[])
    loc = unit.location.map_location()
    if not enemy == loc:
        if not unit.id in ranger_paths or not enemy == ranger_paths[unit.id][-1]:
            ranger_paths[unit.id]  = utilities.find_path(loc, enemy, earth_map, gc)
        if utilities.move(unit, gc, utilities.loc_to_direction(enemy, ranger_paths[unit.id][1])):
            if len(ranger_paths[unit.id]) < 2:
                ranger_paths.__delitem__(unit.id)
            else:
                (ranger_paths[unit.id]).__delitem__(1)
            return True
    return False

class Ranger:

    @staticmethod
    def ranger(unit, gc, earth_map, mars_map):
        return "skip"
        action = ""
        if(unit.location.is_in_garrison() or unit.location.is_in_space()):
            return action
        directions = bc.Direction
        kited = kite(unit, gc,directions)
        attacked = attack(unit,gc)
        if kited:
            action = action + "kited "
        if attacked:
            action = action + "attacked "
        return action

        # if not kited and not attacked:
        #     hunt(unit, gc, enem, earth_map)
        #     return "hunting"


