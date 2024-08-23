
import os
import hashlib
import sys

    
if len(sys.argv) != 2:
    print("Please provide one argument: the name of the folder inside songs that you want to clean")
    sys.exit(1)
    
def remove_duplicate_files(folder_path):
    file_hash = {}
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'rb') as f:
                file_content = f.read()
                file_hash_value = hashlib.md5(file_content).hexdigest()
                
                if file_hash_value in file_hash:
                    print("deleted")
                    os.remove(file_path)
                    print(f"Removed duplicate file: {file_path}")
                else:
                    file_hash[file_hash_value] = file_path

folder_path = f'songs/{sys.argv[1]}'
remove_duplicate_files(folder_path)
