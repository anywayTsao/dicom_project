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


class Dicom:

    def __init__(self, full_path: str):
        self.full_path = full_path
        self.directory = '/'.join(full_path.split('/')[:-1]) + '/'
        dataset = pydicom.dcmread(full_path)
        self.manufacturer = dataset.Manufacturer
        self.modality = dataset.Modality
        self.SOP_Instance_UID = dataset.SOPInstanceUID
        # print(dataset)
        print(self.SOP_Instance_UID)
