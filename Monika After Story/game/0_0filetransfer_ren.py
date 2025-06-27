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

        # For GUI feedback
        self.current_step = ""              # "copying", "deleting", etc.
        self.current_step_description = ""  # current file or directory being processed
        self.current_progress = 0.0         # Progress in percentage or file count fraction

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
        if not os.path.exists(file2):
            return False

        stat1 = os.stat(file1)
        stat2 = os.stat(file2)

        if stat1.st_size != stat2.st_size or stat1.st_mtime != stat2.st_mtime:
            return False

        return self.file_hash(file1) == self.file_hash(file2)

    def sync(self):
        self.current_step = ""              # "copying", "deleting", etc.
        self.current_step_description = ""  # current file or directory being processed
        self.current_progress = 0.0         # Progress in percentage or file count fraction

        start_time = time.time()

        # === Phase 1: Copy/update files ===
        self.current_step = "复制新增文件[1/2]"
        all_files_to_copy = []
        for src_root, dirs, files in os.walk(self.src_path):
            for file in files:
                all_files_to_copy.append(os.path.join(src_root, file))

        copied_count = 0
        total_files_to_copy = len(all_files_to_copy)

        for src_root, dirs, files in os.walk(self.src_path):
            relative_path = os.path.relpath(src_root, self.src_path)
            dst_root = os.path.join(self.dst_path, relative_path)

            if not os.path.exists(dst_root):
                os.makedirs(dst_root, exist_ok=True)

            for file in files:
                src_file = os.path.join(src_root, file)
                dst_file = os.path.join(dst_root, file)

                self.current_step_description = f"正在处理 {src_file}"
                copied_count += 1
                self.current_progress = copied_count / total_files_to_copy if total_files_to_copy > 0 else 1.0
                if self.whitelist.get(file, False):
                    continue

                if self.is_blacklisted(src_file):
                    base_name = os.path.splitext(src_file)[0]
                    if os.path.exists(f"{base_name}.rpy"):
                        continue

                if os.path.exists(dst_file) and self.files_are_same(src_file, dst_file):
                    continue

                if self.is_important_file(src_file):
                    change_type = "changed" if os.path.exists(dst_file) else "added"
                    print(f"Important file {change_type}: {src_file}")
                    self.restart_required = True

                shutil.copy2(src_file, dst_file)

                
                

        # === Phase 2: Delete obsolete files ===
        self.current_step = "移除已删除文件[2/2]"
        all_files_to_check = []
        for dst_root, dirs, files in os.walk(self.dst_path):
            for file in files:
                all_files_to_check.append(os.path.join(dst_root, file))

        checked_count = 0
        total_files_to_check = len(all_files_to_check)

        for dst_root, dirs, files in os.walk(self.dst_path, topdown=False):
            relative_path = os.path.relpath(dst_root, self.dst_path)
            src_root = os.path.normpath(os.path.join(self.src_path, relative_path))

            for file in files:
                dst_file = os.path.join(dst_root, file)
                src_file = os.path.join(src_root, file)

                self.current_step_description = f"正在检查 {dst_file}"
                checked_count += 1
                self.current_progress = checked_count / total_files_to_check if total_files_to_check > 0 else 1.0
                if file.endswith(".rpyc"):
                    src_rpy = os.path.join(src_root, file[:-1])
                    if os.path.exists(src_rpy):
                        continue

                if not os.path.exists(src_file) and not self.whitelist.get(file, False):
                    if self.is_important_file(dst_file):
                        self.restart_required = True
                        self.rpy_deleted = True
                        print(f"Important file removed: {dst_file}")
                    else:
                        print(f"Removing obsolete file: {dst_file}")
                    os.remove(dst_file)

                
                

            # Delete empty directories
            for dir in dirs:
                dst_dir = os.path.join(dst_root, dir)
                src_dir = os.path.join(src_root, dir)
                if not os.path.exists(src_dir):
                    shutil.rmtree(dst_dir, ignore_errors=True)

        self.current_step = "done"
        self.current_step_description = "Sync completed"
        self.current_progress = 1.0

        print(f"Sync completed in {time.time()-start_time:.2f}s. "
              f"{'Restart required' if self.restart_required else 'No changes detected'}")
        return self.restart_required
gameSyncer = FileSynchronizer("/storage/emulated/0/MAS/game", "/data/user/0/and.sirp.masmobile/files/game")
gameSyncer.add_to_whitelist("masrun")
gameSyncer.add_to_whitelist("cacert.pem")

import threading
class AsyncTask(object):
    def __init__(self, func, *args, **kwargs):
        self._func = func
        self._args = args
        self._kwargs = kwargs
        self.result = None
        self.exception = None
        self.is_finished = False
        self.is_success = False
        
        self._thread = threading.Thread(target=self._run)
        self._thread.start()

    def _run(self):
        try:
            self.result = self._func(*self._args, **self._kwargs)
            self.is_success = True
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.exception = e
            self.is_success = False

        finally:
            self.is_finished = True

    @property
    def is_alive(self):
        return self._thread.is_alive()

    def wait(self, timeout=None):
        """等待任务完成（可选超时时间）"""
        self._thread.join(timeout=timeout)
