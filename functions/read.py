import pandas as pd
import os
from pathlib import Path


def mkdir(path, folder):
    path = os.path.join(path, folder)
    Path(path).mkdir(parents=True, exist_ok=True)
    return path


def list_files(path):
    return os.listdir(path)

def read_identification(path):
    df = pd.read_csv(path, delimiter=';')
    df.columns = [i.replace('#', '') for i in df.columns]
    df.columns = [i.replace(' ', '') for i in df.columns]
    df_new = df[df['Hit'] == 1]
    df_new = df_new.copy()
    df_new['Name'] = [i[:i.find('$')] for i in df_new['Name']]
    df_new.set_index('Spectrum', inplace=True)
    path = path[:path.rfind('\\')]
    save_df(df_new, path, 'identification_extracted')
    return df_new
    
    
def save_df(df, path, name):
    path = path + '\\results'
    Path(path).mkdir(parents=True, exist_ok=True)
    path = path + '\\' + name + '.csv'
    print("{0} saved as {1}".format(name,path))
    df.to_csv(path, sep=';', decimal=',', index = True)
    
        
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


            

            path_peaks = mkdir(path, f'results\\peaks')        
            path_to_peak =os.path.join(path_peaks, name)
            with open(path_to_peak, "w") as text_file:
                text_file.write(new_list_string)
  
def sort_files(path):
    files = list_files(path)
    file_names = ['peak_identification', 'peak_spectra', 'chromatogramm']
    dict_files = {}
    for i in file_names:
        for n in files:
            if n.find(i) >= 0:
                dict_files[i] = os.path.join(path, n)
            else:
                pass
    return dict_files

        
def main(path):

    dict_path = sort_files(path)

    read_identification(dict_path['peak_identification'])
    read_peak_spectra(dict_path['peak_spectra'])
    
    
main('C:\\Users\\sverme-adm\\Desktop\\data\Bluete\\2022_02_14\\1')