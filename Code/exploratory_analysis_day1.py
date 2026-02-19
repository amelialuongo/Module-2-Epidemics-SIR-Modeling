#%%
from datetime import date

import pandas as pd
import matplotlib.pyplot as plt


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
#%% Make a plot of the active cases over time
plt.figure(figsize=(10, 6))
plt.plot(data['day'], data['active reported daily cases'], marker='o')
plt.title('Active Cases of Mystery Virus Over Time')
plt.xlabel('Day')
plt.ylabel('Number of Active Cases')
plt.xticks(rotation=45)
plt.grid()
plt.tight_layout()
plt.show()
