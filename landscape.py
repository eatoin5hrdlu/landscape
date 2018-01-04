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

type = 'png'
frameLocation = "/tmp/gifmovie/"

count = 0

def movie_file(name) :
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

maxx = 0
maxy = 0
maxz = 0
for a in range(150):      # Find global peak
    for b in range(150):
        if (z[a][b] > maxz) :
            maxz = z[a][b]
            maxx = a
            maxy = b
        
# Prepare starting locations
n = 50
vx = [0]*n
vy = [0]*n
vz = [0]*n
rix = [0]*n
riy = [0]*n
rx = 0
ry = 0
random.seed(0)  # seed for reproducible 'random' numbers
for i in range(n) :
    rix[i] = random.randrange(0,150)
    riy[i] = random.randrange(0,150)
    vx[i] = x[rix[i]][0]
    vy[i] = y[0][riy[i]]

ls = LightSource(azdeg=0, altdeg=65)
rgb = ls.shade(z, plt.cm.RdYlBu)

elevation = 10
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
    if (count % 2 == 0) :
        if (edir) :
            if (elevation < 30) :
                elevation = elevation + 0.5
            else :
                edir = not edir
        else :
            if (elevation > 0) :
                elevation = elevation - 0.5
            else :
                edir = not edir
        if (adir) :
            if (azimuth < 40) :
                azimuth = azimuth + 0.5
            else :
                adir = not adir
        else :
            if (azimuth > 10) :
                azimuth = azimuth - 0.5
            else :
                adir = not adir
    ax.view_init(elevation,azimuth)
    ax.dist = 4.6
    for i in range(n) : # Crawl randomly ->(100,100) before assigning vz
        if (rix[i] < maxx) :
            dx = random.randint(-1,2)
        else :
            dx = random.randint(-2,1)
        if (riy[i] < maxy) :
            dy = random.randint(-1,2)
        else :
            dy = random.randint(-2,1)
        newx = rix[i] + dx
        if not newx in rix and newx > -1 and newx < 150:
            rix[i] = newx
        newy = riy[i] + dy
        if not newy in riy and newy > -1 and newy < 150:
            riy[i] = newy
        vx[i] = x[rix[i]][0] + random.uniform(-0.02,0.02)
        vy[i] = y[0][riy[i]] + random.uniform(-0.02,0.02)
        vz[i] = z[rix[i]][riy[i]] + 0.2 + random.uniform(-0.04,0.04)

    ax.scatter(np.asarray(vx), np.asarray(vy), np.asarray(vz),
               c='r', marker='o')
    ax.scatter(np.asarray([x[maxx][0]]),np.asarray([y[0][maxy]]),np.asarray([maxz+0.2]),
               c='b', marker='D')

    surf = ax.plot_surface(x, y, z, rstride=1, cstride=1, linewidth=0,
                           antialiased=False, facecolors=rgb)
    plt.savefig(frameLocation + 'frame.png', bbox_inches='tight')
    movie_file(frameLocation + 'frame.png')
    plt.close(1)


    
