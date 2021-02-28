#!/usr/bin/python

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import subprocess

import os
import time
import argparse

parser = argparse.ArgumentParser()

# args
parser.add_argument("target_dir", type=str, help="dir you want to watch")
parser.add_argument("script", type=str, help="script you want to excute")
parser.add_argument("--created_file", action="store_true", help="flag true if you use created file in your script")

args = parser.parse_args()

class Watcher(FileSystemEventHandler):
    def __init__(self, command, created_file_bool):
        self.command = command
        self.created_file_bool = created_file_bool
        self.created_file = "created_file"

    def run_command(self):
        time.sleep(0.1)
        subprocess.run(self.command)

    def on_created(self, event):
        filepath = event.src_path
        filename = os.path.basename(filepath)
        print(filepath)
        if 'crdownload' not in filename:
            print("%s created" %filename)

            if self.created_file_bool:
                for num,snipet in enumerate(self.command):
                    print(snipet)
                    if snipet == self.created_file:
                        self.command[num] = filepath
                        self.created_file = filepath

            self.run_command()
    """
    def on_moved(self, event):
        filepath = event.src_path
        filename = os.path.basename(filepath)
    """

def strTolis(string):
    pos1 = 0
    rtlis = []

    for i, name in enumerate(string):
        if name == " ":
            rtlis.append(string[pos1:i])
            pos1 = i+1
    rtlis.append(string[pos1:i+1])

    return rtlis

def main():

    watcher = Watcher(strTolis(args.script), args.created_file)
    observer = Observer()
    observer.schedule(watcher, args.target_dir, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

main()
