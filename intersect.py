import geopandas as gpd

def calculate_intersect_area(geojson_file1, geojson_file2, output_file, target_crs='EPSG:3857'):
    # Read the GeoJSON files into geopandas GeoDataFrames
    geojson1 = gpd.read_file(geojson_file1)
    geojson2 = gpd.read_file(geojson_file2)
    
    # Reproject to a projected CRS
    #geojson1 = geojson1.to_crs(target_crs)
    #geojson2 = geojson2.to_crs(target_crs)
    
    # Perform the intersection
    intersection = gpd.overlay(geojson1, geojson2, how='intersection')
    
    # Calculate the intersected area
    intersect_area = intersection.geometry.area.sum()

    # Save the intersection result as GeoJSON
    intersection.to_file(output_file, driver='GeoJSON')
    
    return intersect_area



intersect_area = calculate_intersect_area('data/raw/geojson/Waste_2022.geojson', 'data/raw/geojson/Solar_2023.geojson', 'data/generated/Waste_2022_Solar_2023_intersect.geojson')
