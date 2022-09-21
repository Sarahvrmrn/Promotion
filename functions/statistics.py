import numpy as np
import pandas as pd
import os
from pathlib import Path
import json as js
import seaborn as sns
import plotly.express as px
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from datetime import datetime
import test
from bioinfokit.visuz import cluster


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
    print(dfPCA)

    loadings = pca.components_
    num_pc = pca.n_features_
    pc_list = ["PC"+str(i) for i in list(range(1, num_pc+1))]
    loadings_df = pd.DataFrame.from_dict(dict(zip(pc_list, loadings)))
    RT = np.arange(start=0,stop=7032)
    loadings_df['Retention Time'] = RT
    loadings_df['Retention Time'] = loadings_df['Retention Time'].apply(lambda x: x*(11.73/7032)+2)
    loadings_df.set_index('Retention Time', inplace=True)
    loadings_df.to_csv('loadings.csv')
    
    #fig_loadings = cluster.pcaplot(x=loadings[0], y=loadings[1],  labels=df.columns.values, 
    #var1=round(pca.explained_variance_ratio_[0]*100, 2), var2=round(pca.explained_variance_ratio_[1]*100, 2)) 

    #fig_loadings.show()

    #ax = sns.heatmap(loadings_df, annot=True, cmap='Spectral')
    #plt.show()
    

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


    x = df.drop(['date', 'name'], axis=1).values
    
    y =  df['name']
    lda = LinearDiscriminantAnalysis(n_components=components_LDA)
    linearComponents = lda.fit_transform(x,y)

    print(f'components_LDA {components_LDA}, y_unique: {y.unique}')
    dfLDA = pd.DataFrame(data=linearComponents, columns=[
                         f'LD{i+1}' for i in range(components_LDA)])

    dfLDA['label'] = y
    dfLDA['name']= df['name']
    dfLDA['date'] = df['date']
    print(dfLDA)
    
    scalings = lda.scalings_.T
    num_ld = lda.n_features_in_
    ld_list = ["LD"+str(i) for i in list(range(1, num_ld+1))]
    scalings_df = pd.DataFrame.from_dict(dict(zip(ld_list, scalings)))
    RT = np.arange(start=0,stop=7032)
    scalings_df['Retention Time'] = RT
    scalings_df['Retention Time'] = scalings_df['Retention Time'].apply(lambda x: x*(11.73/7032)+2)
    scalings_df.set_index('Retention Time', inplace=True)
    scalings_df.to_csv('scalings.csv')
    


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
    
'''def myplot(score,coeff,labels=None):
    xs = score[:,0]
    ys = score[:,1]
    n = coeff.shape[0]

    plt.scatter(xs ,ys, ) #without scaling
    for i in range(n):
        plt.arrow(0, 0, coeff[i,0], coeff[i,1],color = 'r',alpha = 0.5)
        if labels is None:
            plt.text(coeff[i,0]* 1.15, coeff[i,1] * 1.15, "Var"+str(i+1), color = 'g', ha = 'center', va = 'center')
        else:
            plt.text(coeff[i,0]* 1.15, coeff[i,1] * 1.15, labels[i], color = 'g', ha = 'center', va = 'center')

plt.xlabel("LD{}".format(1))
plt.ylabel("LD{}".format(2))
plt.grid()

#Call the function. '''

    


if __name__ == '__main__':
    path = 'C:\\Users\\sverme-adm\\Desktop\\data\\results\\24-05-2022_17-16-45_results.csv'
    # doPCA(path)



