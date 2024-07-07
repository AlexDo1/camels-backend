import json

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from camels_datasetloader import CAMELS_DE

from camels.models import StationResponse, StationTimeseriesData, StationCatchmentAttributes, StationCatchmentGeometry, StationLocationGeometry


app = FastAPI()

# Allow local frontend to connect from this origin
origins = [
    "http://localhost:3000", 
]

# Add CORS middleware to the app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# initialize the data handler
camels = CAMELS_DE()

@app.get("/stations/{gauge_id}", response_model=StationResponse)
def get_station(gauge_id: str):
    # get the hydrometerological timeseries data for the station
    timeseries_data = camels.get_timeseries(gauge_id)

    # check response
    if not timeseries_data.empty:
        timeseries_data = timeseries_data.to_dict(orient='records')
    else:
        raise HTTPException(status_code=404, detail=f"Timeseries data for Station with id {gauge_id} not found")
    
    # get the catchment attributes for the station
    catchment_attributes = {}

    # get the topographic, soil, landcover, hydrogeology, humaninfluence, climatic, hydrologic, and simulation_benchmark attributes for the station
    for attribute_type in ["topographic", "soil", "landcover", "hydrogeology", "humaninfluence", "climatic", "hydrologic", "simulation_benchmark"]:
        attributes = camels.get_attributes(attribute_type, gauge_id)
        if not attributes.empty:
            catchment_attributes[attribute_type] = attributes.to_dict(orient='records')[0]
        else:
            raise HTTPException(status_code=404, detail=f"{attribute_type} attributes data for Station with id {gauge_id} not found")
    
    # get the catchment shape data for the station
    station_catchment_geometry = camels.get_catchments_geometry(gauge_id)
    station_catchment_geometry = json.loads(station_catchment_geometry.to_json(to_wgs84=True))
    # a feature collection is returned, check that we only have one feature and return it
    if len(station_catchment_geometry["features"]) == 1:
        station_catchment_geometry = station_catchment_geometry["features"][0]
    else:
        raise HTTPException(status_code=404, detail=f"Catchment geometry data for Station with id {gauge_id} contains more than one feature.")
    
    # get the station location
    station_location_geometry = camels.get_stations_geometry(gauge_id)
    station_location_geometry = json.loads(station_location_geometry.to_json(to_wgs84=True))
    # a feature collection is returned, check that we only have one feature and return it
    if len(station_location_geometry["features"]) == 1:
        station_location_geometry = station_location_geometry["features"][0]
    else:
        raise HTTPException(status_code=404, detail=f"Location geometry data for Station with id {gauge_id} contains more than one feature.")

    # create the response
    response = StationResponse(
        timeseries= StationTimeseriesData(data=timeseries_data),
        catchment_attributes=StationCatchmentAttributes(**catchment_attributes),
        catchment_geometry=StationCatchmentGeometry(**station_catchment_geometry),
        location_geometry=StationLocationGeometry(**station_location_geometry)
    )

    return response

@app.get("/all_stations/gauge_locations")
def get_all_stations_gauge_locations():
    try:
        # get the geojson data for all stations
        stations_location_geometry = camels.get_stations_geometry()

        # convert the GeoPandas DataFrame to a GeoJSON
        stations_location_geometry = stations_location_geometry

        return JSONResponse(content=json.loads(stations_location_geometry.to_json(to_wgs84=True)))
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="GeoJSON data for all stations not found.")
    

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)