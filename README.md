# Folder Organizer Script Documentation

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

- **Customization Options**:
  - It is possible to skip the duplicate removal step entirely by setting the `want_to_remove_duplicates` variable to `False` in the `main()` function, which can be useful to save execution time.

  - You can also specify the folders for which you don't want to remove duplicates by adding their names to the `not_allowed_folders` list in the `remove_duplicates()` function.

### Functions

1. **`file_hash(filepath)`**: 
    - This function calculates the MD5 hash of a file specified by the `filepath` parameter.
    - It opens the file in binary mode, reads it in chunks of 4096 bytes, and updates the MD5 hash object with each chunk.
    - Finally, it returns the hexadecimal representation of the calculated hash.


2. **`remove_duplicates(folder_path)`**: 
    - This function removes duplicate files within the specified `folder_path`.
    - It first checks if the folder name is not in the list of folders where duplicate removal is not allowed (specified by `not_allowed_folders`).
    - If duplicate removal is allowed for the folder, it iterates over each file in the folder, calculates its hash using the `file_hash()` function, and compares it with previously seen hashes.
    - If a duplicate file is found (i.e., a file with the same hash already exists), it removes the duplicate file using the `unlink()` method.
    - If the folder is in the `not_allowed_folders` list, it skips duplicate removal for that folder.


    Note that this step can be time-consuming depending on the number and size of files to be processed.

3. **`rename_files(folder_path: Path)`**: 
    - This function renames files within the specified `folder_path` to avoid name conflicts.
    - It creates a temporary subfolder called 'temp' within the specified folder.
    - It uses a regular expression pattern to match files with a numeric index before the extension (e.g., "file (1).txt").
    - It moves files matching the pattern to the temporary folder.
    - For each file in the temporary folder, it generates a new name by removing the index or incrementing it if necessary to avoid name conflicts.
    - It moves the file to the original folder with the new name and prints a message if the name was changed.
    - Finally, it deletes the temporary folder if it's empty.

4. **`organize_files()`**: 
    - This function organizes files in the downloads directory into categorized folders based on their file extensions.
    - It iterates over each file in the downloads directory (specified by `downloads_path`).
    - For each file, it determines the folder name based on the file extension using the `extension_folders` dictionary. If the extension is not found in the dictionary, it assigns the file to the 'Others' folder.
    - It creates the corresponding folder if it doesn't exist and moves the file into that folder.
    - It prints a message indicating the file movement.

5. **`main()`**: 
    - This is the main function that initiates the file organization and cleaning process.
    - It calls the `organize_files()` function to organize files into categorized folders.
    - It creates a "Folders" directory within the downloads directory and moves any existing folders (except the categorized folders and "Others") into the "Folders" directory.
    - If `want_to_remove_duplicates` is set to `True`, it calls the `remove_duplicates()` function for each categorized folder (including "Others") to remove duplicate files.
    - It calls the `rename_files()` function for each categorized folder (including "Others") to rename files and avoid name conflicts.
    - Finally, it prints the execution time of the script.

### Organizing Files

- **Sort Files by Extension**: Files are moved into folders based on their extensions, as defined in the `extension_folders` dictionary. Folders are created as needed.

- **Organize Directories**: A "Folders" directory is created to store miscellaneous directories from the downloads folder, keeping the main directory organized.

### Removing Duplicates and Cleaning Names

- **Remove Duplicate Files**: After sorting, the script removes duplicates within each folder using their MD5 hashes.
  - You can choose whether you want to delete duplicates or not by changing the `want_to_remove_duplicates` variable to `True` or `False` in `main`. As       removing duplicates is the slowest part of the process, this saves time. 

  - In the `remove_duplicates(folder_path)` function, you can also select the folders where you don't want duplicates to be removed. 

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



