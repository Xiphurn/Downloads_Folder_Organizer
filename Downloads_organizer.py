from pathlib import Path
import hashlib
import re

# Define the path to the Downloads folder. Modify this path according to your operating system and user name.
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


# Function to calculate MD5 hash of a file
def file_hash(filepath):
    """Calculate MD5 hash of a file."""
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

# Function to remove duplicate files in the given folder
def remove_duplicates(folder_path):
    """Remove duplicate files in the given folder."""
    hashes = {}
    for file in folder_path.iterdir():
        if file.is_file():
            file_hash_value = file_hash(file)
            if file_hash_value in hashes:
                print(f"Removing duplicate file: {file}")
                file.unlink()  # Remove the file
            else:
                hashes[file_hash_value] = file


def find_new_file_name(base_path, original_stem, suffix, start=1):
    """Find a new file name by appending '(n)' until an unused name is found."""
    for i in range(start, 10000): # Limit the number of attempts to 10000
        new_stem = f"{original_stem} ({i})"
        new_file_path = base_path / f"{new_stem}{suffix}"
        if not new_file_path.exists():
            return new_file_path
    raise Exception("Could not find a new file name.")


def clean_and_rename_file(file_path):
    """Renames a file to the lowest available index if the base name exists."""
    file_parent = file_path.parent
    original_stem = re.sub(r"(\s\(\d+\))+$", "", file_path.stem)  # Remove "(X)" patterns
    file_suffix = file_path.suffix

    # Start with the assumption that we can use the cleaned name directly
    new_file_name = f"{original_stem}{file_suffix}"
    new_file_path = file_parent / new_file_name
    i = 1  # Start the index for numbering

    # If the cleaned name already exists and it's not the file itself, find the next available index
    while new_file_path.exists() and new_file_path != file_path:
        new_file_name = f"{original_stem} ({i}){file_suffix}"
        new_file_path = file_parent / new_file_name
        i += 1

    # Rename the file if the new path is different from the original path
    if new_file_path != file_path:
        file_path.rename(new_file_path)
        print(f"Renamed '{file_path}' to '{new_file_name}'")

# Organizing files by their extensions
for file in downloads_path.iterdir():
    if file.is_file():
        file_extension = file.suffix.lower()
        folder_name = extension_folders.get(file_extension, 'Others')
        folder_path = downloads_path / folder_name
        folder_path.mkdir(exist_ok=True)
        new_file_path = folder_path / file.name
        file.rename(new_file_path)
        print(f'Moved {file.name} to {folder_path}')

print('Files have been organized. \n')

# Create a "Folders" directory if it doesn't exist
folders_path = downloads_path / "Folders"
folders_path.mkdir(exist_ok=True)

# Move existing directories (except those created by the script and the "Folders" directory itself) into the "Folders" directory
for item in downloads_path.iterdir():
    # Check if the item is a directory, it's not the "Folders" directory, and it's not one of the directories created by the script
    if item.is_dir() and item.name != "Folders" and item.name not in extension_folders.values() and item.name != "Others":
        target_folder_path = folders_path / item.name
        # Check if the target folder already exists to avoid overwriting
        if not target_folder_path.exists():
            item.rename(target_folder_path)
            print(f'Moved folder {item.name} to {folders_path}')
        else:
            print(f"Folder {item.name} already exists in {folders_path}, skipping...")
print('Folders have been organized. \n')

# Removing duplicate files in each folder created by the script
for folder in set(extension_folders.values()):
    folder_path = downloads_path / folder
    if folder_path.exists() and folder_path.is_dir():
        remove_duplicates(folder_path)

# Additionally check and remove duplicates in the 'Others' folder
others_path = downloads_path / 'Others'
if others_path.exists() and others_path.is_dir():
    remove_duplicates(others_path)

print('Duplicate files have been removed. \n')

# Apply this function to each file after organizing and removing duplicates
for folder_name in set(extension_folders.values()).union({'Others'}):
    folder_path = downloads_path / folder_name
    if folder_path.exists() and folder_path.is_dir():
        for file in folder_path.iterdir():
            if file.is_file():
                clean_and_rename_file(file)

print('File names have been cleaned up and made unique. \n')