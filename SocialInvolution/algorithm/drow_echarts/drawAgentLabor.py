import pandas as pd
import matplotlib.pyplot as plt
import glob
import numpy as np

# Specify the directory and file pattern
directory = "2024-12-13-全部-订单0.15-30天"
file_pattern = f"{directory}/deliver*.csv"

# Read all CSV files
file_paths = glob.glob(file_pattern)
data_list = []

for file in file_paths:
    df = pd.read_csv(file)
    data_list.append(df)

# Combine all data to calculate daily differences
all_data = pd.concat(data_list, axis=0, keys=range(len(data_list)), names=['Agent', 'Index'])

# Calculate daily differences for each agent
def calculate_daily_diff(group):
    group['dis_diff'] = group['dis'].diff().fillna(0)
    group['money_diff'] = group['money'].diff().fillna(0)
    return group

all_data = all_data.groupby('Agent').apply(calculate_daily_diff)

# Calculate averages across agents
daily_avg = all_data.groupby('day').agg({
    'dis': 'mean',
    'money': 'mean',
    'dis_diff': 'mean',
    'money_diff': 'mean'
})
daily_avg['money/dis'] = daily_avg['money'] / daily_avg['dis'].replace(0, np.nan)

# Plotting with multiple y-axes
fig, ax1 = plt.subplots(figsize=(12, 6))

# Plot Average Daily Distance (dis_diff)
ax1.set_xlabel('Day')
ax1.set_ylabel('Average Daily Distance (dis_diff)', color='tab:blue')
ax1.plot(daily_avg.index, daily_avg['dis_diff'], label='Average Daily Distance (dis_diff)', color='tab:blue')
ax1.tick_params(axis='y', labelcolor='tab:blue')

# Create a second y-axis for Average Daily Money (money_diff)
ax2 = ax1.twinx()
ax2.set_ylabel('Average Daily Money (money_diff)', color='tab:green')
ax2.plot(daily_avg.index, daily_avg['money_diff'], label='Average Daily Money (money_diff)', color='tab:green')
ax2.tick_params(axis='y', labelcolor='tab:green')

# Create a third y-axis for Average Money per Distance (money/dis)
ax3 = ax1.twinx()
ax3.spines['right'].set_position(('outward', 60))  # Offset the third y-axis
ax3.set_ylabel('Average Money per Distance (money/dis)', color='tab:red')
ax3.plot(daily_avg.index, daily_avg['money/dis'], label='Average Money per Distance (money/dis)', color='tab:red')
ax3.tick_params(axis='y', labelcolor='tab:red')

# Add a title and grid
fig.suptitle('Agent Simulation Averages with Daily Differences')
ax1.grid()

# Show the plot
fig.tight_layout()
plt.show()
