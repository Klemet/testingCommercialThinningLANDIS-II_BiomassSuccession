# -*- coding: utf-8 -*-
"""
Created on Thu Aug  7 21:49:20 2025

@author: Clement
"""

#%% Setup and imports
import numpy as np
import random
import os

# User-defined output folder
output_folder = r"D:\OneDrive - UQAM\1 - Projets\Post-Doc - Test effet Eclaircie Commerciale LANDIS-II\SimEffectEC\SimEffectEC-Rep1"  # Change this path as needed

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Set random seed for reproducibility (optional)
random.seed(42)
np.random.seed(42)

print(f"Output folder: {output_folder}")


#%% Generate Initial Community Raster
print("Generating initial community raster...")

# Create raster: 2 rows x 10000 columns, values from 1 to 10001
initial_community = np.zeros((2, 10000), dtype=np.int32)
values = np.arange(1, 10001)

# Both rows have the same values (aligned columns)
initial_community[0, :] = values
initial_community[1, :] = values

# Save as ASCII raster
initial_community_path = os.path.join(output_folder, "initial_community.tif")
with open(initial_community_path, 'w') as f:
    f.write("ncols 10000\n")
    f.write("nrows 2\n")
    f.write("xllcorner 0\n")
    f.write("yllcorner 0\n")
    f.write("cellsize 1\n")
    f.write("NODATA_value -9999\n")

    for row in initial_community:
        f.write(" ".join(map(str, row)) + "\n")

print(f"Initial community raster saved: {initial_community_path}")


#%% Generate Ecoregion Raster
print("Generating ecoregion raster...")

# Create raster: 2 rows x 10000 columns, all values = 328
ecoregion = np.full((2, 10000), 328, dtype=np.int32)

# Save as ASCII raster
ecoregion_path = os.path.join(output_folder, "ecoregion.tif")
with open(ecoregion_path, 'w') as f:
    f.write("ncols 10000\n")
    f.write("nrows 2\n")
    f.write("xllcorner 0\n")
    f.write("yllcorner 0\n")
    f.write("cellsize 1\n")
    f.write("NODATA_value -9999\n")

    for row in ecoregion:
        f.write(" ".join(map(str, row)) + "\n")

print(f"Ecoregion raster saved: {ecoregion_path}")

#%% Generate Management Area Raster
print("Generating management area raster...")

# Create raster: first row = 0, second row = 1
management_area = np.zeros((2, 10000), dtype=np.int32)
management_area[0, :] = 0  # First row
management_area[1, :] = 1  # Second row

# Save as ASCII raster
management_area_path = os.path.join(output_folder, "management_area.tif")
with open(management_area_path, 'w') as f:
    f.write("ncols 10000\n")
    f.write("nrows 2\n")
    f.write("xllcorner 0\n")
    f.write("yllcorner 0\n")
    f.write("cellsize 1\n")
    f.write("NODATA_value -9999\n")

    for row in management_area:
        f.write(" ".join(map(str, row)) + "\n")

print(f"Management area raster saved: {management_area_path}")


#%% Generate Management Area Raster
print("Generating management area raster...")

# Create raster: first row = 0, second row = 1
management_area = np.zeros((2, 10000), dtype=np.int32)
management_area[0, :] = 0  # First row
management_area[1, :] = 1  # Second row

# Save as ASCII raster
management_area_path = os.path.join(output_folder, "management_area.tif")
with open(management_area_path, 'w') as f:
    f.write("ncols 10000\n")
    f.write("nrows 2\n")
    f.write("xllcorner 0\n")
    f.write("yllcorner 0\n")
    f.write("cellsize 1\n")
    f.write("NODATA_value -9999\n")

    for row in management_area:
        f.write(" ".join(map(str, row)) + "\n")

print(f"Management area raster saved: {management_area_path}")

#%% Generate Initial Community Text File
print("Generating initial community text file...")

# Species pool
species_pool = [
    "ABIE.BAL", "ACER.RUB", "ACER.SAH", "BETU.ALL", "BETU.PAP", 
    "FAGU.GRA", "LARI.LAR", "LARI.HYB", "PICE.GLA", "PICE.MAR", 
    "PICE.RUB", "PINU.BAN", "PINU.RES", "PINU.STR", "POPU.TRE", 
    "POPU.HYB", "QUER.RUB", "THUJ.SPP.ALL", "TSUG.CAN"
]

# Generate compositions for each map code (1 to 10000)
compositions = {}

for map_code in range(1, 10001):
    # Random number of species (2-6)
    num_species = random.randint(2, 6)

    # Randomly select species
    selected_species = random.sample(species_pool, num_species)

    composition = {}
    for species in selected_species:
        # Random number of age cohorts (1-3)
        num_cohorts = random.randint(1, 3)

        # Random ages for cohorts (10-90, in 10-year timesteps)
        ages = []
        for _ in range(num_cohorts):
            age = random.randint(1, 8) * 10  # This gives 10, 20, 30, ..., 90
            ages.append(age)

        # Remove duplicates and sort
        ages = sorted(list(set(ages)))
        composition[species] = ages

    compositions[map_code] = composition

# Write to text file
initial_communities_path = os.path.join(output_folder, "initial_communities.txt")
with open(initial_communities_path, 'w') as f:
    f.write('LandisData "Initial Communities"\n\n')
    f.write('MapCode 0\n\n')

    for map_code in range(1, 10001):
        f.write(f'MapCode {map_code}\n')

        for species, ages in compositions[map_code].items():
            age_str = "       ".join(map(str, ages))
            f.write(f'{species}       {age_str}\n')

        f.write('\n')

print(f"Initial communities text file saved: {initial_communities_path}")
print("All files generated successfully!")

#%% Verify file creation
print("Verifying created files...")

files_to_check = [
    "initial_community.tif",
    "ecoregion.tif", 
    "management_area.tif",
    "initial_communities.txt"
]

for filename in files_to_check:
    filepath = os.path.join(output_folder, filename)
    if os.path.exists(filepath):
        size = os.path.getsize(filepath)
        print(f"✓ {filename}: {size:,} bytes")
    else:
        print(f"✗ {filename}: NOT FOUND")

print(f"\nAll files saved in: {output_folder}")

