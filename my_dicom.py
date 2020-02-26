import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
import pydicom
import xml.dom.minidom
import xml.etree.ElementTree as ET
import re

from utils.file_util import deep_scan
from matplotlib import pyplot as plt
from matplotlib import cm

def namespace(element):
    m = re.match(r'\{.*\}', element.tag)
    return m.group(0) if m else ''
    

class GEMedicalSystemsDicom:
    patient_id: str
    instance_number: str
    series_instance_uid: str
    modality: str
    manufacturer: str
    rescale_intercept: str
    rescale_slope: str
    nodule_ge_3mm: []
    nodule_lt_3mm: []
    non_nodule_ge_3mm: []
    has_xml_examination: bool
    image: object

    def __init__(self, full_path: str):
        self.full_path = full_path
        dataset = pydicom.dcmread(full_path)
        self.patient_id = dataset.PatientID
        self.instance_number = dataset.InstanceNumber
        self.SOPInstanceUID = dataset.SOPInstanceUID  # in xml: roi/imageSOP_UID
        if hasattr(dataset, 'ReferencedSOPInstanceUID'):
            self.ReferencedSOPInstanceUID = dataset.ReferencedSOPInstanceUID
        self.StudyInstanceUID = dataset.StudyInstanceUID
        self.series_instance_uid = dataset.SeriesInstanceUID
        # self.FrameofReferenceUID = dataset.FrameofReferenceUID
        # self.UID = dataset.UID
        # self.StorageMediaFileSetUID = dataset.StorageMediaFileSetUID
        print(f'file_name = {full_path.split("/")[-1]}, SOPInstanceUID = {dataset.SOPInstanceUID}')
        self.modality = dataset.Modality
        self.manufacturer = dataset.Manufacturer
        if hasattr(dataset, 'RescaleIntercept'):
            self.rescale_intercept = dataset.RescaleIntercept
        if hasattr(dataset, 'RescaleSlope'):
            self.rescale_slope = dataset.RescaleSlope
        # self.pixel_array = dataset.pixel_array
        self.pixel_array = None
        # TODO: read xml to get examination result, if exist then call _read_image
        current_path = '/'.join(full_path.split('/')[0:-1]) 
        self._read_xml(current_path)

    def _read_image(self):
        self.image = None 
        pass

    # TODO: Remove namespace.....................
    def _read_xml(self, path: str):
        
        for file_path in deep_scan(path, 'xml'):
            # print(file_path)
            xml = ET.parse(file_path)
            root = xml.getroot()
            ns = namespace(root)
            # print(namespace(root))
            # print(root.attrib)
            # for child in root:
            #     print(f'{child.tag} = {child.attrib}')
            # print(root.tag)
            # print(root.attrib)
            # print(root.findall(f'{ns}readingSession'))
            # for readingSession in root.findall(f'{ns}readingSession'):
                # rank = readingSession.find('servicingRadiologistID').text
                # name = readingSession.get('annotationVersion')
                # print(name, rank)
            session_list = root.findall(f'{ns}readingSession')
            # print(len(session_list))
            for session in session_list:
                unblinded_list = session.findall(f'{ns}unblindedReadNodule')
                for unblinded in unblinded_list:
                    roi_list = unblinded.findall(f'{ns}roi')
                    for roi in roi_list:
                        self._read_roi(roi, ns)
                non_list = session.findall(f'{ns}nonNodule')
                for non in non_list:
                    roi_list = non.findall(f'{ns}roi')
                    for roi in roi_list:
                        self._read_roi(roi, ns)
            break
        pass

    def _read_roi(self, roi, ns):
        # print('roi imageSOP_UID = ', roi.find(f'{ns}imageSOP_UID').text)
        if self.SOPInstanceUID == roi.find(f'{ns}imageSOP_UID').text:
            print('found!!!!!!!!!!!!!!!!', self.SOPInstanceUID)

    def plot(self, figsize=(10,10)):
        plt.figure(figsize=figsize)
        plt.imshow(self.pixel_array, cmap='gray')
        plt.show()
