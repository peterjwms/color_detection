# look through all photos to check which ones have them all correct - put those names in csv and go through them
# then can relabel or maybe retrain and relabel each of those later, along with maybe adding the augmentation processes
# augmentation includes taking multiple samples from each picture in final step, and the other possible changes
# read in each photo
# split the file names on _
# take the names, true RGB, observed RGB, observed R-RGB, o G-RGB, o B-RGB

from glob import glob
from pathlib import Path
import pandas as pd
import cv2 
import numpy as np

def extract_rgb(image_path):
    img = cv2.imread(str(image_path))
    if img is None:
        print(f"Error: Could not read image {image_path}")
        return None

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert to RGB color space
    h, w, _ = img.shape  # Get image dimensions

    # Calculate the center region boundaries of the 3x3 grid
    grid_size = 3
    row_start = h // grid_size
    row_end = 2 * (h // grid_size)
    col_start = w // grid_size
    col_end = 2 * (w // grid_size)

    center_region = img[row_start:row_end, col_start:col_end]  # Extract center region
    avg_color = np.mean(center_region, axis=(0, 1))  # Compute mean RGB values

    return tuple(avg_color.astype(int))  # Return integer RGB values


if __name__ == "__main__":
    # for fname in glob("Color_Calibration/outputs2/batch1/*.jpg"):
    #     print(fname)
    dataset = []
    untouched_files = []
    brands = ["valspar", "behr"]
    for brand in brands:
        print(brand)
        filemap = pd.read_csv(Path(f"project1/{brand}_file_mapping.csv"))
        print(filemap)
        
        for i, row in filemap.iterrows():
            ds_row = {"Sample Name": row['color_name'], "Sample Number": row['verified_code'], "File Name": row["new_filename"],
                    "True R": row["R"], "True G": row["G"], "True B": row["B"],
                    "Observed R": None, "Observed G": None, "Observed B": None,
                    "Red R": None, "Red G": None, "Red B": None,
                    "Green R": None, "Green G": None, "Green B": None,
                    "Blue R": None, "Blue G": None, "Blue B": None}

            if row['all_landmarks'] == "y":
                # do all the necessary stuff to extract colors, parse the fname, etc.
                for image in glob(f"Color_Calibration/outputs2/{brand}/{row['new_filename']}*.jpg"):
                    print(image)
                    rgb = (extract_rgb(image))
                    if "black_box" in image:
                        # fill in row
                        ds_row["Observed R"] = rgb[0]
                        ds_row["Observed G"] = rgb[1]
                        ds_row["Observed B"] = rgb[2]
                    elif "blue_pentagon" in image:
                        # fill in row
                        ds_row["Blue R"] = rgb[0]
                        ds_row["Blue G"] = rgb[1]
                        ds_row["Blue B"] = rgb[2]
                    elif "green_triangle" in image:
                        # fill in row
                        ds_row["Green R"] = rgb[0]
                        ds_row["Green G"] = rgb[1]
                        ds_row["Green B"] = rgb[2]
                    elif "red_circle" in image:
                        # fill in row
                        ds_row["Red R"] = rgb[0]
                        ds_row["Red G"] = rgb[1]
                        ds_row["Red B"] = rgb[2]
            
                dataset.append(ds_row)

            else:
                # maybe put these in a new file to hold onto the ones that need to be done again
                untouched_files.append(row)
                continue

    undone_df = pd.DataFrame(untouched_files)
    undone_df.to_csv(Path("project1/all_undone.csv"))

    ds_df = pd.DataFrame(dataset)
    ds_df.to_csv(Path("project1/all_data.csv"), index=False)
