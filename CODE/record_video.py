import serial
import cv2
import time
import os
import numpy as np
import pyautogui
import time


arduino_port = 'COM6'  
baud_rate = 9600
ser = serial.Serial(arduino_port, baud_rate, timeout=1)

def send_command_and_record():
    user = input("Want to send rotate command? Type 'y' for yes and 'n' for no: ")

    if user.lower() == 'y':
        pyautogui.click(1438, 877)

        time.sleep(2)
        ser.write(b'rotate\n')
        print("Command sent")

        while True:
            message = ser.readline().decode('utf-8').strip()
            if message == 'complete':
                pyautogui.click(1438, 877)
                print("Rotation complete, stopping recording")
                return
    else:
        ser.write(b'no\n')
        print("Command not sent")


if __name__ == "__main__":

    send_command_and_record()
    ser.close() 

print("Video saved as output.mp4")