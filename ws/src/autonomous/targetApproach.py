from obstacle_avoidance import ObstacleAvoidance

class TargetApproach():
    def __init__(self) -> None:
        super(TargetApproach, self).__init__()
        self.obstacle_avoidance=ObstacleAvoidance()
    
    def walk(self,objs):
        objs=self.obstacle_avoidance.parse(objs)
        if len(objs)==0:
            return self.obstacle_avoidance.too_far,0,0
        target=None
        for o in objs:
            if o['id']==1:
                if target is None or o['depth']<target['depth']:
                    target=o
        if target is not None:
            self.obstacle_avoidance.target_distance=min(self.obstacle_avoidance.too_far,target['depth'])
        else:
            self.obstacle_avoidance.target_distance=None
        objs=[o for o in objs if self.obstacle_avoidance.is_close_enough(o)]
        if target is not None and len(objs)==1:
            return self.approach(target)
        else:
            return self.obstacle_avoidance.avoid(objs)

    def approach(self,target):
        gap=target['right']-target['left']
        return str(target['depth'])+','+str(gap/2)+',1'
