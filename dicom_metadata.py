import pandas as pd

# 開啟 CSV 檔案
def read_metadata(path: str):
    df = pd.read_csv('../../ntpu_project/LIDC-IDRI_MetaData.csv')
    ge_df = df[df['Manufacturer'] == 'GE MEDICAL SYSTEMS']['Patient Id'].drop_duplicates()