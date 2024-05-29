import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from matplotlib import pyplot as plt
import seaborn as sns

def perform_knn(df):
    new_df = df.query("Year >= 2010 & Year <= 2015")
    X = new_df.drop(['Incident_Type', 'Neighborhood', 'Zip_Code', 'Day', 'Year'], axis = 1)
    y = new_df['Incident_Type']
    print(X)

    scores = []
    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    k_values = range(1, 3)

    for k in k_values:
        print(k)
        knn = KNeighborsClassifier(n_neighbors=k)
        score = cross_val_score(knn, X, y, cv=5)
        scores.append(np.mean(score))

    print(scores)

    sns.lineplot(x = k_values, y = scores, marker = 'o')
    plt.xlabel("K Values")
    plt.ylabel("Accuracy Score")
