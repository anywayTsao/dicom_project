from service.dicom_service import get_ct_dicom_directory, read_ct_xml_definition, read_ct_dicom
from utils.enum import Modality, Manufacturer, NoduleType
from utils.worker import XmlDefinitionWorker

import service.dicom_service as service
import copy

dicom_directory = []
definition_list = []
total_ct_dicom_count = 0
mapped_ct_dicom_list = []  # this is the final data we want to analysis

def get_directory() -> []:
    global dicom_directory
    dicom_directory = get_ct_dicom_directory()

def get_prepair_data() -> []:
    global definition_list
    global total_ct_dicom_count
    global mapped_ct_dicom_list

    my_path_list = copy.deepcopy(dicom_directory)
    # 建立 Worker
    my_worker1 = XmlDefinitionWorker(my_path_list, 1)
    my_worker2 = XmlDefinitionWorker(my_path_list, 2)
    my_worker3 = XmlDefinitionWorker(my_path_list, 3)
    my_worker4 = XmlDefinitionWorker(my_path_list, 4)

    # 讓 Worker 開始處理資料
    my_worker1.start()
    my_worker2.start()
    my_worker3.start()
    my_worker4.start()

    # 等待所有 Worker 結束
    my_worker1.join()
    my_worker2.join()
    my_worker3.join()
    my_worker4.join()

    definition_list.extend(my_worker1.definition_list)
    definition_list.extend(my_worker2.definition_list)
    definition_list.extend(my_worker3.definition_list)
    definition_list.extend(my_worker4.definition_list)
    total_ct_dicom_count += my_worker1.total_ct_dicom_count
    total_ct_dicom_count += my_worker2.total_ct_dicom_count
    total_ct_dicom_count += my_worker3.total_ct_dicom_count
    total_ct_dicom_count += my_worker4.total_ct_dicom_count
    mapped_ct_dicom_list.extend(my_worker1.mapped_ct_dicom_list)
    mapped_ct_dicom_list.extend(my_worker2.mapped_ct_dicom_list)
    mapped_ct_dicom_list.extend(my_worker3.mapped_ct_dicom_list)
    mapped_ct_dicom_list.extend(my_worker4.mapped_ct_dicom_list)
    mapped_ct_dicom_list_unmatched.extend(my_worker1.mapped_ct_dicom_list_unmatched)
    mapped_ct_dicom_list_unmatched.extend(my_worker2.mapped_ct_dicom_list_unmatched)
    mapped_ct_dicom_list_unmatched.extend(my_worker3.mapped_ct_dicom_list_unmatched)
    mapped_ct_dicom_list_unmatched.extend(my_worker4.mapped_ct_dicom_list_unmatched)
    un_mapped_ct_dicom_list.extend(my_worker1.un_mapped_ct_dicom_list)
    un_mapped_ct_dicom_list.extend(my_worker2.un_mapped_ct_dicom_list)
    un_mapped_ct_dicom_list.extend(my_worker3.un_mapped_ct_dicom_list)
    un_mapped_ct_dicom_list.extend(my_worker4.un_mapped_ct_dicom_list)

def describe():
    global mapped_ct_dicom_list
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

def run():
    global dicom_directory
    global definition_list
    global mapped_ct_dicom_list
    global mapped_ct_dicom_list_unmatched
    global un_mapped_ct_dicom_list
    global total_ct_dicom_count

    dicom_directory = []
    definition_list = []
    total_ct_dicom_count = 0
    mapped_ct_dicom_list = []  # this is the final data we want to analysis
    un_mapped_ct_dicom_list = []  # this is the final data we want to analysis
    mapped_ct_dicom_list_unmatched = []
    get_directory()
    get_prepair_data()