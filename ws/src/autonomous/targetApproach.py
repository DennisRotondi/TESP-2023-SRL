from obstacle_avoidance import ObstacleAvoidance
from math import radians

class TargetApproach():
    def __init__(self) -> None:
        super(TargetApproach, self).__init__()
        self.obstacle_avoidance=ObstacleAvoidance()
    
    def walk(self,objs):
        objs=self.obstacle_avoidance.parse(objs)
        print(objs)
        target=None
        for o in objs:
            if o['isTarget']:
                target=o
        print(target)
        if target is not None:
            self.obstacle_avoidance.target_distance=target['depth']
        else:
            self.obstacle_avoidance.target_distance=None
        objs=[o for o in objs if self.obstacle_avoidance.is_close_enough(o)]
        print(objs)
        if target is not None and len(objs)==1:
            return self.approach(target)
        else:
            return self.obstacle_avoidance.avoid(objs)

    def approach(self,target):
        lr=self.obstacle_avoidance.get_border_angles(target)
        print(str(lr['right']-lr['left'])+','+str(target['theta']))
        target['theta']=radians(target['theta'])
        return str(lr['right']-lr['left'])+','+str(target['theta'])
