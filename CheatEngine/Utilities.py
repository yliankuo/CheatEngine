import battlecode as bc
import heapq


def get_direction(loc1, loc2):


class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]


def neighbors(current, gamemap, gc):
    nearby = []
    for i in range(current.x - 1, current.x + 1):
        for j in range(current.y - 1, current.y -1):
            if not i == current.x and not j == current.y and gamemap.on_map(bc.MapLocation(gc.planet(), i, j)):
                nearby.append(bc.MapLocation(gc.planet, i, j))
    return nearby


def cost(loc, game_map):
    if not game_map.is_passable_terrain_at(loc):
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
    def move(unit, gc, direction):
        if gc.is_move_ready(unit.id) and gc.can_move(unit.id, direction):
            gc.move_robot(unit.id, direction)

    @staticmethod
    def initial_karbonite_locations(gc):
        # for
        gc

    @staticmethod
    def find_path(loc1, loc2, game_map, gc):
        frontier = PriorityQueue()
        frontier.put(loc1,0)
        came_from = {}
        cost_so_far = {}
        came_from[loc1] = None
        cost_so_far[loc1] = 0

        while not frontier.empty():
            current = frontier.get()

            if current == loc2 :
                break
            for next in neighbors(current,game_map,gc):
                new_cost = cost_so_far[current] + cost(next)
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + heuristic(loc2, next)
                    frontier.put(next, priority)
                    came_from[next] = current
        return came_from, cost_so_far

    @staticmethod
    def nearest_type(unit, type, distance):
        nearest_dist = 10000000
        for i in range(unit.location.map_location().x - distance, unit.location.map_location().x + distance):
            for j in range(unit.location.map_location().y - distance, unit.location.map_location().y + distance):



