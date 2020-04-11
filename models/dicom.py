import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
import pydicom
import xml.dom.minidom
import xml.etree.ElementTree as ET
import re

from utils.file_util import deep_scan
from utils.enum import NoduleType
from matplotlib import pyplot as plt
from matplotlib import cm
from models.nodule import Nodule

def namespace(element):
    m = re.match(r'\{.*\}', element.tag)
    return m.group(0) if m else ''


class Dicom:

    # TODO: 
    # D:/ntpu_project/DICOM/LIDC-IDRI-0003/01-01-2000-94866/3000611-03264/000001.dcm
    # 1. keep image as binary if have ROI definition
    # 2. normalize the DICOM
    # 3. store all necessay variables
    def __init__(self, full_path: str):
        self.full_path = full_path
        self.directory = '/'.join(full_path.split('/')[:-1]) + '/'
        dataset = pydicom.dcmread(full_path)
        self.patient_id = dataset.PatientID
        self.manufacturer = dataset.Manufacturer
        self.modality = dataset.Modality
        self.SOP_Instance_UID = dataset.SOPInstanceUID
        # self.rescale_intercept = dataset.RescaleIntercept
        # self.rescale_slope = dataset.RescaleSlope

        self.pixel_array = dataset.pixel_array
        # self.pixel_hu_list = self.get_pixels_hu(dataset)

        # examination result in XML file
        self.nodule_list = []
        self.is_same_examination_result = True
        # print(dataset)
        # print(self.SOP_Instance_UID)

    def add_nodule_list(self, nodule: Nodule):
        self.nodule_list.append(nodule)

    def check_examination_result(self):
        """
        Test the result is same or not
        """
        first_edge = None
        first_nodule_type = None
        has_only_one_result = True
        for i, nodule in enumerate(self.nodule_list):
            if i == 0:
                first_edge = nodule.edge_map_list[0]
                first_nodule_type = nodule.type.value
            else:
                has_only_one_result = False
                edge = nodule.edge_map_list[0]
                distance = ((int(first_edge.x) - int(edge.x))**2 + (int(first_edge.y) - int(edge.y))**2) ** 0.5
                nodule_type = nodule.type.value
                if nodule_type not in [NoduleType.NODULE_GREATER_THAN_3MM.value]:
                    print(f'{self.SOP_Instance_UID} nodule_type NODULE_GREATER_THAN_3MM')
                    self.is_same_examination_result = False
                    return
                elif nodule_type != first_nodule_type:
                    print(f'{self.SOP_Instance_UID} nodule_type not same, {first_nodule_type} != {nodule_type}')
                    self.is_same_examination_result = False
                    return
                elif distance >= 30:
                    print(f'{self.SOP_Instance_UID} distance >= 30, ({first_edge.x}, {first_edge.y}) & ({edge.x}, {edge.y})')
                    self.is_same_examination_result = False
                    return
        if has_only_one_result:
            self.is_same_examination_result = False
            print('has_only_one_result')
            return
        print(f'same result!!!!!!!!!!!')

    # TODO: it seems not correct...
    # https://www.kaggle.com/gzuidhof/full-preprocessing-tutorial
    def get_pixels_hu(self, slice): 
        
        image = np.stack([slice.pixel_array])
        # Convert to int32, 
        image = image.astype(np.int32)

        # Set outside-of-scan pixels to 0
        # The intercept is usually -1024, so air is approximately 0
        image[image == -2000] = 0
        
        # Convert to Hounsfield units (HU)
        # HU = pixel_val * slope + intercept
        intercept = self.rescale_intercept
        slope = self.rescale_slope
        
        if slope != 1:
            image[0] = slope * image[0].astype(np.float64)
            image[0] = image[0].astype(np.int32)

        image[0] += np.int32(intercept)
        
        return np.array(image, dtype=np.int32)

    def plot_hu_freqency(self):
        plt.hist(self.pixel_list.flatten(), bins=80, color='c')
        plt.title(self.patient_id)
        plt.xlabel("(Before) Hounsfield Units (HU)")
        plt.ylabel("Frequency")
        plt.show()

        plt.hist(self.pixel_hu_list.flatten(), bins=80, color='c')
        plt.title(self.patient_id)
        plt.xlabel("(After) Hounsfield Units (HU)")
        plt.ylabel("Frequency")
        plt.show()

    def plot_ct(self):
        # Show some slice in the middle
        plt.imshow(self.pixel_list, cmap=plt.cm.gray)
        plt.show()

        # Show some slice in the middle
        plt.imshow(self.pixel_hu_list, cmap=plt.cm.gray)
        plt.show()

    def reshape(self):
        NotImplemented

    def standardlize(self):
        NotImplemented