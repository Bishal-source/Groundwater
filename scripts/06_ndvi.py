"""
06_ndvi.py

Groundwater Potential Mapping Project

Purpose:
Generate NDVI from Sentinel-2 imagery,
calculate statistics,
and export the NDVI raster to Google Drive.
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
    SATELLITE_DATASET,
    START_DATE,
    END_DATE
)

# ==========================================================
# Import Utility Functions
# ==========================================================

from utils import (
    initialize_ee,
    print_header,
    get_state_boundary,
    load_satellite_image,
    calculate_ndvi,
    image_statistics,
    print_statistics,
    export_image_to_drive,
    print_export_status,
    get_image_count
)


def main():

    # ------------------------------------------------------
    # Initialize Earth Engine
    # ------------------------------------------------------

    initialize_ee()

    print_header("STEP 06 : NDVI GENERATION")

    # ------------------------------------------------------
    # Load Study Area
    # ------------------------------------------------------

    boundary = get_state_boundary()

    # ------------------------------------------------------
    # Number of Images
    # ------------------------------------------------------

    image_count = get_image_count(
        SATELLITE_DATASET,
        boundary,
        START_DATE,
        END_DATE
    )

    # ------------------------------------------------------
    # Load Sentinel-2 Composite
    # ------------------------------------------------------

    image = load_satellite_image(
        boundary,
        SATELLITE_DATASET,
        START_DATE,
        END_DATE
    )

    # ------------------------------------------------------
    # Generate NDVI
    # ------------------------------------------------------

    ndvi = calculate_ndvi(image)

    # ------------------------------------------------------
    # Calculate Statistics
    # ------------------------------------------------------

    stats = image_statistics(
        ndvi,
        boundary.geometry(),
        scale=100
    )

    # ------------------------------------------------------
    # Display Information
    # ------------------------------------------------------

    print(f"Study Area     : {STATE_NAME}")
    print("Satellite      : Sentinel-2 SR Harmonized")
    print(f"Date Range     : {START_DATE} to {END_DATE}")
    print(f"Images Used    : {image_count}")

    print("\nNDVI Statistics")

    print_statistics(
        stats,
        "NDVI"
    )

    # ------------------------------------------------------
    # Export NDVI
    # ------------------------------------------------------

    task = export_image_to_drive(
        image=ndvi,
        description="NDVI_Haryana",
        region=boundary.geometry(),
        scale=10
    )

    print_export_status(
        task,
        "NDVI_Haryana"
    )

    print("\n✓ NDVI generation completed successfully.")


if __name__ == "__main__":
    main()