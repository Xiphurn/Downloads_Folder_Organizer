from pathlib import Path
import hashlib
import re
import time
import shutil

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
    '.txt': 'Text Files',
    '.zip': 'Compressed Files',
    '.exe': 'Programs',
    '.msi': 'Programs',
    '.iso': 'Disk Images',
    '.csv': 'CSV Files',
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


# Calculate the MD5 hash of a file for duplicate checking
def file_hash(filepath):
    """Calculate MD5 hash of a file."""
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def remove_duplicates(folder_path):
    """Remove duplicate files in the given folder by comparing their hash."""

    # List of folder names where duplicate removal is not allowed
    # not_allowed_folders = ["Android Apps", "Compressed Files", "Programs", "Others", "Disk Images"]
    # Fullfil the list with the folder names where you don't want to remove duplicates as above
    not_allowed_folders = []

    # Convert folder_path to a Path object if it's not already one
    folder_path = Path(folder_path)

    # Get the name of the last component of the folder_path
    folder_name = folder_path.name

    # Check if folder_name is NOT in the list of not allowed folders
    if folder_name not in not_allowed_folders:
        print(f"Removing duplicates in {folder_path}, this may take a while...")
        hashes = {}
        for file in folder_path.iterdir():
            if file.is_file():
                file_hash_value = file_hash(file)
                if file_hash_value in hashes:
                    print(f"Removing duplicate file: {file}")
                    file.unlink()  # Remove the file
                else:
                    hashes[file_hash_value] = file
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
def organize_files():
    """Organize files in the downloads directory into categorized folders."""
    for file in downloads_path.iterdir():
        if file.is_file():
            file_extension = file.suffix.lower()
            folder_name = extension_folders.get(file_extension, 'Others')
            folder_path = downloads_path / folder_name
            folder_path.mkdir(exist_ok=True)
            file.rename(folder_path / file.name)
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

if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"The script took {execution_time:.2f} seconds to run.")