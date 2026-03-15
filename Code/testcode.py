import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#%%
# Load the data
data = pd.read_csv(
    '/Users/amelialuongo/Desktop/comp bme/Module-2-Epidemics-SIR-Modeling/Data/mystery_virus_daily_active_counts_RELEASE#2.csv',
    parse_dates=['date']
)

# Initial conditions
I0 = data_I[0]
E0 = 0
R0 = 1.835
S0 = N - I0

#%%
# Euler SEIR function
def euler_seir(beta, sigma, gamma, S0, E0, I0, R0, timepoints, N, dt=1):

    S = [S0]
    E = [E0]
    I = [I0]
    R = [R0]

    for t in range(len(timepoints)-1):

        dS = -beta * S[-1] * I[-1] / N
        dE = beta * S[-1] * I[-1] / N - sigma * E[-1]
        dI = sigma * E[-1] - gamma * I[-1]
        dR = gamma * I[-1]

        S_new = S[-1] + dS * dt
        E_new = E[-1] + dE * dt
        I_new = I[-1] + dI * dt
        R_new = R[-1] + dR * dt

        S.append(S_new)
        E.append(E_new)
        I.append(I_new)
        R.append(R_new)

    return np.array(S), np.array(E), np.array(I), np.array(R)

#%%
# Observed infected data
data_I = data["active reported daily cases"].to_numpy()
timepoints = data["day"].to_numpy()

# Population size (larger so infections aren't capped)
N = 17000

# Initial conditions
I0 = data_I[0]
E0 = 0
R0 = 1.835
S0 = N - I0

#%%
# Parameter ranges
beta_range = np.linspace(0.01, 1, 30)
sigma_range = np.linspace(0.01, 1, 30)
gamma_range = np.linspace(0.01, 1, 30)

best_beta = None
best_sigma = None
best_gamma = None
best_SSE = np.inf

# Grid search
for b in beta_range:
    for s in sigma_range:
        for g in gamma_range:

            S, E, I, R = euler_seir(b, s, g, S0, E0, I0, R0, timepoints, N)

            I_model = I[:len(data_I)]

            sse = np.sum((data_I - I_model)**2)

            if sse < best_SSE:
                best_SSE = sse
                best_beta = b
                best_sigma = s
                best_gamma = g

#%%
print("Best beta:", best_beta)
print("Best sigma:", best_sigma)
print("Best gamma:", best_gamma)
print("Best SSE:", best_SSE)

#%%
# Predict future outbreak
future_days = 150
timepoints_future = np.arange(0, future_days)

S, E, I, R = euler_seir(
    best_beta,
    best_sigma,
    best_gamma,
    S0,
    E0,
    I0,
    R0,
    timepoints_future,
    N
)

#%%
# Peak analysis
peak_height = np.max(I)
peak_day = np.argmax(I)

print("Peak infections:", peak_height)
print("Peak occurs on day:", peak_day)

#%%
# Plot results
plt.figure()

plt.scatter(
    data["day"],
    data["active reported daily cases"],
    label="Real Data"
)

plt.plot(
    timepoints_future,
    I,
    label="SEIR Model"
)

plt.xlabel("Days")
plt.ylabel("Active Infections")
plt.title("SEIR Model Fit")
plt.legend()

plt.show()