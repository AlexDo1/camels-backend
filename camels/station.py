from camels.models import StationMetadata, StationTimeseriesData, StationCatchment

from typing import List

class Station:
    """
    Class to represent a station in the CAMELS-DE dataset.
    
    Parameters
    ----------
    station_id : str
        The CAMELS-DE station ID.

    """
    def __init__(self, station_id, timeseries, topographic_data, catchment):
        self.station_id = station_id
        self.timeseries = timeseries
        self.topographic_data = topographic_data
        self.catchment = catchment
    
    def get_metadata(self):
        return StationMetadata(
            station_id=self.station_id,
            station_name=self.topographic_data["gauge_name"],
            water_body_name=self.topographic_data["water_body_name"],
            provider_id=self.topographic_data["provider_id"],
            federal_state=self.topographic_data["federal_state"],
            location={"lat": self.topographic_data["gauge_lat"], "lon": self.topographic_data["gauge_lon"]}
        )
    
    def get_timeseries(self) -> StationTimeseriesData:
        return StationTimeseriesData(
            data=self.timeseries
        )
    
    def get_catchment(self):
        return StationCatchment(
            properties={"station_id": self.station_id},
            geometry=self.catchment["geometry"]
        )

