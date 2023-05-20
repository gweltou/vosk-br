from typing import List
import os



def list_files_with_extension(ext, rep, recursive=True) -> List[str]:
    file_list = []
    if os.path.isdir(rep):
        for filename in os.listdir(rep):
            filename = os.path.join(rep, filename)
            if os.path.isdir(filename) and recursive:
                file_list.extend(list_files_with_extension(ext, filename))
            elif os.path.splitext(filename)[1] == ext:
                file_list.append(filename)
    return file_list



def read_file_drop_comments(path: str) -> List[str]:
    lines = []
    with open(path, 'r') as f:
        for l in f.readlines():
            l = l.strip()
            if l and not l.startswith('#'):
                lines.append(l)
    return lines
