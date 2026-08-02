"""
04_slope.py

Groundwater Potential Mapping Project

Purpose:
Generate the slope layer from the DEM and calculate
basic slope statistics.
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
    calculate_slope,
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

    print_header("STEP 04 : SLOPE MAP")

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
    # Generate Slope
    # ------------------------------------------------------

    slope = calculate_slope(dem)

    # ------------------------------------------------------
    # Calculate Statistics
    # ------------------------------------------------------

    stats = image_statistics(
        slope,
        boundary.geometry(),
        scale=30
    )

    # ------------------------------------------------------
    # Display Results
    # ------------------------------------------------------

    print(f"Study Area : {STATE_NAME}\n")

    print("Slope Statistics")
    print("-" * 35)

    print(f"Minimum Slope : {stats['slope_min']:.2f}°")
    print(f"Maximum Slope : {stats['slope_max']:.2f}°")
    print(f"Mean Slope    : {stats['slope_mean']:.2f}°")

    print("\n✓ Slope map generated successfully.")


if __name__ == "__main__":
    main()