import json, os, re, glob

def decompressAsar(base):
    os.system(f"cd {base} && asar extract app.asar app")

def pack2asar(base):
    os.system(f"cd {base} && asar pack app app.asar")

def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# 获取文件列表
def get_file_list(base, path_pattern):
    base_path = f"{base}/app/"
    if '*' in path_pattern:
        full_path = os.path.join(base_path, path_pattern)
        return glob.glob(full_path)
    else:
        return [os.path.join(base_path, path_pattern)]

# 字符串替换
def replace_in_file(file_path, replacements, option):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    print(f"正在替换文件: {file_path}")
    content = content.replace(r"\u2026", "...").replace(r"\"dev\"", "dev")
    for replacement in replacements:
        for key, value in replacement.items():
            if isinstance(value, list):  # 处理嵌套列表
                for item in value:
                    en_text = item['en']
                    cn_text = item['cn']
                    print(f"正在替换 {en_text} -> {cn_text}")
                    if option == 1:  # 汉化
                        content = re.sub(f'"{key}": "{re.escape(en_text)}"', f'"{key}": "{re.escape(cn_text)}"'.replace('\\', ''), content)
                    elif option == 2:  # 还原
                        content = re.sub(f'"{key}": "{re.escape(cn_text)}"'.replace('\\', ''), f'"{key}": "{re.escape(en_text)}"', content)
            else:
                en_text = replacement['en']
                cn_text = replacement['cn']
                print(f"正在替换 {en_text} -> {cn_text}")
                if option == 1:  # 汉化
                    content = content.replace(en_text, cn_text)
                elif option == 2:  # 还原
                    content = content.replace(cn_text, en_text)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def handleASAR(language_file, base, user_choice):
    # 先对app.asar进行备份，备份文件名为app_backup.asar
    print("备份 app.asar -> app_backup.asar")
    os.system(f"cp -f {base}/app.asar {base}/app_backup.asar")
    # 备份完就对app.asar进行解包操作，这里他妈的app.asar都存在了，还你妈node解包出错的话，你不是傻逼谁是傻逼
    print("解包 app.asar")
    decompressAsar(base)
    # 解包完就开始对文件进行汉化操作
    data = read_json(language_file)
    for path, replacements in data.items():
        files = get_file_list(base, path)
        for file_path in files:
            replace_in_file(file_path, replacements, user_choice)
    # 汉化操作完成后，对app.asar进行打包操作，并删除app文件夹
    print("打包 app.asar")
    pack2asar(base)
    print("删除 app 文件夹")
    os.system(f"rm -rf {base}/app")
    print("StarUML 汉化操作完成")

def main():
    # 用户选择
    print("__  ___        ___  _   _")
    print("\\ \\/ / | __ _ / _ \\| | | | ___")
    print(" \\  /| |/ _` | | | | |_| |/ _ \\")
    print(" /\\/\\| | (_| | |_| |  _  | ___/")
    print("/_/\\_\\_|\\__,_|\\___/|_| |_|\\___|")
    user_choice = int(input("\n1 -> 汉化\n2 -> 还原\n请输入您的选择: \n"))

    if user_choice == 2:
        print("由于我不知道还原会不会有问题，虽然代码里面是支持的，但是我还是不建议")
        print("那既然你都跑代码了，如果你要还原，你自己注释这里")
        exit(1)
    """
        X1a0He留
        其实StarUML的运行机制是可以不需要app.asar文件的，如果只存在app文件夹，没有app.asar文件也可以启动运行，优先级如下
        1. app.asar
        2. app
        我反正是不喜欢app.asar的，我测试都是只留app文件夹的，所以程序处理会有三种情况，处理优先级也是按照下面的顺序来处理的
        1. 仅存在app.asar，则程序默认处理app.asar，处理完app.asar后，会将解包后的app文件夹删除
        2. app.asar和app文件夹共存，因优先级的原因，StarUML启动会依赖app.asar，所以二者共存时候，程序会默认优先处理app.asar
        3. 不存在app.asar，只存在app文件夹，则程序默认处理app文件夹，但并不会对app文件夹进行打包
    """
    # Windows下没测试过，把这个base换成Windows下的resources路径即可
    base = "/Applications/StarUML.app/Contents/Resources"
    language_file = "StarUML_Language.json"
    # 1. 仅存在app.asar，只处理app.asar
    if os.path.exists(f"{base}/app.asar") and not os.path.exists(f"{base}/app"):
        handleASAR(language_file, base, user_choice)
    # 2. app.asar和app文件夹共存，优先处理app.asar
    elif os.path.exists(f"{base}/app.asar") and os.path.exists(f"{base}/app"):
        print("检测到 app.asar 和 app 文件夹共存，优先处理 app.asar")
        handleASAR(language_file, base, user_choice)
    # 3. 不存在app.asar，只存在app文件夹，则只处理app文件夹
    elif not os.path.exists(f"{base}/app.asar") and os.path.exists(f"{base}/app"):
        print("检测到只存在 app 文件夹，本次操作仅对 app 文件夹进行处理")
        data = read_json(language_file)
        for path, replacements in data.items():
            files = get_file_list(base, path)
            for file_path in files:
                replace_in_file(file_path, replacements, user_choice)
        print("StarUML 汉化操作完成")

if __name__ == "__main__":
    main()
