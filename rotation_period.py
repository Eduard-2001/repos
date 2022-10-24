#save the (x,y) coordinate in a txt file in the same directory as this file
#for example in file '1.TXT':
#x1 y1
#x2 y2
#x3 y3
#...
#notice that the dtype of each x and y should be integer
#
#
#When running this code, edit the filename and the result will be saved in a png image
#named after the txt file.

import numpy as np
import re
import matplotlib.pyplot as plt
from scipy.stats import linregress

#open files
filename = '1.TXT'
with open(filename) as f_obj:
    p1 = f_obj.readlines()

#calculate the location of the center of the magnetogram,
#left
lx = 80.
rx = 3996.
oben_y = 4017.
unten_y = 91.   #the 4 parameters above can be changed according to magnetogram
midx = (lx+rx)/2.
midy = (oben_y+unten_y)/2.
R = (midx+midy-lx-unten_y)/2

#convert x-y coordinate to longitude and latitude
def longlat(x,y):
    y = y-midy
    sintheta = y/R
    theta = np.arcsin(sintheta)
    x = x-midx
    r = R*np.cos(theta)
    alpha = np.arcsin(x/r)
    return theta*180/np.pi,alpha*180/np.pi


#read x and y data from the TXT file 
x = []
y = []
lat = np.array([])
long = np.array([])
for p in p1:
    x.append(float(re.match('^(\w*)\D(\w*).*$',p).group(1)))
    y.append(float(re.match('^(\w*)\D(\w*).*$',p).group(2)))

xy = list(zip(x,y))
for t in xy:
    la,lo = longlat(t[0],t[1])
    lat = np.append(lat,la)
    long = np.append(long,lo)

time = np.arange(len(p1))
timeint=4.#the timeinterval between each magnetograms
time = timeint*time

#plot
sum = 0
for l in lat:
    sum += l
averagelat = round(sum/len(p1),2)
long = long-time*1/24
k,b,r,p,stderr=linregress(time,long)
fitted_data = time*k+b
periode = round(-360/k/24,2)
plt.title('Latitude = '+str(averagelat)+'$^\circ$')
plt.xlabel('time(h)')
plt.ylabel('longitude(degree)')
plt.legend()
x0, xmax = plt.xlim()
y0, ymax = plt.ylim()
data_width = xmax - x0
data_height = ymax - y0
plt.text(x0+data_width,y0+data_height*5,'Period: '+str(periode)+' Days')
plt.text(x0+data_width,y0+data_height*10,'$\omega$ = '+str(round(k,2))+'$^\circ/s$')

plt.plot(time,long)

plt.plot(time,fitted_data)


plt.savefig(filename+'.png')

