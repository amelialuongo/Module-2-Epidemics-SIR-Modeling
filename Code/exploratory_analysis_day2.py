#%%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
#%%
# Load the data
data = pd.read_csv('C:\\Users\\ajq2af\\OneDrive - University of Virginia\\Documents\\UVA\\BME 2315\\module2\\Module-2-Epidemics-SIR-Modeling\\Data\\mystery_virus_daily_active_counts_RELEASE#1.csv', parse_dates=['date'], header=0, index_col=None)
#%%
# We have day number, date, and active cases. We can use the day number and active cases to fit an exponential growth curve to estimate R0.
# Let's define the exponential growth function
def exponential_growth(t, r):
    return np.exp(r * t)

# Fit the exponential growth model to the data. 
# We'll use a handy function from scipy called CURVE_FIT that allows us to fit any given function to our data. 
# We will fit the exponential growth function to the active cases data. HINT: Look up the documentation for curve_fit to see how to use it.

# Approximate R0 using this fit

# Add the fit as a line on top of your scatterplot.

#%% Euler's Method Approximation of SEIR
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
data = pd.read_csv('C:\\Users\\ajq2af\\OneDrive - University of Virginia\\Documents\\UVA\\BME 2315\\module2\\Module-2-Epidemics-SIR-Modeling\\Data\\mystery_virus_daily_active_counts_RELEASE#1.csv', parse_dates=['date'], header=0, index_col=None)

def euler_seir(beta, sigma, gamma, S0, E0, I0, R0, timepoints, N):  # function with inputs 
   # empty lists for S, E, I, R
    S = [] 
    E = []
    I = []
    R = []

    # set first item in each list to initial conditions 
    S.append(S0)
    E.append(E0)   
    I.append(I0)
    R.append(R0)

    # loop through timepoints to calculate the changes in S, E, I, R
    for t in timepoints:
        # derivatives for SEIR at time t
        dS = -beta * S[-1] * I[-1] / N
        dE = beta * S[-1] * I[-1] / N - sigma * E[-1]
        dI = sigma * E[-1] - gamma * I[-1]
        dR = gamma * I[-1]

        # update S, E, I, R using Euler's method
        S_new = S[-1] + dS
        E_new = E[-1] + dE
        I_new = I[-1] + dI
        R_new = R[-1] + dR

        # append new values to lists
        S.append(S_new)
        E.append(E_new)
        I.append(I_new)
        R.append(R_new)
        
    return S, E, I, R


timepoints = data["day"].to_numpy() # timepoints are the day from the data
beta = 0.3 # I just put a random value here for now idk if that's right 
sigma = 0.1 # same here
gamma = 0.05 # same here 
# initial conditions from the data
N = 45
I0 = 1
S0 = 44
E0 = 0
R0 = 0
S, E, I, R = euler_seir(beta, sigma, gamma, S0, E0, I0, R0, timepoints, N)

print(S)
print(E)    
print(I)
print(R)

# %%
