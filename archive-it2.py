import os
import shutil
from pathlib import Path

# --- CONFIGURATION ---
BASE_PATH = Path("~").expanduser() / "disks/sp/sp"
FROM_DIR = BASE_PATH / "Downloads"
SEARCH_DIR = BASE_PATH 
TO_BASE = BASE_PATH / "sorted"
DELETE_STAGING = BASE_PATH / "duplicates_to_delete"

CATEGORIES = {
    '3d': ['.stl', '.zip', '.step', '.scad', '.3mf', '.gcode'],
    'doc': ['.pdf', '.xml', '.gp5'],
    'image': ['.png', '.jpg'],
    'win': ['.exe'],
    'mac': ['.dmg']
}

def build_share_index(search_root):
    """
    Creates a dictionary of {filename: size} for every file in the archive.
    This is done once to make the rest of the script lightning fast.
    """
    index = {}
    print("🗂️  Indexing archive... please wait (this scans the 1TB share once).")
    
    # Folders we should never consider 'part of the archive'
    ignore_list = ["Downloads", "sorted", "duplicates_to_delete", "my_env", ".git"]

    for root, dirs, files in os.walk(search_root):
        # Prune ignored directories to speed up the walk
        dirs[:] = [d for d in dirs if d not in ignore_list]
        
        for f in files:
            if f.startswith('.'): continue
            try:
                f_path = Path(root) / f
                # Store the filename and its size
                index[f] = f_path.stat().st_size
            except OSError:
                continue
    
    print(f"✅ Index complete. Found {len(index)} unique filenames in archive.")
    return index

# --- EXECUTION ---
# 1. Prepare Environment
DELETE_STAGING.mkdir(parents=True, exist_ok=True)
TO_BASE.mkdir(parents=True, exist_ok=True)

# 2. Build the Index (The "Memory" of your 1TB share)
share_index = build_share_index(SEARCH_DIR)

# 3. Process Downloads
print(f"\n🚀 Processing files from: {FROM_DIR}")
stats = {"moved": 0, "dupes": 0}

for local_path in FROM_DIR.iterdir():
    if not local_path.is_file() or local_path.name.startswith('.'):
        continue

    filename = local_path.name
    ext = local_path.suffix.lower()
    local_size = local_path.stat().st_size

    # A. Check for Duplicate in Index
    # We check if the name exists AND the size matches
    if filename in share_index and share_index[filename] == local_size:
        shutil.move(str(local_path), str(DELETE_STAGING / filename))
        print(f"🗑️  DUPE: {filename} (Matches archive)")
        stats["dupes"] += 1
    
    # B. If Unique, Sort and Move
    else:
        target_subdir = "misc"
        for cat_name, extensions in CATEGORIES.items():
            if ext in extensions:
                target_subdir = cat_name
                break
        
        dest_folder = TO_BASE / target_subdir
        dest_folder.mkdir(parents=True, exist_ok=True)
        
        shutil.move(str(local_path), str(dest_folder / filename))
        print(f"📦 UNIQUE: {filename} -> sorted/{target_subdir}/")
        stats["moved"] += 1

print(f"\n✨ Cleanup Complete!")
print(f"   - Unique files staged: {stats['moved']}")
print(f"   - Duplicates isolated: {stats['dupes']}")