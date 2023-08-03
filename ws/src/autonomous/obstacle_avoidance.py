from math import pi, sqrt, atan2, degrees, radians
# import copy

class ObstacleAvoidance():

    def __init__(self,min_gap,too_far,fov) -> None:
        self.min_gap=min_gap
        self.too_far=too_far
        self.fov=fov
        self.target_distance=None
        self.right_border_fov=self.fov/2
        self.left_border_fov=-self.right_border_fov
        self.obstacle_param=['left','right','depth','id']

    def parse(self,obst_string):
        obstacles=obst_string.split(';') if ';' in obst_string else [obst_string]
        obstacles=[x.split(',') for x in obstacles if len(x)>0]
        obstacles=[{self.obstacle_param[i]:float(y) for i,y in enumerate(x)} for x in obstacles]
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
        c=opposite/hypotenuse
        s=adjacent/hypotenuse
        angle=atan2(s,c)
        angle=abs(angle)
        left=obstacle['theta']-angle
        right=obstacle['theta']+angle
        left=max(self.get_left_border_fov(),left)
        right=min(self.get_right_border_fov(),right)
        return {'left':left,'right':right}
    
    def is_close_enough(self,obstacle):
        return obstacle['depth']<=self.too_far and (self.target_distance is None or obstacle['depth']<=self.target_distance)
    
    def get_borders_angles(self,borders):
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
        angles=[{'depth_left':self.too_far,'depth_right':lrs[0]['depth'],'left':self.get_left_border_fov(),'right':lrs[0]['left']}]+[{'depth_left':lrs[i-1]['depth'],'depth_right':lrs[i]['depth'],'left':lrs[i-1]['right'],'right':lrs[i]['left']} for i in range(1,len(lrs))]+[{'depth_left':lrs[-1]['depth'],'depth_right':self.too_far,'left':lrs[-1]['right'],'right':self.get_right_border_fov()}]
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
            if a['left']<0 and a['right']>0:
                if abs(a['left'])<self.min_gap/2:
                    return a['depth_left'],a['left']+self.min_gap/2
                elif a['right']<self.min_gap/2:
                    return a['depth_right'],a['right']-self.min_gap/2
                else: 
                    return min(a['depth_left'],a['depth_right']),0
        possible_angles=[vg for vg in valid_gaps]
        depth,angle=self.get_angle_from_gap(possible_angles[0])
        for pa in possible_angles[1:]:     
            d,a=self.get_angle_from_gap(pa)    
            if abs(a)<abs(angle):
                angle=a
                depth=d
        return depth,angle
    
    def get_angle_from_gap(self,gap):
        if gap['right']<0:
            return gap['depth_right'],gap['right']-self.min_gap/2
        elif gap['left']>0:
            return gap['depth_left'],gap['left']+self.min_gap/2
    
    def avoid(self,obstacles):
        if isinstance(obstacles,str):
            obstacles=self.parse(obstacles)
        obstacles=[o for o in obstacles if o['id']!=1]
        gap,angle=self.get_best_angle(obstacles)
        return str(gap)+','+str(angle)+',0'


