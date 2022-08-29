import pandas as pd
import os
from pathlib import Path
import json as js
import plotly.express as px
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from datetime import datetime
import test


components_PCA = 3
components_LDA = 3

def doPCA(df, path, name):
    pathPlot = os.path.join(path, name+'_PCA.html')
    pathData = os.path.join(path, name+'_PCA.csv')

    x = df.drop(['date', 'name'], axis=1).values
    x = StandardScaler().fit_transform(x)
    y = df['name']

    pca = PCA(n_components=components_PCA)
    principalComponents = pca.fit_transform(x)
    dfPCA = pd.DataFrame(data=principalComponents, columns=[
                         f'PC{i+1}' for i in range(components_PCA)])
    
    dfPCA['label'] = y
    dfPCA['name'] = df['name']
    dfPCA['date'] = df['date']
    dfPCA.to_csv(pathData)
    print(pca.explained_variance_ratio_)
    if components_PCA == 3:
        fig = px.scatter_3d(dfPCA, x='PC1', y='PC2', z='PC3',
                            color='label', custom_data=['name', 'date'])
        fig.update_traces(
        hovertemplate="<br>".join([
            "PC1: %{x}",
            "PC2: %{y}",
            "PC3: %{z}",
            "name: %{customdata[0]}",
            "date: %{customdata[1]}",
        ]))

        dfPCA.to_csv(pathData, sep='\t', decimal='.')
        fig.write_html(pathPlot)
        fig.show()
        
    return dfPCA


def doLDA(df, path, name):
    pathPlot = os.path.join(path, name+'_LDA.html')
    pathData = os.path.join(path, name+'_LDA.csv')


    y =  df['name']
    print(y)
    x = df.drop(['date', 'name', 'label'], axis=1).values
    print(f'components_LDA {components_LDA}, y_unique: {y.unique}')
    lda = LinearDiscriminantAnalysis(n_components=components_LDA)
    # linearComponents = lda.fit_transform(x, y)
    linearComponents = lda.fit_transform(x,y)
    dfLDA = pd.DataFrame(data = linearComponents, columns=['LD1', 'LD2', 'LD3'])
    dfLDA['label'] = y
    dfLDA['name']= df['name']
    dfLDA['date'] = df['date']
    print(lda.explained_variance_ratio_)
    if components_LDA == 3:
        fig = px.scatter_3d(dfLDA, x='LD1', y='LD2', z='LD3', color='label', custom_data=['name', 'date'])
        fig.update_traces(
        hovertemplate="<br>".join([
            "LD1: %{x}",
            "LD2: %{y}",
            "LD3: %{z}",
            "name: %{customdata[0]}",
            "date: %{customdata[1]}",  
        ]))

        dfLDA.to_csv(pathData, sep='\t', decimal='.')
        fig.write_html(pathPlot)
        fig.show()
    
    return dfLDA


if __name__ == '__main__':
    path = 'C:\\Users\\sverme-adm\\Desktop\\data\\results\\24-05-2022_17-16-45_results.csv'
    # doPCA(path)



