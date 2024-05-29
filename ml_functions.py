from db_functions import *
import pandas as pd
import sqlite3
import numpy as np
import sklearn

# takes conn and creates db of incidents joined with locations
def get_incidents_join_locations(conn):
    get_incidents_sql = """
    SELECT
	    CAST(strftime('%Y', Datetime) AS INTEGER) Year,
	    CAST(strftime('%m', Datetime) AS INTEGER) Month,
	    CAST(strftime('%d', Datetime) AS INTEGER) Day,
	    CAST(strftime('%w', Datetime) AS INTEGER) WeekDay,
	    CAST(strftime('%H', Datetime) AS INTEGER) Hour,
	    Neighborhood,
	    Latitude,
	    Longitude,
	    Zip_Code,
        Incident_Type
    FROM
	    Incidents
	    INNER JOIN Location ON Location.Location_ID = Incidents.Location_ID
    """
    incident_rows = execute_sql_statement(get_incidents_sql,conn)
    df = pd.read_sql_query(get_incidents_sql, conn)
    return df