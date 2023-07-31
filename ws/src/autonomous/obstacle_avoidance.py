from math import pi, sqrt, atan2
# import copy

class ObstacleAvoidance():

    def __init__(self) -> None:
        self.min_gap=0.1
        self.fov=pi/2
        self.too_far=1
        self.target_distance=None
        self.right_border_fov=self.fov/2
        self.left_border_fov=-self.right_border_fov
        self.obstacle_param=['theta','depth','length','isTarget']

    def parse(self,obst_string):
        obstacles=obst_string.split(';') if ';' in obst_string else [obst_string]
        obstacles=[x.split(',') for x in obstacles if len(x)>0]
        obstacles=[{self.obstacle_param[i]:float(y) if i<len(x)-1 else y.lower()=='true' for i,y in enumerate(x)} for x in obstacles]
        return obstacles
    
    def get_left_border_fov(self):
        return self.left_border_fov
    
    def get_right_border_fov(self):
        return self.right_border_fov
        
    def get_side_length(self,obstacle):
        return obstacle['length']/2

    def get_border_angles(self,obstacle):
        opposite=obstacle['depth']
        adjacent=self.get_side_length(obstacle)
        hypotenuse=sqrt(adjacent**2+opposite**2)
        s=opposite/hypotenuse
        c=adjacent/hypotenuse
        angle=atan2(s,c)
        angle=(pi/2)-angle
        angle=abs(angle)
        left=obstacle['theta']-angle
        right=obstacle['theta']+angle
        left=max(self.get_left_border_fov(),left)
        right=min(self.get_right_border_fov(),right)
        return {'left':left,'right':right}
    
    def is_close_enough(self,obstacle):
        return obstacle['depth']<=self.too_far and (self.target_distance is None or obstacle['depth']<=self.target_distance)
    
    def get_borders_angles(self,obstacles):
        borders=[self.get_border_angles(o) for o in obstacles if self.is_close_enough(o)]
        adjusted=[borders[0]]
        for b in borders[1:]:
            if b['left']<adjusted[-1]['right']:
                adjusted[-1]['right']=b['right']
            else:
                adjusted.append(b)
        return adjusted

    def get_gap_angles(self,obstacles):
        if len(obstacles)==0: return [{'left':self.get_left_border_fov(),'right':self.get_right_border_fov(),'gap_angle':self.fov}]
        lrs=self.get_borders_angles(obstacles)
        angles=[{'left':self.get_left_border_fov(),'right':lrs[0]['left']}]+[{'left':lrs[i-1]['right'],'right':lrs[i]['left']} for i in range(1,len(lrs))]+[{'left':lrs[-1]['right'],'right':self.get_right_border_fov()}]
        if angles[0]['right']==self.left_border_fov:
            angles=angles[1:]
        if angles[-1]['left']==self.right_border_fov:
            angles=angles[:-1]
        for i,a in enumerate(angles):
            angles[i].update({'gap_angle':a['right']-a['left']})
        return angles

    def get_best_angle(self,obstacles):
        angles=self.get_gap_angles(obstacles)
        valid_gaps=[a for a in angles if abs(a['gap_angle'])>self.min_gap]
        for a in valid_gaps:
            if a['left']<0 and a['right']>0 and abs(a['gap_angle'])>self.min_gap:
                if abs(a['left'])<self.min_gap/2:
                    return abs(a['gap_angle']),-self.min_gap
                elif a['right']<self.min_gap:
                    return abs(a['gap_angle']),self.min_gap
                else: return abs(a['gap_angle']),0
        possible_angles=[vg for vg in valid_gaps]
        angle=self.get_angle_from_gap(possible_angles[0]['left'],possible_angles[0]['right'])
        gap_angle=possible_angles[0]['gap_angle']
        for pa in possible_angles[1:]:     
            a=self.get_angle_from_gap(pa['left'],pa['right'])    
            if abs(a)<abs(angle):
                angle=a
                gap_angle=pa['gap_angle']
        return gap_angle,angle
    
    def get_angle_from_gap(self,left,right):
        if right<0:
            return right-self.min_gap/2
        elif left>0:
            return left+self.min_gap/2
        else:
            return (right-left)/2
    
    def avoid(self,obstacles):
        if isinstance(obstacles,str):
            obstacles=self.parse(obstacles)
        obstacles=[o for o in obstacles if not o['isTarget']]
        gap,angle=self.get_best_angle(obstacles)
        return str(gap)+','+str(angle)

