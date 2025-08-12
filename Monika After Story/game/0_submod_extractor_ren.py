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
    
    def debug(msg, *args, **kwargs):
        print(f"[DEBUG] {msg}", *args, **kwargs)
    


class SubmodInstaller:
    def __init__(
        self,
        dp_basedir=None,
        submod_locat=None,
        success_dir=None,
        fail_dir=None,
        gift_dir=None,
        join_dir_max=6
    ):
        # 配置参数
        self.dp_basedir = dp_basedir or self._get_default_basedir()
        self.submod_locat = submod_locat or os.path.join(self.dp_basedir, "ToInstallSubmods")
        self.success_dir = success_dir or os.path.join(self.submod_locat, "Install Success")
        self.fail_dir = fail_dir or os.path.join(self.submod_locat, "Install Failed")
        self.gift_dir = gift_dir or os.path.join(self.dp_basedir, "AvailableGift")
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
        self.ZIP_INCORRECT = "zip文件不正确，这可能意味着这个zip文件并没有根据游戏文件目录来压缩，或包含了非标准子模组所需要的文件夹，为防止出错，请手动解压至正确位置."
        self.NO_HELP_UPDATER_ZIP = "不支持由'辅助更新子模组'创建的压缩包"
        
        # 确保目录存在
        os.makedirs(self.submod_locat, exist_ok=True)
        os.makedirs(self.success_dir, exist_ok=True)
        os.makedirs(self.fail_dir, exist_ok=True)
        os.makedirs(self.gift_dir, exist_ok=True)
    
    def _get_default_basedir(self):
        """获取默认的基础目录"""
        if renpy.android:
            return "/storage/emulated/0/Android/data/and.kns.masmobile/files"
        return renpy.config.basedir
    
    def get_zip_files(self):
        """获取待处理的ZIP文件列表"""
        self._update_stage("扫描ZIP文件")
        zip_files = []
        
        for file_name in os.listdir(self.submod_locat):
            if file_name.endswith('.zip'):
                zip_files.append(file_name)
        
        self.total_zips = len(zip_files)
        self.processed_zips = 0
        return zip_files
    
    def process_zip(self, file_name):
        """处理单个ZIP文件"""
        self.current_zip = file_name
        self.processed_zips += 1
        self._install_completed = False
        
        file_path = os.path.join(self.submod_locat, file_name)
        extracted_dir = f"{file_path}_files"
        
        # 跳过特殊文件
        if 'OldVersionFiles' in file_name:
            self._update_stage("跳过特殊文件", file_name)
            self._move_files(file_path, False, file_name)
            self.logger.error(f"{self.NO_HELP_UPDATER_ZIP}\n")
            return False
        
        # 解压文件
        self._update_stage("解压文件", file_name)
        if not self._unzip(file_path, extracted_dir):
            self._move_files(file_path, False, file_name)
            self.logger.error(f"{self.DECOMPRESSING_FAIL}\n处理出错的文件: '{file_path}'\n")
            return False
        
        # 统计文件总数
        self._update_stage("统计文件", file_name)
        self.total_files = self._count_files(extracted_dir)
        self.processed_files = 0
        
        # 处理解压后的文件
        self._update_stage("处理文件", file_name)
        success = self._process_extracted_directory(extracted_dir, 1)
        
        # 处理结果
        if not self._install_completed:
            self._move_files(file_path, False, file_name)
            self.logger.error(f"这个mod可能没有正确安装: '{file_path}'")
            success = False
        else:
            self._move_files(file_path, True, file_name)
        
        self.logger.info(f"安装zip文件完成：'{file_path}'\n")
        
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
    
    def _process_extracted_directory(self, directory, depth):
        """递归处理解压目录"""
        if depth > self.JOIN_DIR_MAX:
            self.logger.warning(f"达到最大深度 {self.JOIN_DIR_MAX}，停止处理: '{directory}'")
            return True
        
        success = True
        entries = os.listdir(directory)
        
        for entry in entries:
            self.processed_files += 1
            entry_path = os.path.join(directory, entry)
            self._update_stage("处理文件", entry_path)
            
            if not self._copy_dir_or_file(entry, entry_path):
                if os.path.isdir(entry_path) and depth < self.JOIN_DIR_MAX:
                    self.logger.info(f"{depth} - 进入文件夹处理内部文件: '{entry_path}'")
                    if not self._process_extracted_directory(entry_path, depth + 1):
                        success = False
                else:
                    self.logger.info(f"不是文件夹或达到最大深度: '{entry_path}'")
                    success = False
        
        return success

    def _copy_dir_or_file(self, name, path):
        """处理目录或文件"""
        self.logger.info(f"准备复制: '{name}'")
        
        # 特殊目录处理
        special_dirs = {
            'game': os.path.join(self.dp_basedir, "game"),
            'lib': os.path.join(self.dp_basedir, "lib"),
            'log': os.path.join(self.dp_basedir, "log"),
            'piano_songs': os.path.join(self.dp_basedir, "piano_songs"),
            'custom_bgm': os.path.join(self.dp_basedir, "custom_bgm"),
            'Submods': os.path.join(self.dp_basedir, "game", "Submods"),
            'mod_assets': os.path.join(self.dp_basedir, "game", "mod_assets"),
            'python-packages': os.path.join(self.dp_basedir, "game", "python-packages"),
            'gui': os.path.join(self.dp_basedir, "game", "gui")
        }
        
        # 忽略的目录
        ignored_dirs = ['characters', 'gift', 'gifts']
        
        if name in special_dirs:
            target_path = special_dirs[name]
            if name == 'mod_assets' or name == 'game':
                self._check_json(os.path.join(path, "mod_assets") if name == 'game' else path)
            return self._copy_dir(path, target_path)
            
        elif name in ignored_dirs:
            self.logger.info(f"忽略该文件夹: '{name}'")
            return True
            
        # 处理脚本文件
        elif os.path.isfile(path) and (name.endswith('.rpy') or name.endswith('.rpym')):
            ungroup_dir = os.path.join(self.dp_basedir, "game", "Submods", "UnGroupScripts")
            os.makedirs(ungroup_dir, exist_ok=True)
            shutil.copy2(path, ungroup_dir)
            self.logger.warning(f"脚本文件复制到 'Submods/UnGroupScripts': {name}")
            return True
            
        self.logger.info(f"不符合常规子模组结构: '{path}'")
        return False

    def _copy_dir(self, src_path, target_path):
        """复制目录"""
        self.logger.info(f"正在复制: '{src_path}' -> '{target_path}'")
        
        if not os.path.exists(src_path):
            self.logger.error(f"源路径不存在: '{src_path}'")
            return False
            
        # 确保目标目录存在
        os.makedirs(target_path, exist_ok=True)
        
        try:
            if os.path.isdir(src_path):
                shutil.copytree(src_path, target_path, dirs_exist_ok=True)
            else:
                shutil.copy2(src_path, target_path)
                
            self._install_completed = True
            return True
        except Exception as e:
            self.logger.error(f"复制失败: '{e}'")
            return False

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
            mas_submod_utils.submod_log.error(f"解压失败: '{e}'")
            return False

    def _move_files(self, file_path, success, file_name):
        """移动文件到成功/失败目录"""
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

    def _check_json(self, mod_assets_path):
        """检查JSON并生成礼物文件"""
        json_dir = os.path.join(mod_assets_path, "monika", "j")
        
        if not os.path.exists(json_dir):
            self.logger.info(f"未找到JSON文件夹: '{json_dir}'")
            return
            
        self._update_stage("处理JSON文件", json_dir)
        
        for json_file in os.listdir(json_dir):
            if not json_file.endswith('.json'):
                continue
                
            json_path = os.path.join(json_dir, json_file)
            self._update_stage("处理JSON", json_file)
            
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                gift_name = data.get('giftname')
                if not gift_name:
                    self.logger.warning(f"JSON文件缺少giftname: '{json_path}'")
                    continue
                    
                group = data.get('select_info', {}).get('group', '')
                
                # 创建礼物文件
                gift_dir = os.path.join(self.gift_dir, group)
                os.makedirs(gift_dir, exist_ok=True)
                
                gift_path = os.path.join(gift_dir, f"{gift_name}.gift")
                with open(gift_path, 'w') as f:
                    pass  # 创建空文件
                    
                self.logger.info(f"生成礼物文件: '{gift_path}'")
            except Exception as e:
                error_msg = f"处理JSON文件出错: '{json_path}' - {str(e)}"
                self.logger.error(error_msg)

## 使用示例
## 创建安装器实例（参数可自定义）
installer = SubmodInstaller(
    dp_basedir=ANDROID_MASBASE,  # 可选
    join_dir_max=6  # 可选
)
installer.logger = store.mas_submod_utils.submod_log
#
## 获取ZIP文件列表
#zip_files = installer.get_zip_files()
##print(f"ZIP文件列表: {zip_files}")
## 处理所有ZIP文件
#for zip_file in zip_files:
#    # 可以在这里获取进度信息并显示
#    progress = installer.get_progress()
#    #print(f"当前阶段: {progress['stage']}, 处理文件: {progress['current_file']}")
#    
#    # 处理ZIP文件
#    installer.process_zip(zip_file)
#
