
from datetime import date
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# AI Usage Statement: ChatGPT 5.2 for debugging and error checking 
# Load the data
data = pd.read_csv('C:\\Users\\ajq2af\\OneDrive - University of Virginia\\Documents\\UVA\\BME 2315\\module2\\Module-2-Epidemics-SIR-Modeling\\Data\\mystery_virus_daily_active_counts_RELEASE#1.csv', parse_dates=['date'], header=0, index_col=None)

# Define a class to represent the virus data
class Virus:
    data = []

    def __init__(self, day: int, active_cases: int):
        self.day = day
        self.active_cases = active_cases
        Virus.data.append(self)

    def __repr__(self):
        return (
        f"{self.day}: (Active Cases={self.active_cases})"
        )
    def get_active_cases(self):
        return self.active_cases
    
    @classmethod
    def instantiate_from_csv(cls, filename: str):
        with open(filename, encoding="utf8") as f:
            reader = pd.read_csv(f)
            for index, row in reader.iterrows():
                day = row['day']
                active_cases = row['active_cases']
                Virus(day, active_cases)

print(data)

plt.figure(figsize=(10, 6))
plt.plot(data['day'], data['active reported daily cases'], marker='o')
plt.title('Active Cases of Mystery Virus Over Time')
plt.xlabel('Day')
plt.ylabel('Number of Active Cases')
plt.xticks(rotation=45)
plt.grid()
plt.tight_layout()
plt.show()

#calculate the R0 value from early data csv file (first 45 days)
def eponential_growth(t,r):
    return np.exp(r*t)

x_data = data['day'].values.astype(float)
y_data = data['active reported daily cases'].values.astype(float)
popt, pcov = curve_fit(eponential_growth, x_data, y_data)
r_fit = popt[0]

D = 5 # estimated infection period from data 

r0 = np.exp(r_fit * D)

print("Estimated R0 value:", r0)
# add the fitted curve to the plot
y_fitted = eponential_growth(x_data, r_fit)
# plot fitted curve and actual data
plt.figure(figsize=(10, 6))
plt.plot(x_data, y_data, label=' Actual Data')
plt.plot(x_data, y_fitted, color = "red", label = "Estimated Curve")
plt.title('Exponential Growth Fit to Active Cases')
plt.xlabel('Day')
plt.ylabel('Number of Active Cases')
plt.xticks(rotation=45)
plt.grid()
plt.legend()
plt.tight_layout()
plt.show()