import pandas as pd
import geopandas as gpd



def load_shapefile(path: str) -> gpd.GeoDataFrame:
    """
    Loads the shapefile with helsinki postal districts.
    """
    geo_df = gpd.read_file(path)
    geo_df = geo_df.to_crs("WGS84").set_index("Posno")
    geo_df.drop(columns=['Toimip', 'Toimip_ru', 'Nimi_Ru', 'Kunta_nro'], inplace=True)
    geo_df.rename(columns = {'Kunta': 'municipality', 'Nimi': 'neighborhood'}, inplace = True)
    print(geo_df.head())

    return geo_df


def load_paavo_dataset(path: str, encoding: str='ISO-8859-1',delimiter: str=',', skiprows=1) -> pd.DataFrame:
    """
    Loads the csv with PAAVO dataset.
    """
    # Data by postal areas
    census = pd.read_csv(path, encoding=encoding, delimiter=delimiter, skiprows=skiprows)
    print(census.head())
    census['Postal code area'] = census['Postal code area'].str.split('  ', expand=True)[0]
    census = census.set_index('Postal code area')
    census.drop(columns=['X coordinate', 'Y coordinate'], inplace=True)

    return census


def main():
    """
    This function combines PAAVO dataset with 
    postal areas shape file into a GeoDataFrame.
    """
    shapefile_path = 'website/data/postal-areas-2021/PKS_postinumeroalueet_2021_shp.shx'
    geo_df = load_shapefile(shapefile_path)

    paavo_path = 'website/data/census-csv/census_2020.csv'
    census = load_paavo_dataset(paavo_path)

    # Combined DataFrame
    datum = pd.merge(geo_df, census, left_index=True, right_index=True)
    datum.to_file("website/data/datum/datum.geojson", driver='GeoJSON')

    print(datum.describe())
    print(datum.sample(5))


if __name__=='__main__':
    main(delimiter=',')
