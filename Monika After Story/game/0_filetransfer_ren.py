"""renpy
python early: 
"""
import os
import shutil
import hashlib

class FileSynchronizer:
    def __init__(self, src_path, dst_path):
        self.src_path = os.path.normpath(src_path)
        self.dst_path = os.path.normpath(dst_path)
        self.whitelist = {}
        self.blacklist_fileext = [".rpyc"]
        self.restart_required = False
        self.rpy_deleted = False
        self.important_fileext = [".rpy", ".rpa", ".rpyc"]
    def is_important_file(self, filename):
        # Extract the file extension
        _, ext = os.path.splitext(filename)
        # Check if the extension is in the list of important extensions
        return ext in self.important_fileext
    
    def is_blacklisted(self, filename):
        # Extract the file extension
        _, ext = os.path.splitext(filename)
        # Check if the extension is in the blacklist
        return ext in self.blacklist_fileext

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
            是否有文件被更改
        
        """
        rpy_file = []
        # Sync from source to destination
        for root, dirs, files in os.walk(self.src_path):
            print(f"Syncing {root}/{dirs} to {self.dst_path}...")
            relative_path = os.path.relpath(root, self.src_path)
            dst_root = os.path.join(self.dst_path, relative_path)
            
            # Ensure the destination directories exist
            if not os.path.exists(dst_root):
                os.makedirs(dst_root)
            
            # Copy files from source to destination and overwrite existing files
            for file in files:
                if ".rpyc" in file:
                    print(f"rpyc file: {os.path.join(root, file)}")
                if ".rpy" in file:
                    res = os.path.join(root, file)[len(self.src_path):]
                    #if ".rpyc" in file:
                    #    res = res[:-1]
                    rpy_file.append(res)
                    print(f"rpy_file added {res}")
                src_file = os.path.join(root, file)
                dst_file = os.path.join(dst_root, file)
                if not self.whitelist.get(file, False):
                    if self.is_blacklisted(src_file):
                        # 仅在源码存在的情况下忽略rpyc
                        if os.path.exists(src_file[:-1]) and ".rpyc" in src_file:
                            print(f"Skipping blacklisted file: {src_file}")
                            continue
                    if self.is_important_file(src_file):
                        if not os.path.exists(dst_file):
                            print(f"Important file added: {src_file}")
                            self.restart_required = True
                        elif not self.files_are_same(src_file, dst_file):
                            print(f"Important file changed: {src_file}")
                            self.restart_required = True
                    shutil.copy2(src_file, dst_file)
                    
        for root, dirs, files in os.walk(self.dst_path):
            relative_path = os.path.relpath(root, self.dst_path)
            src_root = os.path.join(self.src_path, relative_path.replace("/./", "/"))
            
            # Remove files not present in source
            for file in files:
                dst_file = os.path.join(root, file)
                src_file = os.path.join(src_root, file)
                if not os.path.exists(src_file):
                    print(f"File not found in source: {dst_file}")
                
                # Check if file should be skipped due to rpyc and rpy logic
                should_skip = False
                for item in rpy_file:
                    if item in dst_file:
                        should_skip = True
                        print(f"Skipping '{dst_file}' because find source file '{item}'")
                        break
                
                # If should_skip is True, continue to the next file
                if should_skip:
                    continue

                # Check if the source file doesn't exist and if it's not whitelisted
                if not os.path.exists(src_file) and not file in self.whitelist:
                    if self.is_important_file(dst_file):
                        self.restart_required = True
                        self.rpy_deleted = True
                        print(f"Important file removed: {dst_file}")    
                    else:
                        print(f"Removed file: {dst_file}")   
                    os.remove(dst_file)
                    
     
            # Remove empty directories not present in source
            for dir in dirs:
                dst_dir = os.path.join(root, dir)
                src_dir = os.path.join(src_root, dir)
                if not os.path.exists(src_dir):
                    shutil.rmtree(dst_dir)
        print("Sync complete. {}".format('Restart required.' if self.restart_required else "No restart needed."))
        return self.restart_required



gameSyncer = FileSynchronizer("/storage/emulated/0/MAS/game", "/data/user/0/and.sirp.masmobile/files/game")
gameSyncer.add_to_whitelist("masrun")
gameSyncer.add_to_whitelist("cacert.pem")
