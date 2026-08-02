"""
Generate Digital Elevation Model (DEM)
Groundwater Potential Mapping Project
"""

import os
import sys

# -----------------------------------------
# Add project root to Python path
# -----------------------------------------

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

    print_header("STEP 03 : DIGITAL ELEVATION MODEL")

    # Load Haryana Boundary
    haryana = get_state_boundary()

    # Load DEM
    dem = load_dem(
        haryana,
        DEM_DATASET
    )

    # Calculate Statistics
    stats = image_statistics(
        dem,
        haryana.geometry()
    )

    print("Study Area : Haryana\n")

    print("Elevation Statistics")
    print("-" * 30)

    print(f"Minimum Elevation : {stats['elevation_min']:.2f} m")
    print(f"Maximum Elevation : {stats['elevation_max']:.2f} m")
    print(f"Mean Elevation    : {stats['elevation_mean']:.2f} m")

    print("\n✓ DEM generated successfully.")


if __name__ == "__main__":
    main()