"""
Utility Functions
Groundwater Potential Mapping Project

Author : Tejendra
"""

import os
import sys
import ee

# ==========================================================
# Add Project Root
# ==========================================================

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from config import PROJECT_ID, STATE_NAME


# ==========================================================
# Initialize Earth Engine
# ==========================================================

def initialize_ee():
    """Initialize Google Earth Engine."""
    ee.Initialize(project=PROJECT_ID)


# ==========================================================
# Print Header
# ==========================================================

def print_header(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


# ==========================================================
# Study Area
# ==========================================================

def get_state_boundary(state_name=STATE_NAME):
    """
    Returns the selected state boundary.
    """

    states = ee.FeatureCollection("FAO/GAUL/2015/level1")

    boundary = states.filter(
        ee.Filter.eq("ADM1_NAME", state_name)
    )

    return boundary


# ==========================================================
# DEM
# ==========================================================

def load_dem(boundary, dataset):
    """
    Load SRTM DEM.
    """

    return ee.Image(dataset).clip(boundary)


# ==========================================================
# Sentinel-2 Cloud Mask
# ==========================================================

def mask_sentinel_clouds(image):
    """
    Mask clouds using QA60 band.
    """

    qa = image.select("QA60")

    cloud_bit = 1 << 10
    cirrus_bit = 1 << 11

    mask = (
        qa.bitwiseAnd(cloud_bit).eq(0)
        .And(
            qa.bitwiseAnd(cirrus_bit).eq(0)
        )
    )

    return (
        image
        .updateMask(mask)
        .divide(10000)
    )


# ==========================================================
# Sentinel-2 Image
# ==========================================================

def load_satellite_image(
        boundary,
        dataset,
        start_date,
        end_date):
    """
    Load Sentinel-2 image collection.
    """

    image = (
        ee.ImageCollection(dataset)
        .filterBounds(boundary)
        .filterDate(start_date, end_date)
        .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 20))
        .map(mask_sentinel_clouds)
        .median()
        .clip(boundary)
    )

    return image


# ==========================================================
# NDVI
# ==========================================================

def calculate_ndvi(image):
    """
    Calculate NDVI.
    """

    return image.normalizedDifference(
        ["B8", "B4"]
    ).rename("NDVI")


# ==========================================================
# Slope
# ==========================================================

def calculate_slope(dem):
    """
    Generate slope from DEM.
    """

    return ee.Terrain.slope(dem)


# ==========================================================
# Image Statistics
# ==========================================================

def image_statistics(
        image,
        geometry,
        scale=30):
    """
    Calculate min, max and mean.
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


# ==========================================================
# Print Statistics
# ==========================================================

def print_statistics(stats, band, unit=""):

    print("-" * 35)

    print(
        f"Minimum : {stats[f'{band}_min']:.2f}{unit}"
    )

    print(
        f"Maximum : {stats[f'{band}_max']:.2f}{unit}"
    )

    print(
        f"Mean    : {stats[f'{band}_mean']:.2f}{unit}"
    )

    print()


# ==========================================================
# Area
# ==========================================================

def get_area(boundary):
    """
    Returns area in square kilometres.
    """

    return (
        boundary.geometry()
        .area()
        .divide(1e6)
        .getInfo()
    )