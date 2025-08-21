"""renpy
init python: 
"""

import os
import shutil
import zipfile
import json

class simplelogger:
    def info(msg, *args, **kwargs):
        print(f"[INFO] {msg}", *args, **kwargs)
    
    def error(msg, *args, **kwargs):
        print(f"[ERROR] {msg}", *args, **kwargs)
    
    def warn(msg, *args, **kwargs):
        print(f"[WARN] {msg}", *args, **kwargs)
    
    def warning(msg, *args, **kwargs):
        print(f"[WARN] {msg}", *args, **kwargs)
    
    def debug(msg, *args, **kwargs):
        print(f"[DEBUG] {msg}", *args, **kwargs)

class SubmodUninstaller:
    def __init__(
        self,
        dp_basedir=None,
        uninstall_locat=None,
        success_dir=None,
        fail_dir=None,
        join_dir_max=6
    ):
        """初始化子模组卸载器
        Args:
            dp_basedir: 游戏基础目录
            uninstall_locat: 卸载任务目录（ToUninstallSubmods）
            success_dir: 成功卸载目录
            fail_dir: 失败卸载目录
            join_dir_max: 最大目录深度
        """
        # 配置参数
        self.dp_basedir = dp_basedir or self._get_default_basedir()
        self.uninstall_locat = uninstall_locat or os.path.join(self.dp_basedir, "ToUninstallSubmods")
        self.success_dir = success_dir or os.path.join(self.uninstall_locat, "Uninstall Success")
        self.fail_dir = fail_dir or os.path.join(self.uninstall_locat, "Uninstall Failed")
        self.JOIN_DIR_MAX = join_dir_max
        
        # 进度跟踪状态
        self.current_stage = "初始化"
        self.current_file = ""
        self.total_files = 0
        self.processed_files = 0
        self.current_zip = None
        self.total_zips = 0
        self.processed_zips = 0
        self.logger = simplelogger()
        
        # 错误信息
        self.DECOMPRESSING_FAIL = "解压zip文件时出现错误."
        self.ZIP_INCORRECT = "zip文件不正确，这可能意味着这个zip文件并没有根据游戏文件目录来压缩."
        self.PROTECTED_DIR_WARNING = "检测到受保护目录，为安全起见已跳过删除操作."
        self.PATH_VALIDATION_FAIL = "路径验证失败，操作被拒绝."
        
        # 受保护的目录列表（绝对不允许删除）
        self.PROTECTED_DIRS = {
            'python-packages',  # 绝对不允许删除
            'renpy',           # Ren'Py核心文件
            'lib',             # 系统库文件 
            'log'              # 日志文件夹
        }
        
        # 卸载完成标记
        self._uninstall_completed = False
        
        # 确保目录存在
        os.makedirs(self.uninstall_locat, exist_ok=True)
        os.makedirs(self.success_dir, exist_ok=True)
        os.makedirs(self.fail_dir, exist_ok=True)
    
    def _get_default_basedir(self):
        """获取默认的基础目录"""
        if renpy.android:
            return "/storage/emulated/0/Android/data/and.kns.masmobile/files"
        return renpy.config.basedir
    
    def _validate_path(self, path):
        """验证路径安全性
        Args:
            path: 待验证的路径
        Returns:
            bool: 路径是否安全
        """
        try:
            # 获取绝对路径
            abs_path = os.path.abspath(path)
            abs_basedir = os.path.abspath(self.dp_basedir)
            
            # 检查路径是否在游戏目录范围内
            if not abs_path.startswith(abs_basedir):
                self.logger.error(f"路径超出游戏目录范围: '{abs_path}'")
                return False
            
            # 检查是否为受保护目录
            path_parts = abs_path.replace(abs_basedir, '').strip(os.sep).split(os.sep)
            
            for protected_dir in self.PROTECTED_DIRS:
                if protected_dir in path_parts:
                    self.logger.error(f"尝试访问受保护目录: '{protected_dir}' in '{abs_path}'")
                    return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"路径验证出错: '{e}'")
            return False
    
    def get_zip_files(self):
        """获取待卸载的ZIP文件列表"""
        self._update_stage("扫描卸载ZIP文件")
        zip_files = []
        
        if not os.path.exists(self.uninstall_locat):
            self.logger.warning(f"卸载目录不存在: '{self.uninstall_locat}'")
            return zip_files
        
        for file_name in os.listdir(self.uninstall_locat):
            if file_name.endswith('.zip'):
                zip_files.append(file_name)
        
        self.total_zips = len(zip_files)
        self.processed_zips = 0
        return zip_files
    
    def process_zip(self, file_name):
        """处理单个卸载ZIP文件
        Args:
            file_name: ZIP文件名
        Returns:
            bool: 卸载是否成功
        """
        self.current_zip = file_name
        self.processed_zips += 1
        self._uninstall_completed = False
        
        file_path = os.path.join(self.uninstall_locat, file_name)
        extracted_dir = f"{file_path}_files"
        
        # 跳过特殊文件
        if 'OldVersionFiles' in file_name:
            self._update_stage("跳过特殊文件", file_name)
            self._move_files(file_path, False, file_name)
            self.logger.error(f"不支持处理特殊文件: '{file_name}'\n")
            return False
        
        # 解压文件以分析结构
        self._update_stage("解压文件", file_name)
        if not self._unzip(file_path, extracted_dir):
            self._move_files(file_path, False, file_name)
            self.logger.error(f"{self.DECOMPRESSING_FAIL}\n处理出错的文件: '{file_path}'\n")
            return False
        
        # 统计文件总数
        self._update_stage("统计文件", file_name)
        self.total_files = self._count_files(extracted_dir)
        self.processed_files = 0
        
        # 处理卸载操作
        self._update_stage("卸载文件", file_name)
        success = self._process_uninstall_directory(extracted_dir, 1)
        
        # 清理解压的临时目录
        if os.path.exists(extracted_dir):
            try:
                shutil.rmtree(extracted_dir)
            except Exception as e:
                self.logger.error(f"清理临时目录失败: {e}")
        
        # 处理结果
        if not self._uninstall_completed:
            self._move_files(file_path, False, file_name)
            self.logger.error(f"这个mod可能没有正确卸载: '{file_path}'")
            success = False
        else:
            self._move_files(file_path, True, file_name)
        
        self.logger.info(f"卸载zip文件完成：'{file_path}'\n")
        
        # 重置文件计数
        self.total_files = 0
        self.processed_files = 0
        self.current_zip = None
        
        return success
    
    def get_progress(self):
        """获取当前进度信息"""
        progress = {
            "stage": self.current_stage,
            "current_file": self.current_file,
            "current_zip": self.current_zip,
            "total_files": self.total_files,
            "processed_files": self.processed_files,
            "progress_percent": 0,
            "total_zips": self.total_zips,
            "processed_zips": self.processed_zips,
            "zip_progress_percent": 0
        }
        
        # 计算文件进度百分比
        if self.total_files > 0:
            progress["progress_percent"] = int((self.processed_files / self.total_files) * 100)
        
        # 计算ZIP文件进度百分比
        if self.total_zips > 0:
            progress["zip_progress_percent"] = int((self.processed_zips / self.total_zips) * 100)
        
        return progress
    
    def _update_stage(self, stage, current_file=""):
        """更新当前处理阶段和文件"""
        self.current_stage = stage
        self.current_file = current_file
    
    def _count_files(self, directory):
        """递归统计目录中的文件总数"""
        count = 0
        for root, dirs, files in os.walk(directory):
            count += len(files)
        return count
    
    def _process_uninstall_directory(self, directory, depth):
        """递归处理卸载目录
        Args:
            directory: 要处理的目录
            depth: 当前递归深度
        Returns:
            bool: 处理是否成功
        """
        if depth > self.JOIN_DIR_MAX:
            self.logger.warning(f"达到最大深度 {self.JOIN_DIR_MAX}，停止处理: '{directory}'")
            return True
        
        success = True
        entries = os.listdir(directory)
        
        for entry in entries:
            self.processed_files += 1
            entry_path = os.path.join(directory, entry)
            self._update_stage("处理卸载文件", entry_path)
            
            if not self._uninstall_dir_or_file(entry, entry_path):
                if os.path.isdir(entry_path) and depth < self.JOIN_DIR_MAX:
                    self.logger.info(f"{depth} - 进入文件夹处理内部文件: '{entry_path}'")
                    if not self._process_uninstall_directory(entry_path, depth + 1):
                        success = False
                else:
                    self.logger.info(f"不是文件夹或达到最大深度: '{entry_path}'")
                    success = False
        
        return success
    
    def _uninstall_dir_or_file(self, name, path):
        """卸载目录或文件
        Args:
            name: 文件或目录名
            path: 源路径（ZIP中的路径）
        Returns:
            bool: 卸载是否成功
        """
        self.logger.info(f"准备卸载: '{name}'")
        
        # 特殊目录映射
        special_dirs = {
            'game': os.path.join(self.dp_basedir, "game"),
            'lib': os.path.join(self.dp_basedir, "lib"),
            'log': os.path.join(self.dp_basedir, "log"),
            'piano_songs': os.path.join(self.dp_basedir, "piano_songs"),
            'custom_bgm': os.path.join(self.dp_basedir, "custom_bgm"),
            'Submods': os.path.join(self.dp_basedir, "game", "Submods"),
            'mod_assets': os.path.join(self.dp_basedir, "game", "mod_assets"),
            'gui': os.path.join(self.dp_basedir, "game", "gui")
        }
        
        # 忽略的目录
        ignored_dirs = ['characters', 'gift', 'gifts']
        
        # 检查受保护目录
        if name in self.PROTECTED_DIRS:
            self.logger.error(f"{self.PROTECTED_DIR_WARNING} 受保护目录: '{name}'")
            return False
        
        if name in special_dirs:
            target_path = special_dirs[name]
            return self._uninstall_specific_files(path, target_path)
            
        elif name in ignored_dirs:
            self.logger.info(f"忽略该文件夹: '{name}'")
            return True
            
        # 处理脚本文件
        elif os.path.isfile(path) and (name.endswith('.rpy') or name.endswith('.rpym')):
            ungroup_dir = os.path.join(self.dp_basedir, "game", "Submods", "UnGroupScripts")
            target_file = os.path.join(ungroup_dir, name)
            
            if os.path.exists(target_file):
                return self._remove_file(target_file)
            else:
                self.logger.warning(f"要卸载的脚本文件不存在: '{target_file}'")
                return True
            
        self.logger.info(f"不符合常规子模组结构: '{path}'")
        return False
    
    def _uninstall_specific_files(self, src_path, target_base_path):
        """卸载特定文件或目录
        Args:
            src_path: 源路径（ZIP中的路径结构）
            target_base_path: 目标基础路径
        Returns:
            bool: 卸载是否成功
        """
        self.logger.info(f"开始卸载: '{src_path}' 从目标: '{target_base_path}'")
        
        if not self._validate_path(target_base_path):
            self.logger.error(f"{self.PATH_VALIDATION_FAIL} 目标路径: '{target_base_path}'")
            return False
        
        success = True
        
        try:
            if os.path.isdir(src_path):
                # 递归处理目录中的所有文件
                for root, dirs, files in os.walk(src_path):
                    # 计算相对路径
                    rel_path = os.path.relpath(root, src_path)
                    
                    # 处理文件
                    for file_name in files:
                        src_file = os.path.join(root, file_name)
                        
                        if rel_path == '.':
                            target_file = os.path.join(target_base_path, file_name)
                        else:
                            target_file = os.path.join(target_base_path, rel_path, file_name)
                        
                        if not self._remove_file(target_file):
                            success = False
                
                # 清理空目录
                self._cleanup_empty_directories(target_base_path)
                
            else:
                # 单个文件
                file_name = os.path.basename(src_path)
                target_file = os.path.join(target_base_path, file_name)
                success = self._remove_file(target_file)
            
            if success:
                self._uninstall_completed = True
                
        except Exception as e:
            self.logger.error(f"卸载过程出错: '{e}'")
            success = False
        
        return success
    
    def _remove_file(self, file_path):
        """安全删除文件
        Args:
            file_path: 要删除的文件路径
        Returns:
            bool: 删除是否成功
        """
        # 路径安全验证
        if not self._validate_path(file_path):
            self.logger.error(f"{self.PATH_VALIDATION_FAIL} 文件路径: '{file_path}'")
            return False
        
        try:
            if os.path.exists(file_path):
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    self.logger.info(f"已删除文件: '{file_path}'")
                elif os.path.isdir(file_path):
                    # 只删除空目录
                    try:
                        os.rmdir(file_path)
                        self.logger.info(f"已删除空目录: '{file_path}'")
                    except OSError:
                        self.logger.info(f"目录非空，跳过删除: '{file_path}'")
                return True
            else:
                self.logger.warning(f"要删除的文件不存在: '{file_path}'")
                return True
                
        except Exception as e:
            self.logger.error(f"删除文件失败: '{file_path}' - {e}")
            return False
    
    def _cleanup_empty_directories(self, base_path):
        """清理空目录
        Args:
            base_path: 基础路径
        """
        if not self._validate_path(base_path):
            return
        
        try:
            for root, dirs, files in os.walk(base_path, topdown=False):
                for dir_name in dirs:
                    dir_path = os.path.join(root, dir_name)
                    
                    # 验证路径安全性
                    if not self._validate_path(dir_path):
                        continue
                    
                    try:
                        # 尝试删除空目录
                        if not os.listdir(dir_path):
                            os.rmdir(dir_path)
                            self.logger.info(f"已清理空目录: '{dir_path}'")
                    except OSError:
                        # 目录不为空或其他原因，跳过
                        pass
                        
        except Exception as e:
            self.logger.error(f"清理空目录时出错: '{e}'")
    
    def _unzip(self, file_path, extracted_dir):
        """解压zip文件并跟踪进度"""
        self._update_stage("解压文件", file_path)
        
        try:
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                # 获取ZIP文件总大小
                total_size = sum(file.file_size for file in zip_ref.infolist())
                extracted_size = 0
                
                # 确保目标目录存在
                os.makedirs(extracted_dir, exist_ok=True)
                
                # 逐个文件解压并更新进度
                for file_info in zip_ref.infolist():
                    # 更新当前处理文件
                    self.current_file = file_info.filename
                    
                    # 解压单个文件
                    zip_ref.extract(file_info, extracted_dir)
                    
                    # 更新已解压大小
                    extracted_size += file_info.file_size
                    
                    # 计算解压进度百分比
                    unzip_percent = (extracted_size / total_size) * 100 if total_size > 0 else 0
                    
                    # 更新解压进度状态
                    self.unzip_progress = {
                        "current_file": file_info.filename,
                        "total_size": total_size,
                        "extracted_size": extracted_size,
                        "progress_percent": unzip_percent
                    }
            
            # 解压完成后重置状态
            self.unzip_progress = None
            return True
            
        except Exception as e:
            self.logger.error(f"解压失败: '{e}'")
            return False
    
    def _move_files(self, file_path, success, file_name):
        """移动文件到成功/失败目录
        Args:
            file_path: 源文件路径
            success: 是否成功
            file_name: 文件名
        Returns:
            bool: 移动是否成功
        """
        target_dir = self.success_dir if success else self.fail_dir
        
        # 清理临时文件
        extracted_dir = f"{file_path}_files"
        if os.path.exists(extracted_dir):
            try:
                shutil.rmtree(extracted_dir)
            except Exception as e:
                self.logger.error(f"清理临时文件失败: {e}")
        
        # 移动原始文件
        try:
            target_path = os.path.join(target_dir, file_name)
            if os.path.exists(target_path):
                os.remove(target_path)
            shutil.move(file_path, target_dir)
            return True
        except Exception as e:
            self.logger.error(f"移动文件失败: {e}")
            return False

