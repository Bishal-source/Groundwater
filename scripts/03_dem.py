"""
03_dem.py

Groundwater Potential Mapping Project

Purpose:
Load the Digital Elevation Model (DEM) and calculate
basic elevation statistics.
"""

import os
import sys

# ==========================================================
# Add Project Root to Python Path
# ==========================================================

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

# ==========================================================
# Import Configuration
# ==========================================================

from config import (
    STATE_NAME,
    DEM_DATASET
)

# ==========================================================
# Import Utility Functions
# ==========================================================

from utils import (
    initialize_ee,
    print_header,
    get_state_boundary,
    load_dem,
    image_statistics
)


def main():

    # ------------------------------------------------------
    # Initialize Earth Engine
    # ------------------------------------------------------

    initialize_ee()

    # ------------------------------------------------------
    # Header
    # ------------------------------------------------------

    print_header("STEP 03 : DIGITAL ELEVATION MODEL")

    # ------------------------------------------------------
    # Load Study Area
    # ------------------------------------------------------

    boundary = get_state_boundary()

    # ------------------------------------------------------
    # Load DEM
    # ------------------------------------------------------

    dem = load_dem(
        boundary,
        DEM_DATASET
    )

    # ------------------------------------------------------
    # Calculate Statistics
    # ------------------------------------------------------

    stats = image_statistics(
        dem,
        boundary.geometry(),
        scale=30
    )

    # ------------------------------------------------------
    # Display Results
    # ------------------------------------------------------

    print(f"Study Area : {STATE_NAME}\n")

    print("Elevation Statistics")
    print("-" * 35)

    print(f"Minimum Elevation : {stats['elevation_min']:.2f} m")
    print(f"Maximum Elevation : {stats['elevation_max']:.2f} m")
    print(f"Mean Elevation    : {stats['elevation_mean']:.2f} m")

    print("\n✓ DEM loaded successfully.")


if __name__ == "__main__":
    main()