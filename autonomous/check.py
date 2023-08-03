from automation import Automation

from math import pi, radians

left1=str(radians(-40))
right1=str(radians(-20))
left2=str(radians(-10))
right2=str(radians(5))
left3=str(radians(20))
right3=str(radians(50))
l1='0.1'
l2='0.3'
l3='0.2'
obst=left1+','+right1+',0.5,0;'+left2+','+right2+',0.7,0;'+left3+','+right3+',0.8,1;'
# obst=theta3+',0.8,'+l3+',1;'

auto=Automation()
vw=auto.drive(obst)
print(vw)
