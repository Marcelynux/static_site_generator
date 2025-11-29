import os
import shutil

def copy_static_to_public(src="static", dest="public"):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.mkdir(dest)
    
    def recursive_copy(src_path, dest_path):
        for name in os.listdir(src_path):
            source_item = os.path.join(src_path, name)
            dest_item = os.path.join(dest_path, name)

            if os.path.isfile(source_item):
                print(f"Copying file: {source_item} → {dest_item}")
                shutil.copy(source_item, dest_item)

            else:
                print(f"Entering directory: {source_item}")
                os.mkdir(dest_item)
                recursive_copy(source_item, dest_item)

    recursive_copy(src, dest)
