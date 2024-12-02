
from arcgis.gis import GIS
from arcgis.raster import ImageryLayer

# Connect to the public ArcGIS Online environment (no authentication needed)
gis = GIS()  # Anonymous access

# Define the Image Service URL
image_service_url = "https://gis.apfo.usda.gov/arcgis/rest/services/NAIP/USDA_CONUS_PRIME/ImageServer"
# image_service_url = "https://tiles.arcgis.com/tiles/RvqSyw3diI7dTKo5/arcgis/rest/services/SC_2023_RGB/MapServer"

image_layer = ImageryLayer(image_service_url, gis=gis)

# List of bounding boxes (xmin, ymin, xmax, ymax) in WGS84
bboxes = [
    [-79.87346884357288, 33.16818468357826, -79.83009707002654, 33.20465359374293],
    [-79.83057651422162, 33.16777443539387, -79.78718802000448, 33.20425757451443],
    [-79.78768503867326, 33.167349418407326, -79.74427985654698, 33.20384676528001],
    [-79.87392988935368, 33.13211157720555, -79.83057651422162, 33.16858016195084],
    [-79.83105510461318, 33.131701889620835, -79.78768503867326, 33.16818468357826],
    [-79.7881811722542, 33.131277453409965, -79.74479444821206, 33.16777443539387],
    [-79.87439011398845, 33.09603825552369, -79.83105510461318, 33.13250651515637],
    [-79.8315328426226, 33.09562912808931, -79.7881811722542, 33.13211157720555],
    [-79.7886764222207, 33.0952052721886, -79.74530812350898, 33.131701889620835],
]

# Loop over bounding boxes and query the images
for i, bbox in enumerate(bboxes):
    # Convert bbox list to a comma-separated string
    bbox_str = ",".join(map(str, bbox))

    # Query the image service
    try:
        image_result = image_layer.export_image(
            bbox=bbox_str,  # Bounding box in WGS84
            bbox_sr=4326,  # Spatial reference for the bounding box (WGS84)
            image_sr=4326,  # Spatial reference for the output image
            f="image",  # Format of the request (image)
            export_format="tiff",  # Desired output format
            compression=None,
            compression_quality=100,
            size=[2500,2500]
        )

        # Save the image to a file
        output_file = f"USDA_Santee_Santee_{i + 1}.tif"  # Unique file name for each bbox
        with open(output_file, "wb") as f:
            f.write(image_result)

        print(f"Image {i + 1} saved to {output_file}")

    except Exception as e:
        print(f"Failed to process bbox {i + 1}: {bbox}")
        print(f"Error: {e}")
