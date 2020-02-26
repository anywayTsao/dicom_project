import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
import glob
import pydicom
import re
import service.dicom_service as ds

from lxml import objectify, etree
from matplotlib import cm
from matplotlib import pyplot as plt
from utils.file_util import deep_scan
from models.my_dicom import GEMedicalSystemsDicom
from workflow.data_prepair_workflow import data_prepair_workflow
# import scipy.ndimageimport
# import matplotlib.pyplot as plt

# from skimage import measure, morphology
# from mpl_toolkits.mplot3d.art3d import Poly3DCollection


# print(os.listdir("../../ntpu_project/DICOM/"))
# print()

# # Some constants 
# INPUT_FOLDER = '../../ntpu_project/DICOM/'
# patients = os.listdir(INPUT_FOLDER)
# patients.sort()


def namespace(element):
    m = re.match(r'\{.*\}', element.tag)
    return m.group(0) if m else ''

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
    for i, file_path in enumerate(deep_scan(folder, 'dcm')):
        # print(f'file_path = {file_path}')
        # if (i+1) % 100 == 0:
        #     print(f'reading total...{i+1} dcm file')
        my_dicom = GEMedicalSystemsDicom(file_path)
        dicom_list.append(my_dicom)
        # print(file_path)
        # dataset = pydicom.dcmread(file_path)
        # show_dcm_info(dataset, file_path)
        # plot_pixel_array(dataset)
        # break # TODO: Comment this out to see all
    print(f'finished reading {folder} total...{len(dicom_list)} dcm file')
    return dicom_list

def read_xml(folder: str):
    for file_path in deep_scan(folder, 'xml'):
        print(file_path)
        xml = open(file_path, 'rb').read()
        main = objectify.fromstring(xml)
        try:
            print(main.readingSession[0])
        except Exception:
            pass

def explore_xml(folder: str):
    for file_path in deep_scan(folder, 'xml'):
        print(file_path)
        xml = open(file_path, 'rb').read()
        main = etree.fromstring(xml)
        ns = namespace(main)
        a = main.findall(f'.//{ns}readingSession')
        for element in a.iter():
            print(element.tag)

if __name__ == "__main__":
    # df = pd.read_csv('../../ntpu_project/LIDC-IDRI_MetaData.csv')
    # ge_df = df[df['Manufacturer'] == 'GE MEDICAL SYSTEMS']['Patient Id'].drop_duplicates()

    # dicom_list = []
    # for index, row in ge_df.iteritems():
    #     print(f'{index} reading...Patient Id = {row} data')
    #     dicom_list.extend(read_dicom(f'../../ntpu_project/DICOM/{row}'))
    
    # print(f'len(dicom_list) = {len(dicom_list)}')

    # my_dicom = GEMedicalSystemsDicom('../../ntpu_project/DICOM/LIDC-IDRI-0001/01-01-2000-30178/3000566-03192/000071.dcm')
    # print('SOPInstanceUID = ', my_dicom.SOPInstanceUID)
    # my_dicom.plot()

    # dicom_list = read_dicom('../../ntpu_project/DICOM/LIDC-IDRI-0001/')
    # i = 0
    # for dicom in dicom_list:
    #     i += 1
    #     print('found =>>> modality = ', dicom.modality)
    #     print('found =>>> manufacturer = ', dicom.manufacturer)
    # print(i)
    # read_xml('../../ntpu_project/DICOM/LIDC-IDRI-0001/')
    data_prepair_workflow()
