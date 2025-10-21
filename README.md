# openstreetview-api-exercise
Prompt: Create a REST API that has endpoints for different types of data (roads, POIs, etc.) from OpenStreetMap (OSM), caches the fetched data in a database, and returns properly formatted geojson to the user. Queries should check the cached data first before reaching out to OSM. If data exists for part of a submitted AOI, only fetch the missing data and ensure complete data capture for the AOI. The endpoints should take as input an Area of Interest (Polygon) in geojson format.

Response: A REST API using the FastAPI framework and PostGIS database is implemented. Two exemplar endpoints are implemented, one for roads and one for amenities.


Limitations: ...


Getting started:
Assumptions: docker and docker-compose are available on the machine being used

1. Clone the repository: 
   git clone ...

2. Build the docker image
   docker build -t osm-fastapi-api .

3. Run ./demo_run.sh
   This script does the following:
      Brings up the FastAPI and PostGIS database services
      Confirms the database is initially empty
      Queries OSM for amenity data in the blue region
      Populates amenity data in the blue region into PostGIS database table public.osm_cache
      Returns counts (total entries, entries with key=amenity, entries with key = highway) on that database table t       to stdout
      Queries OSM for road data in the green region

      

   Formatted geojson output is stored in the geojson_output directory and can be inspected via text editor.


<img width="1238" height="714" alt="image" src="https://github.com/user-attachments/assets/afcd5454-f70e-4437-8d64-491c3f3cdf15" />
