# Import Modules
import numpy as np
import cv2 as cv
import random, itertools

# Simulation Initialisation: Random Initialisation using Image Capture
def initialise(sim_height=150, sim_width=150):
    cap = cv.VideoCapture(0)                           # Initialise video capture
    ret, frame = cap.read()                            # Capture Frame
    frame = cv.resize(frame, (sim_height, sim_width))
    food,land,food4trade = cv.split(frame)             # for Food and Land Distribution
    ret, frame = cap.read()                            # Image based Randomise
    frame = cv.resize(frame, (sim_height, sim_width))
    land4trade, food4lease,land4lease = cv.split(frame) # for Leases and Trades Bids

    return [food, land, food4trade, land4trade, food4lease, land4lease]


# Deals Update
def deal(food, land, food4trade, land4trade, food4lease, land4lease):
    
    # Initialise variables
    leaseendfood = np.empty((sim_height, sim_width), dtype='int64')
    leaseendland = np.empty((sim_height, sim_width), dtype='int64')

    # Make (random) deals
    agentids=range(sim_height*sim_width)        # create list of all agent ids
    random.shuffle(agentids)                    # shuffle agent-ids 
    deals=itertools.izip(*[iter(agentids)]*2)   # pair agent-id's into an iterator

    for deal in deals:
        # Compute agent positions based on agent-id
        i = int(deal[0]/sim_width)
        j = deal[0]%sim_width

        l = int(deal[1]/sim_width)
        m = deal[1]%sim_width

        # Track a single agent for correct functionality checking
        if deal[0]==10: 
            print "Food, Land"
            print food[i][j], land[i][j], food[l][m], land[l][m]
            print "Food4Trade Land4Trade, Land4Lease"
            print food4trade[i][j]-food4trade[l][m], land4trade[i][j]-land4trade[l][m], land4lease[i][j]-land4lease[l][m], "\n"
        elif deal[1]==10: 
            print "Food, Land"
            print food[l][m], land[l][m], food[i][j], land[i][j]
            print "Food4Trade Land4Trade, Land4Lease"
            print -(food4trade[i][j]-food4trade[l][m]), -(land4trade[i][j]-land4trade[l][m]), -(land4lease[i][j]-land4lease[l][m]), "\n"

        # agent dead if no food or land
        if (food[i][j]==0 and land[i][j]==0) or (food[l][m]==0 and land[l][m]==0):
            continue

        # Land Lease Start
        land[i][j] = land[i][j] + (land4lease[i][j]-land4lease[l][m])
        land[l][m] = land[l][m] - (land4lease[i][j]-land4lease[l][m])
         
        # Food Trade
        food[i][j] = food[i][j] + (food4trade[i][j]-food4trade[l][m])
        food[l][m] = food[l][m] - (food4trade[i][j]-food4trade[l][m])
        # Land Trade
        land[i][j] = land[i][j] + (land4trade[i][j] - land4trade[l][m])
        land[l][m] = land[l][m] - (land4trade[i][j] - land4trade[l][m])
        
        # Land, Food Lease End
        leaseendland[i][j] = land[i][j] - (land4lease[i][j]-land4lease[l][m])
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

        if leaseendland[i][j] < 0:
            leaseendland[l][m] += leaseendland[i][j]
            leaseendland[i][j] = 0

        if leaseendland[l][m] < 0:
            leaseendland[i][j] += leaseendland[l][m]
            leaseendland[l][m] = 0

    return [food, land, leaseendfood, leaseendland]


def simulate(food, land, leaseendfood, leaseendland, land2food, food2agent):
    food += land2food*land - food2agent;
    land = leaseendland

    return [food, land]


#Execute if file run as script
if __name__ == "__main__":

    # Importing Modules
    import time

    # Initialising Variables 
    i=True
    k=0
    sim_height = 150
    sim_width  = 150
    food = np.empty((sim_height,sim_width), dtype='int64')
    land = np.empty((sim_height,sim_width), dtype='int64')
    food4trade = np.empty((sim_height,sim_width), dtype='int64')
    land4trade = np.empty((sim_height,sim_width), dtype='int64')
    food4lease = np.empty((sim_height,sim_width), dtype='int64')
    land4lease = np.empty((sim_height,sim_width), dtype='int64')

    food, land, food4trade, land4trade, food4lease, land4lease = initialise(sim_height, sim_width)

    while i or k == ord(' '):
        # New Deals
        food, land, leaseendfood, leaseendland = deal(food, land, food4trade, land4trade, food4lease, land4lease)

        # New Food grown on Land
        food, land = simulate(food, land, leaseendfood, leaseendland, 1, 1)

        # New Trades and Leases
        food4trade = np.random.random_integers(0,255,(sim_height,sim_width))
        land4trade = np.random.random_integers(0,255,(sim_height,sim_width))
        food4lease = np.random.random_integers(0,255,(sim_height,sim_width))
        land4lease = np.random.random_integers(0,255,(sim_height,sim_width))

        # Visualisation
        image = np.zeros([sim_height,sim_width,3])
        image[:,:,0] = food
        image[:,:,1] = land
        image[:,:,2] = np.zeros([sim_height,sim_width])
        cv.imshow('Land, Food Distribution Map', image)    

        i=False
        k = cv.waitKey(0) & 0xFF          # capture keypress

        # Exit if Esc pressed
        if k == 27:                       
            cv.imwrite("socialsim2d.jpg",image)
            exit(0)
