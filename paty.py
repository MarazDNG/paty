#
# IT IS NECESSARY TO USE .pack() INSTEAD OF .place()
# TOP PRIORITY!!!
#

import tkinter
from tkinter import font, Frame, ttk
from tkinter import *
from Processed_file_data import (Processed_line,
                                 Processed_file_data,)
from random import shuffle

OPTION = 0


root = tkinter.Tk()
root.geometry('700x350')

BUTTON_COUNT = 5
CANVAS_WIDTH = 150
FRAME_OFFSET = 10
F1_WIDTH = 300
button_font = font.Font(size=12)

mainframe = Frame(root)
mainframe.place(relx=0.5, rely=0.5, anchor=CENTER)

wordsframe = Frame(mainframe)
wordsframe.pack()

checkframe = Frame(mainframe)
checkframe.pack(side=TOP)

frame1 = Frame(wordsframe, width=F1_WIDTH, height=150)
frame1.pack(expand=False, side=LEFT)

frame2 = Frame(wordsframe, width=CANVAS_WIDTH, height=150)
frame2.pack(side=LEFT)

frame3 = Frame(wordsframe, width=F1_WIDTH, height=150)
frame3.pack(side=LEFT)

cvs = tkinter.Canvas(frame2, width=CANVAS_WIDTH)
cvs.place(x=0, y=0)

connections_list = []
vocab = []
active_button = None

buttons = [[], []]
red_lines = []
checked_flag = 0

submit_btn = tkinter.Button(checkframe, text='check')
submit_btn.pack(side=TOP)
submit_btn['font'] = button_font
submit_btn['command'] = lambda: submit()


def create_buttons():
    """Create buttons and assign them command."""
    global buttons
    for i in range(BUTTON_COUNT):
        btn1 = Button_L()
        btn2 = Button_R()
        btn1.btn['command'] = lambda btn1=btn1: button_event(btn1)
        btn2.btn['command'] = lambda btn2=btn2: button_event(btn2)
        btn1.btn['font'] = button_font
        btn2.btn['font'] = button_font
        buttons[0].append(btn1)
        buttons[1].append(btn2)
        frame1['height'] = buttons[0][0].btn.winfo_reqheight() * BUTTON_COUNT
        frame3['height'] = buttons[0][0].btn.winfo_reqheight() * BUTTON_COUNT


def remove_red_lines():
    global red_lines
    for line in red_lines:
        cvs.after(0, cvs.delete, line)
    red_lines = []


class Connection():
    def __init__(self, btn1, btn2):
        self.left_btn = btn1
        self.right_btn = btn2
        self.buttons = {btn1, btn2}
        self.line_id = connect_buttons(btn1, btn2)


class Button():
    def __init__(self):
        self.text = None
        self.btn = tkinter.Button()
        self.command = None
        self.x = 0
        self.y = 0

    def command(self, cmd):
        self.command = cmd
        self.btn['command'] = cmd

    def txt(self, text):
        self.text = text
        self.btn['text'] = text

    def place(self, x, y):
        self.btn.place(x=x, y=y)
        self.x = x
        self.y = y


class Button_R(Button):
    def __init__(self):
        Button.__init__(self)
        self.btn = tkinter.Button(frame3)


class Button_L(Button):
    def __init__(self):
        Button.__init__(self)
        self.btn = tkinter.Button(frame1)


def remove_connections():
    global connections_list
    for conn in connections_list:
        cvs.after(0, cvs.delete, conn.line_id)
    connections_list = []


def add_connection(left, right):
    new_connection = Connection(left, right)
    merge_connection(new_connection)



def merge_connection(connection):
    """Remove any similiar connections in connection_list
    and append connection in argument.
    """
    i = len(connections_list) - 1
    while i >= 0:
        if similiar(connections_list[i], connection):
            cvs.after(0, cvs.delete, connections_list[i].line_id)
            del connections_list[i]
        i -= 1
    connections_list.append(connection)


def similiar(conn1, conn2):
    """Finds out if 2 connection have at least one common button."""
    if conn1.left_btn in conn2.buttons:
        return 1
    if conn1.right_btn in conn2.buttons:
        return 1
    return 0


def button_event(btn):
    """Called when button with word is pressed."""
    global active_button
    if (active_button is None) or (type(btn) is type(active_button)):
        active_button = btn
    else:
        if isinstance(btn, Button_L):
            add_connection(btn, active_button)
        else:
            add_connection(active_button, btn)
        active_button = None


def fill_buttons():
    """Give buttons text."""
    global vocab
    global buttons
    for i in range(BUTTON_COUNT):
        # print(len(buttons))
        # print(len(vocab))
        buttons[0][i].txt(vocab[i].left)
        buttons[1][i].txt(vocab[i].right)


def connect_buttons(btn1, btn2, *args):
    """Third argument is color."""
    # make Line calculations
    if len(args) == 0:
        return cvs.create_line(0, btn1.y + FRAME_OFFSET,
                               CANVAS_WIDTH, btn2.y + FRAME_OFFSET)
    else:
        return cvs.create_line(0, btn1.y + FRAME_OFFSET,
                               CANVAS_WIDTH, btn2.y + FRAME_OFFSET,
                               fill=args[0])


def place_buttons():
    arr_04 = [0, 1, 2, 3, 4]
    shuffle(arr_04)
    for i in range(BUTTON_COUNT):
        buttons[0][i].place(F1_WIDTH - buttons[0][i].btn.winfo_reqwidth(),
                            buttons[0][0].btn.winfo_reqheight() * i)
        buttons[1][arr_04[i]].place(0, buttons[0][0].btn.winfo_reqheight() * i)


def check_answers():
    global data

    for i in range(BUTTON_COUNT):
        if not is_correct(i):
            red_lines.append(
                connect_buttons(buttons[0][i], buttons[1][i], 'red'))
            if OPTION == 0:
                vocab[i].streak = 0
        else:
            if OPTION == 0:
                vocab[i].streak += 1
    if OPTION == 0:
        data.update_streaks_in_chunk(vocab)
        data.update_chunk()


def is_correct(index):
    """Check if there exists a connection for
    a pair of buttons on this index.
    """
    for conn in connections_list:
        if ({buttons[0][index].text, buttons[1][index].text} ==
                {conn.left_btn.text, conn.right_btn.text}):
            return 1
    return 0


def load_vocab():
    global vocab
    # print(len(data.chunk_words_list))
    if OPTION == 0:
        vocab = data.select_from_chunk_words(BUTTON_COUNT)
    elif OPTION == 1:
        vocab = data.select_from_all_words(BUTTON_COUNT)

def submit():
    global checked_flag
    if checked_flag == 0:
        check_answers()
        submit_btn['text'] = 'next'
        checked_flag = 1
    else:
        remove_red_lines()
        load_vocab()
        fill_buttons()
        remove_connections()
        place_buttons()
        submit_btn['text'] = 'check'
        checked_flag = 0


with open('vocabulary_de.txt', 'r', encoding='utf-8') as f:
    lines = f.read()
lines = lines.split('\n')

data = Processed_file_data(lines)

create_buttons()
load_vocab()
fill_buttons()
place_buttons()


root.mainloop()

data.save_data()
