#!/usr/bin/env python3
# pylint: disable=no-member
# requirements: qrcode, opencv-python, pyzbar
import qrcode
from tkinter import Tk, Canvas
from PIL import ImageTk, Image
import cv2
from pyzbar.pyzbar import decode

def create_qr(data):
    """Takes in string and encodes it in QR image"""
    qr = qrcode.QRCode()
    qr.add_data(data)
    img = qr.make_image()
    return img

def draw_image_to_window(window, img):
    """Takes in window and image. Packs canvas with the image to window"""
    side = img.pixel_size
    canvas = Canvas(window, width=side, height=side)
    image = ImageTk.PhotoImage(img)
    canvas.create_image(side/2, side/2, image=image)
    canvas.pack()
    window.update()
    canvas.destroy()

def convert_cv2_frame_to_pil_image(frame):
    """takes in array frame from cv2 video capture and return it as PIL image"""
    cv2img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(cv2img)
    return img

def main():
    window = Tk()
    webcam = cv2.VideoCapture(0)
    data = 'test'
    return_value = True

    # Loop while we get images from webcamera
    while return_value:
        qr = create_qr(str)
        draw_image_to_window(window, qr)
        return_value, frame = webcam.read()
        img = convert_cv2_frame_to_pil_image(frame)
        detected_qr = decode(img)
        if detected_qr:
            # TODO: exfil should plug in here
            data = detected_qr[0].data.decode('utf-8')
            print(data)

if __name__ == "__main__":
    main()