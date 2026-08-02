"""
02_load_data.py

Groundwater Potential Mapping Project

Purpose:
Load the study area boundary and calculate basic information.
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

from config import STATE_NAME

# ==========================================================
# Import Utility Functions
# ==========================================================

from utils import (
    initialize_ee,
    print_header,
    get_state_boundary,
    get_area
)


def main():

    # ------------------------------------------------------
    # Initialize Earth Engine
    # ------------------------------------------------------

    initialize_ee()

    # ------------------------------------------------------
    # Header
    # ------------------------------------------------------

    print_header("STEP 02 : LOAD STUDY AREA")

    # ------------------------------------------------------
    # Load Boundary
    # ------------------------------------------------------

    boundary = get_state_boundary()

    # ------------------------------------------------------
    # Calculate Area
    # ------------------------------------------------------

    area = get_area(boundary)

    # ------------------------------------------------------
    # Display Information
    # ------------------------------------------------------

    print(f"Study Area : {STATE_NAME}")
    print(f"Number of Features : {boundary.size().getInfo()}")
    print(f"Area : {area:.2f} sq.km")

    print("\n✓ Study area loaded successfully.")


if __name__ == "__main__":
    main()