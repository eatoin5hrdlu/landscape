#!/usr/bin/python -u
"""
Fitness landscape for Innatrix Evolution Demonstration
(From: http://matplotlib.org/examples/pylab_examples/shading_example.html
"""

from __future__ import print_function
import numpy as np
import mpl_toolkits.mplot3d as a3
import pylab as pl
import scipy as sp
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.colors as colors
import matplotlib

import random, glob, os, subprocess
from shutil import copyfile
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import LightSource

sdb = False  # String suppression (False for debugging)
type = 'png'
frameLocation = "/tmp/gifmovie/"

count = 0
                          
aa = [    'Ala',    'Arg',    'Asn',    'Asp',    'Asx',    'Cys',    'Glu',
          'Gln',    'Glx',    'Gly',    'His',    'Ile',    'Leu',    'Lys',
          'Met',    'Phe',    'Pro',    'Ser',    'Pro',    'Thr',    'Trp',
          'Tyr',    'Val' ]

aa3 = [[['Phe','Phe','Leu','Leu'],
        ['Leu','Leu','Leu','Leu'],
        ['Ile','Ile','Ile','Met'],
        ['Val','Val','Val','Val'] ],
       [ ['Ser']*4, 
         ['Pro']*4, 
         ['Thr']*4, 
         ['Ala']*4 ],
       [ ['Tyr','Tyr','stop','stop'],
         ['His','His','Gln','Gln'],
         ['Asn','Asn','Lys','Lys'],
         ['Asp','Asp','Glu','Glu'] ],
       [ ['Cys','Cys','stop','Trp'],
         ['Arg']*4,
         ['Ser','Ser','Arg','Arg'],
         ['Gly']*4 ] ]

aa = [    'Ala',    'Arg',    'Asn',    'Asp',    'Asx',    'Cys',    'Glu',
          'Gln',    'Glx',    'Gly',    'His',    'Ile',    'Leu',    'Lys',
          'Met',    'Phe',    'Pro',    'Ser',    'Pro',    'Thr',    'Trp',
          'Tyr',    'Val' ]

n = 30
va = [0]*n
va2 = [0]*n
vb = [0]*n
vb2 = [0]*n
vc = [0]*n
vc2 = [0]*n
# Mutation: Random Amino Acid and random Single-base mutant
def aastr(i) :
    if (sdb) :
        return ''
    va[i], vb[i], vc[i] = [ random.randint(0,2),random.randint(0,2), random.randint(0,2) ]
    va2[i], vb2[i], vc2[i] = [ random.randint(0,2),random.randint(0,2), random.randint(0,2) ]
    return aa3[va[i]][vb[i]][vc[i]] + str(random.randrange(230,315)) + aa3[va[i]][vb2[i]][vc[i]]

def aamut(i) :
    if (sdb) :
        return ''
    while va2[i] == va[i] :
        va2[i] = random.randint(0,2)
    return aa3[va[i]][vb[i]][vc[i]] + str(random.randrange(130,455)) + aa3[va2[i]][vb2[i]][vc2[i]]

def cube() :
    return [   [ [ 0, 0, 0 ], # bottom
                 [ 1, 0, 0 ],
                 [ 1, 1, 0 ],
                 [ 0, 1, 0 ] ],
               [ [ 0, 0, 0 ], # front
                 [ 0, 0, 1 ],
                 [ 1, 0, 1 ],
                 [ 1, 0, 0 ] ],
               [ [ 0, 0, 0 ], # left
                 [ 0, 1, 0 ],
                 [ 0, 1, 1 ],
                 [ 0, 0, 1 ] ],
               [ [ 1, 0, 0 ], # right
                 [ 1, 1, 0 ],
                 [ 1, 1, 1 ],
                 [ 1, 0, 1 ] ],
               [ [ 0, 1, 0 ], # back
                 [ 1, 1, 0 ],
                 [ 1, 1, 1 ],
                 [ 0, 1, 1 ] ],
               [ [ 0, 0, 1 ], # top
                 [ 1, 0, 1 ],
                 [ 1, 1, 1 ],
                 [ 0, 1, 1 ] ] ]
             
# Prepare starting locations
vx = [0]*n
vy = [0]*n
vz = [-20]*n
rix = [0]*n
riy = [0]*n
vp = [aastr(6)]*n

rx = 0
ry = 0
random.seed(0)  # seed for reproducible 'random' numbers

def disp_string(i,x,y,z) :
    if (sdb) :
        return ''
    return str(i) + "(" + str(round(x,2)) + "," + str(round(y,2)) + "," + str(round(z,2)) + ")"

def duplicate(x,y,xs,ys) :
    for i in range(len(xs)) :
        if ( xs[i]==x and ys[i]==y ) :
            return True
    return False

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

