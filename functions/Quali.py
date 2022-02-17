from asyncio.format_helpers import extract_stack
from importlib.resources import path
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile, join
from pathlib import Path

from pyparsing import opAssoc


path_peaks = "C:\\Users\\sverme-adm\\Documents\\PythonScripts\\Tomensa\\2022-02-01\\2022-01-24 PflanzeQual.txt"
path_data = "C:\\Users\\sverme-adm\\Documents\\PythonScripts\\Tomensa\\2022-01-24\\2022-01-24 Pflanze.txt"


def save_fig(myfig, path, name):
    # print(name)
    path = path[:path.rfind('\\')] +'\\' + name +  '.png'     
    path = path + '.png'
    myfig.savefig(path)


def get_info(path):
    date = path[path.rfind('\\')+1:path.rfind(' ')]
    name = path[path.rfind(' '):path.rfind('.')]
    return name, date


def get_peaks(path):
    df = pd.read_csv(path, delimiter='\t', decimal='.', skiprows=8)
    df.set_index('Ret.Time', inplace=True)
    print('peaks\n', df.head())
    return df[['Height', 'Name']]


def get_spectra(path):
    df = pd.read_csv(path, delimiter='\t', decimal='.', skiprows=11)
    df.set_index('Ret.Time', inplace=True)
    print('spectra\n', df.head())
    return df.drop('Relative Intensity', axis=1)


def plot_peaks(df_spectra, df_peaks, name):   
    fig, ax = plt.subplots()
    ax.plot(df_spectra)
    y_values = df_spectra['Absolute Intensity']
    for i in df_peaks.index:
        flag = True
        n = 0
        while flag:
            try:
                ax.plot(i, y_values[i+n], 'x')
                flag = False
            except:
                n += 0.001
    save_fig(fig, path_data, name)


def read_data(path_peaks, path_data):
    name, date = get_info(path_data)
    peaks = get_peaks(path_peaks)
    spectra = get_spectra(path_data)
    plot_peaks(spectra, peaks, name)


if __name__ == "__main__":
    read_data(path_peaks, path_data)
