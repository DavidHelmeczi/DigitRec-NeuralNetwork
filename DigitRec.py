import tkinter as tk
from tkinter import *
from scipy.ndimage import zoom
import numpy as np
import win32gui
from PIL import ImageGrab
#import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model

model = load_model('final_model.h5')


def predict_digit(img):
    img = img.resize((28, 28))
    img = img.convert('L')
    img = np.array(img)
    img = 255 - img
    img = crop_image(img)
    #plt.imshow(img, cmap = 'binary')
    img = np.reshape(img, (1, 28, 28, 1))
    img = img / 255.0
    res = model.predict([img])[0]
    #plt.show()
    return res #np.argmax(res), max(res)



felso = also = jobb = bal = 0


def find_top(img):
    for i in range(0, 28):
        for j in range(0, 28):
            if img[i][j] > 0:
                felso = i
                return felso


def find_bottom(img):
    for i in range(27, -1, -1):
        for j in range(27, -1, -1):
            if img[i][j] > 0:
                also = i
                return also


def find_left(img):
    for i in range(0, 28):
        for j in range(0, 28):
            if img[j][i] > 0:
                bal = i
                return bal


def find_right(img):
    for i in range(27, -1, -1):
        for j in range(27, -1, -1):
            if img[j][i] > 0:
                jobb = i
                return jobb


def crop_image(img):
    felso = find_top(img)
    also = find_bottom(img)
    bal = find_left(img)
    jobb = find_right(img)
    img = img[felso:, bal:]
    img = img[:-(28 - also), :-(28 - jobb)]

    if img.shape[1] < 7 and img.shape[0] < 7:
        img = zoom(img, 4)

    elif img.shape[1] < 13 and img.shape[0] < 13:
        img = zoom(img, 2)

    while img.shape[1] != 28:
        if img.shape[1] != 28:
            img = np.insert(img, 0, 0, axis=1)
        else:
            break
        if img.shape[1] != 28:
            img = np.insert(img, img.shape[1], 0, axis=1)
        else:
            break

    while img.shape[0] != 28:
        if img.shape[0] != 28:
            img = np.insert(img, 0, 0, axis=0)
        else:
            break
        if img.shape[0] != 28:
            img = np.insert(img, img.shape[0], 0, axis=0)
        else:
            break

    return img


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.x = self.y = 0

        self.canvas = tk.Canvas(self, width=300, height=300, bg="white", cursor="cross")
        self.label = tk.Label(self, text="Draw a number", font=("Helvetica", 25))
        self.classify_btn = tk.Button(self, text="Recognize", command=self.classify_handwriting)
        self.button_clear = tk.Button(self, text="Clear", command=self.clear_all)

        self.canvas.grid(row=0, column=0, pady=2, sticky=W, )
        self.label.grid(row=0, column=1, pady=2, padx=2)
        self.classify_btn.grid(row=1, column=1, pady=2, padx=2)
        self.button_clear.grid(row=1, column=0, pady=2)

        self.canvas.bind("<B1-Motion>", self.draw_lines)

    def clear_all(self):
        self.canvas.delete("all")

    def classify_handwriting(self):
        HWND = self.canvas.winfo_id()
        rect = win32gui.GetWindowRect(HWND)
        a, b, c, d = rect
        rect = (a + 4, b + 4, c - 4, d - 4)
        im = ImageGrab.grab(rect)

        re = predict_digit(im)
        digit = np.argmax(re)
        acc = max(re)
        re2 = re
        re2[np.argmax(re)] = 0
        digit2 = np.argmax(re2)
        acc2 = max(re2)
        self.label.configure(
            text=str(digit) + ', ' + str(int(acc * 100)) + '%' + '\n' + str(digit2) + ', ' + str(int(acc2 * 100 + 1)) + '%',
            font=("Helvetica", 48))

    def draw_lines(self, event):
        self.x = event.x
        self.y = event.y
        r = 10
        self.canvas.create_oval(self.x - r, self.y - r, self.x + r, self.y + r, fill='black')


app = App()
mainloop()
