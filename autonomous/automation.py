from math import pi
from targetApproach import TargetApproach
from velocities import Velocities

class Automation():
    def __init__(self) -> None:
        min_gap=1
        too_far=2
        fov=pi/2
        default=50
        default_angular=pi/4
        eps=0.3
        min_distance=1
        max_velocity_change=10
        max_angular_velocity_change=pi/8
        stop_target_distance=0.3
        self.target_approach=TargetApproach(min_gap,too_far,fov)
        self.velocities=Velocities(default,default_angular,eps,min_distance,max_velocity_change,max_angular_velocity_change,stop_target_distance)
    def drive(self,obstacle_string):
        target_direction=self.target_approach.compute_direction(obstacle_string)
        vw=self.velocities.compute_velocities(target_direction)
        return vw
        