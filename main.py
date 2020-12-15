from tkinter import *
import os
import time
import random
from tkinter import font
window = Tk()
window.title("Memory")


timer = 0
images = ["BRAIN", "GUT", "HEART", "KIDNEYS",
          "LIVER", "LUNG", "STOMACH", "TEETH"]*2
open_now = 0
right = 0
gl_time = time.time()


class Card():
    def __init__(self, image, pos, window):
        self.window = window
        self.image = image
        self.start_image = "CARD"
        self.pos = pos
        self.is_open = False
        self.is_life = True
        self.path = os.path.join(BASE_DIR, f"IMAGES\\{self.start_image}.png")
        self.img = PhotoImage(file=self.path)
        self.obj = Label(window, image=self.img)
        self.obj.grid(column=self.pos[0], row=self.pos[1]+1)
        self.obj.bind('<Button-1>', self.open_card)

    def open_card(self, event):
        global open_now
        if self.is_life and self.is_open == False:
            if open_now < 2:
                self.path = os.path.join(BASE_DIR, f"IMAGES\\{self.image}.png")
                self.img = PhotoImage(file=self.path)
                self.obj.config(image=self.img)
                open_now += 1
                self.is_open = True

    def close_card(self):
        if self.is_life:
            self.path = os.path.join(
                BASE_DIR, f"IMAGES\\{self.start_image}.png")
            self.img = PhotoImage(file=self.path)
            self.obj.config(image=self.img)
            self.is_open = False

    def kill(self):
        if self.is_life:
            self.is_life = False
            self.path = os.path.join(BASE_DIR, f"IMAGES\\FINISH.png")
            self.img = PhotoImage(file=self.path)
            self.obj.config(image=self.img)


def loop():
    global open_now, timer, right, gl_time
    if right != 16:
        if open_now == 2:
            if timer == 500:
                get_images = []
                for i in lbls:
                    if i.is_open == True:
                        get_images.append(i)
                    i.close_card()
                if get_images[0].image == get_images[1].image:
                    for i in get_images:
                        i.kill()
                        right += 1

                open_now = 0
                timer = 0
            else:
                timer += 1
        window.after(1, loop)
    else:
        seconds = int((abs(time.time() - gl_time)))
        sec = str(int(seconds % 60))
        if len(sec) == 1:
            sec = '0' + sec
        minutes = str((int(seconds//60) % 60))
        if len(minutes) == 1:
            minutes = '0' + minutes
        hours = int((seconds//60)//60)
        win_lbl["text"] = "%d:%s:%s" % (hours, minutes, sec)
        win_lbl.grid(row=0, column=0, columnspan=4)


win_lbl = Label(window, text=0, font='Bahnschrift 30')
lbls = []
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
for i in range(4):
    for j in range(4):
        rand_image = random.choice(images)
        lbls.append(Card(rand_image, (i, j), window))
        images.remove(rand_image)

window.after(1, loop)
window.mainloop()
