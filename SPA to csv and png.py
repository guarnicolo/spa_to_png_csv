#!/usr/bin/env python
# coding: utf-8

# # Python driving license
# Politecnico di Milano
# 
# #### PhD candidate: Nicolò Guarnieri - Materials Engineering
# 
# ##### Description of the script:
# This script will be used during infrared spectroscopy measurements in order to facicilate the acquisition process. Since Omnic software has as a native .spa format to save spectra which cannot be opened by other software, it is always necessary to save spectra in other format (usually .csv). Unfortunately, .csv file are very boring to handle since there is no a simpe and fast method to visualize the spectrum from a .csv file. Usaully we import it in origin and export a .png image with the x values of the peaks of the spectrum. This process is done for each spectra acquired and it is very tedious.
# 
# The aim of this script is to open all .spa files in a folder and plot them (highlithing the peaks) in a .png image, then export also the .csv file for future manipulation of the spectra.
# 
# In order to do that a free script to read .spa data will be exploited (https://github.com/lerkoah/spa-on-python)
# ![immagine.png](attachment:immagine.png)

# # Step:1
# Importing the read_spa code from GitHub https://github.com/lerkoah/spa-on-python

# In[26]:


#### read_spa code was obtained from https://github.com/lerkoah/spa-on-python: ####

import numpy as np

def read_spa(filepath):
    '''
    Input
    Read a file (string) *.spa
    ----------
    Output
    Return spectra, wavelenght (nm), titles
    '''
    with open(filepath, 'rb') as f:
        f.seek(564)
        Spectrum_Pts = np.fromfile(f, np.int32,1)[0]
        f.seek(30)
        SpectraTitles = np.fromfile(f, np.uint8,255)
        SpectraTitles = ''.join([chr(x) for x in SpectraTitles if x!=0])

        f.seek(576)
        Max_Wavenum=np.fromfile(f, np.single, 1)[0]
        Min_Wavenum=np.fromfile(f, np.single, 1)[0]
        print(Min_Wavenum, Max_Wavenum, Spectrum_Pts)
        Wavenumbers = np.flip(np.linspace(Min_Wavenum, Max_Wavenum, Spectrum_Pts))

        f.seek(288);

        Flag=0
        while Flag != 3:
            Flag = np.fromfile(f, np.uint16, 1)

        DataPosition=np.fromfile(f,np.uint16, 1)
        f.seek(DataPosition[0])

        Spectra = np.fromfile(f, np.single, Spectrum_Pts)
    return Spectra, 1e7/Wavenumbers, SpectraTitles

### end of the code from https://github.com/lerkoah/spa-on-python ####


# # Step:2
# Importing all required python functions

# In[133]:


import os                          #to view/manage file inside the folder
import glob                        #to view/manage file inside the folder
import pandas as pd                #to treat and export .csv files
import matplotlib.pyplot as plt    #to create plots and save as .png files


# # Step:3
# Definition of the folder path and visualization of the nukber of .spa file contained and their names.

# In[356]:


##################

# definition the folder path containing all the .spa files
folder_path = '.'

##################

#to check all files inside the foldes activate following line (delete #):
#os.listdir(folder_path)


# to create a list name spa_files containing all .spa files present in the folder_path
spa_files = [f for f in os.listdir(folder_path) if f.endswith('.SPA')]

#check of the elemnets of the spa_files list
print(f'number of .spa files in the foldar_path: {len(spa_files)}')
print(spa_files)


# # Step:4
# Undestanding which are the outputs of read_spa code.

# In[171]:


#undestanding which is the type of the result from read_spa code
spectrum_test = read_spa(folder_path+"/"+spa_files[0])

print(type(spectrum_test))

#read_spa gives as outputs the min wavenumber, the max wavenumber and the total of points of the spectrum

print(spectrum_test[0]) #are intensities
print(spectrum_test[1]) #are wavelenghts in nm
print(spectrum_test[2]) # is the title

##to obtain wavenumbers in cm-1 from wavelenghts the following expression should be used: wn=10^7/wl


# # step:5
# Plotting a test_spectrum in a 16:9 format, removing y_axis_label and flipping the x axis and adding the title to the plot from filename (deleting extension .spa)

# In[357]:


#plot in 16:9 format
plt.figure(figsize=(10,5.66))

#command to invert x axis (classic format for presenting IR data)
plt.gca().invert_xaxis()

plt.plot(1e7/spectrum_test[1], spectrum_test[0])

plt.xlabel('wavenumber [cm-1]') 
plt.title(spa_file[:-4])  #adding the title to the plot from filename (deleting extension .spa)
plt.ylabel('intensity')
plt.tick_params(labelleft=False, left=False)

plt.show()
plt.close()


