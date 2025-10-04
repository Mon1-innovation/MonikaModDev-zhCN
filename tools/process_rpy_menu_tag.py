import os
import sys
import re, logging

# 全局变量，用于追踪当前处理状态
current_indent = 0
is_menu_block = False
menu_choices = []
current_label = ""
label_tag_count = {}
processed_choices = []

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        #logging.FileHandler('translation_parser.log', mode='w', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def read_existing_translations(translation_dir):
    """读取已有翻译"""
    translations = {}
    for root, _, files in os.walk(translation_dir):
        for file in files:
            if file.endswith(('.rpy', '.rpym')):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # 匹配 translate chinese strings 块
                    pattern_block = re.compile(
                        r'translate\s+chinese\s+strings:\n\n(.*?)(?=\ntranslate|\Z)',
                        re.DOTALL
                    )
                    # 匹配 old-new 翻译
                    pattern_string = re.compile(
                        r'old\s*"((?:\\"|[^"])*?)"\n\s*new\s*"((?:\\"|[^"])*?)"',
                        re.MULTILINE | re.DOTALL
                    )

                    blocks = pattern_block.findall(content)
                    # 也可以匹配单独 old-new
                    blocks.extend(pattern_string.findall(content))

                    for block in blocks:
                        block_str = block[0] if isinstance(block, tuple) else block
                        for match in pattern_string.finditer(block_str):
                            source_file = os.path.basename(file_path)
                            source = match.group(1)
                            translation = match.group(2)
                            source = source.replace('\\"', '"')
                            translation = translation.replace('\\"', '"')

                            if source not in translations:
                                translations[source] = []
                            if not any(t['translation'] == translation for t in translations[source]):
                                translations[source].append({
                                    'translation': translation,
                                    'source_file': source_file
                                })
                                logging.debug(f"Parsed translation: '{source}' -> '{translation}' (from {source_file})")
                except Exception as e:
                    logging.error(f"Error parsing file {file_path}: {e}")
    logging.info(f"Total unique source strings: {len(translations)}")
    return translations

existing_translations = read_existing_translations(r"E:\GithubKu\MAS_Chinese_TlScripts\game\tl\chinese")
def generate_tag(label):
    if label in label_tag_count:
        label_tag_count[label] += 1
    else:
        label_tag_count[label] = 1
    return "{#" + f"{label}_{label_tag_count[label]}" + "}"
def extract_choice_text(line: str) -> str:
    """
    从 menu 选项行里提取纯文本部分
    处理包含表达式的选择项，确保仅选择第一个字符串
    例如:
    '    "No.":' -> 'No.'
    '    "Okay. {#some_label}" :' -> 'Okay. {#some_label}'
    '    "choice" if variable else "alternative":' -> 'choice'
    '    ("choice 1", "choice 2")' -> 'choice 1'
    """
    stripped = line.strip()
    if not stripped.endswith(":"):
        return None
    if stripped[0] not in ("'", '"'):
        return None
    # 去掉结尾的冒号和多余空格
    if stripped.endswith(":"):
        stripped = stripped[:-1].rstrip()

    # 处理元组或者表达式中的多个字符串选项
    # 优先匹配字符串字面量
    string_matches = re.findall(r'"([^"]*)"', stripped)
    if string_matches:
        # 返回第一个找到的字符串
        return string_matches[0].strip()

    # 如果没有匹配到字符串，尝试原有的匹配方式
    match = re.match(r'^"?\s*"(.*)"\s*$', stripped)
    if match:
        return match.group(1).strip()
    else:
        # 如果意外没匹配到
        #print(line + "not match")
        return None

def get_indent(line):
    """
    获取行的缩进级别

    Args:
        line (str): 要检查缩进的行

    Returns:
        int: 行的缩进空格数
    """
    match = re.match(r'^(\s*)', line)
    return len(match.group(1)) if match else 0

def is_menu_start(line):
    """
    判断是否为menu开始行

    Args:
        line (str): 要检查的行

    Returns:
        bool: 是否是menu开始
    """
    return line.strip().startswith('menu') and ':' in line

def is_choice_line(line):
    """
    判断是否为选择项行

    Args:
        line (str): 要检查的行

    Returns:
        bool: 是否是选择项
    """
    stripped_line = line.strip()
    return extract_choice_text(stripped_line)
    #return stripped_line and not stripped_line.startswith('#') and \
    #       not stripped_line.startswith('menu') and \
    #       stripped_line.endswith(':')

def is_label_start(line):
    """
    判断是否为label开始行

    Args:
        line (str): 要检查的行

    Returns:
        str or None: label名称，如果是label行；否则返回None
    """
    label_match = re.match(r'^label\s+(\w+):', line.strip())
    return label_match.group(1) if label_match else None

def process_rpy_file(file_path):
    """
    处理单个.rpy文件：在menu选项中补充缺失的{#tag}
    """
    def add_tag_str(string, tag):
        return string + tag
    global current_label
    current_label = ""  # 重置当前label

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        new_lines = []
        is_menu_block = False
        current_indent = 0

        for line_number, line in enumerate(lines, 1):
            raw_line = line.rstrip("\n")  # 去掉换行但保留原缩进
            line_out = raw_line

            # 检测label开始
            label_name = is_label_start(raw_line)
            if label_name:
                current_label = label_name

            # 检测menu开始
            if is_menu_start(raw_line):
                is_menu_block = True
                current_indent = get_indent(raw_line)
                new_lines.append(raw_line)
                continue

            # 在menu块里处理choice
            if is_menu_block and is_choice_line(raw_line):
                choice_indent = get_indent(raw_line)

                if choice_indent > current_indent:
                    choice_text = extract_choice_text(raw_line)

                    if choice_text and "{#" not in raw_line:
                        default = [{"translation": ''}]

                        # 生成tag并插入
                        tag = generate_tag(current_label)
                        
                        line_out = raw_line.replace(choice_text, add_tag_str(choice_text, tag))

                        processed_choices.append({
                            'original_text': choice_text,
                            'processed_text': extract_choice_text(line_out), 
                            "tl_text": existing_translations.get(choice_text, default)[0]["translation"],
                            'position': "# {}:{} @ {}".format(current_label, line_number, os.path.basename(file_path)),
                        })

            
            # 检测menu结束（缩进回退）
            if is_menu_block and get_indent(raw_line) <= current_indent and raw_line.strip():
                is_menu_block = False
                current_indent = 0

            new_lines.append(line_out)

        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write("\n".join(new_lines) + "\n")

        print(f"Processed file: {file_path}")

    except Exception as e:
        raise
        print(f"Error processing {file_path}: {e}")

def process_directory(directory):
    """
    处理目录下的所有.rpy文件，排除tl文件夹

    Args:
        directory (str): 根目录
    """
    for root, dirs, files in os.walk(directory):
        # 排除tl文件夹
        if 'tl' in dirs:
            dirs.remove('tl')

        for file in files:
            if file.endswith('.rpy'):
                file_path = os.path.join(root, file)
                process_rpy_file(file_path)

def write_translation(file):
    with open(file, 'w', encoding='utf-8') as f:
        f.write("translate chinese string:\n")
        for item in processed_choices:
            f.write(f"    {item['position']}\n")
            f.write(f"    old \"{item['processed_text']}\"\n")
            f.write(f"    new \"{item['tl_text']}\"\n\n")

def main():
    root_dir = r'J:\MAS\MonikaModDev-PC\Monika After Story'
    process_directory(root_dir)
    write_translation(os.path.join(r'J:\MAS\MonikaModDev-PC\Monika After Story\game\generated_menu_text.rpy'))
    

if __name__ == '__main__':
    main()