import numpy as np
import cv2 as cv
from random import randrange, shuffle

# Simulation Initialisation: Random Initialisation using Image Capture
def initialise():
    cap = cv.VideoCapture(0)                           # Initialise video capture
    ret, frame = cap.read()                            # Capture Frame
    frame = cv.resize(frame, (100, 50))
    food,land,food4trade = cv.split(frame)             # for Food and Land Distribution
    ret, frame = cap.read()                            # Image based Randomise
    frame = cv.resize(frame, (100, 50))
    land4trade, food4lease,land4lease = cv.split(frame) # for Leases and Trades Bids

    return [food, land, food4trade, land4trade, food4lease, land4lease]


# Successful Deals[Leases and Trades]
def deals(height, width):
    deal = np.empty((height, width), dtype=int)
    # Assign values from xrange(no.of.agents) to array of simulation matrix dimensions
    k = 0
    for i in xrange(height):
        for j in xrange(width):
            deal[i][j] = k
            k += 1

    # Shuffle to obtain a random and unique agent pairing for successful deal
    np.random.shuffle(deal)
    np.random.shuffle(np.transpose(deal))

    return deal


# Deals Update
def dealsupdate(food, land, food4trade, land4trade, food4lease, land4lease, deals):
    # Initialise variables
    donedeals = []
    leaseendfood = np.empty((food.shape[0],food.shape[1]), dtype=int)
    leaseendland = np.empty((food.shape[0],food.shape[1]), dtype=int)
    food[food < 0] = 0
    land[land < 0] = 0

    for i in xrange(food.shape[0]):
        for j in xrange(food.shape[1]):

            l = deals[i][j]%food.shape[0]
            m = int(deals[i][j]/food.shape[0])

            if (i*food.shape[0]+j) not in donedeals and (l*food.shape[0]+m) not in donedeals:
                # Food, Land Lease Start
                food[i][j] = food[i][j] + (food4lease[i][j]-food4lease[l][m])
                land[i][j] = land[i][j] + (land4lease[i][j]-land4lease[l][m])

                food[l][m] = food[l][m] - (food4lease[i][j]-food4lease[l][m])
                land[l][m] = land[l][m] - (land4lease[i][j]-land4lease[l][m])

                # Food, Land Trade
                food[i][j] = food[i][j] + (food4trade[i][j]-food4trade[l][m])
                food[l][m] = food[l][m] - (food4trade[i][j]-food4trade[l][m])

                land[i][j] = land[i][j] + (land4trade[i][j] - land4trade[l][m])
                land[l][m] = land[l][m] - (land4trade[i][j] - land4trade[l][m])

                # Land, Food Lease End
                leaseendfood[i][j] = food[i][j] - (food4lease[i][j]-food4lease[l][m])
                leaseendland[i][j] = land[i][j] - (land4lease[i][j]-land4lease[l][m])

                leaseendfood[l][m] = food[l][m] + (food4lease[i][j]-food4lease[l][m])
                leaseendland[l][m] = land[l][m] + (land4lease[i][j]-land4lease[l][m])

                # Principle of Conservation of Food and Land. 
                  # can't trade, lease more food than available with each agent in a deal
                if food[i][j] < 0:
                    food[l][m] += food[i][j]
                    food[i][j] -= food[i][j]  # equal to 0

                if land[i][j] < 0:
                    land[l][m] += land[i][j]
                    land[i][j] = 0

                if food[l][m] < 0:
                    food[i][j] += food[l][m]
                    food[l][m] = 0

                if land[l][m] < 0:
                    land[i][j] += land[l][m]
                    land[l][m] = 0

                if leaseendfood[i][j] < 0:
                    leaseendfood[l][m] += leaseendfood[i][j]
                    leaseendfood[i][j] = 0

                if leaseendland[i][j] < 0:
                    leaseendland[l][m] += leaseendland[i][j]
                    leaseendland[i][j] = 0

                if leaseendfood[l][m] < 0:
                    leaseendfood[i][j] += leaseendfood[l][m]
                    leaseendfood[l][m] = 0

                if leaseendland[l][m] < 0:
                    leaseendland[i][j] += leaseendland[l][m]
                    leaseendland[l][m] = 0

                donedeals.append(i+j*food.shape[1])
                donedeals.append(l+m*food.shape[1])

    return [food, land, leaseendfood, leaseendland]


def simulationupdate(food, land, leaseendfood, leaseendland, land2food):
    food = leaseendfood + land2food*land - 1;
    land = leaseendland

    food[food<0] = 0
    land[land<0] = 0

    return [food, land]


#Execute if file run as script
if __name__ == "__main__":
    i=True
    k=0
    food, land, food4trade, land4trade, food4lease, land4lease = initialise()
    while i or k == ord(' '):
        # Simulation
        deal = deals(food.shape[0], food.shape[1])
        food, land, leaseendfood, leaseendland = dealsupdate(food, land, food4trade, land4trade, food4lease, land4lease, deal)
        food, land = simulationupdate(food, land, leaseendfood, leaseendland, 1)

        # Visualisation
        image = np.zeros([food.shape[0],food.shape[1],3])
        last = np.zeros([food.shape[0],food.shape[1]])
        image[:,:,0] = food
        image[:,:,1] = land
        image[:,:,2] = last
        cv.imshow('Win', image)    

        #cv.imwrite('sim2.jpg',image)
        i=False
        k = cv.waitKey(0) & 0xFF          # capture keypress

        # if Esc pressed
        if k == 27:                       
            exit(0)

