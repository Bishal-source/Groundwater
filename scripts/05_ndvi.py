"""
Generate NDVI (Normalized Difference Vegetation Index)

Groundwater Potential Mapping Project
"""

import os
import sys

# ==========================================================
# Add Project Root
# ==========================================================

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from config import (
    SATELLITE_DATASET,
    START_DATE,
    END_DATE
)

from utils import (
    initialize_ee,
    print_header,
    get_state_boundary,
    load_satellite_image,
    calculate_ndvi,
    image_statistics,
    print_statistics
)


def main():

    # ======================================================
    # Initialize Earth Engine
    # ======================================================

    initialize_ee()

    print_header("STEP 05 : NDVI GENERATION")

    # ======================================================
    # Load Study Area
    # ======================================================

    haryana = get_state_boundary()

    print("Study Area :", "Haryana")
    print()

    # ======================================================
    # Number of Sentinel-2 Images
    # ======================================================

    image_collection = (
        __import__("ee")
        .ImageCollection(SATELLITE_DATASET)
        .filterBounds(haryana)
        .filterDate(START_DATE, END_DATE)
        .filter(__import__("ee").Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 20))
    )

    print("Satellite Images Found :", image_collection.size().getInfo())
    print()

    # ======================================================
    # Load Satellite Image
    # ======================================================

    image = load_satellite_image(
        haryana,
        SATELLITE_DATASET,
        START_DATE,
        END_DATE
    )

    # ======================================================
    # Generate NDVI
    # ======================================================

    ndvi = calculate_ndvi(image)

    # ======================================================
    # Statistics
    # ======================================================

    stats = image_statistics(
        ndvi,
        haryana.geometry(),
        scale=10
    )

    print("NDVI Statistics")

    print_statistics(
        stats,
        "NDVI"
    )

    print("✓ NDVI generated successfully.")


if __name__ == "__main__":
    main()