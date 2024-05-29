from db_functions import *

incident_type_dict = {
    "AGG ASSAULT ON P/OFFICER": "ASSAULT",
    "AGGR ASSAULT": "ASSAULT",
    "ASSAULT": "ASSAULT",
    "Assault": "ASSAULT",
    "BURGLARY": "BURGLARY",
    "Breaking & Entering": "BURGLARY",
    "CRIM NEGLIGENT HOMICIDE": "MURDER",
    "Homicide": "MURDER",
    "LARCENY/THEFT": "LARCENY/THEFT",
    "MANSLAUGHTER": "MURDER",
    "MURDER": "MURDER",
    "Other Sexual Offense": "SEXUAL ABUSE",
    "RAPE": "RAPE",
    "ROBBERY": "ROBBERY",
    "Robbery": "ROBBERY",
    "SEXUAL ABUSE": "SEXUAL ABUSE",
    "Sexual Assault": "RAPE",
    "THEFT OF SERVICES": "THEFT OF SERVICES",
    "Theft": "LARCENY/THEFT",
    "Theft of Vehicle": "UUV",
    "UUV": "UUV"
}

def create_zip_code_table(normalized_conn, non_normalized_conn):
    drop_table(normalized_conn, "Location")

    zip_code_table_stmt = """
    CREATE TABLE Zip_Code (
        Zip_Code TEXT NOT NULL PRIMARY KEY
    )
    """
    create_table(normalized_conn, zip_code_table_stmt, "Zip_Code")

    get_zip_codes_stmt = "SELECT DISTINCT ZIP_Code FROM Incidents ORDER BY ZIP_Code"
    zip_codes = execute_sql_statement(get_zip_codes_stmt, non_normalized_conn)
    insert_sql = "INSERT INTO Zip_Code(Zip_Code) VALUES (?)"

    insert(normalized_conn, insert_sql, zip_codes)

def create_location_table(normalized_conn, non_normalized_conn):
    location_table_stmt = """
        CREATE TABLE Location (
            Location_ID INTEGER NOT NULL PRIMARY KEY,
            Latitude REAL,
            Longitude REAL,
            Zip_Code TEXT,
            UNIQUE(Latitude, Longitude),
            FOREIGN KEY(Zip_Code) REFERENCES Zip_Code(Zip_Code)
        )
    """
    create_table(normalized_conn, location_table_stmt, "Location")

    get_locations_stmt = "SELECT DISTINCT Location, ZIP_Code FROM Incidents ORDER BY ZIP_Code"
    locations = execute_sql_statement(get_locations_stmt, non_normalized_conn)

    insert_sql = "INSERT INTO Location(Latitude, Longitude, Zip_Code) VALUES(?, ?, ?)"
    values = []
    for location, zip_code in locations:
        location_coords = location.split(" ")
        latitude = float(location_coords[1][1:])
        longitude = float(location_coords[2][:-1])
        values.append((latitude, longitude, zip_code))
    insert(normalized_conn, insert_sql, values)

# INCIDENT TABLE 
def create_incident_type_table(normalized_conn, non_normalized_conn):
    incidents_table_stmt = """
    CREATE TABLE Incident_Type (
        Incident_Type TEXT NOT NULL PRIMARY KEY
    )
    """
    create_table(normalized_conn, incidents_table_stmt, "Incident_Type")

    get_descriptions_stmt = "SELECT DISTINCT Incident_Type FROM Incidents ORDER BY Incident_Type"
    incident_types = execute_sql_statement(get_descriptions_stmt, non_normalized_conn)
    filtered_types = set((incident_type_dict[incident_type[0]],) for incident_type in incident_types)

    insert_incidents_sql = "INSERT INTO Incident_Type(Incident_Type) VALUES(?)"
    insert(normalized_conn, insert_incidents_sql, list(filtered_types))


def get_loc_dic(conn):
    get_location_id_stmt='SELECT Location_ID,Latitude,Longitude FROM Location' 
    location_rows=execute_sql_statement(get_location_id_stmt,conn)

    loc_ids={}
    for id,lat,long in location_rows:
        loc_ids[(lat, long)]=id

    return loc_ids

# NEIGHBORHOOD TABLE 
def create_neighborhood_table(normalized_conn, non_normalized_conn):
    neighborhood_table_stmt = """
    CREATE TABLE Neighborhood (
        Neighborhood TEXT NOT NULL PRIMARY KEY
    )
    """
    create_table(normalized_conn, neighborhood_table_stmt, "Neighborhood")
   
    get_neighborhood_data_stmt = "SELECT DISTINCT Neighborhood FROM Incidents ORDER BY Neighborhood"
    neighborhood_data = execute_sql_statement(get_neighborhood_data_stmt, non_normalized_conn)

    insert_neighborhood_sql = "INSERT INTO Neighborhood (Neighborhood) VALUES (?)"
    insert(normalized_conn, insert_neighborhood_sql, neighborhood_data)

def create_incident_table(normalized_conn, non_normalized_conn):
    incident_table_stmt='''CREATE TABLE Incidents (
        Incident_ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        Datetime TEXT NOT NULL,
        Incident_Type TEXT NOT NULL,
        Location_ID INTEGER NOT NULL,
        Neighborhood TEXT NOT NULL,
        FOREIGN KEY(Incident_Type) REFERENCES Incident_Type(Incident_Type),
        FOREIGN KEY(Neighborhood) REFERENCES Neighborhood(Neighborhood)
    )'''
    create_table(normalized_conn, incident_table_stmt, "Incidents")

    get_incident_stmt='SELECT Incident_ID,Incident_Datetime,Incident_Type,Location,Neighborhood FROM Incidents'

    incident_rows=execute_sql_statement(get_incident_stmt,non_normalized_conn)
    
    loc_ids=get_loc_dic(normalized_conn)

    incident_modified_rows = []
    for i,row in enumerate(incident_rows):
        incident_id,datetime,incident_type,location,neighborhood=row

        # fix loc format
        location_coords = location.split(" ")
        latitude = float(location_coords[1][1:])
        longitude = float(location_coords[2][:-1])
        loc_id=loc_ids[(latitude,longitude)]

        # fix datetime format
        new_datetime=datetime.split('-')
        new_datetime[1]=new_datetime[1] if int(new_datetime[1])>9 else '0'+new_datetime[1]
        new_datetime='-'.join(new_datetime)

        # fix incident type
        filtered_type = incident_type_dict[incident_type]

        incident_modified_rows.append((incident_id,new_datetime,filtered_type,loc_id,neighborhood))

    insert_incident_stmt='''INSERT INTO Incidents VALUES (?,?,?,?,?)'''
    insert(normalized_conn, insert_incident_stmt,incident_modified_rows)









