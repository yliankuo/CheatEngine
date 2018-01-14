import random
import battlecode as bc


def unload_garrison(unit, gc, directions):
    # print("test")
    garrison = unit.structure_garrison()
    # print("test")
    if len(garrison) > 0:
        d = random.choice(directions)
        if gc.can_unload(unit.id, d):
            print('unloaded a knight!')
            gc.unload(unit.id, d)
    elif gc.can_produce_robot(unit.id, bc.UnitType.Knight):
        gc.produce_robot(unit.id, bc.UnitType.Knight)
        print('produced a knight!')


class Factory:
    def __init__(self):
        self

    @staticmethod
    def factory(unit, gc):
        directions = list(bc.Direction)
        unload_garrison(unit, gc, directions)
