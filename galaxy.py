#!/opt/local/bin/python3
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
markersize=50

nb = 2
m1 = 1.0
m2 = 1.0

def init(rmin,e):
    x = np.zeros((nb,3))
    v = np.zeros((nb,3))
    mtot = m1 + m2
    #e = 0.8
    #rmin = 25.
    a = rmin*(1. - e)
    r = a*(1. + e)
    v0 = np.sqrt(a*(1. - e**2)*mtot)/r
    x[0][:] = [-m2/mtot*r,0.,0.]
    x[1][:] = [m1/mtot*r,0.,0.]
    v[0][:] = [0.,-m2/mtot*v0,0.]
    v[1][:] = [0.,m1/mtot*v0,0.]
#    x[0][:] = [0.,0.,0.]
#    x[1][:] = [60.,0.,0.]
#    v[0][:] = [0.,0.,0.]
#    v[1][:] = [0.,0.4,0.]
    return x,v

def add_galaxy(x,v,nrings,theta,dr):
    for j in range(1,nrings):
        r = j*dr
        nphi = 12 + 6*(j-1)
        dphi = 2.*np.pi/nphi
        for i in range(1,nphi):
            phi = (i-1)*dphi
            nb = nb + 1
            x[:][nb] = x0[:] + [ri*np.cos(phi)*np.cos(theta),ri]

def step(x,v,a,dt):
    v = v + 0.5*dt*a
    x = x + dt*v
    a = get_accel(x)
    v = v + 0.5*dt*a
    return(x,v,a)

def get_sep(x1,x2):
    dx = x2 - x1
    r = np.sqrt(np.dot(dx,dx))
    return r,dx

def get_accel(x):
    a = np.zeros((nb,3))
    r, dx = get_sep(x[0][:],x[1][:])
    a[0][:] = m2/r**3*dx[:]
    a[1][:] = -m1/r**3*dx[:]
    return a

fig = plt.figure()
ax = plt.axes()
ax.set_xlim(xmax=100)
ax.axis('square')
body1, = ax.plot([],[],color='black',marker='o',ms=markersize)
body2, = ax.plot([],[],color='green',marker='o',ms=markersize)

x,v = init(100.,0.5)
a = get_accel(x)
dt = 5.

def init_anim():
    body1.set_data([],[])
    return body1,

def animate(i):
    x,v,a = step(x,v,a,dt)
    body1.set_data(x[0][0],x[0][1])
    body2.set_data(x[1][0],x[1][1])
    return body1,

#for i in range(0,500):
#    plt.xlim(-50.,50.)
#    plt.ylim(-50.,50.)
#    plt.gca().set_aspect('equal', adjustable='box')
#    for body in range(0,nb):
#        plt.scatter(x[body][0],x[body][1])


# call the animator.  blit=True means only re-draw the parts that have changed.
# Note: when using the Mac OS X Backend, blit=True will not work!!
#       Need to manually set matplotlib.use('TkAgg') first....
anim = animation.FuncAnimation(fig, animate, init_func=init_anim,
                               frames=100, interval=1, blit=False)
plt.show()

#print ("done")
