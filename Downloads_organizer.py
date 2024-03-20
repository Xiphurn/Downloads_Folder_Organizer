from pathlib import Path
import hashlib
import re
import time
import shutil
import os
import json
import random

# Define the path to the Downloads folder. Modify this path according to your operating system and user name.
# Example: downloads_path = Path(r"C:\Users\YourUserName\Downloads")
downloads_path = Path(r"Path to downloads folder ")

# Create a dictionary to map file extensions to folder names
extension_folders = {
    '.pdf': 'PDFs',
    '.mp3': 'Music',
    '.mp4': 'Videos',
    '.docx': 'Documents',
    '.odt': 'Documents',
    '.doc': 'Documents',
    '.xlsx': 'Spreadsheets',
    '.jpg': 'Images',
    '.png': 'Images',
    '.gif': 'Images',
    '.jpeg': 'Images',
    '.heic': 'Images',
    '.txt': 'Text Files',
    '.zip': 'Compressed Files',
    '.exe': 'Programs',
    '.msi': 'Programs',
    '.dmg': 'Disk Images',
    '.app': 'Programs',
    '.iso': 'Disk Images',
    '.csv': 'CSV Files',
    '.xls': 'Spreadsheets',
    '.xltx': 'Spreadsheets',
    '.ott': 'Documents',
    '.dot': 'Documents',
    '.pptx': 'Presentations',
    '.ppt': 'Presentations',
    '.ics': 'Calendar Files',
    '.js': 'Web Pages',
    '.css': 'Web Pages',
    '.php': 'Web Pages',
    '.html': 'Web Pages',
    '.xml': 'Web Pages',
    '.py': 'Python Scripts',
    '.ipynb': 'Jupyter Notebooks',
    '.json': 'JSON Files',
    '.db': 'Database Files',
    '.sql': 'Database Files',
    '.jar': 'Java Programs',
    '.java': 'Java Programs',
    '.class': 'Java Programs',
    '.c': 'C Programs',
    '.cpp': 'C++ Programs',
    '.h': 'Header Files',
    '.ps1': 'PowerShell Scripts',
    '.sh': 'Shell Scripts',
    '.app': 'Applications',
    '.apk': 'Android Apps',
    '.xapk': 'Android Apps',
    '.appx': 'Windows Apps',
    '.ipa': 'iOS Apps',
    '.msu': 'Windows Updates',
    '.torrent': 'Torrent Files',
    '.cfg': 'Configuration Files',
    '.ini': 'Configuration Files',
    '.bak': 'Backup Files',
    '.temp': 'Temporary Files',
    '.md': 'Markdown Files',
    '.yml': 'YAML Files',
    '.yaml': 'YAML Files',
    '.avi': 'Videos',
    '.mov': 'Videos',
    '.wmv': 'Videos',
    '.flv': 'Videos',
    '.mkv': 'Videos',
    '.wav': 'Music',
    '.aiff': 'Music',
    '.flac': 'Music',
    '.ogg': 'Music',
    '.aac': 'Music',
    '.epub': 'E-books',
    '.mobi': 'E-books',
    '.azw': 'E-books',
    '.rar': 'Compressed Files',
    '.7z': 'Compressed Files',
    '.gz': 'Compressed Files',
    '.tar': 'Compressed Files',
    '.ts': 'TypeScript Files',
    '.mdb': 'Database Files',
    '.accdb': 'Database Files',
    '.sqlite': 'Database Files',
    '.sqlitedb': 'Database Files',
    '.stl' : '3D Model Files',
    '.obj' : '3D Model Files',
    '.fbx' : '3D Model Files',
    '.dwg' : 'CAD Files',
    '.dxf' : 'CAD Files',
    '.sldprt' : 'CAD Files',
    '.sldasm' : 'CAD Files',
    '.stp' : 'CAD Files',
}


def load_hash_cache(cache_file):
    if cache_file.exists():
        try:
            with open(cache_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"\nThe cache file '{cache_file}' is empty or does not exist.")
            print("A new empty cache will be used instead...\n")
            return {}
    else:
        return {}

def save_hash_cache(cache_file, hash_cache):
    with open(cache_file, 'w') as f:
        json.dump(hash_cache, f)

def file_hash(file_path, hash_cache):
    mtime = os.path.getmtime(file_path)
    cache_key = f"{file_path}|{mtime}"  # Convert tuple to string
    
    if cache_key in hash_cache:
        return hash_cache[cache_key]
    else:
        with open(file_path, "rb") as f:
            md5_hash = hashlib.md5()
            for chunk in iter(lambda: f.read(4096), b""):
                md5_hash.update(chunk)
        file_hash = md5_hash.hexdigest()
        hash_cache[cache_key] = file_hash
        return file_hash

