import geopandas as gpd
from shapely.geometry import shape, Point


def load_data():
    """
    This function loads the necessary data.
    Args: None

    Returns: 
        regions, stations (object: gpd.GeoDataFrame): Geodataframe
    """
    regions = gpd.read_file(open("website/data/datum/datum.geojson"), crs="WGS84")
    stations = gpd.read_file(open("website/data/mobility/HSL_stations.geojson"), crs="WGS84")
    return regions, stations


def count_points(regions: gpd.GeoDataFrame, points: gpd.GeoDataFrame) -> list:
    """
    Args: 
        regions (object: gpd.GeoDataFrame)
        points (object: gpd.GeoDataFrame)

    Returns: 
        num_of_stations (list): Number of points that are inside each region.
    """
    num_of_stations = []
    postal_regions = regions['geometry'].to_list()

    for region in postal_regions:
        count = 0
        polygon = shape(region)
        for point in points['geometry'].to_list():
            if polygon.contains(Point(point)):
                count += 1
        num_of_stations.append(count)

    print(len(num_of_stations), len(postal_regions))
    return num_of_stations


def get_mobility_index(num_of_stations: list, gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Calculates the Mobility Index.
    #TODO add more parameters to the index.
    Args: 
        num_of_stations (list)
        gdf (object: gpd.GeoDataFrame)

    Returns: 
        regions (object: gpd.GeoDataFrame)
    """
    gdf['mobility_nodes'] = num_of_stations
    regions = gdf[['index', 'mobility_nodes', 'Surface area']]
    regions['mobility_index'] = regions['mobility_nodes']/regions['Surface area']
    return regions


def min_max_normalize(gdf: gpd.GeoDataFrame, column: str = 'mobility_index') -> gpd.GeoDataFrame:
    """
    This function normalizes the values in a given column
    Args: 
        gdf (object: gpd.GeoDataFrame)
        column (str): Name of the column to normalize

    Returns: 
        gdf (object: gpd.GeoDataFrame)
    """
    diff = gdf[column].max() - gdf[column].min()
    gdf[column] = (gdf[column] - gdf[column].min()) / diff
    return gdf


def main():
    """
    """
    regions, stations = load_data()
    num_of_stations = count_points(regions, stations)
    regions = get_mobility_index(num_of_stations, regions)
    regions = min_max_normalize(regions)
    print(regions.head(), regions.describe())
    regions.to_csv('website/data/mobility/mobility.csv', index=False)


if __name__ == '__main__':
    main()
