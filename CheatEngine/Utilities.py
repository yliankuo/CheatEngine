import battlecode as bc


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
    def find_path(loc1, loc2, game_map):
        loc1
