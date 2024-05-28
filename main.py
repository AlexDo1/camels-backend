from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from camels.station import Station
from camels.data_handler import DataHandler
from camels.models import StationResponse


app = FastAPI()
data_handler = DataHandler(data_directory="/app/data/camels_de/")

@app.get("/stations/{station_id}", response_model=StationResponse)
def get_station(station_id: str):
    # get the hydrometerological timeseries data for the station
    timeseries_data = data_handler.get_station_timeseries_data(station_id)

    # check response
    if timeseries_data.empty:
        raise HTTPException(status_code=404, detail=f"Timeseries data for Station with id {station_id} not found")
    
    # get the topographic data for the station
    topographic_data = data_handler.get_station_topographic_data(station_id)

    # check response
    if topographic_data.empty:
        raise HTTPException(status_code=404, detail=f"Topographic data for Station with id {station_id} not found")
    
    # get the catchment shape data for the station
    catchment = data_handler.get_station_catchment_shape(station_id)

    # initialize the station object
    station = Station(
        station_id, 
        timeseries=timeseries_data.to_dict(orient='records'),
        topographic_data=topographic_data.to_dict(orient='records')[0],
        catchment=catchment
    )

    # create the response
    response = StationResponse(
        metadata=station.get_metadata(),
        timeseries=station.get_timeseries(),
        catchment=station.get_catchment()
    )

    return response

@app.get("/all_stations/gauge_locations")
def get_all_stations_gauge_locations():
    try:
        # get the geojson data for all stations
        geojson_data = data_handler.get_all_stations_gauge_locations()
        return JSONResponse(content=geojson_data)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="GeoJSON data for all stations not found (CAMELS_DE_gauging_stations.gpkg)")
    

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)