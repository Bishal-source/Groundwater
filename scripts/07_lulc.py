"""
07_lulc.py

Groundwater Potential Mapping Project

Purpose:
Generate Land Use / Land Cover (LULC) map using
Sentinel-2 imagery and Random Forest Classification.

Reference Labels:
ESA WorldCover v200
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
    export_image_to_drive,
    print_export_status,
    get_image_count
)

# ==========================================================
# WorldCover Dataset
# ==========================================================

WORLDCOVER_DATASET = "ESA/WorldCover/v200"

# ==========================================================
# Number of Trees
# ==========================================================

NUMBER_OF_TREES = 100

# ==========================================================
# Number of Training Samples
# ==========================================================

SAMPLE_SIZE = 500

# ==========================================================
# Load WorldCover
# ==========================================================

def load_worldcover(boundary):
    """
    Load ESA WorldCover 2021 dataset.
    """

    worldcover = (
        ee.ImageCollection(WORLDCOVER_DATASET)
        .first()
        .select("Map")
        .clip(boundary)
    )

    print("WorldCover bands:", worldcover.bandNames().getInfo())
    print("WorldCover loaded successfully.")

    return worldcover

# ==========================================================
# Remap WorldCover Classes
# ==========================================================

def remap_worldcover(worldcover):
    """
    Convert ESA WorldCover classes
    into project classes.

    Final Classes

    0 -> Water
    1 -> Vegetation
    2 -> Built-up
    3 -> Bare Land
    """

    original = [
    10,   # Trees
    20,   # Shrubland
    30,   # Grassland
    40,   # Cropland
    50,   # Built-up
    60,   # Bare
    80,   # Water
    90,   # Wetland
    95,   # Mangroves
    100   # Moss
]

    remapped = [
      1,
      1,
      1,
      1,
      2,
      3,
      0,
      0,
      1,
      1
    ]

    lulc = worldcover.remap(
        original,
        remapped
    ).rename("LULC")

    return lulc

# ==========================================================
# Generate Training Samples
# ==========================================================

def generate_training_samples(image, lulc, boundary):
    """
    Generate stratified samples and split into
    training and testing datasets.
    """

    training_image = image.addBands(lulc)

    samples = training_image.stratifiedSample(
        numPoints=SAMPLE_SIZE,
        classBand="LULC",
        region=boundary.geometry(),
        scale=10,
        seed=42,
        geometries=True
    )

    # Random split

    samples = samples.randomColumn("random", 42)

    training = samples.filter(
        ee.Filter.lt("random", 0.7)
    )

    testing = samples.filter(
        ee.Filter.gte("random", 0.7)
    )

    return training, testing

# ==========================================================
# Train Random Forest Classifier
# ==========================================================

def train_random_forest(samples):
    """
    Train a Random Forest classifier using
    ESA WorldCover training samples.
    """

    bands = [
        "B2", "B3", "B4",
        "B5", "B6", "B7",
        "B8", "B8A",
        "B11", "B12"
    ]

    classifier = (
        ee.Classifier.smileRandomForest(
            numberOfTrees=NUMBER_OF_TREES,
            seed=42
        )
        .train(
            features=samples,
            classProperty="LULC",
            inputProperties=bands
        )
    )

    return classifier

# ==========================================================
# Classify Image
# ==========================================================

def classify_image(image, classifier):
    """
    Apply Random Forest classifier.
    """

    bands = [
        "B2", "B3", "B4",
        "B5", "B6", "B7",
        "B8", "B8A",
        "B11", "B12"
    ]

    classified = (
        image
        .select(bands)
        .classify(classifier)
        .rename("LULC")
    )

    return classified


# ==========================================================
# Main
# ==========================================================

def main():

    # ------------------------------------------------------
    # Initialize Earth Engine
    # ------------------------------------------------------

    initialize_ee()

    print_header("STEP 07 : LAND USE / LAND COVER (LULC)")

    # ------------------------------------------------------
    # Study Area
    # ------------------------------------------------------

    boundary = get_state_boundary()

    # ------------------------------------------------------
    # Image Count
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
    # Load ESA WorldCover
    # ------------------------------------------------------

    worldcover = load_worldcover(boundary)

    # ------------------------------------------------------
    # Remap Classes
    # ------------------------------------------------------

    lulc_reference = remap_worldcover(worldcover)

    training, testing = generate_training_samples(
    image,
    lulc_reference,
    boundary
)

    classifier = train_random_forest(training)

    classified = classify_image(
    image,
    classifier
)

    print("\nRandom Forest Classification")
    print("-" * 35)
    print("Training completed successfully.")
    print("Classification completed successfully.")

    # ------------------------------------------------------
    # Display Information
    # ------------------------------------------------------

    print(f"Study Area      : {STATE_NAME}")
    print("Satellite       : Sentinel-2 SR Harmonized")
    print(f"Images Used     : {image_count}")
    print(f"Training Points : {SAMPLE_SIZE}")
    print(f"Random Forest   : {NUMBER_OF_TREES} Trees")

    # ------------------------------------------------------
    # Export LULC
    # ------------------------------------------------------

    task = export_image_to_drive(
        image=classified.toInt(),
        description="LULC_Haryana",
        region=boundary.geometry(),
        scale=10
    )

    print_export_status(
        task,
        "LULC_Haryana"
    )

    print("\n✓ LULC classification completed successfully.")


# ==========================================================
# Run
# ==========================================================

if __name__ == "__main__":
    main()