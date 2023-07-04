
# Python driving license

Politecnico di Milano
PhD candidate: Nicolò Guarnieri - Materials Engineering

# spa_to_png_csv
Plot .spa  as .png files and export also as .csv exploiting python read_spa code from lerkoah
Description of the script:

This script will be used during infrared spectroscopy measurements in order to facicilate the acquisition process. Since Omnic software has as a native .spa format to save spectra which cannot be opened by other software, it is always necessary to save spectra in other format (usually .csv). Unfortunately, .csv file are very boring to handle since there is no a simpe and fast method to visualize the spectrum from a .csv file. Usaully we import it in origin and export a .png image with the x values of the peaks of the spectrum. This process is done for each spectra acquired and it is very tedious.

The aim of this script is to open all .spa files in a folder and plot them (highlithing the peaks) in a .png image, then export also the .csv file for future manipulation of the spectra.

In order to do that a free script to read .spa data will be exploited (https://github.com/lerkoah/spa-on-python) 
