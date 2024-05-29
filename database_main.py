from normalized_tables import *
from create_non_normalized import *
from ml_functions import *
from knn import *

normalized_db_filename = "normalized.db"
non_normalized_db_filename = "non_normalized.db"
csv_filename = "Crime_Incidents.csv"

#create_non_normalized_table(csv_filename, non_normalized_db_filename)

normalized_conn = create_connection(normalized_db_filename)
non_normalized_conn = create_connection(non_normalized_db_filename)

drop_table(normalized_conn, 'Incidents')
create_zip_code_table(normalized_conn, non_normalized_conn)
create_location_table(normalized_conn, non_normalized_conn)
create_incident_type_table(normalized_conn, non_normalized_conn)
create_neighborhood_table(normalized_conn, non_normalized_conn)
create_incident_table(normalized_conn,non_normalized_conn)

normalized_conn.close()
non_normalized_conn.close()