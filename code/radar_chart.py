import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import pi

# Load data from CSV file
def load_data(file_path):
    data = pd.read_csv(file_path, index_col=0)
    return data

# Function to create a radar chart
def create_radar_chart(data, title, save_path):
    categories = list(data.index)
    num_vars = len(categories)

    # Compute the angle for each axis
    angles = [n / float(num_vars) * 2 * pi for n in range(num_vars)]
    angles += angles[:1]

    # Initialize the radar chart
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

    # Draw one line per network
    for network in data.columns:
        values = data[network].tolist()
        values += values[:1]
        ax.plot(angles, values, label=network)
        ax.fill(angles, values, alpha=0.1)

    # Add labels for metrics
    ax.set_yticks(np.arange(0, 1.1, 0.1))
    ax.set_yticklabels([f'{x:.1f}' for x in np.arange(0, 1.1, 0.1)], color="grey", size=8)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=10)

    # Add a title and legend
    ax.set_title(title, size=15, color='darkblue', pad=20)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))

    # Save the chart
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()

# Main script
def main():
    file_path = "radar.csv"  # path to  CSV file
    save_path = "../images/radar_chart.png"  # save path for the plot
    data = load_data(file_path)
    create_radar_chart(data, "P2P Network Metrics Radar Chart", save_path)

if __name__ == "__main__":
    main()
