import sys
from tkinter import *
import tkinter.font as tkFont

def center_window(window):
    window.update_idletasks()

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width - 750)//2
    y = (screen_height - 250)//2

    window.geometry(f"{750}x{250}+{x}+{y}")

gameStarted = False
def on_space_press(event):
    global gameStarted
    if not bool(gameStarted):
        label.pack_forget()
        gameStarted = True
    else:
        print("jumping")

def on_escape_press(event):
    sys.exit()

root = Tk()
root.title("Dino Game")
center_window(root)
root.resizable(False, False)

#set window above everything else
root.attributes("-topmost", True)
#force it to process
root.update()
#allow it to be unfocused again
root.attributes("-topmost",False)

font = tkFont.Font(family="Arial", size = 25, weight="bold")
label = Label(root, text = "press the spacebar to start",font=font)
label.pack(anchor = "center")

root.bind("<space>", on_space_press)
root.bind("<Escape>", on_escape_press)
root.mainloop()