# # Step:6
# Plotting the same test_spectrum but finding the peaks and adding their x coordinates in the plot.Saving the spectrum as .png file in the same folder of .spa file, maintaing its original name.
# 
# In oder to avoid overlapping a if-else method is implemented. The method add an offset if the x coordinate of the peak is a multiple of 7,6,5,3,2.

# In[349]:


import numpy as np
from scipy.signal import find_peaks

#defining x and y for semplicity
x = 1e7/spectrum_test[1]
y = spectrum_test[0]

# find_peaks from scipy
peak_indices, _ = find_peaks(y, height=0.01, distance=1)

# rename indices of the two coordinates
peak_x_values = x[peak_indices]
peak_y_values = y[peak_indices]

#create a plot in 16:9 format with inverted x axis (see above)
plt.figure(figsize=(10,5.66))
plt.gca().invert_xaxis()

# plot and peak visualization in black and vertical line
plt.plot(x, y)
plt.scatter(peak_x_values, peak_y_values, color='0', marker='|')

# visualization of the x coordinate of the peak, the if-else rule aims at avoiding 
# overlapping of the text changing the y position of the text in order to make it readable.
for i, peak_x in enumerate(peak_x_values):
    offset = 0
    if i % 7 == 0:
        offset = 20
    elif i % 6 == 0:
        offset = 40
    elif i % 3 == 0:
        offset = 10
    elif i % 5 == 0:
        offset = 15
    elif i % 2 == 0:
        offset = 30
    else:
        offset = 50
    plt.annotate(f"{peak_x:.0f}", (peak_x, peak_y_values[i]),
                 textcoords="offset points", xytext=(0,offset), ha='center', fontsize=6, rotation=90)


#adding the title to the plot from filename and changing names o th axes, removing label of x axis
plt.xlabel('wavenumber [cm-1]') #adding the title to the plot from filename (deleting extension .spa)
plt.title(spa_file[:-4])
plt.ylabel('intensity')
plt.tick_params(labelleft=False, left=False)

#saving the plot in .png in the same folder with same name
plt.savefig(folder_path + "/" +spa_file[:-4]+".png", dpi=300)
plt.show()
plt.close()
#printing a list of all the x values of the peaks
print("list of peak:",peak_x_values)




# # Step:7
# Saving the data as .csv file in the same folder and using the same name.

# In[353]:


# Save the data as a CSV file
csv = {'wavenumber cm-1': x, 'intensity': y}
csv_df = pd.DataFrame(data)
    
csv_df.to_csv(folder_path + "/" +spa_file[:-4]+".csv", index=False)


# # Step:8
# Implementation of step 5,6,7 for all the .spa files in the folder.

# In[355]:


#implementation to iterate all this process to all the .spa file in the folder


for spa_file in spa_files:

    spectrum = read_spa(folder_path+"/"+spa_file)
        
    #defining x and y for semplicity
    x = 1e7/spectrum[1]
    y = spectrum[0]
    
    # find_peaks from scipy
    peak_indices, _ = find_peaks(y, height=0.01, distance=1)

    # rename indices of the two coordinates
    peak_x_values = x[peak_indices]
    peak_y_values = y[peak_indices]
    
    #create a plot in 16:9 format with inverted x axis (see above)
    plt.figure(figsize=(10,5.66))
    plt.gca().invert_xaxis()
    
    # plot and peak visualization in black and vertical line
    plt.plot(x, y)
    plt.scatter(peak_x_values, peak_y_values, color='0', marker='|')
    
    # visualization of the x coordinate of the peak, the if-else rule aims at avoiding 
    # overlapping of the text changing the y position of the text in order to make it readable.
    for i, peak_x in enumerate(peak_x_values):
        offset = 0
        if i % 7 == 0:
            offset = 20
        elif i % 6 == 0:
            offset = 40
        elif i % 3 == 0:
            offset = 10
        elif i % 5 == 0:
            offset = 15
        elif i % 2 == 0:
            offset = 30
        else:
            offset = 50
        plt.annotate(f"{peak_x:.0f}", (peak_x, peak_y_values[i]), textcoords="offset points", xytext=(0,offset), ha='center', fontsize=6, rotation=90)


    #adding the title to the plot from filename and changing names o th axes, removing label of x axis
    plt.xlabel('wavenumber [cm-1]') #adding the title to the plot from filename (deleting extension .spa)
    plt.title(spa_file[:-4])
    plt.ylabel('intensity')
    plt.tick_params(labelleft=False, left=False)

    #saving the plot in .png in the same folder with same name
    plt.savefig(folder_path + "/" +spa_file[:-4]+".png", dpi=300)
    plt.show()
    
    
    # Save the data as a CSV file
    csv = {'wavenumber cm-1': x, 'intensity': y}
    csv_df = pd.DataFrame(csv)
    csv_df.to_csv(folder_path + "/" +spa_file[:-4]+".csv", index=False)
    
    plt.close()


# # end

# In[ ]:




