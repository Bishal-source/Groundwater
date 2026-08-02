import ee

ee.Initialize(project="spherical-park-503216-d1")

try:
    img = ee.ImageCollection("ESA/WorldCover/v200").first()
    print(img.bandNames().getInfo())
except Exception as e:
    print(e)