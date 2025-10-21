from typing import List, Optional

import psycopg2
from sqlmodel import Session
from sqlalchemy import text
import json

def is_area_covered(session: Session, aoi_wkt: str, key: Optional[str], value: Optional[str]) -> bool:
    """Return True if the union of cached geometries for this key/value covers the AOI."""
    print(f"Checking area coverage for AOI: {aoi_wkt}, key: {str(key)}, value: {value}")
    params = {"aoi": aoi_wkt,"key":str(key)}

    sql = f"""
    SELECT COUNT(*) AS feature_count 
    FROM public.osm_cache
    WHERE query_key = :key AND ST_Intersects(
        geom,
        ST_GeomFromText(
            :aoi,
            4326
        )
    ); """
    result_tmp = session.execute(text(sql), params)
    #pull_new_poly = session.fetchone()
    print("RESULT_TMP :", type(result_tmp), result_tmp)
    result = session.execute(text(sql), params).first()
    print("RESULT     :", type(result))
    #print(f"result: {result}")
    if not result:
        return False
    return bool(result[0])


def get_cached_features_intersecting(session: Session, aoi_wkt: str, key: Optional[str], value: Optional[str]) -> dict:
    """Return a GeoJSON FeatureCollection of cached features that intersect the AOI."""
    print("in cached features intersection")

    params = {"aoi": aoi_wkt}
    where_clause = ""
    if key is not None:
        where_clause += " AND query_key = :k"
        params["k"] = key
    if value is not None:
        where_clause += " AND query_value = :v"
        params["v"] = value

    print("params", params)
    print("where clause", where_clause)

    sql = f"""
    SELECT id, ST_AsGeoJSON(geom) as geom_json, properties
    FROM osm_cache
    WHERE ST_Intersects(geom, ST_GeomFromText(:aoi,4326)) {where_clause}
    """

    print('sql', sql)
    rows = session.execute(text(sql), params).all()
    print("number of rows", len(rows))
    features = []
    for r in rows:
        geom_json = json.loads(r[1]) if r[1] else None
        props = r[2] or {}
        features.append({
            "type": "Feature",
            "properties": props,
            "geometry": geom_json
        })
    print("features", features)
    return {"type": "FeatureCollection", "features": features}


def insert_features(session: Session, features: List[dict], key: Optional[str], value: Optional[str]) -> None:
    """Insert GeoJSON features into osm_cache. Uses ST_GeomFromGeoJSON for geometry."""

    insert_sql = text(
        "INSERT INTO osm_cache (query_key, query_value, geom, properties) "
        "VALUES (:k, :v, ST_SetSRID(ST_GeomFromGeoJSON(:geojson),4326), :props)"
    )
    for feat in features:
        geom = feat.get("geometry")
        props = feat.get("properties") or {}
        if not geom:
            continue
        geojson_text = json.dumps(geom)
        params = {"k": key, "v": value, "geojson": geojson_text, "props": json.dumps(props)}

        try:
            session.execute(insert_sql, params)
            session.commit()
        except psycopg2.Error as e:
            print(f"Error: {e}")
            session.rollback()