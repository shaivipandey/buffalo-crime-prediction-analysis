from ml_functions import *
from db_functions import *
from knn import *

normalized_db_filename = "normalized.db"
normalized_conn = create_connection(normalized_db_filename)

df = get_incidents_join_locations(normalized_conn)
perform_knn(df)
