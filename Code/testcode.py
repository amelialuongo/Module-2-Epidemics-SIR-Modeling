import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = pd.read_csv(
    r'C:\Users\ajq2af\OneDrive - University of Virginia\Documents\UVA\BME 2315\module2\Module-2-Epidemics-SIR-Modeling\Data\mystery_virus_daily_active_counts_RELEASE#2.csv',
    parse_dates=['date']
)

def euler_seir(beta, sigma, gamma, S0, E0, I0, R_init, timepoints, N):
    S = [S0]
    E = [E0]
    I = [I0]
    R = [R_init]

    for _ in range(len(timepoints) - 1):
        dS = -beta * S[-1] * I[-1] / N
        dE = beta * S[-1] * I[-1] / N - sigma * E[-1]
        dI = sigma * E[-1] - gamma * I[-1]
        dR = gamma * I[-1]

        S_new = S[-1] + dS
        E_new = E[-1] + dE
        I_new = I[-1] + dI
        R_new = R[-1] + dR

        # prevent tiny negative values from numerical issues
        S.append(max(S_new, 0))
        E.append(max(E_new, 0))
        I.append(max(I_new, 0))
        R.append(max(R_new, 0))

    return np.array(S), np.array(E), np.array(I), np.array(R)
print("ji")
timepoints = data["day"].to_numpy()
data_I = data["active reported daily cases"].to_numpy()

# Use first observed value as initial infected
I0 = float(data_I[0])
R_init = 0

# Choose N large enough to allow the outbreak shape
# If assignment requires N=45, keep that, but fit may still be poor.
N = 45

best_beta = None
best_sigma = None
best_gamma = None
best_E0 = None
best_SSE = np.inf

beta_range = np.linspace(0.05, 1.5, 40)
sigma_range = np.linspace(0.05, 0.5, 30)
gamma_range = np.linspace(0.05, 0.5, 30)
E0_range = np.arange(0, 16, 1)

for b in beta_range:
    for s in sigma_range:
        for g in gamma_range:
            for E0 in E0_range:
                S0 = N - I0 - E0 - R_init

                if S0 < 0:
                    continue

                S, E, I, R = euler_seir(b, s, g, S0, E0, I0, R_init, timepoints, N)

                I_model = I[:len(data_I)]
                sse = np.sum((data_I - I_model) ** 2)

                if sse < best_SSE:
                    best_SSE = sse
                    best_beta = b
                    best_sigma = s
                    best_gamma = g
                    best_E0 = E0

print("best_beta:", best_beta)
print("best_sigma:", best_sigma)
print("best_gamma:", best_gamma)
print("best_E0:", best_E0)
print("best_SSE:", best_SSE)

S0_best = N - I0 - best_E0 - R_init
S, E, I, R = euler_seir(best_beta, best_sigma, best_gamma,
                        S0_best, best_E0, I0, R_init,
                        timepoints, N)

plt.figure()
plt.scatter(data["day"], data["active reported daily cases"], label="Real Data")
plt.plot(timepoints, I, label="Best-fit SEIR Model")
plt.xlabel("Days")
plt.ylabel("Active Infections")
plt.title("SEIR Model Fit")
plt.legend()
plt.show()