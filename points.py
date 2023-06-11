import geopandas as gpd
import pandas as pd

names = ['Waste_2022', 'Waste_2023', 'Solar_2022', 'Solar_2023']

for name in names:
    gdf = gpd.read_file('data/raw/geojson/'+name+'.geojson')

    points_gdf = gpd.GeoDataFrame()

    gdf['centroid'] = None

    for index, row in gdf.iterrows():
        centroid = row['geometry'].centroid
        gdf.at[index, 'centroid'] = centroid
        gdf.at[index, 'area'] = (row['geometry'].area * 10000000)

    gdf['geometry'] = gdf['centroid']

    gdf = gdf.drop(columns='centroid')

    output_file_path = "data/generated/points/"+name+"_points.geojson"
    gdf.to_file(output_file_path, driver='GeoJSON')