def remove_duplicates(folder_path):
    """Remove duplicate files in the given folder by comparing their hash."""
    
    not_allowed_folders = []
    
    folder_path = Path(folder_path)
    folder_name = folder_path.name
    
    if folder_name not in not_allowed_folders:
        print(f"Removing duplicates in {folder_path}, this may take a while...")
        
        # Get the directory of the current script
        script_dir = Path(__file__).parent
        
        # Create the cache file path in the same directory as the script
        cache_file = script_dir / 'hash_cache.json'
        
        # Create the cache file if it doesn't exist
        cache_file.touch(exist_ok=True)
        
        hash_cache = load_hash_cache(cache_file)
        hashes = {}
        for file in folder_path.iterdir():
            if file.is_file():
                file_hash_value = file_hash(str(file), hash_cache)
                if file_hash_value in hashes:
                    print(f"Removing duplicate file: {file}")
                    file.unlink()
                else:
                    hashes[file_hash_value] = file
        save_hash_cache(cache_file, hash_cache)
    else:
        print(f"Skipping {folder_path} folder.")

def rename_files(folder_path: Path):
    # Create a temporary subfolder called 'temp' in the specified folder
    temp_folder = folder_path / 'temp'
    temp_folder.mkdir(exist_ok=True)

    # Regular expression pattern to match files with a numeric index before the extension
    pattern = re.compile(r'(.+) \((\d+)\)(\.[^.]+)$')

    # Move files with an index to the temporary folder
    for file in folder_path.glob('*'):
        if pattern.match(file.name):
            shutil.move(str(file), str(temp_folder))

    # Process files in the temporary folder
    for file in temp_folder.glob('*'):
        match = pattern.match(file.name)
        if match:
            base_name, _, extension = match.groups()
            new_index = 0
            while True:
                new_name = f'{base_name}{extension}' if new_index == 0 else f'{base_name} ({new_index}){extension}'
                new_path = folder_path / new_name
                if not new_path.exists():
                    break
                new_index += 1
            
            # Move the file to the original folder with the new name
            shutil.move(str(file), str(new_path))
            # Print only if the new name is different from the old name
            if new_path.name != file.name:
                print(f"Renamed '{file.name}' to '{new_path.name}'")

    # Delete the temporary folder if it's empty
    if not any(temp_folder.iterdir()):
        temp_folder.rmdir()


# Organize files into folders based on their extension
def organize_files(downloads_path=downloads_path):
    """Organize files in the downloads directory into categorized folders."""
    for file in downloads_path.iterdir():
        if file.is_file():
            file_extension = file.suffix.lower()
            folder_name = extension_folders.get(file_extension, 'Others')
            folder_path = downloads_path / folder_name
            folder_path.mkdir(exist_ok=True)
            
            # Check if a file with the same name already exists in the destination folder
            new_file_path = folder_path / file.name
            if new_file_path.exists():
                # If a file with the same name exists, rename the file being moved
                print(f"File with name '{file.name}' already exists in {folder_name}, trying a different name...")
                while True:
                    random_number = random.randint(1000, 9999)
                    new_name = f"{file.stem} ({random_number}){file.suffix}"
                    new_file_path = folder_path / new_name
                    if not new_file_path.exists():
                        print(f"Found a unique name: '{new_name}'")
                        break
                    else:
                        print(f"File with name '{new_name}' already exists. Trying a different name...")
                file.rename(new_file_path)
                print(f'Moved and renamed {file.name} to {new_file_path}')
            else:
                file.rename(new_file_path)
                print(f'Moved {file.name} to {folder_path}')

# Main function to initiate file organization and cleaning
def main():
    # Set this to True if you want to remove duplicate files and False otherwise
    # removing duplicates can be time consuming !!!
    want_to_remove_duplicates = True

    organize_files()
    print('Files have been organized.\n')

    folders_path = downloads_path / "Folders"
    folders_path.mkdir(exist_ok=True)
    for item in downloads_path.iterdir():
        if item.is_dir() and item.name not in extension_folders.values() and item.name != "Others" and item.name != "Folders":
            item.rename(folders_path / item.name)
            print(f'Moved folder {item.name} to {folders_path}')

    print('Folders have been organized. \n')

    if want_to_remove_duplicates:
        for folder in set(extension_folders.values()).union({'Others'}):
            folder_path = downloads_path / folder
            if folder_path.exists() and folder_path.is_dir():
                remove_duplicates(folder_path)
        
        print('Duplicate files have been removed. \n')

    for folder in set(extension_folders.values()).union({'Others'}):
        folder_path = downloads_path / folder
        if folder_path.exists() and folder_path.is_dir():
            rename_files(folder_path)
    
    print('Files have been renamed. \n')


start_time = time.time()
main()
end_time = time.time()
execution_time = end_time - start_time
print(f"The script took {execution_time:.2f} seconds to run.")