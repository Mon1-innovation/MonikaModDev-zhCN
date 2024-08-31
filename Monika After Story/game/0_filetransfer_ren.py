"""renpy
early python:
"""
import os
import shutil
import hashlib

class FileSynchronizer:
    def __init__(self, src_path, dst_path):
        self.src_path = src_path
        self.dst_path = dst_path
        self.whitelist = {}
    
    def add_to_whitelist(self, file_name, enable_override=False):
        """
        将文件添加到白名单中。
        
        Args:
            file_name (str): 需要添加至白名单的文件名。
            enable_override (bool, optional): 是否覆盖同名文件的原有状态，默认为False。
        
        Returns:
            None
        """
        self.whitelist[file_name] = enable_override

    def file_hash(self, file_path):
        """
        计算给定文件路径的文件内容的SHA-256哈希值。

        Args:
            file_path (str): 文件路径。

        Returns:
            str: 文件内容的SHA-256哈希值。

        """
        hash_func = hashlib.sha256()
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                hash_func.update(chunk)
        return hash_func.hexdigest()
    
    def files_are_same(self, file1, file2):
        """
        判断两个文件是否相同。
        
        Args:
            file1 (str): 第一个文件的路径。
            file2 (str): 第二个文件的路径。
        
        Returns:
            bool: 如果两个文件相同则返回True，否则返回False。
        
        """
        return self.file_hash(file1) == self.file_hash(file2)
    
    def sync(self):
        """
        同步源目录(self.src_path)到目标目录(self.dst_path)，
        保持目录结构不变，并删除目标目录中源目录不存在的文件。
        
        Args:
            无
        
        Returns:
            无返回值
        
        Raises:
            无异常抛出
        
        """
        if not os.path.exists(self.dst_path):
            os.makedirs(self.dst_path)
        
        for root, _, files in os.walk(self.src_path):
            relative_path = os.path.relpath(root, self.src_path)
            dst_dir = os.path.join(self.dst_path, relative_path)
            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)
            
            for file_name in files:
                src_file = os.path.join(root, file_name)
                dst_file = os.path.join(dst_dir, file_name)
                
                if os.path.exists(dst_file):
                    if file_name in self.whitelist and not self.whitelist[file_name]:
                        continue  # Skip, don't override
                    if not self.files_are_same(src_file, dst_file):
                        shutil.copy2(src_file, dst_file)
                else:
                    shutil.copy2(src_file, dst_file)
        
        # Delete files in dst_path that are not in src_path and not in the whitelist
        for root, _, files in os.walk(self.dst_path):
            relative_path = os.path.relpath(root, self.dst_path)
            src_dir = os.path.join(self.src_path, relative_path)
            
            if os.path.exists(src_dir):
                for file_name in files:
                    dst_file = os.path.join(root, file_name)
                    if file_name not in self.whitelist:
                        src_file = os.path.join(src_dir, file_name)
                        if not os.path.exists(src_file):
                            os.remove(dst_file)
            else:
                for file_name in files:
                    if file_name not in self.whitelist:
                        os.remove(os.path.join(root, file_name))


syncer = FileSynchronizer("/sdcard/MAS/game/", "/data/data/and.sirp.masmobile/files/game")
syncer.sync()