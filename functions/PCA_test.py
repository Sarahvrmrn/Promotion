import pandas as pd
import os
from pathlib import Path
import json as js
import plotly.express as px
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler





def doPCA(path):
    pathPlot = path[:path.rfind('.csv')] +'.html' 

    df = pd.read_csv(path, delimiter = '\t', decimal='.')
    x = df.drop(['date', 'name'], axis=1).values
    x = StandardScaler().fit_transform(x)
    y =  df['name']

    pca = PCA(n_components=3)
    principalComponents = pca.fit_transform(x)
    dfPCA = pd.DataFrame(data= principalComponents, columns=['PC1', 'PC2', 'PC3'])
    dfPCA['label'] = y
    dfPCA['name'] = df['name']
    dfPCA['date'] = df['date']
    

    fig = px.scatter_3d(dfPCA, x='PC1', y='PC2', z='PC3', color='label', custom_data=['name', 'date'])
    fig.update_traces(
    hovertemplate="<br>".join([
        "PC1: %{x}",
        "PC2: %{y}",
        "PC3: %{z}",
        "name: %{customdata[0]}",
        "date: %{customdata[1]}",
        
    ])
)


    fig.write_html(pathPlot)
    fig.show()



if __name__ == '__main__':
    path = 'C:\\Users\\sverme-adm\\Desktop\\data\\results\\24-05-2022_17-16-45_results.csv'
    doPCA(path)



