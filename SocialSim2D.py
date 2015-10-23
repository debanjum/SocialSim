import numpy as np
import cv2 as cv
from random import randrange, shuffle

# Initialise video capture
cap = cv.VideoCapture(0)

# Capture frame
ret, frame = cap.read()                         # Image based Randomise
food,land,food4lease = cv.split(frame)           # for Food and Land Distribution
ret, frame = cap.read()                         # Image based Randomise
food4trade,land4lease,land4trade = cv.split(frame) # for Leases and Trades Calls
#gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

# Successful Deals[Leases and Trades]
foodtradedeals = np.empty((f.shape[0], f.shape[1]), dtype=int)
foodleasedeals = np.empty((f.shape[0], f.shape[1]), dtype=int)
landtradedeals = np.empty((f.shape[0], f.shape[1]), dtype=int)
landleasedeals = np.empty((f.shape[0], f.shape[1]), dtype=int)

k = 0
for i in xrange(0,f.shape[0]):
    for j in xrange(0,f.shape[1]):
        foodtradedeals[i][j] = k
        foodleasedeals[i][j] = k
        landtradedeals[i][j] = k
        landleasedeals[i][j] = k
        k += 1

np.random.shuffle(foodleasedeals)
np.random.shuffle(np.transpose(foodleasedeals))
np.random.shuffle(foodtradedeals)
np.random.shuffle(np.transpose(foodtradedeals))
np.random.shuffle(landleasedeals)
np.random.shuffle(np.transpose(landleasedeals))
np.random.shuffle(landtradedeals)
np.random.shuffle(np.transpose(landtradedeals))

# Deals Update
foodupdate = []
landupdate = []
flag = 0
leasestartfood = np.empty((f.shape[0],f.shape[1]), dtype=int)
leasestartland = np.empty((f.shape[0],f.shape[1]), dtype=int)
leaaseendfood = np.empty((f.shape[0],f.shape[1]), dtype=int)
leaseendland = np.empty((f.shape[0],f.shape[1]), dtype=int)

for i in xrange(len(f.shape[0])):
    for j in xrange(len(f.shape[1])):
        if f[i][j] > 0:                                     # if alive
            if len(update)>=f.shape[0]*f.shape[1]:          # deals terminating condition: if total deals equal to half of total pop
                flag=1
            if flag=0:
                if food[i][j] not in foodupdate:
                    l = foodtradedeals[i][j]%f.shape[1]
                    m = int(foodtradedeals[i][j]/f.shape[1])

                    leasestartfood[i][j] = food[i][j] + food4lease[i][j]
                    leasestartland[i][j] = land[i][j] + land4lease[i][j]

                    leasestartfood[l][m] = food[l][m] - food4lease[i][j]
                    leasestartland[l][m] = land[l][m] - land4lease[i][j]

                    leaseendfood[i][j] = leasestartfood[i][j] - food4lease[l][m]
                    leaseendland[i][j] = leasestartland[i][j] - land4lease[l][m]

                    leaseendfood[l][m] = leasestartfood[l][m] + food4lease[i][j]
                    leaseendland[l][m] = leasestartland[l][m] + land4lease[i][j]

                    foodupdate.append(food[i][j])
                    landupdate.append(land[i][j])

                    tradefood[i][j] = food[i][j] + food4trade[i][j]
                    tradefood[l][m] = food[l][m] - food4trade[i][j]

        
frame=cv.merge((f,l,fl))
print f.item(10,10)

# Display the resulting frame
cv.imshow('frame',frame)

# On keypress
cv.waitKey(0)
# Release the capture
cap.release()
# Destroy all windows
cv.destroyAllWindows()
