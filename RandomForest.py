from db_functions import *
from ml_functions import *

import pandas as pd
import sqlite3
import numpy as np
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.tree import plot_tree
from sklearn.model_selection import cross_val_score
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import KFold
from sklearn.metrics import precision_recall_fscore_support

def perform_RF(df,max_n=100):
	X=df[['Month','Day','WeekDay','Hour','Latitude','Longitude','Neighborhood','Zip_Code']]
	X=pd.get_dummies(X)
	y=df[['Incident_Type']]
    
	scores=[]
	for n in range(1,max_n):
		splits=KFold(n_splits=5,shuffle=True, random_state=42)

		for train_index,test_index in splits:
			rf=RandomForestClassifier(n_estimators=n)

			X_train=X.iloc[train_index]
			X_test=X.iloc[test_index]
			y_train=y.iloc[train_index]
			y_test=y.iloc[test_index]

			rf.fit(X_train,y_train)

			pred=rf.predict(X_test)
			actual=y_test

		
scores
        
        