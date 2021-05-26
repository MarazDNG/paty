# importing only those functions which
# are needed
import tkinter as tk
from tkinter import Frame
# creating tkinter window

BUTTON_COUNT = 5

root = tk.Tk()


frame1 = tk.Frame(root,width=1000, height=10)
#frame2 = tk.Frame(root, width=50, height = 50, background="#b22222")

tk.Button(frame1).place(x=10, y=10)
frame1.pack()
frame1['height'] = 100
#frame2.place(relx=.5, rely=.5, anchor="c")

root.mainloop()
