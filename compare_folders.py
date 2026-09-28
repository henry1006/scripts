import os
import sys

def get_files(folder):
    file_dict = {}
    folder = os.path.abspath(folder)
    for root, _, files in os.walk(folder):
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, folder)
            try:
                size = os.path.getsize(full_path)
                file_dict[rel_path] = size
            except OSError:
                pass
    return folder, file_dict

def compare_folders(dir1, dir2):
    path1, files1 = get_files(dir1)
    path2, files2 = get_files(dir2)
    
    set1 = set(files1.keys())
    set2 = set(files2.keys())
    
    missing_in_2 = set1 - set2
    missing_in_1 = set2 - set1
    common = set1.intersection(set2)
    
    diff_size = [f for f in common if files1[f] != files2[f]]
    
    print(f"--- Comparing ---\nFolder 1: {path1}\nFolder 2: {path2}\n")
    
    print(f"Missing in Folder 2 ({len(missing_in_2)}):")
    for f in sorted(missing_in_2):
        print(f"  {f}")
        
    print(f"\nMissing in Folder 1 ({len(missing_in_1)}):")
    for f in sorted(missing_in_1):
        print(f"  {f}")
        
    print(f"\nDifferent sizes ({len(diff_size)}):")
    for f in sorted(diff_size):
        print(f"  {f} (Folder 1: {files1[f]} bytes, Folder 2: {files2[f]} bytes)")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python compare_folders.py <folder1> <folder2>")
        sys.exit(1)
    compare_folders(sys.argv[1], sys.argv[2])
