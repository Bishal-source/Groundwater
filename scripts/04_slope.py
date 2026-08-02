"""
Generate Slope Map
Groundwater Potential Mapping Project
"""

import os
import sys
import ee

# ----------------------------------------
# Add project root to Python path
# ----------------------------------------

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from config import DEM_DATASET
from utils import (
    initialize_ee,
    print_header,
    get_state_boundary,
    load_dem,
    image_statistics
)


def main():

    # Initialize Earth Engine
    initialize_ee()

    print_header("STEP 04 : SLOPE MAP")

    # Load Haryana Boundary
    haryana = get_state_boundary()

    # Load DEM
    dem = load_dem(
        haryana,
        DEM_DATASET
    )

    # Generate Slope
    slope = ee.Terrain.slope(dem)

    # Calculate Statistics
    stats = image_statistics(
        slope,
        haryana.geometry()
    )

    print("Study Area : Haryana\n")

    print("Slope Statistics")
    print("-" * 30)

    print(f"Minimum Slope : {stats['slope_min']:.2f}°")
    print(f"Maximum Slope : {stats['slope_max']:.2f}°")
    print(f"Mean Slope    : {stats['slope_mean']:.2f}°")

    print("\n✓ Slope map generated successfully.")


if __name__ == "__main__":
    main()