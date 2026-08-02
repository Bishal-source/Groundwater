import os
import sys
import ee

# Add project root to Python path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

from config import PROJECT_ID, STATE_NAME

# -----------------------------------
# Initialize Earth Engine
# -----------------------------------

ee.Initialize(project=PROJECT_ID)

print("=" * 60)
print("Google Earth Engine Connected")
print("=" * 60)

# -----------------------------------
# Load India State Boundaries
# -----------------------------------

states = ee.FeatureCollection("FAO/GAUL/2015/level1")

# Select Haryana
haryana = states.filter(
    ee.Filter.eq("ADM1_NAME", STATE_NAME)
)

# -----------------------------------
# Basic Information
# -----------------------------------

print(f"Study Area : {STATE_NAME}")

count = haryana.size().getInfo()
print(f"Number of Features : {count}")

if count == 0:
    print("ERROR: Haryana boundary not found!")
else:
    print("Boundary loaded successfully.")

# Area in square kilometers
area = haryana.geometry().area().divide(1e6).getInfo()

print(f"Area : {area:,.2f} sq.km")

print("=" * 60)