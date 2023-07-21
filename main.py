# -*- coding: utf-8 -*-
"""
Software CG-6: Testing
            
@author: Viraldi Diyesa
"""

# Importing library
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import datetime
from scipy import stats
from tkinter import *
from tkinter import filedialog, ttk

### Define ###


# File Explorer
def browseFiles():
    global file
    file = filedialog.askopenfilename(initialdir = "/", title = "Select a File", filetypes = (("Text files", "*.txt*"),("all files","*.*")))
    #file = open(filename, 'r')
    label_file_explorer.configure(text="File Opened: " + file)
    return file

# Processing
def processing():
    
    global df, ef
    
    if cCG.get() == 'CG-6':
        df = pd.read_table(file, skiprows = 20, delim_whitespace = True)
    
        # Renaming first columns
        df = df.rename(columns = {df.columns[0] : 'Station'})
    
        # Tide vs DecTime
        try: 
            df['DetTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
    
        except:
            for i in np.arange(len(df.index)):
                df['Time'][i] = str(datetime.timedelta(hours = df['Time'][i] * 24))
            df['DetTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
    
        
        for i in np.arange(len(df.index)):
            df['DetTime'][i] = df['DetTime'][i].replace(hour = df['DetTime'][i].hour + time_plus.get())
            
        df['DecTime'] = df['DetTime']
        for i in np.arange(len(df.index)):
            df['DecTime'][i] = df['DetTime'][i].year*10000 + df['DetTime'][i].month*100 + df['DetTime'][i].day + df['DetTime'][i].hour/24 + df['DetTime'][i].minute/(24*60) + df['DetTime'][i].second/(24*60*60)
        
        # Gravity
        #base_name = input('Input looping information Name : ')
        base_name = 'BASE'
        #df.loc[df['Station'].str.match(base_name) == True, 'Station'] = 'Start' 
        
        for i in df.index:
            if df['Station'][i] in [base_name]:
                if df['DecTime'][i] - df['DecTime'][len(df.index)-1] < -0.1: #Asumsi 2,4 Jam
                    df['Station'][i] = str(base_name) + '_OPEN'
                else:
                    df['Station'][i] = str(base_name) + '_CLOSE'
            else:
                pass
        
        n_Station = len(df['Station'].unique()) - 1
        t_first = np.mean(df.loc[df['Station'].str.match(df['Station'].unique()[0])]['DecTime'])
        t_last = np.mean(df.loc[df['Station'].str.match(df['Station'].unique()[n_Station])]['DecTime'])
        
        df['GravMinTide'] = df['RawGrav'] - df['TideCorr']
        
        RawGrav_first = np.mean(df.loc[df['Station'].str.match(df['Station'].unique()[0])]['GravMinTide'])
        RawGrav_last = np.mean(df.loc[df['Station'].str.match(df['Station'].unique()[n_Station])]['GravMinTide'])
        
        
        df['DriftCalc'] = ((df['DecTime'] - t_first) / (t_last - t_first)) * (RawGrav_last - RawGrav_first)
        
        ### Sparsing ###
        # Sparse Station into DataFrame
        group = df.groupby('Station')
        
        for i, g in group:
            globals()['df_' + str(i)] =  g    
        list_files = list(group.groups.keys())
        
        for i in np.arange(len(list_files)):
            globals()['df_' + list_files[i]] = globals()['df_' + list_files[i]].reset_index()
            globals()['df_' + list_files[i]] = globals()['df_' + list_files[i]].drop('index', axis = 1)
        
        ### Making single point ###
        list_points = []
        for i in np.arange(len(list_files)):
            globals()['ef_' + list_files[i]] = pd.DataFrame(stats.mode(globals()['df_' + list_files[i]])[0])
            list_points.append(globals()['ef_' + list_files[i]])
            
        ef = pd.concat(list_points) # Final Output of The File
        ef.columns = list(df.columns.values)
        ef = ef.sort_values(by = ['DetTime'])
        
    else:
        header = ['Line', 'Station', 'Elev', 'RawGrav', 'StdDev', 'X', 
		  'Y', 'TempCorr', 'TideCorr', 'MeasurDur', 'REJ', 'Time', 
		  'DecTimeDdate(Original)', 'Terrain', 'Date', 'DeltaTime','GravMinTide', 
          'DriftCorr']

        df = pd.read_table(file, skiprows = 20, delim_whitespace = True)
        df.columns = header
        
        df['Station'] = df['Station'].values.astype(str)
        
        ### Processing ###
            
        #Tide vs DecTime
        try: 
            df['DetTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
        
        except:
            for i in np.arange(len(df.index)):
                df['Time'][i] = str(datetime.timedelta(hours = df['Time'][i] * 24))
            df['DetTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
        
        for i in np.arange(len(df.index)):
            df['DetTime'][i] = df['DetTime'][i].replace(hour = df['DetTime'][i].hour + time_plus.get())
        print(df['DetTime'])
            
        df['DecTime'] = df['DetTime']
        for i in np.arange(len(df.index)):
            df['DecTime'][i] = df['DetTime'][i].year*10000 + df['DetTime'][i].month*100 + df['DetTime'][i].day + df['DetTime'][i].hour/24 + df['DetTime'][i].minute/(24*60) + df['DetTime'][i].second/(24*60*60)
        
        # # # Gravity
        #base_name = input('Input looping information Name : ')
        base_name = 'BASE'
        #df.loc[df['Station'].str.match(base_name) == True, 'Station'] = 'Start' 
        
        for i in df.index:
            if df['Station'][i] in [base_name]:
                if df['DecTime'][i] - df['DecTime'][len(df.index)-1] < -0.1: #Asumsi 2,4 Jam
                    df['Station'][i] = str(base_name) + '_OPEN'
                else:
                    df['Station'][i] = str(base_name) + '_CLOSE'
            else:
                pass
        
        n_Station = len(df['Station'].unique()) - 1
        t_first = np.mean(df.loc[df['Station'].str.match(df['Station'].unique()[0])]['DecTime'])
        t_last = np.mean(df.loc[df['Station'].str.match(df['Station'].unique()[n_Station])]['DecTime'])
        
        df['GravMinTide'] = df['RawGrav'] - df['TideCorr']
        
        RawGrav_first = np.mean(df.loc[df['Station'].str.match(df['Station'].unique()[0])]['GravMinTide'])
        RawGrav_last = np.mean(df.loc[df['Station'].str.match(df['Station'].unique()[n_Station])]['GravMinTide'])
        
        
        df['DriftCalc'] = ((df['DecTime'] - t_first) / (t_last - t_first)) * (RawGrav_last - RawGrav_first)
        
        ### Sparsing ###
        # Sparse Station into DataFrame
        group = df.groupby('Station')
        
        for i, g in group:
            globals()['df_' + str(i)] =  g    
        list_files = list(group.groups.keys())
        
        for i in np.arange(len(list_files)):
            globals()['df_' + list_files[i]] = globals()['df_' + list_files[i]].reset_index()
            globals()['df_' + list_files[i]] = globals()['df_' + list_files[i]].drop('index', axis = 1)
        
        ### Making single point ###
        list_points = []
        for i in np.arange(len(list_files)):
            globals()['ef_' + list_files[i]] = pd.DataFrame(stats.mode(globals()['df_' + list_files[i]])[0])
            list_points.append(globals()['ef_' + list_files[i]])
            
        ef = pd.concat(list_points) # Final Output of The File
        ef.columns = list(df.columns.values)
        ef = ef.sort_values(by = ['DetTime'])
    
    return df, ef

def print_data():
    if cCG.get() == 'CG-6':
        ef.to_excel(excel_writer = 'CG6-' + str(ef.DetTime.iloc[1].year) + '-' + str(ef.DetTime.iloc[1].month) + '-' + str(ef.DetTime.iloc[1].day) + '_final.xlsx')
    else:
        ef.to_excel(excel_writer = 'CG5-' + str(ef.DetTime.iloc[1].year) + '-' + str(ef.DetTime.iloc[1].month) + '-' + str(ef.DetTime.iloc[1].day) + '_final.xlsx')
     
    
def exit():
    window.quit()
    
### Plot ###
    
def plot_dectide():
    plt.plot(df['DecTime'], df['TideCorr'], '-or')
    plt.title('Decimal Time vs Tid e Correction')
    plt.xlabel('Decimal TIme (/day)')
    plt.ylabel('Tide Corr (mGal)')
    plt.grid(True)              
    plt.show()

# Decimal Time vs Temperature
def plot_dectemp():
    plt.plot(df['DecTime'], df['TempCorr'], 'o')
    plt.title('Decimal Time vs Temperature Correction')
    plt.xlabel('Decimal TIme (/day)')
    plt.ylabel('Temperature Correction (mK)')
    plt.grid(True)
    plt.show()
    
# Standard Deviation
def plot_decstddev():
    plt.plot(df['DecTime'], df['StdDev'], 'or')
    plt.title('Decimal Time vs Standard Deviation')
    plt.xlabel('Decimal TIme (/day)')
    plt.ylabel('Standard Deviation (mGal)')
    plt.grid(True)
    plt.show()

# Decimal Time vs Drift Calculation (Robby, 2021)
def plot_decdrift():
    plt.plot(df['DecTime'], df['DriftCalc'], '-r')
    plt.plot(df['DecTime'], df['DriftCalc'], 'ob')
    plt.title('Decimal Time vs Drift Correction')
    plt.xlabel('Decimal TIme (/day)')
    plt.ylabel('Drift (mGal)')
    plt.grid(True)
    plt.show()
    
# Tilt Angle Plot
def plot_tiltxy():
    # Making Figure
    fig, ax = plt.subplots(nrows = 1, ncols = 1)
    
    ax.scatter(df['X'].values, df['Y'].values, color = 'red')
    ax.axis('square')
    ax.axhline()
    ax.axvline()
    ax.set_xlim([-15, 15])
    ax.set_ylim([-15, 15])
    ax.grid(color='y', lw = 0.1)
    create_circle = matplotlib.patches.Circle((0, 0),10, fill=False)
    ax.add_artist(create_circle)
    ax.set_title('TILTX vs TILTY')
    
# Plot All
def plot_all():
   fig, ax = plt.subplots(nrows = 1, ncols = 3)
   fig.suptitle('Drift - Tide - SD Plot')
   figsize=(13,40)
   
   # Track 1
   ax[0].grid(True)
   ax[0].set_ylabel('Drift (mGal)')
   ax[0].set_xlabel('\u0394t (days)')
   ax[0].set_ylim(0, max(df['DriftCalc']))
   ax[0].plot(df['DecTime'], df['DriftCalc'], '-or')
   
   # Track 2 
   ax[1].grid(True)
   ax[1].set_ylabel('Tide (mGal)')
   ax[1].set_xlabel('\u0394t (days)')
   ax[1].plot(df['DecTime'], df['TideCorr'], '-ob')
   
   # Track 3
   ax[2].grid(True)
   ax[2].set_ylabel('SD (mGal)')
   ax[2].set_xlabel('St nth')
   ax[2].set_ylim(0, 0.1)
   ax[2].plot(df['StdDev'].index + 1, df['StdDev'], 'oc')
   
### GUI ###
window = Tk()
window.title('CG-6 File Editor')
# window.geometry('400x400')

time_plus = IntVar()
cCG = StringVar()

### Label ###

# Label File Explorer
label_file_explorer = Label(window,
							text = "Input File (.txt)",
							fg = "black")
label_CG = Label(window,
                 text = "Pilih Instrumen CG-",
                 fg = 'black')

label_time_plus = Label(window, text = 'Time Plus : ', fg = 'black')


# Button Explore Files and Folder
button_explore = Button(window,
						text = "Browse Files",
						command = browseFiles)

# Button Processing
button_processing = Button(window,
                           text = "Processing",
                           command = processing)

### Button Plot ###
button_plot_1 = Button(window,
                       text = "Plot \u0394t vs Tide",
                       command = plot_dectide)

button_plot_2 = Button(window,
                       text = "Plot \u0394t vs Temp",
                       command = plot_dectemp)

button_plot_3 = Button(window,
                       text = "Plot \u0394t vs Std Dev",
                       command = plot_decstddev)

button_plot_4 = Button(window,
                       text = "Plot \u0394t vs Drift",
                       command = plot_decdrift)

button_plot_5 = Button(window,
                       text = "Plot Tilt X vs Y",
                       command = plot_tiltxy)
button_plot_all = Button(window,
                         text = 'Plot All',
                         command = plot_all)
button_print = Button(window, 
                      text = "Print Data to Excel",
                      command = print_data)

# Combobox
combo_CG = ttk.Combobox(window, text = 'Combobox', textvariable = cCG)
combo_CG.set('...')
combo_CG['values'] = ('CG-5', 'CG-6')

# Input Box
time_plus_box = ttk.Entry(textvariable = time_plus)

# Grid 

# Label Grid
label_file_explorer.grid(column = 1, row = 0)
label_CG.grid(column = 0, row = 1)
label_time_plus.grid(column = 0, row = 2)

#  Button Grid
button_explore.grid(column = 0, row = 0)
button_processing.grid(column = 1, row = 3)
button_plot_1.grid(column = 1, row = 4)
button_plot_2.grid(column = 1, row = 5)
button_plot_3.grid(column = 1, row = 6)
button_plot_4.grid(column = 1, row = 7)
button_plot_5.grid(column = 1, row = 8)
button_plot_all.grid(column = 1, row = 9)
button_print.grid(column = 1, row = 10)

# Combo Grid
combo_CG.grid(column = 1, row = 1)

# Box Grid
time_plus_box.grid(columns = 5, row = 2)

# Mainloop Event
window.mainloop()