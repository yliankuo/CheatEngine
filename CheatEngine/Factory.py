import random
import battlecode as bc

ranger_paths = {}
def unload_garrison(unit, gc, directions):
    # print("test")
    garrison = unit.structure_garrison()
    # print("test")
    unloaded = False
    for i in range(0, len(garrison)):
        for d in directions:
            if gc.can_unload(unit.id, d):
                gc.unload(unit.id, d)
                unloaded = True
        if unloaded:
            return True

    return False



def produce_troop(unit, gc, type):
    if gc.can_produce_robot(unit.id, type):
        gc.produce_robot(unit.id, type)
        return True
    return False


class Factory:
    def __init__(self):
        self

    @staticmethod
    def factory(unit, gc, type):
        directions = list(bc.Direction)
        if unload_garrison(unit, gc, directions):
            return "unload"
        if produce_troop(unit, gc, type):
            return "produce"
        return ""