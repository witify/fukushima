import geopandas as gpd
import utm

fukushima = gpd.read_file('data/fukushima-2.geojson')

projection = '+proj=cea +lat_0=35.68250088833567 +lon_0=139.7671 +units=m'

fukushima = fukushima.to_crs(projection)

waste2022 = gpd.read_file('data/raw/geojson/Waste_2022.geojson')
waste2023 = gpd.read_file('data/raw/geojson/Waste_2023.geojson')
solar2022 = gpd.read_file('data/raw/geojson/Solar_2022.geojson')
solar2023 = gpd.read_file('data/raw/geojson/Solar_2023.geojson')

waste2022 = waste2022.to_crs(projection)
waste2023 = waste2023.to_crs(projection)
solar2022 = solar2022.to_crs(projection)
solar2023 = solar2023.to_crs(projection)


for index, city in fukushima.iterrows():
    city = fukushima.iloc[[index]]

    interWaste2022 = gpd.overlay(city, waste2022, how='intersection')
    interWaste2023 = gpd.overlay(city, waste2023, how='intersection')
    interSolar2022 = gpd.overlay(city, solar2022, how='intersection')
    interSolar2023 = gpd.overlay(city, solar2023, how='intersection')

    fukushima.at[index, 'area'] = city.geometry.area.sum()
    fukushima.at[index, 'waste2022'] = interWaste2022.geometry.area.sum()
    fukushima.at[index, 'waste2023'] = interWaste2023.geometry.area.sum()
    fukushima.at[index, 'solar2022'] = interSolar2022.geometry.area.sum()
    fukushima.at[index, 'solar2023'] = interSolar2023.geometry.area.sum()
    fukushima.at[index, 'intersection'] = (fukushima.iloc[index].solar2023 - fukushima.iloc[index].solar2022) + (
        fukushima.iloc[index].waste2022 - fukushima.iloc[index].waste2023)


fukushima = fukushima.to_crs('4326')

fukushima.to_file('data/generated/fukushima.geojson', driver='GeoJSON')
