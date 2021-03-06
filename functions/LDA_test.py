import pandas as pd
import os
from pathlib import Path
import json as js
import plotly.express as px
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis



def doLDA(path):
    pathPlot = path[:path.rfind('.csv')] +'.html' 

    df = pd.read_csv(path, delimiter = ',', decimal='.')
    x = df.drop(['date', 'name', 'label'], axis=1).values
    
    y =  df['name']

    lda = LinearDiscriminantAnalysis(n_components=3)
    linearComponents = lda.fit_transform(x, y)
    dfLDA = pd.DataFrame(data = linearComponents, columns=['LD1','LD2', 'LD3'])
    dfLDA['label'] = y
    dfLDA['name']= df['name']
    dfLDA['date'] = df['date']
    fig = px.scatter_3d(dfLDA, x='LD1', y='LD2', z='LD3', color='label', custom_data=['name', 'date'])
    fig.update_traces(
    hovertemplate="<br>".join([
        "LD1: %{x}",
        "LD2: %{y}",
        "LD3: %{z}",
        "name: %{customdata[0]}",
        "date: %{customdata[1]}",
        
    ]))

    
    fig.write_html(pathPlot)
    fig.show()


doLDA('C:\\Users\sverme-adm\\Desktop\\data\\resultsPCA\\01-06-2022_10-43-31_results.csv')



