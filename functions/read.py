import pandas as pd
import os
from pathlib import Path
import json as js
from matplotlib import pyplot as plt

class Filehandling:
    def mkdir(path, folder):
        path = os.path.join(path, folder)
        Path(path).mkdir(parents=True, exist_ok=True)
        return path


    def list_files(path):
        return os.listdir(path)


    def save_df(df, path, name):
        path = path + '\\results'
        Path(path).mkdir(parents=True, exist_ok=True)
        path = path + '\\' + name + '.csv'
        print("{0} saved as {1}".format(name,path))
        df.to_csv(path, sep=';', decimal=',', index = True)

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



def read_identification(path):
    df = pd.read_csv(path, delimiter='\t', skiprows=8, encoding='latin1')
    df.set_index('Ret.Time', inplace=True)
    path = path[:path.rfind('\\')]
    ## saving df ##
    # Filehandling.save_df(df, path, 'identification_extracted')
    return df
    
# reading chromatogram   
def read_chromatogramm(path):
    df = pd.read_csv(path, delimiter='\t', decimal='.', skiprows=11, encoding='latin1')
    df.drop([0, 1, 2], inplace=True)
    df.set_index('Ret.Time', inplace=True)
    try:
        df.drop('Relative Intensity', axis=1, inplace=True)
    except:
        pass
    return df


def plot_chromatogram(df_chrom, df_peaks):
    fig, ax = plt.subplots(figsize=(12, 8), dpi=100)
    ax.plot(df_chrom)
    y_values = df_chrom['Absolute Intensity']
    

    for i in df_peaks.index:
        flag = True
        n = 0
        while flag:
            try:
                ax.plot(i+n, y_values[i+n], 'x')
                ax.annotate(df_peaks['Name'][i], (i, y_values[i+n]+10000), rotation=90, size=8)
                flag = False
            except:
                n += 0.001
    plt.show()


def read_peak_spectra(path):
    # read file
    path_peak_spectra = path
    path = path[:path.rfind('\\')]
    with open(path_peak_spectra) as file:
        lines = file.readlines()
        # searching slice index
        start_index = []
        for line, index in zip(lines, range(len(lines))):
            if line.find('[MS Spectrum]') >= 0:
                start_index.append(index)

        
        # slicing data to peaks
        for s_index, index in zip(start_index, range(len(start_index))):
            new_list = []
            try:
                new_list = lines[s_index:start_index[index+1]-1]
            except:
                new_list = lines[s_index:]

            name = new_list[2][new_list[2].find(';')+1:]
            name = name[:name.find(' ')].replace('.', '_')
            
            # removing header
            new_list = new_list[6:]
            
            # creating one string for each peak
            new_list_string = ''
            for i in new_list:
                i = i.replace(';','\t')
                new_list_string +=i


            

            path_peaks = Filehandling.mkdir(path, f'results\\peaks')        
            path_to_peak =os.path.join(path_peaks, name)
            with open(path_to_peak, "w") as text_file:
                text_file.write(new_list_string)
  


        
def main(path):
    # matching path
    dict_path = Filehandling.sort_files(path)

    # reading data
    df_identification = read_identification(dict_path['peak_identification'])
    read_peak_spectra(dict_path['peak_spectra'])
    df_chromatogramm = read_chromatogramm(dict_path['chromatogramm'])

    # plotting data
    plot_chromatogram(df_chromatogramm, df_identification)
    


main('C:\\Users\\sverme-adm\\Desktop\\data\Bluete\\2022_02_14\\1')
