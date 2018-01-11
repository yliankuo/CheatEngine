import random
import battlecode as bc


class Worker:
    def __init__(self):
        self

    @staticmethod
    def build_blueprint(unit, gc, nearby_units):
        for other in nearby_units:
            if gc.can_build(unit.id, other.id):
                gc.build(unit.id, other.id)
                print('built ' + str(other.unit_type))

    @staticmethod
    def place_factory(unit, gc, directions):
        d = random.choice(directions)
        if gc.karbonite() > bc.UnitType.Factory.blueprint_cost() and gc.can_blueprint(unit.id, bc.UnitType.Factory, d):
            gc.blueprint(unit.id, bc.UnitType.Factory, d)
            print('placed blueprint factory')

    @staticmethod
    def replicate(gc, unit, directions):
        d = random.choice(directions)
        if gc.can_replicate(unit.id, d):
            gc.replicate(unit.id, d)
            print("replicated")