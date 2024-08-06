# import rasterio
# from rasterio.warp import transform
# from shapely.geometry import Polygon
# import numpy as np
# import cv2

# def get_image_corners(image_path):
#     with rasterio.open(image_path) as src:
#         bounds = src.bounds
#         crs = src.crs
        
#         corners = [
#             (bounds.left, bounds.top),     
#             (bounds.right, bounds.top),    
#             (bounds.right, bounds.bottom),
#             (bounds.left, bounds.bottom)   
#         ]
        
#         corners_wgs84 = transform(crs, {'init': 'epsg:4326'}, 
#                                   [corner[0] for corner in corners], 
#                                   [corner[1] for corner in corners])
        
#         corners_wgs84 = list(zip(corners_wgs84[0], corners_wgs84[1]))
        
#     return corners_wgs84

# def calculate_polygon_area(polygon_coords):
#     polygon = Polygon(polygon_coords)
#     area = polygon.area  
    
#     # Convert to square meters (approximate)
#     area_sqm = area * (111320 * 111320)
    
#     return area_sqm

# def pixel_to_meter_conversion_factor(image_path):
#     with rasterio.open(image_path) as src:
#         width = src.width
#         height = src.height
#         image_area_pixels = width * height
    
#     corners_wgs84 = get_image_corners(image_path)
#     image_area_sqm = calculate_polygon_area(corners_wgs84)
    
#     conversion_factor = image_area_sqm / image_area_pixels
#     return conversion_factor, width, height

# def calculate_building_areas_from_masks(mask, conversion_factor):
#     num_labels, labels_im = cv2.connectedComponents(mask)
    
#     building_areas_pixels = []
#     for label in range(1, num_labels):  # Start from 1 to skip background
#         area_pixels = np.sum(labels_im == label)
#         building_areas_pixels.append(area_pixels)
    
#     building_areas_sqm = [area_pixels * conversion_factor for area_pixels in building_areas_pixels]
#     return building_areas_sqm

# def calculate_total_area(image_path, mask):
#     corners_wgs84 = get_image_corners(image_path)
#     image_area_sqm = calculate_polygon_area(corners_wgs84)
#     conversion_factor, _, _ = pixel_to_meter_conversion_factor(image_path)
#     building_areas = calculate_building_areas_from_masks(mask, conversion_factor)
#     total_building_area = sum(building_areas)
#     return total_building_area, image_area_sqm

# if __name__ == "__main__":
#     # You can add some test code here to verify the functions
#     image_path = "path/to/your/test/image.tif"
#     mask = np.random.randint(0, 2, (256, 256), dtype=np.uint8)  # Example random mask
    
#     total_building_area, image_area = calculate_total_area(image_path, mask)
#     print(f"Total building area: {total_building_area} sq meters")
#     print(f"Total image area: {image_area} sq meters")




import cv2
import numpy as np
import logging

logger = logging.getLogger(__name__)

def calculate_total_area(image_path, mask):
    logger.debug(f"Calculating total area for image: {image_path}")
    
    try:
        # Load the image
        image = cv2.imread(image_path)
        if image is None:
            logger.error(f"Failed to load image: {image_path}")
            return None, None

        # Get image dimensions
        height, width = image.shape[:2]
        logger.debug(f"Image dimensions: {width}x{height}")

        # Calculate the total area of the image in pixels
        image_area = height * width
        logger.debug(f"Total image area: {image_area} pixels")

        # Ensure mask is binary
        mask = (mask > 0).astype(np.uint8)

        # Calculate the total area of the buildings (white pixels in the mask)
        building_area = np.sum(mask)
        logger.debug(f"Building area: {building_area} pixels")

        # Convert areas to square meters (you may need to adjust this conversion factor)
        pixel_to_meter_ratio = 0.3  # This is an example value, adjust based on your image resolution
        building_area_sqm = building_area * (pixel_to_meter_ratio ** 2)
        image_area_sqm = image_area * (pixel_to_meter_ratio ** 2)

        logger.debug(f"Building area: {building_area_sqm:.2f} sq meters")
        logger.debug(f"Image area: {image_area_sqm:.2f} sq meters")

        return building_area_sqm, image_area_sqm

    except Exception as e:
        logger.error(f"Error in calculate_total_area: {str(e)}")
        return None, None
