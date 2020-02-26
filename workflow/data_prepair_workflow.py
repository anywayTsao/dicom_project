from service.dicom_service import get_ct_dicom_directory, read_ct_xml_definition, read_ct_dicom
from utils.enum import Modality, Manufacturer, NoduleType


mapped_ct_dicom_list = []  # this is the final data we want to analysis

def data_prepair_workflow():
    
    path = '../../../ntpu_project/DICOM/'
    directory_list = get_ct_dicom_directory(path)

    # read all the definition
    for directory in directory_list:
        print(f'============{directory}============')
        definition_list = read_ct_xml_definition(directory)

        ct_dicom_list = read_ct_dicom(directory)
        
        for ct_dicom in ct_dicom_list: 
            for definition in definition_list:
                if definition.image_uid == ct_dicom.SOP_Instance_UID:
                    ct_dicom.add_nodule_list(definition)
            if len(ct_dicom.nodule_list) > 0:
                mapped_ct_dicom_list.append(ct_dicom)
    
    print(len(mapped_ct_dicom_list))
    count_type_1 = 0
    count_type_2 = 0
    count_type_3 = 0
    for ct_dicom in mapped_ct_dicom_list:
        for nodule in ct_dicom.nodule_list:
            if nodule.type == NoduleType.NODULE_GREATER_THAN_3MM:
                count_type_1 += 1
            elif nodule.type == NoduleType.NODULE_LESS_THAN_3MM:
                count_type_2 += 1
            elif nodule.type == NoduleType.NON_NODULE_GREATER_THAN_3MM:
                count_type_3 += 1
    # print(len(definition_list))
    print(f' NODULE_GREATER_THAN_3MM count = {count_type_1}')
    print(f' NODULE_LESS_THAN_3MM count = {count_type_2}')
    print(f' NON_NODULE_GREATER_THAN_3MM count = {count_type_3}')



