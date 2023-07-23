# -*- coding: utf-8 -*-
"""
Created on Sun Jul 23 03:35:45 2023

@author: Leander
"""

from tkinter import *
from tkinter import ttk

root = Tk()
frm = ttk.Frame(root, padding=10)
frm.grid()

Label(frm, text='Session Key').grid(column=0, row=0)
Label(frm, text='Private Key(optional)').grid(column=0, row=1)
Label(frm, text='Last used key').grid(column=0, row=2)
Label(frm, text='Data').grid(column=0, row=3)
e1 = Entry(frm, width=66)
e2 = Entry(frm, width=66)
e2.insert(END, '0000000000000000000000000000000000000000000000000000000000000000')
e3 = Entry(frm, width=66)
e4 = Entry(frm, width=66)
e1.grid(column=1, row=0)
e2.grid(column=1, row=1)
e3.grid(column=1, row=2)
e4.grid(column=1, row=2)
btnEncrypt = Button(frm, text='Encrypt').grid(column=0, row=3, columnspan=2)

# tk.Label(frm, text="Hello World!").grid(column=0, row=0)
# tk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)

root.mainloop()