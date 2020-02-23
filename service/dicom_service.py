from utils.file_util import deep_scan
from models.dicom import Dicom
from utils.enum import Modality, Manufacturer
from lxml import objectify, etree

import os, re

def namespace(element):
    m = re.match(r'\{.*\}', element.tag)
    return m.group(0) if m else ''

ct_dicom_directory_list = []

def get_ct_dicom_directory() -> []:
    ''' get the first patient dicom to find the manufacturer and modality we want,
        here we want:
            Manufacturer.GE_MEDICAL_SYSTEMS
            Modality.CT
    '''
    # path = '../../../ntpu_project/DICOM/LIDC-IDRI-0001/01-01-2000-30178/3000566-03192/'
    path = '../../../ntpu_project/DICOM/LIDC-IDRI-0001/01-01-2000-30178/'
    # path = '../../../ntpu_project/DICOM/'
    directory_list = [ name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name)) ]
    for i, directory in enumerate(directory_list):  # each patient
        for file_path in deep_scan(path+directory+"/", 'dcm'):
            if (i+1) % 100 == 0:
                print(f'reading total...{i+1} patient folders')
            my_dicom = Dicom(file_path)
            if my_dicom.manufacturer == Manufacturer.GE_MEDICAL_SYSTEMS.value and my_dicom.modality == Modality.CT.value:
                ct_dicom_directory_list.append(my_dicom.directory)
            # break  
    # print(ct_dicom_directory_list[:1])
    return ct_dicom_directory_list

def read_ct_xml_definition() -> []:
    path = '../../../ntpu_project/DICOM/LIDC-IDRI-0001/01-01-2000-30178/3000566-03192/'
    
    for file_path in deep_scan(path, 'xml'):
        print(file_path)
        xml = open(file_path, 'rb').read()
        main = etree.fromstring(xml)
        ns = namespace(main)
        a = main.findall(f'.//{ns}readingSession')
        print(a)