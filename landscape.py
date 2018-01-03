#!/usr/bin/python -u
"""
Fitness landscape for Innatrix Evolution Demonstration
(From: http://matplotlib.org/examples/pylab_examples/shading_example.html
"""

from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
import random, glob, os, subprocess
from shutil import copyfile
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import LightSource

count = 0

def movie_file(name) :
    type = 'png'
    frameLocation = "/tmp/gifmovie/"
    out = 'evolution.gif'
    numstart = len(frameLocation)
    next_file = frameLocation + '00000m.' + type
    numend = numstart + 5
    imfiles = glob.glob(frameLocation+'*m.'+type)
    if (len(imfiles)>0) :
        last_file = max(imfiles, key=os.path.getctime)
        seq = int(last_file[numstart:numend]) + 1
        next_file =  last_file[:-10]+"{0:0>5}".format(seq)+"m."+type
    copyfile(name, next_file)
    print("Saved frame: " + next_file)
    if (count % 10 == 0) :
	cmd=['convert','-delay','20','-loop','0','0*.png',out]
        subprocess.call(cmd,cwd=frameLocation)
        print("Saved movie: " + frameLocation + out)


# Test data: Matlab `peaks()`
x, y = np.mgrid[-3:3:150j,-3:3:150j]
z =  3*(1 - x)**2 * np.exp(-x**2 - (y + 1)**2) \
   - 10*(x/5 - x**3 - y**5)*np.exp(-x**2 - y**2) \
   - 1./3*np.exp(-(x + 1)**2 - y**2) 

# Prepare starting locations
n = 50
vx = [0]*n
vy = [0]*n
vz = [0]*n
rx = 0
ry = 0
random.seed(0)  # seed for reproducible 'random' numbers
for i in range(n) :
    rx = random.randrange(0,150)
    ry = random.randrange(0,150)
    vx[i] = x[rx][0]
    vy[i] = y[0][ry]

ls = LightSource(azdeg=0, altdeg=65)
rgb = ls.shade(z, plt.cm.RdYlBu)

elevation = 26
edir = True
azimuth = 11
adir = True
while True :
    fig = plt.figure(1)
    ax = fig.gca(projection='3d')
    plt.hold(True)
    ax.grid(False) # Hide grid lines
    ax.axis('off') # OR #ax.set_xticks([])#ax.set_yticks([])#ax.set_zticks([])
    count = count + 1
    if (count % 4 == 0) :
        if (edir) :
            if (elevation < 30) :
                elevation = elevation + 1
            else :
                edir = not edir
        else :
            if (elevation > 10) :
                elevation = elevation - 1
            else :
                edir = not edir
        if (adir) :
            if (azimuth < 40) :
                azimuth = azimuth + 1
            else :
                adir = not adir
        else :
            if (azimuth > 10) :
                azimuth = azimuth - 1
            else :
                adir = not adir
    ax.view_init(elevation,azimuth)
    ax.dist = 4
    for i in range(n) : # Crawl randomly ->(100,100) before assigning vz
        if (rx < 100) :
            dx = random.randint(-1,2)
        else :
            dx = random.randint(-2,1)
        if (ry < 100) :
            dy = random.randint(-1,2)
        else :
            dy = random.randint(-2,1)
        rx = rx + dx
        ry = ry + dy
        vx[i] = x[rx][0]
        vy[i] = y[0][ry]
        vz[i] = z[rx][ry] + 1.0

    ax.scatter(np.asarray(vx), np.asarray(vy), np.asarray(vz),
               c='r', marker='o')

    surf = ax.plot_surface(x, y, z, rstride=1, cstride=1, linewidth=0,
                           antialiased=False, facecolors=rgb)

    plt.savefig('frame.png', bbox_inches='tight')
    movie_file('frame.png')
    plt.close(1)


    
