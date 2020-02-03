import os


def deep_scan(path: str, file_type: str):
    file_list = []
    for root, directory, files in os.walk(path):
        for f in files:
            full_path = os.path.join(root, f)
            # print(fullpath)
            if full_path[-3:] == file_type:
                file_list.append(full_path.replace('\\', '/'))
    return file_list