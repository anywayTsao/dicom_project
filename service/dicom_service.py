from utils.file_util import deep_scan
from models.dicom import Dicom
from utils.enum import Modality, Manufacturer
from lxml import objectify, etree
from models.nodule import Nodule

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

# TODO: 
def read_ct_xml_definition() -> []:
    path = '../../../ntpu_project/DICOM/LIDC-IDRI-0001/01-01-2000-30178/3000566-03192/'
    definition_list = []
    for file_path in deep_scan(path, 'xml'):
        print(file_path)
        xml = open(file_path, 'rb').read()
        main = etree.fromstring(xml)
        ns = namespace(main)
        session_list = main.findall(f'.//{ns}readingSession')
        # print(session_list)
        for i, session in enumerate(session_list):
            # print(f'=========session {i+1}============')
            unblinded_nodule_list = session.findall(f'.//{ns}unblindedReadNodule')
            non_nodule_list = session.findall(f'.//{ns}nonNodule')
            
            for j, nodule in enumerate(unblinded_nodule_list):
                # print(f'========= unblinded_nodule {j+1} ============')
                definition = parse_roi(ns, nodule)
                definition_list.extend(definition)
                # break
            
            for j, nodule in enumerate(non_nodule_list):
                # print(f'========= non_nodule_list {j+1} ============')
                definition = parse_roi(ns, nodule, True)
                definition_list.extend(definition)
                # break
            # break
            print(len(unblinded_nodule_list))
            print(len(non_nodule_list))
        # break
    print(definition_list[-1])
    print(definition_list[-4])
    return definition_list
    
def parse_roi(ns, nodule, is_non_nodule = False):
    if is_non_nodule:
        roi_element_list = [nodule]
    else:
        roi_element_list = nodule.findall(f'{ns}roi')
    nodule_list = []
    for roi in roi_element_list:
        nodule = Nodule(ns, roi)
        nodule_list.append(nodule)
    return nodule_list
    