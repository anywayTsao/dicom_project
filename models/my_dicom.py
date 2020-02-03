import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
import pydicom


class MyDicom:
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
        self.series_instance_uid = dataset.SeriesInstanceUID
        self.modality = dataset.Modality
        self.manufacturer = dataset.Manufacturer
        self.rescale_intercept = dataset.RescaleIntercept
        self.rescale_slope = dataset.RescaleSlope
        # TODO: read xml to get examination result, if exist then call _read_image

    def _read_image(self):
        image = None 
        pass