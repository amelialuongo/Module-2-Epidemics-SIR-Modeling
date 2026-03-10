# ChatGPT was used on this assignment - mostly for fixing errors

#%%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
#%%
# Load the data
data = pd.read_csv('/Users/amelialuongo/Desktop/comp bme/Module-2-Epidemics-SIR-Modeling/Data/mystery_virus_daily_active_counts_RELEASE#2.csv', parse_dates=['date'], header=0, index_col=None)
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
data = pd.read_csv('/Users/amelialuongo/Desktop/comp bme/Module-2-Epidemics-SIR-Modeling/Data/mystery_virus_daily_active_counts_RELEASE#2.csv', parse_dates=['date'], header=0, index_col=None)

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
    for t in range(len(timepoints) - 1):
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
beta = 0.2 # I just put a random value here for now idk if that's right 
sigma = 0.083 # 12 days of incubation period
gamma = 0.14 # 7 days of infection 
# initial conditions from the data
N = 70
I0 = 1
S0 = 44
E0 = 0
R0 = 0
S, E, I, R = euler_seir(beta, sigma, gamma, S0, E0, I0, R0, timepoints, N)

# print(S)
# print(E)    
# print(I)
# print(R)

# %%
# Observed infected data
data_I = data["active reported daily cases"].to_numpy()

# parameter ranges for beta sigma and gamma
beta_range = np.linspace(0.01, 1, 30)
sigma_range = np.linspace(0.01, 1, 30)
gamma_range = np.linspace(0.01, 1, 30)

# create an empty list to store SSE values
SSE = []

# record best parameters
best_beta = None
best_sigma = None
best_gamma = None
best_SSE = np.inf

# Loop through parameter ranges
for b in beta_range:
    for s in sigma_range:
        for g in gamma_range:

            # Run SEIR model
            S, E, I, R = euler_seir(b, s, g, S0, E0, I0, R0, timepoints, N)

            # Convert model I values to numpy array and trim to data length
            I_model = np.array(I[:len(data_I)])

            # Calculate SSE
            sse = np.sum((data_I - I_model) ** 2)

            # Append to SSE list
            SSE.append(sse)

            # Check if this is the best fit
            if sse < best_SSE:
                best_SSE = sse
                best_beta = b
                best_sigma = s
                best_gamma = g

# Print results
print("best_beta:", best_beta)
print("best_sigma:", best_sigma)
print("best_gamma:", best_gamma)
print("SSE:", best_SSE)


#%% use the best parameters to predict the future
future_days = 150
timepoints_future = np.arange(0, future_days)

S, E, I, R = euler_seir(best_beta, best_sigma, best_gamma,
                        S0, E0, I0, R0,
                        timepoints_future, N)

# Convert to numpy array
I = np.array(I)

# peak height of infections
peak_height = np.max(I)

# what day does the peak occur
peak_day = np.argmax(I)

print("Peak infections:", peak_height)
print("Peak occurs on day:", peak_day)

plt.figure()

# add the real data to the plot
plt.scatter(data["day"], data["active reported daily cases"], label="Real Data")

# add the model prediction to the plot
plt.plot(timepoints_future, I, label="SEIR Model")

plt.xlabel("Days")
plt.ylabel("Active Infections")
plt.title("SEIR Model")
plt.legend()

plt.show()