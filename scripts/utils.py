"""
Utility functions for Groundwater Potential Mapping Project
Author: Tejendra
"""

import os
import sys
import ee

# --------------------------------------------------
# Add project root to Python path
# --------------------------------------------------

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from config import PROJECT_ID, STATE_NAME


# --------------------------------------------------
# Initialize Earth Engine
# --------------------------------------------------

def initialize_ee():
    """
    Initialize Google Earth Engine.
    """

    ee.Initialize(project=PROJECT_ID)


# --------------------------------------------------
# Print Header
# --------------------------------------------------

def print_header(title):
    """
    Print a formatted title.
    """

    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


# --------------------------------------------------
# Load State Boundary
# --------------------------------------------------

def get_state_boundary(state_name=STATE_NAME):
    """
    Returns the selected state boundary.
    """

    states = ee.FeatureCollection("FAO/GAUL/2015/level1")

    state = states.filter(
        ee.Filter.eq("ADM1_NAME", state_name)
    )

    return state


# --------------------------------------------------
# Load DEM
# --------------------------------------------------

def load_dem(boundary, dataset):
    """
    Load and clip DEM.
    """

    return ee.Image(dataset).clip(boundary)


# --------------------------------------------------
# Image Statistics
# --------------------------------------------------

def image_statistics(image, geometry, scale=30):
    """
    Calculate minimum, maximum and mean values.
    """

    stats = image.reduceRegion(
        reducer=ee.Reducer.minMax().combine(
            reducer2=ee.Reducer.mean(),
            sharedInputs=True
        ),
        geometry=geometry,
        scale=scale,
        maxPixels=1e13
    )

    return stats.getInfo()