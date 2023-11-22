from threading import Thread
import time
import msvcrt
import cv2
import os
import sys
from mss import mss
from PIL import Image
import numpy as np
from queue import Queue

class lib:
    def __init__(self, delay: float, start_index: int, dir: str, interval: float):
        self.stop = False
        self.allow = True
        self.delay = delay
        self.index = start_index
        self.dir = dir
        self.interval = interval
        self.queue = Queue(maxsize=10)  # Buffer size of 10 images

    def get_input(self):
        while True:
            if not self.stop:
                print("Press the \'S\' key to stop capturing")
                if msvcrt.getch().decode('ascii') == 's':
                    self.stop = True
                    print("Capture Stopped.")
            else:
                print("Press \'C\' to compile and quit the program. Press \'Q\' to quit the program without compiling.")
                key = msvcrt.getch().decode('ascii')
                if key == 'c':
                    self.compile()
                    break
                elif key == 'q':
                    break

    def get_filename(self) -> int:
        self.index += 1
        return self.index - 1

    def wait(self):
        self.allow = False
        time.sleep(self.delay)
        self.allow = True

    def fast_screenshot(self):
        with mss() as sct:
            screenshot = sct.grab(sct.monitors[0])
            img = Image.frombytes('RGB', screenshot.size, screenshot.bgra, 'raw', 'BGRX')
            img = img.convert('RGB')
            img_np = np.array(img)[:,:,::-1]
            return img_np

    def capture(self):
        while not self.stop:
            if self.allow:
                image = self.fast_screenshot()
                self.queue.put(image)  # Add image to the queue
                Thread(target=self.wait).start()

    def compile(self):
        print("Compiling... this may take a couple minutes.")
        while self.queue.qsize() < 10:  # Wait until there are 10 frames in the queue
            time.sleep(0.1)  # Sleep for a short time to reduce CPU usage

        height, width, layers = self.queue.queue[0].shape
        # Specify a frame rate of 30 frames per second
        # Use the 'mp4v' codec
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video = cv2.VideoWriter("vid\\video.mp4", fourcc, 30, (width,height))

        while not (self.stop and self.queue.empty()):  # Continue until both conditions are met
            image = self.queue.get()  # Get image from the queue
            video.write(image)

        cv2.destroyAllWindows()
        video.release()
        print("Compilation Completed!")
        sys.exit()

    def run(self):
        self.get_input()  # Get input before starting the other threads

        capture_thread = Thread(target=self.capture)
        compile_thread = Thread(target=self.compile)

        capture_thread.start()
        compile_thread.start()

        while True:
            if self.stop:
                capture_thread.join()  # Wait for the capture thread to finish
                break

        compile_thread.join()  # Wait for the compile thread to finish