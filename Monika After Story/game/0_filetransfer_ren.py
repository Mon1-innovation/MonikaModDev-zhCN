"""renpy
python early: 
"""
import os
import shutil
import hashlib
import time

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
        _, ext = os.path.splitext(filename)
        return ext in self.important_fileext

    def is_blacklisted(self, filename):
        _, ext = os.path.splitext(filename)
        return ext in self.blacklist_fileext

    def add_to_whitelist(self, file_name, enable_override=False):
        self.whitelist[file_name] = enable_override

    def file_hash(self, file_path):
        hash_func = hashlib.sha256()
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                hash_func.update(chunk)
        return hash_func.hexdigest()

    def files_are_same(self, file1, file2):
        """Optimized comparison with metadata check first"""
        if not os.path.exists(file2):
            return False
            
        stat1 = os.stat(file1)
        stat2 = os.stat(file2)
        
        # First check size and modification time
        if stat1.st_size != stat2.st_size:
            return False
        if stat1.st_mtime != stat2.st_mtime:
            return False
            
        # Fallback to content hash
        return self.file_hash(file1) == self.file_hash(file2)

    def sync(self):
        if not os.path.exists("/storage/emulated/0/MAS/bypass_filetransfer"):
            pass
        start_time = time.time()
        
        # Phase 1: Copy/update files from source to destination
        for src_root, dirs, files in os.walk(self.src_path):
            relative_path = os.path.relpath(src_root, self.src_path)
            dst_root = os.path.join(self.dst_path, relative_path)

            # Create directory structure first
            if not os.path.exists(dst_root):
                os.makedirs(dst_root, exist_ok=True)

            for file in files:
                src_file = os.path.join(src_root, file)
                dst_file = os.path.join(dst_root, file)
                
                # Skip whitelisted files
                if self.whitelist.get(file, False):
                    continue
                
                # Handle blacklisted files
                if self.is_blacklisted(src_file):
                    base_name = os.path.splitext(src_file)[0]
                    src_rpy = f"{base_name}.rpy"
                    if os.path.exists(src_rpy):
                        continue

                # Skip unchanged files
                if os.path.exists(dst_file) and self.files_are_same(src_file, dst_file):
                    continue
                
                # Handle important files
                if self.is_important_file(src_file):
                    change_type = "changed" if os.path.exists(dst_file) else "added"
                    print(f"Important file {change_type}: {src_file}")
                    self.restart_required = True
                
                # Perform actual copy
                shutil.copy2(src_file, dst_file)

        # Phase 2: Clean up obsolete files in destination
        for dst_root, dirs, files in os.walk(self.dst_path, topdown=False):
            relative_path = os.path.relpath(dst_root, self.dst_path)
            src_root = os.path.normpath(os.path.join(self.src_path, relative_path))

            # Clean files
            for file in files:
                dst_file = os.path.join(dst_root, file)
                src_file = os.path.join(src_root, file)
                
                # Handle .rpyc files with existing .rpy
                if file.endswith(".rpyc"):
                    src_rpy = os.path.join(src_root, file[:-1])
                    if os.path.exists(src_rpy):
                        continue
                
                # Delete if source file missing and not whitelisted
                if not os.path.exists(src_file) and not self.whitelist.get(file, False):
                    if self.is_important_file(dst_file):
                        self.restart_required = True
                        self.rpy_deleted = True
                        print(f"Important file removed: {dst_file}")
                    else:
                        print(f"Removing obsolete file: {dst_file}")
                    os.remove(dst_file)

            # Clean directories
            for dir in dirs:
                dst_dir = os.path.join(dst_root, dir)
                src_dir = os.path.join(src_root, dir)
                if not os.path.exists(src_dir):
                    shutil.rmtree(dst_dir, ignore_errors=True)

        print(f"Sync completed in {time.time()-start_time:.2f}s. "
              f"{'Restart required' if self.restart_required else 'No changes detected'}")
        return self.restart_required


gameSyncer = FileSynchronizer("/storage/emulated/0/MAS/game", "/data/user/0/and.sirp.masmobile/files/game")
gameSyncer.add_to_whitelist("masrun")
gameSyncer.add_to_whitelist("cacert.pem")
