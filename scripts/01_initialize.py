"""
01_initialize.py

Groundwater Potential Mapping Project

Purpose:
Initialize Google Earth Engine and verify the project configuration.
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

from config import PROJECT_ID

# ==========================================================
# Import Utility Functions
# ==========================================================

from utils import (
    initialize_ee,
    print_header
)


def main():

    # ------------------------------------------------------
    # Initialize Earth Engine
    # ------------------------------------------------------

    initialize_ee()

    # ------------------------------------------------------
    # Display Header
    # ------------------------------------------------------

    print_header("STEP 01 : INITIALIZE GOOGLE EARTH ENGINE")

    print("Google Earth Engine initialized successfully.\n")

    print(f"Project ID : {PROJECT_ID}")

    print("\n✓ Initialization completed.")


if __name__ == "__main__":
    main()