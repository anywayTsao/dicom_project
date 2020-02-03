import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
import glob
import pydicom

from matplotlib import cm
from matplotlib import pyplot as plt
from utils.file_util import deep_scan
from models.my_dicom import MyDicom
# import scipy.ndimage
# import matplotlib.pyplot as plt

# from skimage import measure, morphology
# from mpl_toolkits.mplot3d.art3d import Poly3DCollection


# print(os.listdir("../../ntpu_project/DICOM/"))
# print()

# # Some constants 
# INPUT_FOLDER = '../../ntpu_project/DICOM/'
# patients = os.listdir(INPUT_FOLDER)
# patients.sort()

def show_dcm_info(dataset, file_path):
    # print(dataset)
    print("Filename.........:", file_path)
    print("Storage type.....:", dataset.SOPClassUID)
    # print()
    print("Patient id..........:", dataset.PatientID)
    print("Instance Number..........:", dataset.InstanceNumber)
    print("Modality.........:", dataset.Modality)
    print("Manufacturer..........:", dataset.Manufacturer)
    print("Rescale Intercept..........:", dataset.RescaleIntercept)
    print("Rescale Slope..........:", dataset.RescaleSlope)
    # print("Patient's Age.......:", dataset.PatientAge)
    # print("Patient's Sex.......:", dataset.PatientSex)
    # print("Modality............:", dataset.Modality)
    # print("Body Part Examined..:", dataset.BodyPartExamined)
    # print("View Position.......:", dataset.ViewPosition)
    
    if 'PixelData' in dataset:
        rows = int(dataset.Rows)
        cols = int(dataset.Columns)
        print("Image size.......: {rows:d} x {cols:d}, {size:d} bytes".format(
            rows=rows, cols=cols, size=len(dataset.PixelData)))
        if 'PixelSpacing' in dataset:
            print("Pixel spacing....:", dataset.PixelSpacing)

def plot_pixel_array(dataset, figsize=(10,10)):
    plt.figure(figsize=figsize)
    plt.imshow(dataset.pixel_array, cmap=plt.cm.bone)
    plt.show()

def read_dicom(folder: str):
    # print(folder)
    dicom_list = []
    for file_path in deep_scan(folder, 'dcm'):
        my_dicom = MyDicom(file_path)
        dicom_list.append(my_dicom)
        # print(file_path)
        # dataset = pydicom.dcmread(file_path)
        # show_dcm_info(dataset, file_path)
        # plot_pixel_array(dataset)
        # break # TODO: Comment this out to see all
    return dicom_list

def read_xml(folder: str):
    for file_path in deep_scan(folder, 'xml'):
        print(os.path.isfile(file_path))

if __name__ == "__main__":
    dicom_list = read_dicom('../../ntpu_project/DICOM/LIDC-IDRI-0001/')
    print(dicom_list[68].full_path)
    print(dicom_list[68].series_instance_uid)
# read_dicom('../../ntpu_project/DICOM/LIDC-IDRI-0001/')
# read_xml('../../ntpu_project/DICOM/LIDC-IDRI-0001/')
