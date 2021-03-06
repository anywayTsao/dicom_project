from service.dicom_service import read_ct_xml_definition, read_ct_dicom

import time
import threading
import queue

# Worker 類別，負責處理資料
class XmlDefinitionWorker(threading.Thread):
    
    def __init__(self, my_list, num):
        threading.Thread.__init__(self)
        self.my_list = my_list
        self.num = num
        self.definition_list = []
        # self.mapped_ct_dicom_list = []  # 驗片結果一致的 CT
        # self.mapped_ct_dicom_list_unmatched = []  # 驗片結果不一致的 CT
        # self.un_mapped_ct_dicom_list = []  # 無驗片結果的 CT
        self.big_nodule_ct_dicom_list = []
        self.small_nodule_ct_dicom_list = []
        self.non_nodule_ct_dicom_list = []
        self.not_mapped_ct_dicom_list = []
        self.not_same_ct_dicom_list = []
        self.total_ct_dicom_count = 0

    def run(self):
        while len(self.my_list) > 0:
        # 取得新的資料
            path = self.my_list.pop(0)

            # 處理資料
            print("Worker %d: %s" % (self.num, path))
            time.sleep(0.1)
            print(f'=========read xml=========')
            self.definition_list.extend(read_ct_xml_definition(path))

            print(f'=========read dicom=========')
            ct_dicom_list = read_ct_dicom(path)
            self.total_ct_dicom_count += len(ct_dicom_list)
            for ct_dicom in ct_dicom_list: 
                for definition in self.definition_list:
                    if definition.image_uid == ct_dicom.SOP_Instance_UID:
                        ct_dicom.add_nodule_list(definition)
                
                ct_dicom.check_examination_result()

                if ct_dicom.nodule_type in [2]:
                    self.big_nodule_ct_dicom_list.append(ct_dicom)
                elif ct_dicom.nodule_type in [1]:
                    self.small_nodule_ct_dicom_list.append(ct_dicom)
                elif ct_dicom.nodule_type in [0]:
                    self.non_nodule_ct_dicom_list.append(ct_dicom)
                elif ct_dicom.nodule_type in [999]:
                    self.not_same_ct_dicom_list.append(ct_dicom)
                else:
                    self.not_mapped_ct_dicom_list.append(ct_dicom)
                
                # if len(ct_dicom.nodule_list) > 0:
                #     if ct_dicom.is_same_examination_result:
                #         self.mapped_ct_dicom_list.append(ct_dicom)
                #     else:
                #         self.mapped_ct_dicom_list_unmatched.append(ct_dicom)
                # else:
                #     self.un_mapped_ct_dicom_list.append(ct_dicom)

