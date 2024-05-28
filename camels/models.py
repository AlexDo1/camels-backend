from pydantic import BaseModel
from typing import List, Dict, Union, Optional


class StationTimeseriesData(BaseModel):
    data: List[Dict]


class StationMetadata(BaseModel):
    station_id: str
    provider_id: str
    federal_state: str
    location: Dict[str, float]
    station_name: str
    water_body_name: str


class StationCatchment(BaseModel):
    type: str = "Feature"
    properties: Dict[str, str]
    geometry: Dict[str, Union[str, List[List[List[float]]]]]


class StationResponse(BaseModel):
    metadata: StationMetadata
    timeseries: StationTimeseriesData
    catchment: StationCatchment
