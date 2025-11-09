from tkinter import *
import tkinter.font as tkFont

def center_window(window):
    window.update_idletasks()

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width - 750)//2
    y = (screen_height - 250)//2

    window.geometry(f"{750}x{250}+{x}+{y}")

root = Tk()
root.title("Dino Game")
center_window(root)
root.resizable(False, False)
root.attributes("-topmost", True)
root.update()
root.attributes("-topmost",False)

font = tkFont.Font(family="Arial", size = 25, weight="bold")
label = Label(root, text = "press the spacebar to start",font=font)
label.pack(anchor = "center")

root.mainloop()