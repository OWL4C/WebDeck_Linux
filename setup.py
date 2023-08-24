from cx_Freeze import setup, Executable
build_options = {'packages': [], 'excludes': ["cx_Freeze"], "zip_include_packages": "*", "zip_exclude_packages": "_sounddevice_data"}

import sys, os, json, shutil
sys.setrecursionlimit(10000)
base = 'Win32GUI' if sys.platform=='win32' else None
#base = 'console' if sys.platform=='win32' else None

executables = [
    # tray icon
    Executable('main.py', base=base, target_name='WebDeck', icon='static/files/icon.ico'),
    # bishokus.fr/webdeck/start
    #Executable('start_server.py', base=base, target_name='WD_start'),
    # actual code
    Executable('main_server.py', base=base, target_name='WD_main')
]

with open('static/files/version.json', encoding="utf-8") as f:
    version = json.load(f)['actual_version']

setup(name='WebDeck',
    version = version,
    options = {'build_exe': build_options},
    executables = executables)


exclude_folders = ['!buttons', '.git', '.vscode', '__pycache__', 'build', 'webdeck', '%.html%WebDeck']

script_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(script_dir, 'build')

if os.path.exists(build_dir):
    first_folder = next(entry for entry in os.listdir(build_dir) if os.path.isdir(os.path.join(build_dir, entry)))
    target_dir = os.path.join(build_dir, first_folder)
    
    for item in os.listdir(script_dir):
        item_path = os.path.join(script_dir, item)
        if item != target_dir and item not in exclude_folders and item.endswith('.py') == False:
            if os.path.isdir(item_path):
                shutil.copytree(item_path, os.path.join(target_dir, item))
            else:
                shutil.copy2(item_path, target_dir)
            print(f'copying {item_path} -> {target_dir}')


print('build done!')