import geopandas as gpd
import utm

fukushima = gpd.read_file('data/fukushima.geojson')
# fukushima.crs = 'epsg:900913'
# fukushima = fukushima.to_crs(crs=3857)

waste2022 = gpd.read_file('data/raw/geojson/Waste_2022.geojson')
waste2023 = gpd.read_file('data/raw/geojson/Waste_2023.geojson')
solar2022 = gpd.read_file('data/raw/geojson/Solar_2022.geojson')
solar2023 = gpd.read_file('data/raw/geojson/Solar_2023.geojson')
# waste2022.crs = 'epsg:4326'
# waste2022 = waste2022.to_crs(crs=3857)


for index, city in fukushima.iterrows():
    city = fukushima.iloc[[index]]

    # print(city.ward_en.to_string(index=False), city.geometry.area.sum() * 10000)

    # city = city.to_crs(crs=3857)

    interWaste2022 = gpd.overlay(city, waste2022, how='intersection')
    interWaste2023 = gpd.overlay(city, waste2023, how='intersection')
    interSolar2022 = gpd.overlay(city, solar2022, how='intersection')
    interSolar2023 = gpd.overlay(city, solar2023, how='intersection')

    fukushima.at[index, 'area'] = city.geometry.area.sum() * 1000000
    fukushima.at[index, 'waste2022'] = interWaste2022.geometry.area.sum() * \
        1000000
    fukushima.at[index, 'waste2023'] = interWaste2023.geometry.area.sum() * \
        1000000
    fukushima.at[index, 'solar2022'] = interSolar2022.geometry.area.sum() * \
        1000000
    fukushima.at[index, 'solar2023'] = interSolar2023.geometry.area.sum() * \
        1000000
    fukushima.at[index, 'intersection'] = (fukushima.iloc[index].solar2023 - fukushima.iloc[index].solar2022) + (
        fukushima.iloc[index].waste2022 - fukushima.iloc[index].waste2023)


fukushima.to_file('data/generated/fukushima.geojson', driver='GeoJSON')
