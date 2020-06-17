from robot_sim import CordSys
from robot_sim.cordinates import plot

a = CordSys(0, 0, 0, 0, 0, 0)
b = CordSys(0, 5, 0, 30, 0, 0)
c = CordSys(0, 7, 0, 0, 30, 0)

plot([a, b, c])