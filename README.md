# File Organizer Script Documentation

This script is designed to automate the organization of files within a specified downloads directory on your computer. It sorts files into predefined folders based on their extensions, renames files to avoid naming conflicts, removes duplicate files, and reorganizes folders to maintain a clean directory structure.

## How the Script Works
**Please Note !** : Before running the script, it is strongly recommended to back up your files. I cannot be held responsible for any data loss or damage that may occur as a result of using this script.


### Setup and Initial Definitions

- **Define Downloads Path**: At the beginning of the script, you'll set the path to your downloads folder. This path needs to be customized to match the location of your downloads directory on your computer.

- **Extension to Folder Mapping**: The `extension_folders` dictionary maps file extensions to folder names. This mapping determines where files of each type should be moved within the downloads directory. You are free to modify this dictionary to suit your organizational preferences.

```python
extension_folders = {
    '.pdf': 'PDFs',
    '.mp3': 'Music',
    # Add or modify mappings as needed
}
```

### Functions

1. **`file_hash(filepath)`**: Calculates the MD5 hash of a file for identifying duplicates. It processes files in chunks, making it efficient for handling large files. This function reads the file in segments, ensuring that it can compute the hash for large files without consuming excessive memory. Note that this step can be time-consuming depending on the number and size of files to be processed.

2. **`remove_duplicates(folder_path)`**: Iterates over files in a specified folder, computes their MD5 hashes, and removes any duplicate files.

3. **`find_new_file_name(base_path, original_stem, suffix, start=1)`**: Generates a unique filename by appending a number to the original name if a file with the same name exists.

4. **`clean_and_rename_file(file_path)`**: This function streamlines file names within a directory by removing unordered indices and reassigning them in a sequential order. This is particularly useful after duplicate files have been removed and only non-identical files with matching base names remain, potentially leaving gaps in the numbering sequence. The function ensures that all files with the same base name are numbered sequentially without gaps.

### Organizing Files

- **Sort Files by Extension**: Files are moved into folders based on their extensions, as defined in the `extension_folders` dictionary. Folders are created as needed.

- **Organize Directories**: A "Folders" directory is created to store miscellaneous directories from the downloads folder, keeping the main directory organized.

### Removing Duplicates and Cleaning Names

- **Remove Duplicate Files**: After sorting, the script removes duplicates within each folder using their MD5 hashes.

- **Rename and Clean File Names**: Files are renamed to ensure uniqueness and to follow a standardized naming convention, eliminating numbers added for previous naming conflicts.


## Application example
### State of Downloads folder before script execution 
```
Downloads/
│
├── Project_Report.docx
├── vacation_photo (1).jpg
├── Project_Report (2).docx
├── song_track.mp3
├── Project_Report.pdf
├── song_track (1).mp3
├── research_paper.pdf
├── research_paper (4).pdf
├── research_paper (7).pdf
├── Folder1
├── Folder2
└── miscellaneous_notes.txt
```
### State of Downloads folder after script execution 
```
Downloads/
│
├── Documents/
│ ├── Project_Report.docx
│ └── Project_Report (1).docx
│
├── PDFs/
│ ├── Project_Report.pdf
│ ├── research_paper.pdf
│ ├── research_paper (1).pdf (previously research_paper (4).pdf)
│ └── research_paper (2).pdf (previously research_paper (7).pdf)
│
├── Images/
│ └── vacation_photo.jpg
│
├── Music/
│ ├── song_track.mp3
│ └── song_track (1).mp3
│
├── Folders/
│ ├── Folder1
│ └── Folder2
│
└── Text Files/
  └── miscellaneous_notes.txt
```

## Conclusion and Disclaimer

This script is intended as a small project to automate the organization of files in a download directory. While it has been tested to ensure it functions as intended, it is provided "as is", without warranty of any kind, express or implied. Please be advised that I am not responsible for any data loss or damage that may arise from using this script. It is highly recommended to back up your files before running the script, especially when using it for the first time. Your feedback and contributions are welcome to improve its reliability and functionality.



