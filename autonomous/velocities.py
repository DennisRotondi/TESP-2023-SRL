from math import sin, cos, pi

class Velocities():
    
    def __init__(self,default,default_angular,eps,min_distance,max_velocity_change,max_angular_velocity_change,stop_target_distance) -> None:
        self.default=default
        self.default_angular=default_angular
        self.eps=eps
        self.min_distance=min_distance
        self.max_velocity_change=max_velocity_change
        self.max_angular_velocity_change=max_angular_velocity_change
        self.stop_target_distance=stop_target_distance
        self.params_names=['depth','theta','id']
        self.current_velocity=self.default
        self.current_angular_velocity=self.default_angular

    def parse(self,depth_theta):
        depth_theta=depth_theta.split(',')
        depth_theta=[float(n) for n in depth_theta]
        depth_theta={self.params_names[i]:depth_theta[i] for i in range(len(depth_theta))}
        return depth_theta
    
    def compute_velocities(self,depth_theta):
        if isinstance(depth_theta,str):
            depth_theta=self.parse(depth_theta)
        
        if depth_theta['depth']>self.min_distance and self.current_velocity<self.default:
            self.current_velocity=min(self.current_velocity+self.max_velocity_change,self.default)
            self.current_angular_velocity=min(self.current_angular_velocity+self.max_angular_velocity_change,self.default_angular)
        elif depth_theta['depth']<self.min_distance:
            mult=(depth_theta['depth']-self.stop_target_distance*(depth_theta['id']==1))+self.eps*(depth_theta['id']!=1)
            self.current_velocity=max(self.current_velocity*mult,self.current_velocity-self.max_velocity_change)
            self.current_angular_velocity=max(self.current_angular_velocity*depth_theta['theta'],self.current_angular_velocity-self.max_angular_velocity_change)

        return str(self.current_velocity)+','+str(self.current_angular_velocity)