from service.dicom_service import get_ct_dicom_directory, read_ct_xml_definition, read_ct_dicom
from utils.enum import Modality, Manufacturer, NoduleType
from utils.worker import XmlDefinitionWorker

import service.dicom_service as service
import copy


def get_directory() -> []:
    global dicom_directory
    dicom_directory = get_ct_dicom_directory()

def get_prepair_data() -> []:
    global definition_list
    global total_ct_dicom_count
    global big_nodule_list
    global small_nodule_list
    global non_nodule_list
    global not_mapped_list
    global not_same_ct_dicom_list

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
    
    big_nodule_list.extend(my_worker1.big_nodule_ct_dicom_list)
    big_nodule_list.extend(my_worker2.big_nodule_ct_dicom_list)
    big_nodule_list.extend(my_worker3.big_nodule_ct_dicom_list)
    big_nodule_list.extend(my_worker4.big_nodule_ct_dicom_list)
    
    small_nodule_list.extend(my_worker1.small_nodule_ct_dicom_list)
    small_nodule_list.extend(my_worker2.small_nodule_ct_dicom_list)
    small_nodule_list.extend(my_worker3.small_nodule_ct_dicom_list)
    small_nodule_list.extend(my_worker4.small_nodule_ct_dicom_list)
    
    non_nodule_list.extend(my_worker1.non_nodule_ct_dicom_list)
    non_nodule_list.extend(my_worker2.non_nodule_ct_dicom_list)
    non_nodule_list.extend(my_worker3.non_nodule_ct_dicom_list)
    non_nodule_list.extend(my_worker4.non_nodule_ct_dicom_list)
    
    not_mapped_list.extend(my_worker1.not_mapped_ct_dicom_list)
    not_mapped_list.extend(my_worker2.not_mapped_ct_dicom_list)
    not_mapped_list.extend(my_worker3.not_mapped_ct_dicom_list)
    not_mapped_list.extend(my_worker4.not_mapped_ct_dicom_list)
    
    not_same_ct_dicom_list.extend(my_worker1.not_same_ct_dicom_list)
    not_same_ct_dicom_list.extend(my_worker2.not_same_ct_dicom_list)
    not_same_ct_dicom_list.extend(my_worker3.not_same_ct_dicom_list)
    not_same_ct_dicom_list.extend(my_worker4.not_same_ct_dicom_list)
    # mapped_ct_dicom_list.extend(my_worker1.mapped_ct_dicom_list)
    # mapped_ct_dicom_list.extend(my_worker2.mapped_ct_dicom_list)
    # mapped_ct_dicom_list.extend(my_worker3.mapped_ct_dicom_list)
    # mapped_ct_dicom_list.extend(my_worker4.mapped_ct_dicom_list)
    
    # mapped_ct_dicom_list_unmatched.extend(my_worker1.mapped_ct_dicom_list_unmatched)
    # mapped_ct_dicom_list_unmatched.extend(my_worker2.mapped_ct_dicom_list_unmatched)
    # mapped_ct_dicom_list_unmatched.extend(my_worker3.mapped_ct_dicom_list_unmatched)
    # mapped_ct_dicom_list_unmatched.extend(my_worker4.mapped_ct_dicom_list_unmatched)
    
    # un_mapped_ct_dicom_list.extend(my_worker1.un_mapped_ct_dicom_list)
    # un_mapped_ct_dicom_list.extend(my_worker2.un_mapped_ct_dicom_list)
    # un_mapped_ct_dicom_list.extend(my_worker3.un_mapped_ct_dicom_list)
    # un_mapped_ct_dicom_list.extend(my_worker4.un_mapped_ct_dicom_list)

def describe():
    global big_nodule_list
    global small_nodule_list
    global non_nodule_list
    global not_mapped_list
    global not_same_ct_dicom_list

    # print(len(definition_list))
    print(f' big_nodule_list count = {len(big_nodule_list)}')
    print(f' small_nodule_list count = {len(small_nodule_list)}')
    print(f' non_nodule_list count = {len(non_nodule_list)}')
    print(f' not_same_ct_dicom_list count = {len(not_same_ct_dicom_list)}')
    print(f' not_mapped_list count = {len(not_mapped_list)}')

def run():
    global dicom_directory
    global definition_list
    # global mapped_ct_dicom_list
    # global mapped_ct_dicom_list_unmatched
    # global un_mapped_ct_dicom_list
    global big_nodule_list
    global small_nodule_list
    global non_nodule_list
    global total_ct_dicom_count
    global not_mapped_list
    global not_same_ct_dicom_list

    dicom_directory = []
    definition_list = []
    total_ct_dicom_count = 0
    # mapped_ct_dicom_list = []  # this is the final data we want to analysis
    # un_mapped_ct_dicom_list = []  # this is the final data we want to analysis
    # mapped_ct_dicom_list_unmatched = []
    big_nodule_list = []
    small_nodule_list = []
    non_nodule_list = []
    not_mapped_list = []
    not_same_ct_dicom_list = []
    get_directory()
    get_prepair_data()