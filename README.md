# openstreetview-api-exercise
Prompt: Create a REST API that has endpoints for different types of data (roads, POIs, etc.) from OpenStreetMap (OSM), caches the fetched data in a database, and returns properly formatted geojson to the user. Queries should check the cached data first before reaching out to OSM. If data exists for part of a submitted AOI, only fetch the missing data and ensure complete data capture for the AOI. The endpoints should take as input an Area of Interest (Polygon) in geojson format.

## Response: 
A REST API using the FastAPI framework and PostGIS database is implemented. Two exemplar endpoints are implemented, one for roads and one for amenities. Both take a geojson polygon as input.


### Limitations/To Dos:
This implementation does not handle identifying the missing data from a partially overlapping polygon and fetching only that data from OSM. This is in progress in another working repo.

Overpass sometimes times out when requests are made. It would be useful for endpoints to be able to have a real or mock data mode. This feature is also in progress in the aforemnetioned working repo.


## Getting started:
### Assumptions: 
   Docker and docker-compose are available on the machine being used

1. Clone the repository: \
   git clone https://github.com/earai/openstreetview-api-exercise.git

2. Build the docker image \
   docker build -t osm-fastapi-api .

3. Run ./demo_run.sh \
     This script does the following: 
      - Brings up the FastAPI and PostGIS database services
      - Confirms the database is initially empty
      - Queries OSM for amenity data in the blue region
      - Populates amenity data in the blue region into PostGIS database table public.osm_cache
      - Returns counts (total entries, entries with key=amenity, entries with key = highway) on that database table to stdout
      - Checks cache, queries OSM for road data in the green region
      - Writes road data to public.osm_cache
      - Returns updated counts on the database to stdout
      - Request for the same amenity data as before is issued, the cache is checked and no new API calls to OSM are issued
      - Returns counts on the database again
      - Request for amenity data in the purple area that overlaps the green road area.
      - Cache is checked, and data is requested from OSM since the objects have different keys (amenity vs highway)
      - Data is written to database
      - Returns updated counts on the database to stdout
      
   Formatted geojson output from each Overpass request is stored in the geojson_output directory and can be inspected via text editor.

<img width="1265" height="680" alt="image" src="https://github.com/user-attachments/assets/eff94007-202d-4075-8ae4-8625f5467fe3" />

