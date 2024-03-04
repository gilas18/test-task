import os
import shutil
import time
import argparse
from datetime import datetime

def sync_folders(source_folder, replica_folder, interval, log_file):
    if not os.path.exists(replica_folder):
        os.makedirs(replica_folder)
    sync_files(source_folder, replica_folder, log_file)
    while True:
        time.sleep(interval)
        sync_files(source_folder, replica_folder, log_file)

def sync_files(source_folder, replica_folder, log_file):
    with open(log_file, 'a') as log:
        log.write(f"Syncing at {datetime.now()}\n")
        for root, dirs, files in os.walk(source_folder):
            for file in files:
                source_file_path = os.path.join(root, file)
                replica_file_path = os.path.join(replica_folder, os.path.relpath(source_file_path, source_folder))
                try:
                    if not os.path.exists(replica_file_path) or os.stat(source_file_path).st_mtime > os.stat(replica_file_path).st_mtime:
                        shutil.copy2(source_file_path, replica_file_path)
                        log.write(f"Copied: {source_file_path} -> {replica_file_path}\n")
                        print(f"Copied: {source_file_path} -> {replica_file_path}\n")
                except Exception as e:
                    log.write(f"Error: {str(e)}\n")
                    print(f"Error: {str(e)}")
        for root, dirs, files in os.walk(replica_folder):
            for file in files:
                replica_file_path = os.path.join(root, file)
                source_file_path = os.path.join(source_folder, os.path.relpath(replica_file_path, replica_folder))
                if not os.path.exists(source_file_path):
                    os.remove(replica_file_path)
                    log.write(f"Removed: {replica_file_path}\n")
                    print(f"Removed: {replica_file_path}")
        for root, dirs, files in os.walk(source_folder):
            for directory in dirs:
                replica_dir_path = os.path.join(replica_folder, os.path.relpath(os.path.join(root, directory), source_folder))
                if not os.path.exists(replica_dir_path):
                    os.makedirs(replica_dir_path)
                    log.write(f"Created directory: {replica_dir_path}\n")
                    print(f"Created directory: {replica_dir_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Synchronize two folders")
    parser.add_argument("source_folder", type=str, help="Path to source folder")
    parser.add_argument("replica_folder", type=str, help="Path to replica folder")
    parser.add_argument("interval", type=int, help="Synchronization interval in seconds")
    parser.add_argument("log_file", type=str, help="Path to log file")
    args = parser.parse_args()

    source_folder = args.source_folder
    replica_folder = args.replica_folder
    interval = args.interval
    log_file = args.log_file

    sync_folders(source_folder, replica_folder, interval, log_file)

