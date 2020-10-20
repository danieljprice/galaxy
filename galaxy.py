#!/usr/bin/env python3
"""
  A simple galaxy simulator
  (c) 2020 Daniel Price for ASP2062
  Monash University, Melbourne, Australia

  The idea is similar to the "galaxies.exe" file distributed
  with Carroll & Ostlie, Introduction to Modern Astrophysics

  Original reference:
    Toomre & Toomre (1972) "Galactic Bridges and Tails", ApJ, 178, 623-666
    http://adsabs.harvard.edu/abs/1972ApJ...178..623T
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
#
# Parameters for the simulation
#
m1 = 5.0
m2 = 0.25*m1
x2 = [30.,-30.,0.]
v2 = [0.,0.34,0.34]
nrings = 6
nsteps = 540
x1 = [0.,0.,0.]
v1 = [0.,0.,0.]
dt = 1.
dr = 15./(nrings-1) # spacing between rings
markersize=10
#
# initialise various quantities
#
time = 0.
xyplot = []
xzplot = []
maxb = 2 + 12*nrings + 6*sum(range(nrings)) # max number of bodies

def init():
    """
      Set up the initial conditions for the simulation
    """
    x = np.zeros((maxb,3))
    v = np.zeros((maxb,3))
    mtot = m1 + m2
    nb = 2
    x[0][:] = x1
    x[1][:] = x2
    v[0][:] = v1
    v[1][:] = v2
    x, v, nb = add_galaxy(nb,x[0][:],v[0][:],m1,nrings,0.,dr,x,v)
    a = get_accel(x,nb)
    return (x,v,a,nb)

def add_galaxy(nb,x0,v0,m0,nrings,theta,dr,x,v):
    """
      Add test particles around a body in a series of rings orbiting the body
      nb refers to the number of bodies in total

      INPUTS:
         nrings : number of rings to add
         theta  : inclination angle for the disc of material
         dr     : separation between rings
         x0, v0 : initial position and velocity of central body (as vectors)
         m0     : mass of central body
      OUTPUTS:
         nb     : number of bodies
         x, v   : position and velocity arrays for all bodies
    """
    for j in range(nrings):
        r = 5. + j*dr
        nphi = 12 + 6*j # see also formula for maxb
        dphi = 2.*np.pi/nphi
        vphi = np.sqrt(m0/r)  # assume Keplerian rotation
        for i in range(nphi):
            phi = i*dphi
            if (nb < maxb):
               x[nb][:] = x0[:] + [r*np.cos(phi)*np.cos(theta),r*np.sin(phi),-r*np.cos(phi)*np.sin(theta)]
               v[nb][:] = v0[:] + [-vphi*np.sin(phi)*np.cos(theta),vphi*np.cos(phi),vphi*np.sin(phi)*np.sin(theta)]
               nb = nb + 1
    return x,v,nb

def step(x,v,a,dt):
    """
      Solve ODEs using Leapfrog integrator in Velocity-Verlet form
      https://en.wikipedia.org/wiki/Leapfrog_integration
      https://en.wikipedia.org/wiki/Verlet_integration
    """
    v = v + 0.5*dt*a
    x = x + dt*v
    a = get_accel(x,nb)
    v = v + 0.5*dt*a
    return(x,v,a)

def get_sep(x1,x2):
    """
      Function to return the separation between two vectors
      Both as a vector (dx) and its magnitude (r)
    """
    dx = x2 - x1
    r = np.sqrt(np.dot(dx,dx))
    return r,dx

def get_accel(x,nb):
    """
      Compute the acceleration on all bodies given their positions
      Input is current position of all bodies, output
      is the acceleration of all bodies at the same instance
    """
    a = np.zeros((maxb,3))
    r, dx = get_sep(x[0][:],x[1][:]) # separation between 1 and 2
    a[0][:] = m2/r**3*dx[:]    # acceleration on body 1
    a[1][:] = -m1/r**3*dx[:]   # acceleration on body 2
    for j in range(2,nb):
        # acceleration on test particles ONLY due to bodies 1 and 2
        # i.e. they do not feel each other
        r1, dx1 = get_sep(x[j][:],x[0][:]) # test particle and body 1
        r2, dx2 = get_sep(x[j][:],x[1][:]) # test particle and body 2
        a[j][:] = m1/r1**3*dx1[:] + m2/r2**3*dx2[:]
    return a

def init_plotting():
    """
       initialise the figure for plotting
    """
    global time_text
    fig, (ax1, ax2) = plt.subplots(1,2,figsize=(12,6))
    ax1.axis('square') # use square aspect ratio
    ax1.set_xlim(-100.,100.)  # x limits
    ax1.set_ylim(-100.,100.)  # y limits
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')
    ax2.axis('square')  # same settings for x-z plot
    ax2.set_xlim(-100.,100.)
    ax2.set_ylim(-100.,100.)
    ax2.set_xlabel('x')
    ax2.set_ylabel('z')
    #
    # add text to print the time
    #
    time_text = ax1.text(-95.,85.,'',fontsize=15)
    #
    # plot two central bodies with large marker
    #
    colours = ['black','green']
    for j in range(2):
        xy, = ax1.plot([],[],color=colours[j],marker='o',ms=markersize)
        xz, = ax2.plot([],[],color=colours[j],marker='o',ms=markersize)
        xyplot.append( xy, )
        xzplot.append( xz, )
    #
    # plot other bodies with small markers, in blue
    #
    for j in range(nb-2):
        xy, = ax1.plot([],[],color='blue',marker='o',ms=markersize/10)
        xz, = ax2.plot([],[],color='blue',marker='o',ms=markersize/10)
        xyplot.append( xy, )
        xzplot.append( xz, )
    return fig

def init_anim():
    """
       initialise the animation for each frame, i.e. delete old positions
    """
    for j in range(nb):
        xyplot[j].set_data([],[])
        xzplot[j].set_data([],[])
    return

def animate(i):
    """
       function called by each iteration of the animator
       steps forward in time by dt and updates positions on the plot
    """
    global x,v,a,time
    # step forwards in time by dt
    time += dt
    x,v,a = step(x,v,a,dt)
    # update body positions on the plot
    for j in range(nb):
        xyplot[j].set_data(x[j][0],x[j][1])
        xzplot[j].set_data(x[j][0],x[j][2])
    time_text.set_text("t="+str(time))
    return

print("Welcome to The Ultimate Galaxy Simulator^TM")
print("Written by Daniel Price, Monash University, 2020")

#
# set initial conditions and compute initial acceleration
#
x,v,a,nb = init()
fig = init_plotting()

# call the animator.  blit=True means only re-draw the parts that have changed.
# Note: when using the Mac OS X Backend, blit=True will not work!!
#       Need to manually set matplotlib.use('TkAgg') first....
anim = animation.FuncAnimation(fig, animate, init_func=init_anim, repeat=False,
                               frames=nsteps, interval=1, blit=False)

#
# uncomment the following line to save your animation as an mp4
# you will need to have ffmpeg installed, e.g. using "sudo apt install ffmpeg"
#
#anim.save('galaxies.mp4', writer="ffmpeg")
#anim.save('galaxies.gif', writer="imagemagick")
plt.show()
