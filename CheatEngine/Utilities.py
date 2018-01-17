import battlecode as bc
import heapq
import Utilities as utilities
import math as math

sortedf = {}
enem = []
sortede = {}

def neighbors(current, gamemap, gc):
    nearby = []
    for i in range(current.x - 1, current.x + 2):
        for j in range(current.y - 1, current.y + 2):
            tloc = bc.MapLocation(gc.planet(), i, j)
            if not tloc == current and gamemap.on_map(tloc):
                nearby.append(tloc)
    return nearby


def get_node(array):
    fkey = next(iter(array[0]))
    fprior = array[0][fkey]
    ind = 0
    for i in range(0, len(array)):
        tkey = next(iter(array[i]))
        tprior = array[i][tkey]
        if tprior < fprior:
            fkey = tkey
            fprior = tprior
    return bc.MapLocation.from_json(fkey), ind


# def heappush(elements, priority, item):
#     i = 0
#     while(i < len(elements) and elements[i][0] < priority):
#         i = i + 1
#     # if(i < len(elements)):
#     #     elements.insert(i, (priority,item))
#     # else:
#     elements.append((priority,item))
# class PriorityQueue:
#     def __init__(self):
#         self.elements = []
#
#     def empty(self):
#         return len(self.elements) == 0
#
#     def put(self, item, priority):
#         print(priority)
#         print(item)
#         heappush(self.elements, priority, item)
#
#     def get(self):
#         return self.elements[0][1]


def cost(loc, game_map, gc):
    if not game_map.is_passable_terrain_at(loc):
        return 10000
    if gc.has_unit_at_location(loc):
        return 10000
    return 1


def heuristic(node, goal):
    p = 1.001
    dx = abs(node.x - goal.x)
    dy = abs(node.y - goal.y)
    return (dx + dy - 1 * min(dx, dy)) * p


