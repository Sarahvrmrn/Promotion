from pathlib import Path
import pandas as pd
import os
from pathlib import Path
from datetime import datetime
from matplotlib import pyplot as plt
from statistics import doPCA, doLDA
from threading import Thread
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis


path_new = 'C:\\Users\\sverme-adm\\Desktop\\data_neu'
path_old = 'C:\\Users\\sverme-adm\\Desktop\\data'

class DataProcessing:
    def list_files_entire_path(path):
        return [os.path.join(path, i) for i in os.listdir(path)]



    def create_sub_list(path):
        sub1 = DataProcessing.list_files_entire_path(path)  # Locations
        sub2 = []  # date
        sub3 = []  # number
        for i in sub1:
            sub2 += DataProcessing.list_files_entire_path(i)
        for i in sub2:
            try:
                sub3 += DataProcessing.list_files_entire_path(i)
            except Exception as e:
                print(f'problems while checking {i}')
        return DataProcessing.clean_subs(sub3)

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
        if len(myList[-1]) > 1:
            name = myList[-2]
            date = myList[-1]
        else:
            name = myList[-3]
            date = myList[-2]
        return date, name


    def sort_files(path):
        files = DataProcessing.list_files(path)
        file_names = ['peak_identification', 'peak_spectra', 'chromatogramm']
        dict_files = {}
        for i in file_names:
            for n in files:
                if n.find(i) >= 0:
                    dict_files[i] = os.path.join(path, n)
                else:
                    pass
        return dict_files

    def list_files(path):
        return os.listdir(path)

    def readData(path_root):
        directorys = DataProcessing.create_sub_list(path_root)
        directorys = [i for i in directorys if i.find('results')<0]
        dfResult = pd.DataFrame()
        dates = []
        names = []

    # extracting data from all measurements
        for path in directorys:
            date, name = DataProcessing.extract_properties(path)
            dates.append(date)
            names.append(name)

            dict_path = DataProcessing.sort_files(path)
            thisDf = pd.read_csv(dict_path['chromatogramm'], delimiter='\t', decimal='.', header=10, encoding='latin1')
            thisDf.drop(thisDf.index[range(300)], inplace=True)
            thisDf.set_index('Ret.Time', inplace=True)
            thisDf.drop('Relative Intensity', axis=1, inplace=True)
            dfResult = pd.concat([dfResult, thisDf], axis=1)
            

        # formating df result
        dfResult = dfResult.T.fillna(0).reset_index(drop=True)
        dfResult['date'] = dates
        dfResult['name'] = names

        # cerating folder with result if not exist
        pathSave = os.path.join(path_root, 'results')
        Path(pathSave).mkdir(parents=True, exist_ok=True)


        dt_string = datetime.now().strftime("%d-%m-%Y_%H-%M-%S") 
        pathSaveResult = os.path.join(pathSave, dt_string +'_results.csv')
        
        dfResult.to_csv(pathSaveResult, decimal='.', sep='\t', index=False)
        
        # processing PCA
        df_PC = doPCA(dfResult,  pathSave, dt_string)
        

        # procesing LDA
        dfLDA = doLDA(dfResult,  pathSave, dt_string)
        #myplot(dfLDA[:,0:2], LinearDiscriminantAnalysis.scalings_) 
        #plt.show()





DataProcessing.readData(path_new)
