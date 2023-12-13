import os
import shutil
import time
from datetime import datetime
import argparse

def synchronize_folders(source_folder, replica_folder, log_file):
    while(True):
        #Get every file path and last modified timestamp(in order to compare timestamps between backups to see if it needs to be updated)    
        source_files = {}
        for root, _, files in os.walk(source_folder):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, source_folder)
                source_files[relative_path] = os.path.getmtime(file_path)

        replica_files = {}
        for root, _, files in os.walk(replica_folder):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, replica_folder)
                replica_files[relative_path] = os.path.getmtime(file_path)

        # Files to be copied/updated
        to_copy = {file: source_files[file] for file in source_files if file not in replica_files or source_files[file] != replica_files[file]}

        # Files to be removed from replica folder
        to_remove = [file for file in replica_files if file not in source_files]
        
        if to_copy or to_remove:
            with open(log_file, 'a') as log:
                log.write(f"\n{datetime.now()}\n")
                    
            for file, timestamp in to_copy.items():
                source_path = os.path.join(source_folder, file)
                replica_path = os.path.join(replica_folder, file)
                shutil.copy2(source_path, replica_path)
                print(f"Copied: '{file}'")
                with open(log_file, 'a') as log:
                    log.write(f"Copied: '{file} - {timestamp}'\n")
            
            # Remove extra files from replica
            for file in to_remove:
                replica_path = os.path.join(replica_folder, file)
                os.remove(replica_path)
                print(f"Removed: '{file}'")
                with open(log_file, 'a') as log:
                    log.write(f"Removed: '{file} - {timestamp}'\n")
    
        time.sleep(60)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Folder Synchronization Program')
    parser.add_argument('source_folder', help='Path to source folder')
    parser.add_argument('replica_folder', help='Path to replica folder')
    parser.add_argument('log_file', help='Path to log file')
    args = parser.parse_args()
    
    if not os.path.exists(args.source_folder):
        print(f"Source folder '{args.source_folder}' does not exist.")
    elif not os.path.exists(args.replica_folder):
        print(f"Replica folder '{args.replica_folder}' does not exist.")
    elif not os.path.exists(args.log_file):
        print(f"Log file '{args.log_file}' does not exist.")
    else:
        synchronize_folders(args.source_folder, args.replica_folder, args.log_file)