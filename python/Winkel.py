bogenm=input("Geben Sie ein Bogenmaß ein!")
from math import pi
winkel=float(bogenm)*180/pi
while winkel>360:
    winkel-=360
print("Der Winkel beträgt", winkel,"°")
