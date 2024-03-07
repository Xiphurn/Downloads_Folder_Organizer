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
  - It is possible to skip the duplicate removal step entirely by setting the `want_to_remove_duplicates` variable to `False` in the `main()` function, which can be useful to save execution time. While this can be useful to save execution time, the impact of skipping duplicate removal is less significant since the implementation of the caching mechanism. The hash cache optimizes the duplicate removal process by avoiding redundant hash calculations, making it more efficient even when dealing with a large number of files. However, if you are certain that there are no duplicate files or if you prefer to keep all files regardless of duplicates, you can still choose to skip the duplicate removal step.

  - You can also specify the folders for which you don't want to remove duplicates by adding their names to the `not_allowed_folders` list in the `remove_duplicates()` function.

### New Caching Mechanism :
  The script employs a caching mechanism to optimize the duplicate file removal process. When dealing with a large number of files, calculating the hash for each file can be time-consuming. To avoid redundant hash calculations, the script utilizes a hash cache.

  The hash cache is implemented using a dictionary (`hash_cache`) where the keys are unique identifiers for each file, and the values are the corresponding file hashes. The unique identifier is a combination of the file path and its last modified time. This ensures that if a file is modified, it will be treated as a new file and its hash will be recalculated.

  When the script needs to calculate the hash of a file, it first checks if the file's unique identifier exists in the `hash_cache` dictionary. If the identifier is found, it means the file hash was previously calculated and stored in the cache. In this case, the script retrieves the cached hash value instead of recalculating it. If the identifier is not found in the cache, the script calculates the file hash using the MD5 algorithm and stores it in the `hash_cache` dictionary for future reference.

  The hash cache is persisted across multiple runs of the script by storing it in a JSON file (`hash_cache.json`) located in the same directory as the script. The `load_hash_cache()` function is responsible for loading the existing hash cache from the JSON file, while the `save_hash_cache()` function saves the updated hash cache back to the JSON file.

  By utilizing the hash cache, the script avoids redundant hash calculations, significantly improving the performance of the duplicate file removal process, especially when dealing with a large number of files or running the script multiple times on the same set of files.

### Functions

1. **`file_hash(filepath, hash_cache`**: 
    - This function calculates the MD5 hash of a file specified by the `filepath` parameter.
    - It first checks if the file's hash is already present in the `hash_cache` dictionary using the file path and last modified time as the key.
    - If the hash is found in the cache, it returns the cached hash value.
    - If the hash is not found in the cache, it opens the file in binary mode, reads it in chunks of 4096 bytes, and updates the MD5 hash object with each chunk.
    - Finally, it returns the hexadecimal representation of the calculated hash and updates the `hash_cache` dictionary with the new hash value.

2. **`remove_duplicates(folder_path)`**: 
    - This function removes duplicate files within the specified `folder_path`.
    - It first checks if the folder name is not in the list of folders where duplicate removal is not allowed (specified by `not_allowed_folders`).
    - If duplicate removal is allowed for the folder, it loads the existing hash cache from the JSON file using the `load_hash_cache()` function.
    - It iterates over each file in the folder, calculates its hash using the `file_hash()` function, and compares it with previously seen hashes.
    - If a duplicate file is found (i.e., a file with the same hash already exists), it removes the duplicate file using the `unlink()` method.
    - If the folder is in the `not_allowed_folders` list, it skips duplicate removal for that folder.
    - After processing all files, it saves the updated hash cache to the JSON file using the `save_hash_cache()` function.

    Note that this step can be time-consuming the first time you run the script depending on the number and size of files to be processed. It will be much faster for next runs (due to the caching system)

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

5. **`load_hash_cache(cache_file)`**: 
    - This function loads the hash cache from a JSON file specified by `cache_file`.
    - If the cache file exists and contains valid JSON data, it returns the loaded hash cache as a dictionary.
    - If the cache file doesn't exist or contains invalid JSON data, it returns an empty dictionary.

6. **`save_hash_cache(cache_file, hash_cache)`**: 
    - This function saves the `hash_cache` dictionary to a JSON file specified by `cache_file`.
    - It opens the file in write mode and uses `json.dump()` to write the `hash_cache` dictionary to the file.

7. **`main()`**: 
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
  - You can choose whether you want to delete duplicates or not by changing the `want_to_remove_duplicates` variable to `True` or `False` in `main`. As       removing duplicates is the slowest part of the process, this saves time. Removing duplicates is typically the slowest part of the process, but the implementation of the caching mechanism has significantly reduced the impact of this choice on the overall execution time. The hash cache optimizes the duplicate removal process by avoiding redundant hash calculations, making it more efficient even when dealing with a large number of files. However, if you prefer to keep all files regardless of duplicates or if you are certain that there are no duplicates, you can set `want_to_remove_duplicates` to `False` to skip the duplicate removal step entirely.

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



