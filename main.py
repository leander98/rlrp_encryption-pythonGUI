# -*- coding: utf-8 -*-
"""
Created on Sun Jul 23 03:35:45 2023

@author: Leander
"""

from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext

class RlrpEncryptionGUI:
    def __init__(self, master):
        self.master = master
        master.title("Random Length Random Padding - GUI client")

        frm = ttk.Frame(master, padding=10)
        frm.grid()

        dataTypeOptions = [
            'ASCII UTF-8',
            'ASCII ISO-8859-1',
            'HEX',
            'BIN',
        ]

        # Session Groupbox
        #   (pulic) session key
        #   private session key - optional
        #   Display of last used key - important for next transmission and data encryption/decryption - MUST be identical on both clients!
        #   confirm keys
        #   reset session - needed when last key is not identical between on both clients
        sessionFrame = LabelFrame(frm, text="Session")
        sessionFrame.grid(column=0, row=0)
        Label(sessionFrame, text='Session Key').grid(column=0, row=0)
        Label(sessionFrame, text='Private Key(optional)').grid(column=0, row=1)
        eSessionKey = Entry(sessionFrame, width=66)
        ePrivateKey = Entry(sessionFrame, width=66)
        eSessionKey.grid(column=1, row=0)
        ePrivateKey.grid(column=1, row=1)
        ePrivateKey.insert(END, '0000000000000000000000000000000000000000000000000000000000000000')
        Label(sessionFrame, text='Last used key').grid(column=0, row=2)
        eLastKey = Entry(sessionFrame, width=66)
        eLastKey.grid(column=1, row=2)
        btnConfirm = Button(sessionFrame, text="Confirm keys").grid(column=0, row=3)
        btnReset = Button(sessionFrame, text="Reset last used key").grid(column=1, row=3)

        # Transmission groupbox
        #   Encrypt and Decrypt sub tabs
        transmissionFrame = LabelFrame(frm, text="Transmission")
        transmissionFrame.grid(column=0, row=1)
        tabControl = ttk.Notebook(transmissionFrame)
        tabEncrypt = ttk.Frame(tabControl)
        tabDecrypt = ttk.Frame(tabControl)
        tabControl.add(tabEncrypt, text='Encrypt')
        tabControl.add(tabDecrypt, text='Decrypt')
        tabControl.pack(expand = 1, fill='both')

        # Encrypt tab
        #   Input datatype display
        #   Input data textfield
        #   Encrypt button
        #   Output datatype display
        #   Output data textfield
        Label(tabEncrypt, text='Data').grid(column=0, row=0)
        clickedDataEncIn = StringVar()
        clickedDataEncIn.set("UTF-8")
        dropDataEncIn = OptionMenu(tabEncrypt, clickedDataEncIn, *dataTypeOptions).grid(column=1, row=0)
        eDataEncIn = scrolledtext.ScrolledText(tabEncrypt, wrap=WORD, width=66, height=8)
        eDataEncIn.grid(column=0, row=1, columnspan=2)
        btnEncrypt = Button(tabEncrypt, text='Encrypt').grid(column=0, row=2, columnspan=2)
        Label(tabEncrypt, text='Encrypted data').grid(column=0, row=3)
        clickedDataEncOut = StringVar()
        clickedDataEncOut.set("UTF-8")
        dropDataEncOut = OptionMenu(tabEncrypt, clickedDataEncOut, *dataTypeOptions).grid(column=1, row=3)
        tDataEncOut = scrolledtext.ScrolledText(tabEncrypt, wrap=WORD, width=66, height=8)
        tDataEncOut.grid(column=0, row=4, columnspan=2)

        # Decrypt tab
        #   Input datatype display
        #   Input data textfield
        #   Decrypt button
        #   Output datatype display
        #   Output data textfield
        Label(tabDecrypt, text='Encrypted Data').grid(column=0, row=0)
        clickedDataDecIn = StringVar()
        clickedDataDecIn.set("UTF-8")
        dropDataDecIn = OptionMenu(tabDecrypt, clickedDataDecIn, *dataTypeOptions).grid(column=1, row=0)
        eDataEncIn = scrolledtext.ScrolledText(tabDecrypt, wrap=WORD, width=66, height=8)
        eDataEncIn.grid(column=0, row=1, columnspan=2)
        btnEncrypt = Button(tabDecrypt, text='Decrypt').grid(column=0, row=2, columnspan=2)
        Label(tabDecrypt, text='Decrypted data').grid(column=0, row=3)
        clickedDataDecOut = StringVar()
        clickedDataDecOut.set("UTF-8")
        dropDataDecOut = OptionMenu(tabDecrypt, clickedDataDecOut, *dataTypeOptions).grid(column=1, row=3)
        tDataEncOut = scrolledtext.ScrolledText(tabDecrypt, wrap=WORD, width=66, height=8)
        tDataEncOut.grid(column=0, row=4, columnspan=2)

root = Tk()
rlrpEncryptionGUI = RlrpEncryptionGUI(root)
root.mainloop()