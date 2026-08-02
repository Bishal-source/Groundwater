import ee
import os
import sys

# Add the project root to Python's search path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import PROJECT_ID


def initialize_earth_engine():
    try:
        ee.Initialize(project=PROJECT_ID)

        print("=" * 50)
        print("Google Earth Engine Initialized Successfully")
        print("=" * 50)
        print(f"Project ID : {PROJECT_ID}")

    except Exception as e:
        print("Initialization Failed!")
        print(e)


if __name__ == "__main__":
    initialize_earth_engine()