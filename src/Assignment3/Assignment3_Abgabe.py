import sys
import numpy as np
import cv2
from matplotlib import pyplot as plt
import math

# from __future__ import print_function

# Task 2
gray = cv2.imread('imageraw.png',0)
#make it gray

cv2.imwrite("imagegray.png",gray)
# Task 3
    #bi_gray
bi_gray_max = 255
bi_gray_min = 245
ret,thresh1=cv2.threshold(gray, bi_gray_min, bi_gray_max, cv2.THRESH_BINARY);

# Save to image
cv2.imwrite('image_bw.png',thresh1)
 
  # Task 4 
# Search for white points
black_white = cv2.imread('image_bw.png',0)

x_max = 640
y_max = 480
narray = []
for i in range(black_white.shape[0]):
	for j in range(black_white.shape[1]):
		if black_white[i,j] == 255:
			narray.append((i,j))

		#print("Coordinates: "+ str(i)+","+str(j)+": "+str(black_white[i,j]))
		#print("i = " + str(i))
		#print("j ="+str(j))
#print array with coordinates for all white pixels
print("white points: "+str(narray))


#reads a black and white file?
def identify_blobs(data):
  #...
  
  #b,g,r = cv2.split(data)
  
  bloblist = []
   #local function infect(i,j)
  #paints a cell in a shade of red if it was white before
  #does the same to neighbouring cells etc
  #resulting in painting an entire blob in 1 color
  def infect(i,j):
      if data[i,j] ==255:
        #set color to length of bloblist - cause we're creating one blob at a time, so each blob gets its own slightly different color this way
        color = len(bloblist*10) #*20 so it becomes visible in red
        data[i,j] = color
        #b[i,j] = 0
        #g[i,j] = 0
        #add coordinate to blob
        bloblist[len(bloblist)-1].append((i,j))
        #now, recursively infect neighboring cells, if on the board
        #up
        if i < data.shape[0]-1:
          infect (i+1, j)
        #down
        if i > 0:
          infect (i-1, j)
        #left
        if j > 0:
          infect (i, j-1)
        #right
        if j < data.shape[1]-1:
          infect (i, j+1)
      #else:
          #do nothing

    #try a blob infection on every cell of the entire image. 
    #black cells and already infected cells (by a different blob) will be spared
  for i in range(data.shape[0]):
    for j in range(data.shape[1]):  
      if data[i,j] == 255:   #just checking r should be enough since its been turned gray
          #we doublechecked r[i,j] for 255 to only add new blobs here
        blob = []
        bloblist.append(blob)   
        infect(i,j)	
	  
    #count blobs

    #if count > 6 look at blobsize
    #delete smallest blob until count = 6
    while len(bloblist)>6:
        #delete smallest blob
        smallest_blob = 0
        for i in range(len(bloblist)):
          if (len(bloblist[i]) < len(bloblist[smallest_blob])):
            smallest_blob = i        
        del bloblist[smallest_blob]
    
    #shave blobs
    blob_middlepoint_list = []
    for i in range(len(bloblist)):
      total = (0,0)
      for j in range(len(bloblist[i])):
        total = (total[0]+bloblist[i][j][0], total[1]+bloblist[i][j][1])
      total = (total[0]/len(bloblist[i]), total[1]/len(bloblist[i]))
      blob_middlepoint_list.append(total)
    #done!
  
  return blob_middlepoint_list #(blob-koordinaten ausspucken)
  #return data #(bild ausspucken)

#main part:
img = cv2.imread('image_bw.png', 0)
#img = identify_blobs(img)
#cv2.imwrite('imageblobs.png', img)
blobskoords = identify_blobs(img)
print("Coordinates for white points grouped: "+str(blobskoords))
#print(len(blobskoords))



# Task 5
fx=614.1699 
fy=614.9002
cx=329.9491
cy=237.2788
cameraMatrix = np.array([[fx, 0.0, cx],[0.0, fy, cy],[0.0, 0.0, 1.0]])
#print(cameraMatrix)

k1=0.1115
k2=-0.1089
t1=0
t2=0
distCoeffs = np.array([k1,k2,t1,t2]) 
#print(distCoeffs)

objectPoints = np.array([[0,0,0],[0.4,0,0],[0,0.3,0],[0.4,0.3,0],[0,0.6,0],[0.4,0.6,0]])
#print(objectPoints)
imagePoints = np.array(blobskoords)

solved =cv2.solvePnP(objectPoints, imagePoints, cameraMatrix, distCoeffs)

rotation = solved[1]
translation = solved[2]

print("Rotation vector: "+str(rotation))
print("Translation vector: "+str(translation))

# Task 6
rodrigues = cv2.Rodrigues(rotation)
#Rotation matrix
rotation_matrix = rodrigues[0]
print("Rotation matrix = "+str(rotation_matrix))

print(rotation_matrix[0])
print(translation[0])

comb = rotation_matrix + translation
print(comb)

### inverse Homogenous transformation
inverse = np.linalg.inv(comb)
print("Inverse: "+str(inverse))
###

 
sy = math.sqrt(rotation_matrix[0,0] * rotation_matrix[0,0] +  rotation_matrix[1,0] * rotation_matrix[1,0])

singular = sy < 1e-6

if (~singular):

     x = math.atan2(-rotation_matrix[2,1] , rotation_matrix[2,2])
     y = math.atan2(-rotation_matrix[2,0], sy)
     z = math.atan2(rotation_matrix[1,0], rotation_matrix[0,0])

else:

     x = math.atan2(-rotation_matrix[1,2], rotation_matrix[1,1])
     y = math.atan2(-rotation_matrix[2,0], sy)
     z = 0;

print('x,y,z', x,y,z)