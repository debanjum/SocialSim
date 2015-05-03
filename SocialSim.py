#!/usr/bin/env python

# Import Modules
import numpy as np
import matplotlib.pyplot as plt
from random import randrange, shuffle

# Bid for trading and leasing food, land
def Bid(A0, A1):
    if (randrange(0,1)):
        Flo  = [ randrange(0,a) if a>0 else 0 for a in A0 ]                     # Food to Lease Out    
        Fto  = [ randrange(0,a) if a>0 else 0 for a in np.subtract(A0,Flo) ]    # Food to Trade Out

        Llo  = [ randrange(0,a) if a>0 else 0 for a in A1 ]                     # Land to Lease Out    
        Lto  = [ randrange(0,a) if a>0 else 0 for a in np.subtract(A1,Llo) ]    # Land to Trade Out

    else:
        Fto  = [ randrange(0,a) if a>0 else 0 for a in A0 ]                     # Food to Trade Out    
        Flo  = [ randrange(0,a) if a>0 else 0 for a in np.subtract(A0,Fto) ]    # Food to Lease Out

        Lto  = [ randrange(0,a) if a>0 else 0 for a in A1 ]                     # Land to Trade Out    
        Llo  = [ randrange(0,a) if a>0 else 0 for a in np.subtract(A1,Lto) ]    # Land to Lease Out


    Fli = [ randrange(0,N) if a>0 else 0 for a in A0 ]#np.random.randint(40,size=N)                                           # Food to Lease In
    Lli = [ randrange(0,N) if a>0 else 0 for a in A1 ]#np.random.randint(40,size=N)                                           # Land to Lease In

    Fti = [ randrange(0,N) if a>0 else 0 for a in A0 ]#np.random.randint(40,size=N)                                           # Food to Trade In
    Lti = [ randrange(0,N) if a>0 else 0 for a in A1 ]#np.random.randint(40,size=N)                                           # Land to Trade In

    return [Flo, Llo, Fto, Lto, Fli, Lli, Fti, Lti]


# Compute successful deals, i.e who's offers accepted by who
def Deals(Flo, Llo, Fli, Lli):
    Deals = list(range(0,100))
    shuffle(Deals)

    return Deals #list of who's deal accepted by who = [1,5,4] => 1 trades with self(=no trade), 2's offer accepted by 5, 3's offer accepted by 4


# Actions 
def Allocate(B0, B1):
    Fc = [ randrange(0,a) if a>0 else 0 for a in B0 ]                  # Food for Consumption
    Lw = [ randrange(0,a) if a>0 else 0 for a in B1 ]                  # Land for Work

    return [Fc, Lw]


# Compute after deals assets of agents, alive-dead state given current state, actions, deals, survival
def DealsUpdate(A0, A1, Flo, Llo, Fto, Lto, Fli, Lli, Fti, Lti, Trades, Leases):
    B0 = np.empty(N, dtype=int)
    B1 = np.empty(N, dtype=int)
    C0 = np.empty(N, dtype=int)
    C1 = np.empty(N, dtype=int)

    for i in xrange(len(A0)):
        if A0[i]>0:
            if i<Leases[i]:
                # Asset value after lease period starts
                B0[i] = A0[i] + Fli[i]
                B1[i] = A1[i] + Lli[i]
                B0[Leases[i]] = A0[Leases[i]] - Fli[i]
                B1[Leases[i]] = A1[Leases[i]] - Lli[i]

                # Asset value after lease period over 
                C0[i] = B0[i] - Flo[i]
                C1[i] = B1[i] - Llo[i]
                C0[Leases[i]] = B0[i] + Llo[i]
                C1[Leases[i]] = B0[i] + Llo[i]

            else: 
                B0[i] = A0[i]
                B1[i] = A1[i]
                C0[i] = A0[i]
                C1[i] = A1[i]

                if i<Trades[i]:
                    B0[i] = B0[i] + (Fti[i]-Fto[i])
                    B1[i] = B1[i] + (Lti[i]-Lto[i])
                    B0[Trades[i]] = B0[Trades[i]] - (Fti[i]-Fto[i])
                    B1[Trades[i]] = B1[Trades[i]] - (Lti[i]-Lto[i])
        else:
            B0[i] = A0[i]
            B1[i] = A1[i]
            C0[i] = A0[i]
            C1[i] = A1[i]
            
    return [B0, B1, C0, C1]


def StateUpdate(C0, C1, Fc, Lw):
    for i in xrange(len(C0)):
        if Fc[i] > kfs:
            C0[i] = C0[i] - Fc[i] + klf*Lw[i]
        else:
            C0[i] = 0
            C1[i] = 0

    return [C0,C1]


# Run Simulation
if __name__ == '__main__':
    # Import Modules
    from timer import Timer

    # Setup Initial Agent State
    N = 100                             # Sample Size
    klf = 1                             # Land Worked on to Food Produced Ratio
    kfs = 2                             # Food Consumed to Survival Ratio
    A0 = np.random.randint(100,size=N)  # Initial Food Allocation(Random)
    A1 = np.random.randint(100,size=N)  # Initial Land Allocation(Random)

    while(len(filter(lambda a: a>0, A0))>0):  # is anybody out there ?
        # Bidding Round
        Flo, Llo, Fto, Lto, Fli, Lli, Fti, Lti = Bid(A0,A1)

        # Successful Lease Deals
        Leases = Deals(Flo, Llo, Fli, Lli)

        # Successful Trade Deals
        Trades = Deals(Fto, Lto, Fti, Lti)

        # Updating Agent Assets based on Deals
        B0,B1,C0,C1  = DealsUpdate(A0, A1, Flo, Llo, Fto, Lto, Fli, Lli, Fti, Lti, Trades, Leases)

        # Agent Allocate Food for Consumption, Land to work on 
        Fc, Lw = Allocate(B0,B1)

        # Update System State
        A0, A1 = StateUpdate(C0,C1,Fc,Lw)

        # Debugging
        print "Population:", 100*len(filter(lambda a: a>0, A0))/len(A0), "%"

        # Environment Parameter Visualisation[Population, Assets Distribution]
        plt.plot(A0)
        plt.ylabel('Food Distribution')
        plt.show()
