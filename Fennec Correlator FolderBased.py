#Fennec Correlator?
import PIL
from PIL import Image, ImageOps
import matplotlib as mpl
import matplotlib.pyplot as plt
import math
import numpy as np
#FOLDER STRUCTURE
#character_colorrefs
#|- input
#   |- base folder (can be anywhere but input is the best place to put it because you can copy and rename it in-place)
#   |- bodypart1
#   |- bodypart2
#|- output
#   |- output histograms
directory='character_colorrefs/input/'
fn='bodypart'
colors_list=[]

import os
j=os.listdir(directory+fn)
i2=0
for i in j:
    i2+=1
    print(f'{i2}/{len(j)}: {i}')
    img=Image.open(directory+fn+'/'+i).convert('RGBA')
    imageBox = img.getbbox()
    img=img.crop(imageBox)
    pixels=img.load()
    found=0
    for x in range(img.width):
        for y in range(img.height):
            pixel=pixels[x,y]
            #print(pixel)
            try:
                if pixel[3]>0:
                    colors_list.append(f'{pixel[0]},{pixel[1]},{pixel[2]}')
                    found+=1
            except:
                pass
    print(f'found {found} pixels worth')
            

x1=[]
y1=[]
z1=[]

print('plotting color values...')
for i in colors_list:
    z=[int(i2) for i2 in i.split(',')]
    x1.append(z[1])
    y1.append(z[2])
    z1.append((z[0],z[1],z[2]))

mappedColor=[]
mappedFilter=[]

print('normalizing frequency values... step 1/4')
for i in range (0, 256):
    new = []
    for j in range (0, 256):
        new.append((0,0,0))
    mappedColor.append(new)
print('normalizing frequency values... step 2/4')
for i in range (0, 256):
    new = []
    for j in range (0, 256):
        new.append(0)
    mappedFilter.append(new)
print('normalizing frequency values... step 3/4')
for i in range(len(x1)):
    mappedColor[x1[i]][y1[i]]=z1[i]
    mappedFilter[x1[i]][y1[i]]+=1

print('normalizing frequency values... step 4/4')
x=np.array(x1)
y=np.array(y1)
z=np.array(z1)
#print(z1)


flattened_list = [item for sublist in mappedFilter for item in sublist]
min_value = min(flattened_list)
max_value = max(flattened_list)
ya=(max_value - min_value)
if ya==0: ya=1
normalized_flattened_list = [(x - min_value) / ya for x in flattened_list]
normalized_2d_list = np.array(normalized_flattened_list).reshape(len(mappedFilter), -1)

mappedFilter=normalized_2d_list

#plt.scatter(x,y,c=z/255,s=1)
fig, ax = plt.subplots()
ax.scatter(x,y,c=z/255)

print('generating gamut maps...')
for filter_level in range(0,10):
    print(f'generating {filter_level*10}-100%')
    canvas=Image.new(size=(256,256),mode='RGB')
    for y in range(0,256):
        for x in range(0,256):
            if mappedFilter[x][y]>=filter_level/10:
                canvas.putpixel((x,255-y), mappedColor[x][y])
    imageBox = canvas.getbbox()
    canvas=canvas.crop(imageBox)
    canvas=canvas.resize((canvas.width*4,canvas.height*4),resample=Image.NEAREST)
    #print(f'{bbox_x1}, {bbox_y1}, {bbox_x2}, {bbox_y2}')
    canvas.save(f'character_colorrefs/output/{fn}_filter-level_{filter_level}.png')

#fig.show()
