import os


def deep_scan(path: str, file_type: str):
    file_list = []
    for root, directory, files in os.walk(path):
        for f in files:
            full_path = os.path.join(root, f)
            if full_path[-3:] == file_type:
                file_list.append(full_path.replace('\\', '/'))
                # print(full_path)
    return file_list

def read_xml(folder: str):
    for file_path in deep_scan(folder, 'xml'):
        print(os.path.isfile(file_path))
