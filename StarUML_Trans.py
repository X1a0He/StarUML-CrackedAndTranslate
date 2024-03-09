import json
import os
import re

def decompressAsar():
    os.system("asar extract app.asar app")

def pack2asar():
    os.system("asar pack app app.asar")

def load_replacements(file_path, direction):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    replacements = { }
    keys = ('strings', 'label', 'text', 'description')
    for key in keys:
        if key in data:
            if direction == 1:  # 汉化
                replacements.update({ item['en']: item['cn'] for item in data[key] })
            else:  # 还原
                replacements.update({ item['cn']: item['en'] for item in data[key] })
    return replacements

def replace_keys(obj, replacements, key_to_replace):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == key_to_replace and value in replacements:
                obj[key] = replacements[value]
                # print(f"替换 {obj[key]} -> {replacements[value]}")
            elif isinstance(value, (dict, list)):
                replace_keys(value, replacements, key_to_replace)
    elif isinstance(obj, list):
        for item in obj:
            replace_keys(item, replacements, key_to_replace)

def update_files(files_path, replacements):
    for file_info in files_path:
        for directory in file_info['path']:
            for key_to_replace in file_info['key_to_replace']:
                for root, dirs, files in os.walk(directory):
                    for file_name in files:
                        if file_name.endswith(file_info['file_pattern']):
                            file_path = os.path.join(root, file_name)
                            print(f"正在替换文件: {file_path} 的 {key_to_replace} 字段")
                            with open(file_path, 'r', encoding='utf-8') as file:
                                if file_path.endswith('.json'):
                                    data = json.load(file)
                                    replace_keys(data, replacements, key_to_replace)
                                    with open(file_path, 'w', encoding='utf-8') as file:
                                        json.dump(data, file, indent=4, ensure_ascii=False)
                                elif file_path.endswith('.js'):
                                    data = file.read()
                                    data = data.replace(r"\u2026", "...")
                                    data = data.replace(r"\"dev\"", "dev")
                                    matches = re.findall(r': \"(.*?)\"', data)
                                    for match in matches:
                                        if match in replacements:
                                            data = data.replace(f": \"{match}\"", f": \"{replacements[match]}\"")
                                            # print(f"替换 {match} -> {replacements[match]}")
                                    with open(file_path, 'w', encoding='utf-8') as file:
                                        file.write(data)

def main():
    # 用户选择
    user_choice = int(input("1 -> 汉化\n2 -> 还原\n请输入您的选择: \n"))
    if user_choice == 2:
        print("由于我不知道还原会不会有问题，虽然代码里面是支持的，但是我还是不建议")
        print("那既然你都跑代码了，如果你要还原，你自己注释这里")
        exit(1)

    if not os.path.exists("app"):
        print("正在解包app.asar")
        decompressAsar()

    # 加载汉化文件
    replacements = load_replacements('StarUML_Language.json', user_choice)

    files_path = [
        {
            'path': [
                'app/resources/default/menus/',
                'app/extensions/essential/uml/menus/',
                'app/extensions/essential/aws/menus',
                'app/extensions/essential/bpmn/menus/',
                'app/extensions/essential/c4/menus/',
                'app/extensions/essential/gcp/menus/',
                'app/extensions/essential/erd/menus/',
                'app/extensions/essential/wireframe/menus/',
                'app/extensions/default/staruml-v1/menus/',
                'app/extensions/default/html-export/menus/',
                'app/extensions/essential/sysml/menus/',
                'app/extensions/default/alignment/menus/',
                'app/extensions/default/diagram-layout/menus/',
                'app/extensions/essential/mindmap/menus/',
                'app/extensions/essential/flowchart/menus/',
                'app/extensions/default/find/menus/',
                'app/extensions/default/diagram-generator/menus/',
                'app/extensions/default/minimap/menus/',
                'app/extensions/default/diagram-thumbnails/menus/',
                'app/extensions/default/relationship-view/menus/',
                'app/extensions/default/markdown/menus/',
                'app/extensions/default/debug/menus/',
                'app/extensions/essential/dfd/menus/',
                'app/extensions/essential/c4/toolbox/',
                'app/extensions/essential/bpmn/preferences/',
                'app/extensions/essential/uml/toolbox/',
                'app/extensions/essential/common/toolbox',
                'app/extensions/default/robustness/toolbox/'
            ],
            'file_pattern': '.json',
            'key_to_replace': ['label']
        },
        {
            'path': [
                'app/resources/default/preferences/',
                'app/extensions/essential/aws/preferences/',
                'app/extensions/essential/bpmn/preferences/',
                'app/extensions/essential/c4/preferences/',
                'app/extensions/essential/dfd/preferences/',
                'app/extensions/essential/erd/preferences/',
                'app/extensions/essential/flowchart/preferences/',
                'app/extensions/essential/gcp/preferences/',
                'app/extensions/essential/mindmap/preferences/',
                'app/extensions/essential/sysml/preferences/',
                'app/extensions/essential/uml/preferences/',
            ],
            'file_pattern': '.json',
            'key_to_replace': ['text', 'description', 'name']
        },
        {
            'path': [
                'app/src/'
            ],
            'file_pattern': 'strings.js',
            'key_to_replace': ['strings']
        }
    ]
    update_files(files_path, replacements)

if __name__ == "__main__":
    main()
