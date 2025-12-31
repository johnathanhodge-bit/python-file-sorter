import os
import shutil
import json
import logging
import tkinter as tk
from tkinter import filedialog, messagebox

# Set up logging - use script's directory for log file
script_dir = os.path.dirname(os.path.abspath(__file__))
log_file_path = os.path.join(script_dir, 'organizer.log')
logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def select_folder():
    """Open a dialog to select a folder"""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    folder_path = filedialog.askdirectory(title="Select folder to organize")
    root.destroy()
    return folder_path

def load_config():
    """Load configuration from config.json file"""
    # Use the script_dir already defined at module level
    config_path = os.path.join(script_dir, "config.json")
    
    # First try: same directory as the script
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            return config
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in config.json at {config_path}: {e}")
            return None
    
    # Fallback: try current working directory
    cwd_config = os.path.join(os.getcwd(), "config.json")
    if os.path.exists(cwd_config):
        try:
            with open(cwd_config, 'r') as f:
                config = json.load(f)
            return config
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in config.json at {cwd_config}: {e}")
            return None
    
    # If we get here, file wasn't found
    print(f"Error: config.json not found at {config_path} or {cwd_config}")
    return None

def organize_folder():
    # Load configuration from JSON file
    config = load_config()
    if not config:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Error", "Failed to load config.json. Please check the file.")
        root.destroy()
        return 0
    
    # Allow user to select the folder
    current_dir = select_folder()
    
    # If user cancels, exit
    if not current_dir:
        print("No folder selected. Exiting.")
        return 0
    
    print(f"Organizing folder: {current_dir}")
    
    # Get categories and script name from config
    folders = config.get("categories", {})
    script_name = config.get("script_name", "organizer.py")
    
    # Counter for files moved
    files_moved = 0

    # Loop through every file in the current folder
    for filename in os.listdir(current_dir):
        # Skip the script itself so it doesn't move itself!
        if filename == script_name:
            continue

        # Get the filename in lowercase for comparison
        filename_lower = filename.lower()

        # Check which category the extension belongs to
        # Check if filename ends with any of the extensions (handles multi-part extensions like .transcript.vtt)
        for folder_name, extensions in folders.items():
            # Sort extensions by length (longest first) to match specific extensions like .transcript.vtt before .vtt
            sorted_extensions = sorted(extensions, key=len, reverse=True)
            
            # Check if filename ends with any extension in this category
            matched = False
            matched_ext = None
            for ext in sorted_extensions:
                if filename_lower.endswith(ext.lower()):
                    matched = True
                    matched_ext = ext
                    break
            
            if matched:
                # Create the category folder if it doesn't exist
                folder_path = os.path.join(current_dir, folder_name)
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                
                # Move the file
                print(f"Moving {filename} to {folder_name}")
                try:
                    shutil.move(os.path.join(current_dir, filename), 
                                os.path.join(current_dir, folder_name, filename))
                    logging.info(f"Moved {filename} to {folder_name}")
                    files_moved += 1
                except PermissionError:
                    print(f'Could not move {filename} due to permission issues')
                break  # Move to next file after attempting to move (success or failure)
    
    return files_moved

if __name__ == "__main__":
    files_moved = organize_folder()
    
    # Only show message box if folder was actually organized (not cancelled)
    if files_moved is not None and files_moved >= 0:
        # Create the message with file count and log file path
        # (log_file_path is already defined at module level)
        message = f"Folder is now organized.\n\nFiles moved: {files_moved}\n\nLog file: {log_file_path}"
        
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        messagebox.showinfo("Done", message)
        root.destroy()