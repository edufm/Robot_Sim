import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

fig, ax = plt.subplots(subplot_kw=dict(projection="3d"))

x1 = 0
y1 = 0
z1 = 0
angx1 = 0
angy1 = 0
angz1 = 0

x2 = 0
y2 = 0
z2 = 0
angx2 = np.sin(np.radians(90))
angy2 = 0
angz2 = 0

frames = 100

def get_arrow(x, y, z, theta_x, theta_y, theta_z):

    u = np.sin(theta_x) + x
    v = np.sin(theta_y) + y
    w = np.cos(theta_z) + z

    return x,y,z,u,v,w

quiver_x = ax.quiver(*get_arrow(x1, y1, z1, angx1, angy1, angz1))
quiver_y = ax.quiver(*get_arrow(x1, y1, z1, angx1, angy1+np.pi/2, angz1))
quiver_z = ax.quiver(*get_arrow(x1, y1, z1, angx1, angy1, angz1+np.pi/2))

ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_zlim(-2, 2)

def update(vector):
    global quiver_x
    global quiver_y
    global quiver_z

    quiver_x.remove()
    quiver_y.remove()
    quiver_z.remove()

    vector_x = vector.copy()
    vector_y = vector.copy()
    vector_z = vector.copy()
    vector_y[4] += np.pi/2
    vector_z[5] += np.pi/2

    quiver_x = ax.quiver(*get_arrow(*vector_x))
    quiver_y = ax.quiver(*get_arrow(*vector_y))
    quiver_z = ax.quiver(*get_arrow(*vector_z))

moves = [np.linspace(x1, x2, frames),
         np.linspace(y1, y2, frames),
         np.linspace(z1, z2, frames),
         np.linspace(angx1, angx2, frames),
         np.linspace(angy1, angy2, frames),
         np.linspace(angz1, angz2, frames)]
moves = np.transpose(np.array(moves))

ani = FuncAnimation(fig, update, frames=moves, interval=50)
plt.show()