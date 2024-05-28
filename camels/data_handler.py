import os
import pandas as pd
import geopandas as gpd
import json


class DataHandler:
    """
    Class to handle data from the CAMELS dataset.
    
    """
    def __init__(self, data_directory: str):
        self.data_directory = data_directory

    def get_station_timeseries_data(self, station_id: str) -> pd.DataFrame:
        """
        Get the hydrometeorological timeseries data for a station.
        
        """
        # Construct the file path
        file_path = os.path.join(self.data_directory, f"timeseries/CAMELS_DE_hydromet_timeseries_{station_id}.csv")
        
        # Check if the file exists
        if not os.path.exists(file_path):
            # Return an empty DataFrame if file doesn't exist
            return pd.DataFrame()
        
        return pd.read_csv(file_path)
    
    def get_station_topographic_data(self, station_id: str) -> pd.DataFrame:
        """
        Get the topographic data for a station.
        
        """
        # Construct the file path
        file_path = os.path.join(self.data_directory, f"CAMELS_DE_topographic_attributes.csv")

        # Check if the file exists
        if not os.path.exists(file_path):
            # Return an empty DataFrame if file doesn't exist
            return pd.DataFrame()
        
        # Read the data from the file
        df = pd.read_csv(file_path)

        # Filter the data for the station
        df = df[df['gauge_id'] == station_id]

        return df.reset_index(drop=True)
    
    def get_station_catchment_shape(self, station_id: str) -> dict:
        """
        Get the catchment shape data for the stations in GeoJSON format.
        
        """
        # Construct the file path
        file_path = os.path.join(self.data_directory, f"CAMELS_DE_catchment_boundaries/catchments/CAMELS_DE_catchments.gpkg")
        
        # Check if the file exists
        if not os.path.exists(file_path):
            # Return an empty GeoDataFrame if file doesn't exist
            return gpd.GeoDataFrame()
        
        # Read the data from the file
        gdf = gpd.read_file(file_path)

        # Filter the data for the stations
        gdf = gdf[gdf['id'] == station_id]

        # Drop columns we don't need here
        gdf = gdf.drop(columns=["id", "name", "result", "area_calc", "area_reported"])

        # Reset the index
        gdf = gdf.reset_index(drop=True)

        # Convert the geometry to EPSG:4326
        gdf = gdf.to_crs(epsg=4326)

        # convert the GeoPandas DataFrame to a GeoJSON
        catchment_geojson = json.loads(gdf.to_json())

        return catchment_geojson["features"][0]
    
    def get_all_stations_gauge_locations(self) -> dict:
        """
        Get the locations of all stations in GeoJSON format.
        
        """
        # Construct the file path
        file_path = os.path.join(self.data_directory, 'CAMELS_DE_catchment_boundaries/gauging_stations/CAMELS_DE_gauging_stations.gpkg')
        
        # Read the data from the file
        gdf = gpd.read_file(file_path)

        # Convert the geometry to EPSG:4326
        gdf = gdf.to_crs(epsg=4326)

        return json.loads(gdf.to_json())