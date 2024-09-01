"""renpy
python early: 
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
        同步源目录到目标目录。
        
        Args:
            无
        
        Returns:
            无
        
        """
        rpy_file = []
        # Sync from source to destination
        for root, dirs, files in os.walk(self.src_path):
            print(f"Syncing {root}/{dirs}/{files} to {self.dst_path}...")
            relative_path = os.path.relpath(root, self.src_path)
            dst_root = os.path.join(self.dst_path, relative_path)
            
            # Ensure the destination directories exist
            if not os.path.exists(dst_root):
                os.makedirs(dst_root)
            
            # Copy files from source to destination and overwrite existing files
            for file in files:
                if ".rpy" in file:
                    rpy_file.append(os.path.join(root, file))
                src_file = os.path.join(root, file)
                dst_file = os.path.join(dst_root, file)
                if not self.whitelist.get(file, False):
                    shutil.copy2(src_file, dst_file)
                    
        # Remove files and directories from destination that are not in source
        for root, dirs, files in os.walk(self.dst_path):
            relative_path = os.path.relpath(root, self.dst_path)
            src_root = os.path.join(self.src_path, relative_path)
            
            # Remove files not present in source
            for file in files:
                # 如果找到rpyc对应的rpy
                for item in rpy_file:
                    if item in file:
                        continue
                dst_file = os.path.join(root, file)
                src_file = os.path.join(src_root, file)
                if not os.path.exists(src_file) and file not in self.whitelist:
                    os.remove(dst_file)
            
            # Remove empty directories not present in source
            for dir in dirs:
                dst_dir = os.path.join(root, dir)
                src_dir = os.path.join(src_root, dir)
                if not os.path.exists(src_dir):
                    shutil.rmtree(dst_dir)


gameSyncer = FileSynchronizer("/storage/emulated/0/MAS/game", "/data/data/and.sirp.masmobile/files/game")
gameSyncer.add_to_whitelist("masrun")
