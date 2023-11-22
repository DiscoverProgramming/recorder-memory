from lib import lib
import os

def get_float_input(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_int_input(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input. Please enter an integer.")

def get_directory_input(prompt: str) -> str:
    while True:
        dir = input(prompt)
        if os.path.isdir(dir) and os.access(dir, os.W_OK):
            return dir
        else:
            print("Invalid directory. Please enter a valid and writable directory.")

delay = get_float_input("Delay between screenshots(Seconds): ")
start_index = get_int_input("Starting index for image names: ")
interval = get_float_input("Interval between frames shown on video(Seconds): ")
dir = get_directory_input("Directory to save images: ")

capture = lib(delay=delay, start_index=start_index, dir=dir, interval=interval)

capture.run()