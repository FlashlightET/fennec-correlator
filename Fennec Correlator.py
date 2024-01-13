#Fennec Correlator? - this is the old version of the script that used a colors list, a list of screengrabbed colors sampled with a script im not releasing because its someone elses code but macguyvered
import PIL
from PIL import Image, ImageOps
import matplotlib as mpl
import matplotlib.pyplot as plt
import math
import numpy as np
fn='fennec_arms'
with open(f'{fn}.txt','r') as f:
    colors_list=[i.strip('\r\n') for i in f.readlines()]

x1=[]
y1=[]
z1=[]

for i in colors_list:
    z=[int(i2) for i2 in i.split(',')]
    x1.append(z[1])
    y1.append(z[2])
    z1.append((z[0],z[1],z[2]))

mappedColor=[]
mappedFilter=[]
              
for i in range (0, 256):
    new = []
    for j in range (0, 256):
        new.append((0,0,0))
    mappedColor.append(new)

for i in range (0, 256):
    new = []
    for j in range (0, 256):
        new.append(0)
    mappedFilter.append(new)

for i in range(len(x1)):
    mappedColor[x1[i]][y1[i]]=z1[i]
    mappedFilter[x1[i]][y1[i]]+=1


x=np.array(x1)
y=np.array(y1)
z=np.array(z1)
print(z1)
#plt.scatter(x,y,c=z/255,s=1)
fig, ax = plt.subplots()
ax.scatter(x,y,c=z/255)

for filter_level in range(1,7):
    canvas=Image.new(size=(256,256),mode='RGB')
    for y in range(0,256):
        for x in range(0,256):
            if mappedFilter[x][y]>=filter_level:
                canvas.putpixel((x,255-y), mappedColor[x][y])

    canvas.save(f'fennec_colorrefs/output/{fn}_filter-level_{filter_level}.png')

#fig.show()
