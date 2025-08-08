# -*- coding: utf-8 -*-
"""
Created on Thu Aug  7 22:11:32 2025

@author: Clement Hardy + Help from AI
"""

#%% Setup and imports
import numpy as np
import matplotlib.pyplot as plt
import os
import rasterio
import pandas as pd

# User-defined input folder containing the biomass rasters
input_folder = r"D:\OneDrive - UQAM\1 - Projets\Post-Doc - Test effet Eclaircie Commerciale LANDIS-II\SimEffectEC\output\biomass"  # Change this path as needed

# Verify folder exists
if not os.path.exists(input_folder):
    print(f"Warning: Input folder does not exist: {input_folder}")
else:
    print(f"Input folder: {input_folder}")

# Define timesteps (0, 5, 10, ..., 100)
timesteps = list(range(0, 101, 5))
print(f"Timesteps to analyze: {timesteps}")


#%% Read biomass rasters and calculate ANPP
print("Reading biomass rasters and calculating ANPP...")

# Storage for results
anpp_data = {
    'timestep': [],
    'anpp_area0': [],  # Management area 0 (row 0)
    'anpp_area1': []   # Management area 1 (row 1)
}

# Read biomass data for each timestep
biomass_data = {}

for timestep in timesteps:
    filename = f"biomass-TotalBiomass-{timestep}.img"
    filepath = os.path.join(input_folder, filename)

    if os.path.exists(filepath):
        try:
            # Read raster using rasterio
            with rasterio.open(filepath) as src:
                biomass_array = src.read(1)  # Read first (and likely only) band
                biomass_data[timestep] = biomass_array
                print(f"✓ Read {filename}: shape {biomass_array.shape}")
        except Exception as e:
            print(f"✗ Could not open {filename}: {e}")
    else:
        print(f"✗ File not found: {filename}")

print(f"Successfully read {len(biomass_data)} biomass rasters")



#%% Calculate ANPP for each timestep interval
print("Calculating ANPP for each management area...")

for i in range(1, len(timesteps)):
    current_timestep = timesteps[i]
    previous_timestep = timesteps[i-1]

    if current_timestep in biomass_data and previous_timestep in biomass_data:
        current_biomass = biomass_data[current_timestep]
        previous_biomass = biomass_data[previous_timestep]

        # Calculate biomass change (ANPP) for each pixel
        biomass_change = current_biomass - previous_biomass

        # Extract data for each management area (row)
        # Row 0 = Management area 0 (not affected)
        # Row 1 = Management area 1 (affected)
        area0_change = biomass_change[0, :]  # First row
        area1_change = biomass_change[1, :]  # Second row

        # Calculate average ANPP for each area
        # Convert to annual values (divide by 5 since timesteps are 5 years apart)
        avg_anpp_area0 = np.mean(area0_change) / 5
        avg_anpp_area1 = np.mean(area1_change) / 5

        # Store results
        anpp_data['timestep'].append(current_timestep)
        anpp_data['anpp_area0'].append(avg_anpp_area0)
        anpp_data['anpp_area1'].append(avg_anpp_area1)

        print(f"Timestep {current_timestep}: ANPP Area0={avg_anpp_area0:.2f}, Area1={avg_anpp_area1:.2f}")

print(f"Calculated ANPP for {len(anpp_data['timestep'])} time intervals")


#%% Create DataFrame and display summary statistics
print("Creating summary statistics...")

# Create DataFrame for easier analysis
df_anpp = pd.DataFrame(anpp_data)
print("\nANPP Summary Statistics:")
print(df_anpp.describe())

print(f"\nAverage ANPP over entire simulation period:")
print(f"Not affected (Area 0): {df_anpp['anpp_area0'].mean():.2f}")
print(f"Affected (Area 1): {df_anpp['anpp_area1'].mean():.2f}")
print(f"Difference: {df_anpp['anpp_area1'].mean() - df_anpp['anpp_area0'].mean():.2f}")


#%% Plot ANPP comparison
print("Creating ANPP comparison plot...")

plt.figure(figsize=(12, 8))

# Plot ANPP for both management areas
plt.plot(anpp_data['timestep'], anpp_data['anpp_area0'], 
         marker='o', linewidth=2, markersize=6, 
         label='Not affected by Commercial Thinning', color='#a3be8c')

plt.plot(anpp_data['timestep'], anpp_data['anpp_area1'], 
         marker='s', linewidth=2, markersize=6, 
         label='Affected by Commercial Thinning', color='#ebcb8b')

# Customize plot
plt.xlabel('Simulation Year', fontsize=12)
plt.ylabel('Average Annual Net Primary Productivity (ANPP) (g/m2)', fontsize=12)
plt.title('ANPP Comparison Between Management Areas', fontsize=14, fontweight='bold')
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)

# Set axis limits and ticks
plt.xlim(min(anpp_data['timestep'])-2, max(anpp_data['timestep'])+2)
plt.xticks(range(5, 101, 10))

# Add horizontal line at y=0 for reference
plt.axhline(y=0, color='black', linestyle='--', alpha=0.5)

plt.tight_layout()
plt.show()

# Save plot
plot_path = os.path.join(input_folder, "ANPP_comparison.png")
plt.savefig(plot_path, dpi=300, bbox_inches='tight')
print(f"Plot saved: {plot_path}")

#%% Export results to CSV
print("Exporting results to CSV...")

# Save results to CSV file
csv_path = os.path.join(input_folder, "ANPP_results.csv")
df_anpp.to_csv(csv_path, index=False)
print(f"Results exported to: {csv_path}")

# Display final summary
print("\n" + "="*50)
print("ANALYSIS COMPLETE")
print("="*50)
print(f"Files analyzed: {len(biomass_data)} biomass rasters")
print(f"Time intervals calculated: {len(anpp_data['timestep'])}")
print(f"Results saved to: {csv_path}")
print(f"Plot saved to: {plot_path}")
