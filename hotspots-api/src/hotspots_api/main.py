from fastapi.middleware.cors import CORSMiddleware
import redis
from fastapi import FastAPI, Depends, UploadFile, File
from fastapi.responses import JSONResponse
import os
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine
import json
from geojson_pydantic import FeatureCollection
import pandas as pd
import geopandas as gpd

models.Base.metadata.create_all(bind=engine)

rd = redis.Redis(host="localhost", port=6379, db=0)

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def make_response_hotspot_properties(hotspot):
    return schemas.HotspotProperties(hotspot_id=hotspot.hotspot_id, radius=hotspot.radius, tz=hotspot.tz, satellite=hotspot.satellite) 

def make_response_hotspot_feature(hotspot, db):
    feature = json.loads(db.scalar(hotspot.geometry.ST_AsGeoJSON()))
    props = make_response_hotspot_properties(hotspot)
    return schemas.HotspotFeature(type="Feature", geometry=feature, properties=props) 

def make_response_hotspot_collection(hotspots, db):
    response = []
    for i in hotspots:
        response.append(make_response_hotspot_feature(i, db))
    feature_collection = FeatureCollection(type='FeatureCollection', features=response)
    return feature_collection

# @app.get("/hotspots/redis", response_model=schemas.HotspotCollection)
@app.get("/hotspots/redis") 
async def read_hotspots_redis():
    return JSONResponse(json.loads(rd.get('hotspots')))
    
@app.get("/hotspots/", response_model=schemas.HotspotCollection)
async def read_hotspots_bbox_time(start_date: str, end_date: str, bounding_box: str, db: Session = Depends(get_db)):
    db_hotspots = crud.get_hotspots_datetime_bbox(db, start_date=start_date, end_date=end_date, bbox=bounding_box)
    hotspots_feature_collection = make_response_hotspot_collection(db_hotspots, db)
    return hotspots_feature_collection


@app.get("/hotspots/postgis", response_model=schemas.HotspotCollection)
async def read_hotspots_postgis(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_hotspots = crud.get_hotspots(db, skip=skip, limit=limit)
    hotspots_feature_collection = make_response_hotspot_collection(db_hotspots, db)
    return hotspots_feature_collection


@app.post("/hotspots/batch-upload/")
async def create_batch_hotspots(file: UploadFile = File(...), db: Session = Depends(get_db)):
    features = []
    tmp_file = os.path.join("./", file.filename)

    with open(tmp_file, mode="wb+") as f:
        f.write(file.file.read())

    df = pd.read_csv(tmp_file)

    df['tz'] = pd.to_datetime(df['tz'])

    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.lon, df.lat), crs="EPSG:4326")

    del gdf['lon']
    del gdf['lat']

    gdf.to_postgis('hotspots', engine, if_exists='append')
    
    db_hotspots = crud.get_all_hotspots(db) 
    hotspots_feature_collection = make_response_hotspot_collection(db_hotspots, db)
    rd.delete('hotspots')
    rd.set('hotspots', hotspots_feature_collection.json())
    
    os.remove(tmp_file)

    return {"success": "data from csv was uploaded succesfully"}
    # return {"hotspots": hotspots_geojson}