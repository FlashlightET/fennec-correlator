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
j=os.listdir(os.path.join(directory,fn))
i2=0
#go through every image in folder
for i in j:
    i2+=1
    print(f'{i2}/{len(j)}: {i}') #progress
    #todo: make this an os.path.join and not strings
    img=Image.open(directory+fn+'/'+i).convert('RGBA') #converting incase the image got auto-detected during save as indexed or smth by paint.net
    #here we crop the image to its bounding box to save on processing time (only process e.g. 32x190 worth of pixels in an otherwise 1920x1080 image)
    imageBox = img.getbbox()
    img=img.crop(imageBox)
    #make the pixels IOable
    pixels=img.load()
    #found is for feedback only and has no programmatic function
    found=0
    #iterate over width and height
    for x in range(img.width):
        for y in range(img.height):
            #quicker reference for the current pixel to make code more readable and speed up processing time barely
            pixel=pixels[x,y]
            #this try except probably isnt necessary, i think it was here before i added that .convert(RGBA) up there so this try except would just skip images that werent RGBA as pixel[3] would return an index error on images without a pixel[3] (non-rgba images)
            try:
                if pixel[3]>0: #if the alpha is greater than 0
                    colors_list.append(f'{pixel[0]},{pixel[1]},{pixel[2]}') #add the color of that pixel to the list of colors
                    found+=1
            except:
                pass
    print(f'found {found} pixels worth') #feedback
            

x1=[]
y1=[]
z1=[]
#plot color values on an image. x1 is x positions, y1 is y positions, and z1 is color values at the xy. i dont know why i used three separate lists.
print('plotting color values...')
for i in colors_list:
    z=[int(i2) for i2 in i.split(',')]
    #curreently it's mapped to X=G Y=B. this can be modified by setting x1, y1 to append z[0-2] (R-B) instead.
    x1.append(z[1])
    y1.append(z[2])
    z1.append((z[0],z[1],z[2]))

mappedColor=[]
mappedFilter=[]
#normalize frequencies from 0-459028354 to a better range
#i unfortunately forgot what this code does exactly
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
flattened_list = [item for sublist in mappedFilter for item in sublist]
min_value = min(flattened_list)
max_value = max(flattened_list)
ya=(max_value - min_value)
if ya==0: ya=1
normalized_flattened_list = [(x - min_value) / ya for x in flattened_list]
normalized_2d_list = np.array(normalized_flattened_list).reshape(len(mappedFilter), -1)
mappedFilter=normalized_2d_list

#make the gamut map
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
    canvas.save(f'character_colorrefs/output/{fn}_filter-level_{filter_level}.png')

#output filter levels:
#0 is   0 -   9%
#1 is  10 -  19%
#2 is  20 -  29%
#3 is  30 -  39%
#4 is  40 -  49%
#5 is  50 -  59%
#6 is  60 -  69%
#7 is  70 -  79%
#8 is  80 -  89%
#9 is  90 - 100% or 99% i cant tell but it shouldnt matter because only 0-20% is generally useful, higher numbers could have "bleed" from sets of a lot of images with a different color balance (??)