class Utilities:

    def __init__(self):
        self



    @staticmethod
    def sense_nearby_units(loc, radius, team, types, gc):
        units = []
        for i in range(loc.x - math.floor(math.sqrt(radius)),loc.x + math.floor(math.sqrt(radius))):
            for j in range(loc.y - math.floor(math.sqrt(radius)), loc.y + math.floor(math.sqrt(radius))):
                loc = bc.MapLocation(gc.planet(),i,j)
                if gc.has_unit_at_location(loc):
                    unit = gc.sense_unit_at_location(loc)
                    if unit.team == team and unit.unit_type in types:
                        units.append(unit)
        return units

    @staticmethod
    def pcounter_reset():
        pcount = {}
        for unit in bc.UnitType:
            pcount[unit] = 0
        return pcount

    @staticmethod
    def get_friendly_units(type):
        tlist = []
        if type in sortedf:
            tlist = sortedf[type]
        return tlist

    @staticmethod
    def try_add_friendly_units(unit):
        u_type = unit.unit_type
        u_side = unit.team
        if not u_type in sortedf:
            sortedf[u_type] = []
        if not unit in sortedf[u_type]:
            sortedf[u_type].append(unit.id)


    # @staticmethod
    # def sort_units(unit_list, sortedf, sortede, enem, gc):
    #     for unit in unit_list:
    #         u_type = unit.unit_type
    #         u_side = unit.team
    #         if not gc.team() == u_side:
    #             if not u_side in sortede:
    #                 sortede[u_type] = []
    #             sortede[u_type].append(unit.id)
    #             if not unit.id in enem:
    #                 enem.append(unit.id)
    #         else:
    #             if not u_type in sortedf:
    #                 sortedf[u_type] = []
    #             sortedf[u_type].append(unit.id)
    #             # print("append")
    #     return sortedf, sortede, enem

    # @staticmethod
    # def clean_units(sortedf, gc):
    #     for key in sortedf:
    #         for id in sortedf[key]:
    #             try:
    #                 gc.unit(id)
    #             except Exception as e:
    #                 sortedf[key].remove(id)
    #     return sortedf

    @staticmethod
    def loc_to_direction(loc1, loc2):
        if loc1.add(bc.Direction.North) == loc2:
            return bc.Direction.North
        if loc1.add(bc.Direction.East) == loc2:
            return bc.Direction.East
        if loc1.add(bc.Direction.South) == loc2:
            return bc.Direction.South
        if loc1.add(bc.Direction.West) == loc2:
            return bc.Direction.West
        if loc1.add(bc.Direction.Northeast) == loc2:
            return bc.Direction.Northeast
        if loc1.add(bc.Direction.Northwest) == loc2:
            return bc.Direction.Northwest
        if loc1.add(bc.Direction.Southeast) == loc2:
            return bc.Direction.Southeast
        if loc1.add(bc.Direction.Southwest) == loc2:
            return bc.Direction.Southwest
        print("could not find direction")
        return bc.Direction.Center


    @staticmethod
    def neighbors(current, gamemap, gc):
        nearby = []
        for i in range(current.x - 1, current.x + 1):
            for j in range(current.y - 1, current.y + 1):
                if not i == current.x and not j == current.y and gamemap.on_map(bc.MapLocation(gc.planet(), i, j)):
                    nearby.append(bc.MapLocation(gc.planet(), i, j))
        return nearby

    @staticmethod
    def initial_karbonite(tmap):
        karb_dep = []
        for i in range(0, tmap.width):
            for j in range(0, tmap.height):
                loc = bc.MapLocation(bc.Planet.Earth,i,j)
                if tmap.initial_karbonite_at(loc):
                    karb_dep.append(loc)
        return karb_dep


    @staticmethod
    def move(unit, gc, direction):
        if gc.is_move_ready(unit.id) and gc.can_move(unit.id, direction):
            gc.move_robot(unit.id, direction)
            # print("Moving")
            return True
        return False

    # @staticmethod
    # def find_path(loc1, loc2, game_map, gc):
    #     frontier = []
    #     frontier.append(loc1)
    #     came_from = {}
    #     while not len(frontier) == 0:
    #         current = frontier[0]
    #         frontier.__delitem__(0)
    #         if(current == loc2):
    #             break
    #         for next in neighbors(current,game_map,gc):
    #             if next.to_json() not in came_from:
    #                 frontier.append(next)
    #                 came_from[next.to_json()] = current
    #     path = []
    #     if len(frontier) == 0:
    #         path.append(loc1)
    #         path.append(loc1)
    #         return path
    #     current = loc2
    #     # print(came_from.keys())
    #     # print("loc1: " + loc1.to_json())
    #     # print("loc2: " + loc2.to_json())
    #     while current.to_json() != loc1.to_json():
    #         # print("current" + current.to_json())
    #         path.append(current)
    #         if current.to_json() not in came_from:
    #             path = []
    #             path.append(loc1)
    #             break
    #         current = came_from[current.to_json()]
    #
    #     path.append(loc1)  # optional
    #     if len(path) == 1:
    #         path.append(loc1)
    #     path.reverse()  # optional
    #     # print('end')
    #     return path


    # A* TOO SLOW
    @staticmethod
    def find_path(loc1, loc2, game_map, gc):
        prev = loc1
        frontier = []
        frontier.append({loc1.to_json() : 0})
        came_from = {}
        cost_so_far = {}
        came_from[loc1.to_json()] = None
        cost_so_far[loc1.to_json()] = 0
        while not len(frontier) == 0:
            current, ind = get_node(frontier)
            frontier.__delitem__(ind)
            if current == loc2:
                if current.to_json() not in came_from:
                    came_from[current.to_json()] = prev
                # print("broken")
                # print(current.to_json())
                break
            for next in neighbors(current, game_map, gc):
                new_cost = cost_so_far[current.to_json()] + cost(next, game_map, gc)
                if (next.to_json() not in cost_so_far or new_cost < cost_so_far[next.to_json()] or next.to_json() not in came_from) and new_cost < 9000:
                    cost_so_far[next.to_json()] = new_cost
                    priority = new_cost + heuristic(loc2, next)
                    frontier.append({next.to_json() : priority})
                    came_from[next.to_json()] = current
                # print(cost_so_far.keys())
            prev = current
        path = []
        if len(frontier) == 0:
            path.append(loc1)
            path.append(loc1)
            return path
        current = loc2
        # print(came_from.keys())
        # print("loc1: " + loc1.to_json())
        # print("loc2: " + loc2.to_json())
        while current.to_json() != loc1.to_json():
            # print("current" + current.to_json())
            path.append(current)
            if current.to_json() not in came_from:
                path = []
                path.append(loc1)
                break
            current = came_from[current.to_json()]

        path.append(loc1)  # optional
        if len(path) == 1:
            path.append(loc1)
        path.reverse()  # optional
        # print('end')
        return path

    @staticmethod
    def nearest_karbonite(unit, karbonites, gc):
        min_dist = 100000
        result = unit.location.map_location()
        for loc in karbonites:
            dist = unit.location.map_location().distance_squared_to(loc)
            if dist < min_dist:
                if (gc.can_sense_location(loc) and gc.karbonite_at(loc) == 0) or gc.has_unit_at_location(loc):
                    continue
                min_dist = dist
                result = loc
        return result, min_dist

    @staticmethod
    def nearest_unit(unit, unit_list, gc, avoid):
        min_dist = 100000
        result = unit.location.map_location()
        for un in unit_list:
            try:
                u = gc.unit(un)
            except Exception as e:
                continue
            dist = unit.location.map_location().distance_squared_to(u.location.map_location())
            if not u.unit_type in avoid and dist < min_dist:
                min_dist = dist
                result = u
        return result.location.map_location(), min_dist

    # @staticmethod
    # def nearest_type(gc, unit, type, distance):


