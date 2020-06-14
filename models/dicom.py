import numpy as np # linear algebra
import os
import pydicom
import xml.dom.minidom
import xml.etree.ElementTree as ET
import re
import cv2

from utils.file_util import deep_scan
from utils.enum import NoduleType
from matplotlib import pyplot as plt
from matplotlib import cm
from models.nodule import Nodule
from utils.enum import Modality, Manufacturer

def namespace(element):
    m = re.match(r'\{.*\}', element.tag)
    return m.group(0) if m else ''

kernel_x = np.array([
    [-1, -4, -6, -4, -1],
    [-2, -8, -12, -8, -2],
    [0, 0, 0, 0, 0],
    [2, 8, 12, 8, 2],
    [1, 4, 6, 4, 1],
])

kernel_y = np.array([
    [1, 2, 0, -2, -1],
    [4, 8, 0, -8, -4],
    [6, 12, 0, -12, -6],
    [4, 8, 0, -8, -4],
    [1, 2, 0, -2, -1],
    
])
 

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
        self.manufacturer = dataset.Manufacturer
        if self.manufacturer != Manufacturer.GE_MEDICAL_SYSTEMS.value:
            return
        self.modality = dataset.Modality
        self.patient_id = dataset.PatientID
        self.SOP_Instance_UID = dataset.SOPInstanceUID
        self.rescale_intercept = dataset.RescaleIntercept
        self.rescale_slope = dataset.RescaleSlope

        self.pixel_array = cv2.resize(dataset.pixel_array, dsize=(128, 128), interpolation=cv2.INTER_CUBIC)
        # self.sobel_x = None
        # self.sobel_y = None
        # self.pixel_hu_list = self.get_pixels_hu(dataset)

        # examination result in XML file
        self.nodule_list = []
        self.is_same_examination_result = False
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
        first_center_x = None
        first_center_y = None
        has_only_one_result = True
        for i, nodule in enumerate(self.nodule_list):
            if i == 0:
                self.is_same_examination_result = True
                first_center_x = np.sum([int(edge.x) for edge in nodule.edge_map_list]) / len(nodule.edge_map_list)
                first_center_y = np.sum([int(edge.y) for edge in nodule.edge_map_list]) / len(nodule.edge_map_list)
                # first_edge = nodule.edge_map_list[0]
                first_nodule_type = nodule.type.value
            else:
                center_x = np.sum([int(edge.x) for edge in nodule.edge_map_list]) / len(nodule.edge_map_list)
                center_y = np.sum([int(edge.y) for edge in nodule.edge_map_list]) / len(nodule.edge_map_list)
                has_only_one_result = False
                edge = nodule.edge_map_list[0]
                # distance = ((int(first_edge.x) - int(edge.x))**2 + (int(first_edge.y) - int(edge.y))**2) ** 0.5
                distance = ((int(first_center_x) - int(center_x))**2 + (int(first_center_y) - int(center_y))**2) ** 0.5
                nodule_type = nodule.type.value
                if nodule_type not in [NoduleType.NODULE_GREATER_THAN_3MM.value]:
                    print(f'{self.SOP_Instance_UID} nodule_type NODULE_GREATER_THAN_3MM')
                    self.is_same_examination_result = False
                    return
                elif nodule_type != first_nodule_type:
                    print(f'{self.SOP_Instance_UID} nodule_type not same, {first_nodule_type} != {nodule_type}')
                    self.is_same_examination_result = False
                    return
                elif distance >= 5:
                    # print(f'{self.SOP_Instance_UID} distance >= 5, ({first_edge.x}, {first_edge.y}) & ({edge.x}, {edge.y})')
                    print(f'{self.SOP_Instance_UID} distance >= 5, ({first_center_x}, {first_center_y}) & ({center_x}, {center_y})')
                    self.is_same_examination_result = False
                    return
        if has_only_one_result:
            self.is_same_examination_result = False
            print('has_only_one_result')
            return
        print(f'same result!!!!!!!!!!!')
        
        # self.sobel_x = cv2.filter2D(self.pixel_array, ddepth=-1 , dst=-1, kernel=kernel_x, anchor=(-1, -1), delta=0, borderType=cv2.BORDER_DEFAULT)
        # self.sobel_y = cv2.filter2D(self.pixel_array, ddepth=-1 , dst=-1, kernel=kernel_y, anchor=(-1, -1), delta=0, borderType=cv2.BORDER_DEFAULT)


    # TODO: it seems not correct...
    # https://www.kaggle.com/gzuidhof/full-preprocessing-tutorial
    # https://vincentblog.xyz/posts/medical-images-in-python-computed-tomography
    def transform_to_hu(self):
        intercept = self.rescale_intercept
        slope = self.rescale_slope
        hu_image = self.pixel_array * slope + intercept
        
        return hu_image

    def window_image(self, window_center, window_width):
        img_min = window_center - window_width // 2
        img_max = window_center + window_width // 2
        window_image = self.transform_to_hu().copy()
        window_image[window_image < img_min] = img_min
        window_image[window_image > img_max] = img_max
        print(np.max(window_image))
        print(np.min(window_image))
        
        return window_image

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

    def plot(self, pixel_array):
        # Show some slice in the middle
        plt.imshow(pixel_array, cmap=plt.cm.gray)
        plt.show()

        # Show some slice in the middle
        plt.imshow(self.pixel_hu_list, cmap=plt.cm.gray)
        plt.show()

    def reshape(self):
        NotImplemented

    def standardlize(self):
        
        image = self.transform_to_hu()
        # Convert to int32, 
        image = image.astype(np.int32)
        
        max = np.max(image)
        min = np.min(image)

        image = (image - min) / (max - min)
        
        return image