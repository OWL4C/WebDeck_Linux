import os
import sys
import json
import shutil
from win32com.client import Dispatch

from app.updater import check_files
from app.functions.load_lang_file import load_lang_file
from app.functions.plugins.load_plugins import load_plugins

from app.on_start.on_start import *


def on_start():
    if not os.path.exists("config.json"):
        # Create config.json
        shutil.copy("config_default.json", "config.json")
        
        if os.name == 'nt':
            
            # Set DLLs directory
            os.add_dll_directory(os.getcwd())
    
            # Add windows shortcut
            file_path = (
                os.getenv("APPDATA") + r"\Microsoft\Windows\Start Menu\Programs\WebDeck.lnk"
            )
            if not os.path.exists(file_path) and getattr(sys, "frozen", False):
                dir = os.getenv("APPDATA") + r"\Microsoft\Windows\Start Menu\Programs"
                name = "WebDeck.lnk"
                path = os.path.join(dir, name)
                target = os.getcwd() + r"\\WebDeck.exe"
                working_dir = os.getcwd()
                icon = os.getcwd() + r"\\WebDeck.exe"

                shell = Dispatch("WScript.Shell")
                shortcut = shell.CreateShortCut(path)
                shortcut.Targetpath = target
                shortcut.WorkingDirectory = working_dir
                shortcut.IconLocation = icon
                shortcut.save()
                
    # Create uploaded dir if needed
    if not os.path.exists("static/files/uploaded"):
        try:
            os.makedirs("static/files/uploaded")
        except FileExistsError:
            pass

    # Update new files
    check_files("static/files/version.json", "data.json")

    # Load config
    with open("config.json", encoding="utf-8") as f:
        config = json.load(f)
    
    # Load text
    text = load_lang_file(config["settings"]["language"])
    
    # Load commands
    with open("commands.json", encoding="utf-8") as f:
        commands = json.load(f)
        commands = load_plugins(commands)
    
    # Colors json
    sort_colorsjson()
    
    # Nircmd
    if not os.path.isfile("nircmd.exe"):
        download_nircmd()
    
    # Config updater
    config = check_json_update(config)
    with open("config.json", "w", encoding="utf-8") as json_file:
        json.dump(config, json_file, indent=4)
    
    return config, text, commands