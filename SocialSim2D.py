import numpy as np
import cv2 as cv
from random import randrange, shuffle

# Initialise video capture
cap = cv.VideoCapture(0)

# Capture frame
ret, frame = cap.read()    # Image based Randomise
f,l,fl = cv.split(frame)   # for Food and Land Distribution
ret, frame = cap.read()    # Image based Randomise
ft,ll,lt = cv.split(frame) # for Leases and Trades Calls
#gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

# Successful Leases and Trades
tr = np.empty((f.shape[0], f.shape[1]), dtype=int)
le = np.empty((f.shape[0], f.shape[1]), dtype=int)
k = 0
for i in xrange(0,f.shape[0]):
    for j in xrange(0,f.shape[1]):
        tr[i][j] = k
        le[i][j] = k
        k += 1

np.random.shuffle(le)
np.random.shuffle(np.transpose(le))
np.random.shuffle(tr)
np.random.shuffle(np.transpose(tr))


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
