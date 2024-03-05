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


# Calculate the MD5 hash of a file for duplicate checking
def file_hash(filepath):
    """Calculate MD5 hash of a file."""
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

# Remove duplicate files in a given folder
def remove_duplicates(folder_path):
    """Remove duplicate files in the given folder by comparing their hash. Rename remaining files to remove unnecessary indices."""
    print(f"Removing duplicates in {folder_path}, this may take a while...")
    hashes = {}
    for file in folder_path.iterdir():
        if file.is_file():
            file_hash_value = file_hash(file)
            if file_hash_value in hashes:
                print(f"Removing duplicate file: {file}")
                file.unlink()  # Remove the file
                # Check if the remaining file has an index in its name and rename it if necessary
                original_file = hashes[file_hash_value]
                match = re.match(r"(.*) \(\d+\)(\.[^.]+)$", original_file.name)
                if match:
                    new_name = f"{match.group(1)}{match.group(2)}"
                    new_file_path = original_file.parent / new_name
                    if not new_file_path.exists():
                        original_file.rename(new_file_path)
                        print(f"Renamed {original_file} to {new_name}")
            else:
                hashes[file_hash_value] = file

# Find a new, unique file name if the target name already exists
def find_new_file_name(base_path, original_stem, suffix, start=1):
    """Find a new file name by appending '(n)' until an unused name is found."""
    for i in range(start, 10000):  # Limit attempts to avoid infinite loop
        new_stem = f"{original_stem} ({i})"
        new_file_path = base_path / f"{new_stem}{suffix}"
        if not new_file_path.exists():
            return new_file_path
    raise Exception("Could not find a new file name.")

# Rename and organize files into folders based on their extension
def organize_files():
    """Organize files in the downloads directory into categorized folders, ensuring names are kept as simple as possible."""
    for file in downloads_path.iterdir():
        if file.is_file():
            file_extension = file.suffix.lower()
            folder_name = extension_folders.get(file_extension, 'Others')
            folder_path = downloads_path / folder_name
            folder_path.mkdir(exist_ok=True)

            target_file_path = folder_path / file.name
            if target_file_path.exists():
                # Extract the stem (file name without extension) and check if it ends with an index pattern
                original_stem = file.stem
                match = re.match(r"(.*) \(\d+\)$", original_stem)
                if match:
                    # Try to find a new name without unnecessary indices
                    base_stem = match.group(1)
                    new_file_path = find_new_file_name(folder_path, base_stem, file.suffix)
                else:
                    # If no index pattern, just find a new name normally
                    new_file_path = find_new_file_name(folder_path, original_stem, file.suffix)
            else:
                new_file_path = target_file_path

            file.rename(new_file_path)
            print(f'Moved {file.name} to {new_file_path}')

# Main function to initiate file organization and cleaning
def main():
    organize_files()
    print('Files have been organized.\n')

    # Creating and moving directories into a "Folders" directory
    folders_path = downloads_path / "Folders"
    folders_path.mkdir(exist_ok=True)
    for item in downloads_path.iterdir():
        if item.is_dir() and item.name not in extension_folders.values() and item.name != "Others" and item.name != "Folders":
            target_folder_path = folders_path / item.name
            if not target_folder_path.exists():
                item.rename(target_folder_path)
                print(f'Moved folder {item.name} to {folders_path}')
            else:
                print(f"Folder {item.name} already exists in {folders_path}, skipping...")

    print('Folders have been organized. \n')

    # Removing duplicate files in organized folders
    for folder in set(extension_folders.values()).union({'Others'}):
        folder_path = downloads_path / folder
        if folder_path.exists() and folder_path.is_dir():
            remove_duplicates(folder_path)
    
    print('Duplicate files have been removed. \n')

if __name__ == "__main__":
    main()