import sqlite3
from db_functions import *

def create_non_normalized_table(csv_filename, non_normalized_db_filename):

    non_normalized_conn=create_connection(non_normalized_db_filename)

    create_non_normalized_sql='''
    CREATE TABLE IF NOT EXISTS 
        Incidents (Incident_ID INT NOT NULL PRIMARY KEY,
        Incident_Datetime INT NOT NULL, Incident_Type TEXT NOT NULL, 
        Incident_Hour INT NOT NULL, Incident_Day TEXT NOT NULL, 
        Location TEXT NOT NULL, Neighborhood TEXT NOT NULL, ZIP_Code INT NOT NULL)'''

    create_table(non_normalized_conn,create_non_normalized_sql,drop_table_name='Incidents')

    # parse CSV file
    with open(csv_filename,'r') as f:
        next(f)
        
        insert_incident_sql = '''
        INSERT INTO Incidents
            (Incident_ID,
            Incident_Datetime, 
            Incident_Type, 
            Incident_Hour, 
            Incident_Day, 
            Location,
            Neighborhood, 
            ZIP_Code) 
        VALUES(?,?,?,?,?,?,?,?)'''

        # datetime, type, hour, day, location, neighborhood, zip
        column_indices=[1,3,6,7,11,22,28]
        
        incidents=[] # collect rows to insert
        incident_id = 1 # unique id
        
        # iterate through rows
        for line in f:
            line_split=line.split(',')
            row = [incident_id]+[line_split[i] for i in column_indices] 
            if not ('' in row or 'UNKNOWN' in row): # only insert complete rows
                incidents.append(row)
                incident_id+=1 # get new id
                
        insert(non_normalized_conn,insert_incident_sql,incidents)