# 使用示例
def create_uninstaller_example():
    """创建卸载器使用示例"""
    # 创建卸载器实例
    uninstaller = SubmodUninstaller(
        dp_basedir="E:\MAS_Cn001280\MAS_CN0012F0",  # 可选，使用你的游戏基础目录
        join_dir_max=6  # 可选
    )
    
    # 设置日志记录器（如果可用）
    # uninstaller.logger = store.mas_submod_utils.submod_log
    
    # 获取待卸载ZIP文件列表
    zip_files = uninstaller.get_zip_files()
    print(f"待卸载ZIP文件列表: {zip_files}")
    
    # 处理所有ZIP文件
    for zip_file in zip_files:
        # 获取进度信息并显示
        progress = uninstaller.get_progress()
        print(f"当前阶段: {progress['stage']}, 处理文件: {progress['current_file']}")
        
        # 处理ZIP文件
        success = uninstaller.process_zip(zip_file)
        print(f"卸载{'成功' if success else '失败'}: {zip_file}")

#create_uninstaller_example()

# 实例化卸载器（根据需要调整参数）
#uninstaller = SubmodUninstaller(
#    dp_basedir=ANDROID_MASBASE,  # 可选
#    join_dir_max=6  # 可选
#)
# uninstaller.logger = store.mas_submod_utils.submod_log