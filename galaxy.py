#!/opt/local/bin/python3
import numpy as np
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
    print("got dx = ",dx)
    r = np.sqrt(np.dot(dx,dx))
    print("got dx = ",dx," dr = ",r)
    return r,dx

def get_accel(x):
    a = np.zeros((nb,3))
    r, dx = get_sep(x[0][:],x[1][:])
    a[0][:] = m2/r**3*dx[:]
    a[1][:] = -m1/r**3*dx[:]
    return a

x,v = init(25.,0.8)
#print("x=",x,' v=',v)

#r, dx = getr(x[:][0],x[:][1])
#print("r=",r,"dx=",dx)

print("# x  y  z")
print("%f %f %f" % (x[0][0],x[0][1],x[0][2]))

a = get_accel(x)
dt = 5.
import matplotlib.pyplot as plt
for i in range(0,500):
    print(i," pos body1",x[0][:])
    print(i," pos body2",x[1][:])
    print(i," v body1",v[0][:])
    print(i," v body2",v[1][:])
    print(i," a body1",a[0][:])
    print(i," a body2",a[1][:])

    x,v,a = step(x,v,a,dt)
    print(i," pos body1",x[0][:])
    print(i," pos body2",x[1][:])
    plt.xlim(-200.,200.)
    plt.ylim(-200.,200.)
    plt.scatter(x[:][0],x[:][1])
    print("%f %f %f" % (x[0][0],x[0][1],x[0][2]))

plt.show()

# call the animator.  blit=True means only re-draw the parts that have changed.
# Note: when using the Mac OS X Backend, blit=True will not work!!
#       Need to manually set matplotlib.use('TkAgg') first....
#anim = animation.FuncAnimation(fig, animate, init_func=init,
#                               frames=n_frames, interval=1, blit=False)

#print ("done")
