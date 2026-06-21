#!/usr/bin/env python3

import os
import shutil
import sys
import requests
from pathlib import Path

def check_folder_exists(path, folder_name, required=True):
    folder_path = os.path.join(path, folder_name)
    if os.path.isdir(folder_path):
        print(f"Found {folder_name} folder")
        return folder_path
    else:
        if required:
            print(f"Stop! {folder_name} folder not found")
            sys.exit(1)
        else:
            return None

def check_folder_not_exists(path, folder_name):
    folder_path = os.path.join(path, folder_name)
    if os.path.isdir(folder_path):
        print(f"Stop! {folder_name} folder exists (should not)")
        sys.exit(1)
    else:
        print(f"{folder_name} folder doesn't exist (good)")

def download_and_replace(folder_path, filename, github_url):
    file_path = os.path.join(folder_path, filename)
    
    if os.path.exists(file_path):
        print(f"  Deleting existing {filename}")
        os.remove(file_path)
    
    try:
        print(f"  Downloading {filename}")
        response = requests.get(github_url, timeout=10)
        response.raise_for_status()
        
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print(f"  Downloaded '{filename}'")
    except Exception as e:
        print(f"  Failed to download '{filename}': {e}")
        sys.exit(1)

def main():
    response = requests.get("https://raw.githubusercontent.com/SamtendoNetwork/ElectrodeUpdater/refs/heads/main/ver", timeout=10)
    response.raise_for_status()

    if response.text.strip() != "0.0.6":
        print("ElectrodeUpdater is outdated (ironic, right?). Please download the latest version from https://github.com/SamtendoNetwork/ElectrodeUpdater/releases/latest.")
        sys.exit(1)
    # Please don't change this check just to get around the check
    # Otherwise, ElectrodeUpdater will download the wrong release if the URLs aren't changed

    drive_letter = input("Enter your SD card drive letter (e.g. D, E, F): ").strip().upper()
    
    if sys.platform == "win32":
        sd_path = f"{drive_letter}:\\"
    else:
        sd_path = f"/mnt/{drive_letter.lower()}"
    
    if not os.path.exists(sd_path):
        print(f"STOP! Drive '{drive_letter}:' not found")
        sys.exit(1)
    
    print(f"\nChecking SD card at {sd_path}...\n")
    
    wiiu_path = check_folder_exists(sd_path, "wiiu", required=True)
    check_folder_exists(wiiu_path, "environments", required=True)
    check_folder_not_exists(wiiu_path, "aroma")
    plugins_path = check_folder_exists(wiiu_path, "plugins", required=True)
    modules_path = check_folder_exists(wiiu_path, "modules", required=True)
    
    print("\nSD card looks good!!")
    print("\nUpdating Electrode files...\n")
    
    wps = "https://github.com/SamtendoNetwork/Electrode/releases/download/v0.0.6/Electrode-samtendo.wps"
    wms = "https://github.com/SamtendoNetwork/Electrode/releases/download/v0.0.6/Electrode-samtendo.wms"
    
    print("Plugins:")
    download_and_replace(plugins_path, "Electrode-samtendo.wps", wps)
    
    print("\nModules:")
    download_and_replace(modules_path, "Electrode-samtendo.wms", wms)
    
    print("\nUpdated! Thanks for choosing Samtendo ^^")

if __name__ == "__main__":
    main()
