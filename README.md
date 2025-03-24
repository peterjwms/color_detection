This repo is for the color calibration project for COSI 149b.

File descriptions
 - name_color_files.ipynb is an interactive notebook intended to be run in Google Colab to scrape the true RGB values from the Behr and Valspar websites to get the true values for our dataset.
 - train_colors.ipynb is another interactive notebook written in Google Colab which contains code to train several different models with scikit-learn.
 - dataset_conversion.py converts the dataset from images of the landmark sections of each whole image instance into just rgb values for each instance by sampling and extracting rgb values from each one.

The main part of the pipeline missing here is the code that extracts the landmarks from each image, which comes from Jeff's code at https://github.com/jeffliulab/Color_Calibration/tree/main.
