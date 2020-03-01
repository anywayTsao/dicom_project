# dicom_project
## run env.bat in cmd to set environment variable first

import workflow.dicom_workflow as workflow

workflow.get_directory()
workflow.get_prepair_data()

len(workflow.definition_list)
workflow.total_ct_dicom_count
len(workflow.dicom_directory)
len(workflow.mapped_ct_dicom_list)