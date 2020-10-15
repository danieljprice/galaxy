#!/opt/local/bin/python3
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
markersize=10
maxb = 122
m1 = 1.0
m2 = 1.0

def init(rmin,e):
    x = np.zeros((maxb,3))
    v = np.zeros((maxb,3))
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
    nb = 2
    #x[0][:] = [0.,0.,0.]
    #x[1][:] = [60.,0.,0.]
    #v[0][:] = [0.,0.,0.]
    #v[1][:] = [0.,0.4,0.]
    x, v, nb = add_galaxy(nb,x[0][:],v[0][:],m1,5,0.,3.,x,v)
    return x,v,nb

def add_galaxy(nb,x0,v0,m0,nrings,theta,dr,x,v):
    for j in range(nrings):
        r = (j+1)*dr
        nphi = 12 + 6*j
        dphi = 2.*np.pi/nphi
        vphi = np.sqrt(m0/r) # keplerian rotation
        for i in range(nphi):
            phi = i*dphi
            if (nb < maxb):
               x[nb][:] = x0[:] + [r*np.cos(phi)*np.cos(theta),r*np.sin(phi),-r*np.cos(phi)*np.sin(theta)]
               v[nb][:] = v0[:] + [-vphi*np.sin(phi)*np.cos(theta),vphi*np.cos(phi),vphi*np.sin(phi)*np.sin(theta)]
               nb = nb + 1
    return x,v,nb

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
    for j in range(2,nb):
        r1, dx1 = get_sep(x[j][:],x[0][:])
        r2, dx2 = get_sep(x[j][:],x[1][:])
        a[j][:] = m1/r1**3*dx1[:] + m2/r2**3*dx2[:]
    return a

print("Welcome to the ultimate ASP2062 Galaxy simulator^TM")
print("Written by Daniel Price, 2020")

#
# set initial conditions and compute initial acceleration
#
x,v,nb = init(100.,0.5)
a = get_accel(x)
dt = 1.

#
# set up figure
#
fig = plt.figure(figsize=(12,12))
ax = plt.axes()
ax.axis('square')
ax.set_xlim(-100.,100.)
ax.set_ylim(-100.,100.)
bodies = []
#
# plot two central bodies with large marker
#
body, = ax.plot([],[],color='black',marker='o',ms=markersize)
bodies.append( body, )
body, = ax.plot([],[],color='green',marker='o',ms=markersize)
bodies.append( body, )
#
# plot other bodies with small markers, in blue
#
for j in range(nb-2):
    body, = ax.plot([],[],color='blue',marker='o',ms=markersize/10)
    bodies.append( body, )

def init_anim():
    for j in range(nb):
        bodies[j].set_data([],[])
    return

def animate(i):
    global x,v,a
    x,v,a = step(x,v,a,dt)
    for j in range(nb):
        bodies[j].set_data(x[j][0],x[j][1])
    return

# call the animator.  blit=True means only re-draw the parts that have changed.
# Note: when using the Mac OS X Backend, blit=True will not work!!
#       Need to manually set matplotlib.use('TkAgg') first....
anim = animation.FuncAnimation(fig, animate, init_func=init_anim,
                               frames=1000, interval=1, blit=False)
#anim.save('galaxies.mp4', writer="ffmpeg")
plt.show()
