import os
import zipfile
import yaml

current_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(current_dir, "Assets")
output_dir = os.path.join(current_dir, "Output")

if not os.path.exists(assets_dir):
    os.mkdir(assets_dir)
else:
    print("Assets存在，请将资源包放入Assets文件夹")

if not os.path.exists(output_dir):
    os.mkdir(output_dir)
else:
    print("Output存在")

zip_files = []
for file in os.listdir(assets_dir):
    if file.endswith(".zip"):
        zip_files.append(file)

print("请选择一个 prpr 资源包文件(zip):")
for i, file in enumerate(zip_files):
    print(f"{i+1}: {file}")
print("0: 退出程序")

selected_file = None
while selected_file is None:
    user_input = input("请输入序号: ")
    if user_input == "0":
        exit()
    try:
        selected_index = int(user_input) - 1
        selected_file = zip_files[selected_index]
    except (ValueError, IndexError):
        print("无效输入")

new_folder_name = os.path.splitext(selected_file)[0]
new_folder_path_assets = os.path.join(assets_dir, new_folder_name)
new_folder_path_output = os.path.join(output_dir, new_folder_name)

if not os.path.exists(new_folder_path_assets):
    os.mkdir(new_folder_path_assets)
else:
    print(str(new_folder_name)+"已存在")

if not os.path.exists(new_folder_path_output):
    os.mkdir(new_folder_path_output)
else:
    print(str(new_folder_name)+"已存在")

zip_file_path = os.path.join(assets_dir, selected_file)
with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
    zip_ref.extractall(new_folder_path_assets)

info_file_path = os.path.join(new_folder_path_assets, "info.yml")
with open(info_file_path, "rb") as f:
    info_data = yaml.safe_load(f)

hitFxDuration = info_data.get('hitFxDuration', 0.5)
hitFxScale = info_data.get('hitFxScale', 1.0)
hitFxRotate = info_data.get('hitFxRotate', False)
hideParticles = info_data.get('hideParticles', False)
holdKeepHead = info_data.get('holdKeepHead', False)
holdRepeat = info_data.get('holdRepeat', False)
holdCompact = info_data.get('holdCompact', False)

config_file_path = os.path.join(new_folder_path_output, "config.txt")
with open(config_file_path, "w") as f:
    f.write(f"packageName: \"{info_data['name']}\";\n")
    f.write(f"author: \"{info_data['author']}\";\n")
    f.write("isFrameSequence: false;\n")
    f.write(f"hitFx: {info_data['hitFx']};\n")
    f.write(f"hitFxDuration: {hitFxDuration};\n")
    f.write(f"hitFxScale: {hitFxScale};\n")
    f.write(f"holdAtlas: {info_data['holdAtlas']};\n")
    f.write(f"holdAtlasHL: {info_data['holdAtlasMH']};\n")
    f.write(f"hitFxRotate: {hitFxRotate};\n")
    f.write(f"hideParticles: {hideParticles};\n")
    f.write(f"holdKeepHead: {holdKeepHead};\n")
    f.write(f"holdRepeat: {holdRepeat};\n")
    f.write(f"holdCompact: {holdCompact};\n")

notes_folder_path = os.path.join(new_folder_path_output, "notes")
if not os.path.exists(notes_folder_path):
    os.mkdir(notes_folder_path)

sounds_folder_path = os.path.join(new_folder_path_output, "sounds")
if not os.path.exists(sounds_folder_path):
    os.mkdir(sounds_folder_path)

for filename in os.listdir(new_folder_path_assets):
    file_path = os.path.join(new_folder_path_assets, filename)
    if os.path.isfile(file_path):
        if filename in ['click.png', 'click_mh.png', 'drag.png', 'drag_mh.png', 'flick.png', 'flick_mh.png', 'hold.png', 'hold_mh.png']:
            new_filename = filename.replace('click', 'Tap').replace('drag', 'Drag').replace('flick', 'Flick').replace('hold', 'Hold')
            if '_mh.' in new_filename:
                new_filename = new_filename.replace('_mh', 'HL')
            new_file_path = os.path.join(notes_folder_path, new_filename)
        elif filename in ['click.ogg', 'drag.ogg', 'flick.ogg']:
            new_filename = filename.replace('click', 'Tap').replace('drag', 'Drag').replace('flick', 'Flick')
            new_file_path = os.path.join(sounds_folder_path, new_filename)
        elif filename == 'hold.ogg':
            new_file_path = os.path.join(sounds_folder_path, 'Hold.ogg')
        elif filename == 'ending.mp3':
            new_file_path = os.path.join(sounds_folder_path, filename)
        elif filename == 'hit_fx.png':
            new_file_path = os.path.join(new_folder_path_output, filename)
        else:
            new_file_path = os.path.join(new_folder_path_output, filename)
        os.rename(file_path, new_file_path)

zip_file_path = os.path.join(output_dir, new_folder_name + ".pap")
with zipfile.ZipFile(zip_file_path, "w", zipfile.ZIP_DEFLATED) as zip_file:
    for folder_name, subfolders, filenames in os.walk(new_folder_path_output):
        for filename in filenames:
            file_path = os.path.join(folder_name, filename)
            zip_file.write(file_path, os.path.relpath(file_path, output_dir), zipfile.ZIP_DEFLATED)
            
print(str(new_folder_name)+"处理完成")