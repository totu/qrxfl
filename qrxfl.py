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

def draw_image_to_canvas(canvas, img, size=2):
    """Takes in canvas and image."""
    sides = [int(x*size) for x in img.size]
    img = img.resize((sides[0], sides[1]))
    image = ImageTk.PhotoImage(img)
    canvas.create_image(sides[0]/2, sides[1]/2, image=image)

def convert_cv2_frame_to_pil_image(frame):
    """takes in array frame from cv2 video capture and return it as PIL image"""
    cv2img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(cv2img)
    return img

def main():
    window = Tk()
    webcam = cv2.VideoCapture(0)
    data = 'jotain ihan muuta'
    last_data = None
    return_value = True

    # Loop while we get images from webcamera
    while return_value:
        for child in window.winfo_children():
            child.destroy()
        return_value, frame = webcam.read()
        canvas = Canvas(window, width=2000, height=1000)

        # make qr code, resize and draw
        qr = create_qr(data)
        qr = qr.resize((500, 500))
        qr = ImageTk.PhotoImage(qr)
        canvas.create_image(700, 500/2, image=qr)

        # convert webcame to image, resize and draw
        img = convert_cv2_frame_to_pil_image(frame)
        pic = img.resize((int(1920/8), int(1480/8)))
        pic = ImageTk.PhotoImage(pic)
        canvas.create_image(1200, 600, image=pic, anchor="nw")

        # detect for qr codes from webcam
        detected_qr = decode(img)
        canvas.pack()
        window.update_idletasks()
        window.update()
        if detected_qr:
            # TODO: exfil should plug in here
            for qr in detected_qr:
                qr_data = qr.data.decode('utf-8')
                if qr_data != last_data:
                    last_data = qr_data
                    data = "{}asd".format(last_data)

        # draw canvas and shit

if __name__ == "__main__":
    main()