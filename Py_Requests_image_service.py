import requests

# Base URL of the Image Server
# base_url = "https://gis.apfo.usda.gov/arcgis/rest/services/NAIP/USDA_CONUS_PRIME/ImageServer"
base_url = "https://tiles.arcgis.com/tiles/RvqSyw3diI7dTKo5/arcgis/rest/services/SC_2023_RGB/MapServer"

# Parameters to export the highest resolution
params = {
    "f": "image",  # Output format
    "bbox": "-8887217.429786,3917654.481616,-8884236.385683,3920489.817634",  # Define area of interest
    "bboxSR": "3857",  # Spatial reference of the bounding box (use the service's native SR)
    "imageSR": "3857",  # Spatial reference of the output image
    "format": "tiff",  # TIFF for high quality
    "pixelType": "UNKNOWN",  # Keep native pixel depth
    "noData": "0",  # Set to match service's no-data value
    "compression": "None"  # Request uncompressed image
}

# Construct the export image URL
export_image_url = f"{base_url}/exportImage"

# Request the image
response = requests.get(export_image_url, params=params, stream=True)

# Check for errors
response.raise_for_status()

# Save the image to a file
with open("highest_res_output.tif", "wb") as f:
    for chunk in response.iter_content(chunk_size=8192):
        if not chunk:
            break
        f.write(chunk)

print("Image saved successfully.")
