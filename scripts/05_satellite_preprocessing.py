"""
05_satellite_preprocessing.py

Groundwater Potential Mapping Project

Purpose:
Load Sentinel-2 imagery, apply cloud masking,
generate a median composite, and report basic
information about the satellite data.
"""

import os
import sys
import ee

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
    load_satellite_image
)


def main():

    # ------------------------------------------------------
    # Initialize Earth Engine
    # ------------------------------------------------------

    initialize_ee()

    print_header("STEP 05 : SATELLITE PREPROCESSING")

    # ------------------------------------------------------
    # Load Study Area
    # ------------------------------------------------------

    boundary = get_state_boundary()

    # ------------------------------------------------------
    # Load Image Collection
    # ------------------------------------------------------

    collection = (
        ee.ImageCollection(SATELLITE_DATASET)
        .filterBounds(boundary)
        .filterDate(START_DATE, END_DATE)
        .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 20))
    )

    image_count = collection.size().getInfo()

    # ------------------------------------------------------
    # Create Cloud-Free Composite
    # ------------------------------------------------------

    composite = load_satellite_image(
        boundary,
        SATELLITE_DATASET,
        START_DATE,
        END_DATE
    )

    # ------------------------------------------------------
    # Display Information
    # ------------------------------------------------------

    print(f"Study Area      : {STATE_NAME}")
    print(f"Satellite       : Sentinel-2 SR Harmonized")
    print(f"Date Range      : {START_DATE} to {END_DATE}")
    print(f"Images Used     : {image_count}")

    print("\nAvailable Bands")
    print("-" * 35)

    bands = composite.bandNames().getInfo()

    for band in bands:
        print(f"• {band}")

    print("\n✓ Satellite preprocessing completed successfully.")


if __name__ == "__main__":
    main()