#z =  3*(1 - x/2)**2 * np.exp(-x**2 - (y + 1)**2) \
#   - 2*(x/6 - (x**3)/7 - y**3)*np.exp(-x**2 - y**2) \
#   - 2.0*np.exp(-(x + 1)**2 - y**3) 

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

print(" Maxima = "+disp_string(0,maxx,maxy,maxz))

for i in range(n) :
    rix[i] = random.randrange(0,150)
    riy[i] = random.randrange(0,150)
    vx[i] = x[rix[i]][0]
    vy[i] = y[0][riy[i]]
    vz[i] = z[rix[i]][riy[i]]
    vp[i] = aastr(6)

ls = LightSource(azdeg=20, altdeg=65)
rgb = ls.shade(z, plt.cm.RdYlBu)
plt.rc( 'font', size=8)
elevation = 25
edir = True
azimuth = 80
adir = True

while True :
    fig = plt.figure(1)
    ax = fig.gca(projection='3d')
    plt.hold(True)
    ax.grid(False) # Hide grid lines
    ax.axis('off') # OR #ax.set_xticks([])#ax.set_yticks([])#ax.set_zticks([])
    ax.view_init(elevation, azimuth)
    ax.dist = 5

    count = count + 1
    if (count < 3) :
        origin = 'Start'
    else :
        origin = '(0,0)'
    if False :  # (count % 2 == 0) :
        if (edir) :
            if (elevation < 40) :
                elevation = elevation + 0.5
            else :
                edir = not edir
        else :
            if (elevation > 0) :
                elevation = elevation - 0.5
            else :
                edir = not edir
        if (adir) :
            if (azimuth < 180) :
                azimuth = azimuth + 0.5
            else :
                adir = not adir
        else :
            if (azimuth > 10) :
                azimuth = azimuth - 0.5
            else :
                adir = not adir
    ax.text( -3, -3, 0.4, origin, None, color='g')
    ax.scatter(np.asarray(-3), np.asarray(-3), np.asarray(0.3), c='g', marker='s')
    # Grab one at random and place it in the box
    if (count % 14 == 0) :
        randi = random.randint(0,n)
        rix[randi] = 144
        riy[randi] = 144
        vz[randi] = z[rix[randi]][riy[randi]] + 2.0
        print("  z["+str(randi)+"] = "+str(vz[randi])+vp[randi])
    for i in range(n) : # Crawl randomly ->(100,100) before assigning vz
        if (rix[i] < maxx) :
            dx = random.randint(-2,3)
        else :
            dx = random.randint(-3,2)
        if (riy[i] < maxy) :
           dy = random.randint(-2,3)
        else :
            dy = random.randint(-3,2)
        # Randomish walk, but don't go out of bounds, and no duplicates, and never downhill
        newx = rix[i] + dx
        newy = riy[i] + dy
        if newx>0 and newx<150 and newy>0 and newy<150 and z[rix[i]][riy[i]] < maxz :
            if not duplicate(newx,newy,rix,riy) :
                rix[i] = newx
                riy[i] = newy
                vp[i] = aamut(i)
        vx[i] = x[rix[i]][0] + random.uniform(-0.02,0.02)
        vy[i] = y[0][riy[i]] + random.uniform(-0.02,0.02)
        vz[i] = max(1.6,z[rix[i]][riy[i]]) + 1.9 + random.uniform(-0.04,0.04)
        ax.text(vx[i],vy[i],vz[i],vp[i], None)
    ax.scatter(np.asarray(vx), np.asarray(vy), np.asarray(vz),
               c='r', marker='o')
    ax.scatter(np.asarray([x[maxx][0]]),np.asarray([y[0][maxy]]),np.asarray([maxz+0.2]),
               c='b', marker='D')
#    ax.text(x[maxx][0],y[0][maxy],maxz+0.2,"Goal",'y')
#    for vtx in [ sp.rand(4,3)*2 + 2 for i in range(10) ] :
    for vtx in np.asarray(cube())*np.asarray([[1,1,2],[1,1,2],[1,1,2],[1,1,2]])+2 :
        tri = a3.art3d.Poly3DCollection([vtx],facecolors='w', linewidths=1, alpha=0.5)
        tri.set_color(colors.rgb2hex(sp.rand(3)))
        tri.set_edgecolor('k')
        ax.add_collection3d(tri)

    surf = ax.plot_surface(x, y, z, rstride=1, cstride=1, linewidth=0,
                           antialiased=False, facecolors=rgb)
    plt.savefig(frameLocation + 'frame.png', bbox_inches='tight')
    movie_file(frameLocation + 'frame.png')
    plt.close(1)




