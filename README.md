# openstreetview-api-exercise
Prompt: Create a REST API that has endpoints for different types of data (roads, POIs, etc.) from OpenStreetMap (OSM), caches the fetched data in a database, and returns properly formatted geojson to the user. Queries should check the cached data first before reaching out to OSM. If data exists for part of a submitted AOI, only fetch the missing data and ensure complete data capture for the AOI. The endpoints should take as input an Area of Interest (Polygon) in geojson format.

Getting started:
Assumptions: docker and docker-compose are available on the machine being used

1. Clone the repository: 
   git clone ...

2. Build the docker image
   docker build -t osm-fastapi-api .

3. Run ./demo_run.ps
4. Formatted geojson output is stored in the geojson_output directory and can be inspected via text editor.
