from pydantic import BaseModel
from typing import List, Dict, Union


class StationTimeseriesData(BaseModel):
    data: List[Dict]


# TODO: possibly more detailed, one model for each attribute type
class StationCatchmentAttributes(BaseModel):
    topographic: Dict
    soil: Dict
    landcover: Dict
    hydrogeology: Dict
    humaninfluence: Dict
    climatic: Dict
    hydrologic: Dict
    simulation_benchmark: Dict


class StationCatchmentGeometry(BaseModel):
    type: str = "Feature"
    properties: Dict[str, str]
    geometry: Dict[str, Union[str, List[List[List[float]]]]]


class StationLocationGeometry(BaseModel):
    type: str = "Feature"
    properties: Dict[str, str]
    geometry: Dict[str, Union[str, List[List[List[float]]]]]


class StationResponse(BaseModel):
    timeseries: StationTimeseriesData
    catchment_attributes: StationCatchmentAttributes
    catchment_geometry: StationCatchmentGeometry
    location_geometry: StationLocationGeometry
