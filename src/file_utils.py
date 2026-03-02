import os
import shutil

def remove_dir(path):
    shutil.rmtree(path)

def create_dir(path):
    os.makedirs(path, exist_ok=True)

def copy_tree(src, dst):
    shutil.copytree(src, dst)
