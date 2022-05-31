from pathlib import Path
import pandas as pd
import os
from pathlib import Path
import json as js
from datetime import datetime
from matplotlib import pyplot as plt
from PCA_test import doPCA
from PCA_test import doLDA

class Filehandling:

    # creates directory for files
    def mkdir(path, folder):
        path = os.path.join(path, folder)
        Path(path).mkdir(parents=True, exist_ok=True)
        return path

    # lists files in directory
    def list_files(path):
        return os.listdir(path)

    # saves dataframe in directory
    def save_df(df, path, name):
        path = path + '\\results'
        Path(path).mkdir(parents=True, exist_ok=True)
        path = path + '\\' + name + '.csv'
        print("{0} saved as {1}".format(name,path))
        df.to_csv(path, sep=';', decimal=',', index = True)
    # sorts files and only shows files with special filenames
    def sort_files(path):
        files = Filehandling.list_files(path)
        file_names = ['peak_identification', 'peak_spectra', 'chromatogramm']
        dict_files = {}
        for i in file_names:
            for n in files:
                if n.find(i) >= 0:
                    dict_files[i] = os.path.join(path, n)
                else:
                    pass
        return dict_files

    
    def list_files_entire_path(path):
        print([os.path.join(path, i) for i in os.listdir(path) ])
        return [os.path.join(path, i) for i in os.listdir(path) ]


    # creates a list with all subdirectories with depth 3, files can be included
    def create_sub_list(path):
        sub1 = Filehandling.list_files_entire_path(path) # Locations
        sub2 = [] # date
        sub3 = []# number
        for i in sub1:
            sub2 += Filehandling.list_files_entire_path(i)
        for i in sub2:
            try:
                sub3 += Filehandling.list_files_entire_path(i)
            except Exception as e:
                print(f'problems while checking {i}')  
        return Filehandling.clean_subs(sub3)


    # deleting files and add their parent folder
    def clean_subs(subs):
        reduced_subs = []
        for i in subs:
            if i.find('.csv') < 0 and i.find('results') < 0:
                reduced_subs.append(i)
            else:
                reduced_subs.append(i[:i.rfind('\\')])
        reduced_subs = list(set(reduced_subs))
        return reduced_subs


def extract_properties(path):
    myList = path.split('\\')
    print(myList)
    if len(myList[-1]) >1:
        name = myList[-2] 
        date = myList[-1]
    else:
        name = myList[-3] 
        date = myList[-2]

    return date,name


def main(path_root):
    directorys = Filehandling.create_sub_list(path_root)
    dfResult = pd.DataFrame()
    dates  = []
    names = []


    for path in directorys:
        date, name = extract_properties(path)
        dates.append(date)
        names.append(name)
        
        dict_path = Filehandling.sort_files(path)
        thisDf = pd.read_csv(dict_path['chromatogramm'], delimiter='\t', decimal='.', header=10, encoding='latin1')
        thisDf.set_index('Ret.Time', inplace=True)
        thisDf.drop('Relative Intensity', axis=1, inplace=True)
        dfResult = pd.concat([dfResult, thisDf], axis=1)
        
        # print(thisDf.head())
        # print(dict_path['chromatogramm'])
    dfResult = dfResult.T
    dfResult = dfResult.fillna(0)
    dfResult = dfResult.reset_index(drop=True)
    dfResult['date'] = dates
    dfResult['name'] = names
    
    print(dfResult[dfResult['name'] == 'Bluete'])
    dt_string = datetime.now().strftime("%d-%m-%Y_%H-%M-%S") 
    dt_string = dt_string + '_results.csv'
    pathSavePCA = os.path.join(path_root,'resultsPCA')
    Path(pathSavePCA).mkdir(parents=True, exist_ok=True)
    pathSavePCA = os.path.join(pathSavePCA, dt_string)
    dfResult.to_csv(pathSavePCA, decimal='.', sep='\t', index=False)
    doPCA(pathSavePCA)
    
    pathSaveLDA = os.path.join(path_root,'resultsLDA')
    Path(pathSaveLDA).mkdir(parents=True, exist_ok=True)
    pathSaveLDA = os.path.join(pathSaveLDA, dt_string)
    dfResult.to_csv(pathSaveLDA, decimal='.', sep='\t', index=False)
    doLDA(pathSaveLDA)


  

main('C:\\Users\\sverme-adm\\Desktop\\data')