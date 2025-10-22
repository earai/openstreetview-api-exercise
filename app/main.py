import sys
import os

from fastapi import FastAPI, Body, Depends, Query
from sqlmodel import Session

from app.db import init_db, get_session
from app.utils import fetch_osm_by_polygon, write_mock_geojson_to_db

app = FastAPI(title="OSM FastAPI with PostGIS Cache")
MOCK_FILE_PATH=os.getenv("MOCK_FILE_PATH","./tests/test_data")
mock_amenity_file = "amenities_region1_trunc.geojson"
# -------------------------------------------------------
# 🧭 Initialize Database on Startup
# -------------------------------------------------------
@app.on_event("startup")
def on_startup():
    print("🚀 Initializing database and creating tables…", flush=True)
    try:
        init_db()
        print("✅ Database initialization complete.", flush=True)
    except Exception as e:
        print(f"❌ Database initialization failed: {e}", file=sys.stderr, flush=True)

# -------------------------------------------------------
# 🟡 Polygon Amenity Endpoints
# -------------------------------------------------------
@app.post("/osm/amenity/polygon")
def get_osm_amenity_polygon(
    polygon: dict = Body(...),
    mock_mode: bool = Query(False, description="If true, return mock amenity data instead of querying OSM"),
    session: Session = Depends(get_session)
):
    key = 'amenity'
    value = None
    print('mock mode: ', mock_mode)

    if mock_mode:
        filename = os.path.join(MOCK_FILE_PATH, mock_amenity_file)
        return write_mock_geojson_to_db(filename, key, value, session)

    query_template = """
        [out:json];
        (
            node["amenity"](poly:"{poly}");
        );
        (._;>;);
        out geom;
    """
    #this returns geojson features)
    return fetch_osm_by_polygon(polygon, key=key, value=value, query_template=query_template, session=session)

# -------------------------------------------------------
# 🟡 Polygon Point of Interest Endpoints
# -------------------------------------------------------
@app.post("/osm/roads/polygon")
def get_osm_roads_polygon(
    polygon: dict = Body(...),
    session: Session = Depends(get_session)
):
    query_template = """
        [out:json];
        (
            way["highway"](poly:"{poly}");
        );
        (._;>;);
        out geom;
    """
    return fetch_osm_by_polygon(polygon, key="highway", value=None, query_template=query_template, session=session)

