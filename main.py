# -*- coding: utf-8 -*-
"""
Created on Sun Jul 23 03:35:45 2023

@author: Leander
"""

DEBUG = 1 #None

from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext

from encrypt import encInData
from encrypt import encOutData
from encrypt import RlrpEncrypt

class RlrpEncryptionGUI:
    def __init__(self, master):
        '''GUI SETUP'''
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
        
        self.sessionKey = StringVar()
        self.privateKey = StringVar()
        self.lastKey = StringVar()

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
        eSessionKey = Entry(sessionFrame, width=66, textvariable=self.sessionKey)
        ePrivateKey = Entry(sessionFrame, width=66, textvariable=self.privateKey)
        eSessionKey.grid(column=1, row=0)
        ePrivateKey.grid(column=1, row=1)
        #ePrivateKey.insert(END, '0000000000000000000000000000000000000000000000000000000000000000')
        Label(sessionFrame, text='Last used key').grid(column=0, row=2)
        eLastKey = Entry(sessionFrame, width=66, textvariable=self.lastKey)
        eLastKey.grid(column=1, row=2)
        btnConfirm = Button(sessionFrame, text="Confirm keys", command=self.confirmKey).grid(column=0, row=3)
        btnReset = Button(sessionFrame, text="Reset last used key", command=self.resetLastKey).grid(column=1, row=3)

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
        dropDataEncIn = OptionMenu(tabEncrypt, clickedDataEncIn, *dataTypeOptions, command=self.dataEncInEncoding).grid(column=1, row=0)
        self.eDataEncIn = scrolledtext.ScrolledText(tabEncrypt, wrap=WORD, width=66, height=8)
        self.eDataEncIn.grid(column=0, row=1, columnspan=2)
        btnEncrypt = Button(tabEncrypt, text='Encrypt', command=self.encrypt).grid(column=0, row=2, columnspan=2)
        Label(tabEncrypt, text='Encrypted data').grid(column=0, row=3)
        clickedDataEncOut = StringVar()
        clickedDataEncOut.set("UTF-8")
        dropDataEncOut = OptionMenu(tabEncrypt, clickedDataEncOut, *dataTypeOptions, command=self.dataEncOutEncoding).grid(column=1, row=3)
        self.tDataEncOut = scrolledtext.ScrolledText(tabEncrypt, wrap=WORD, width=66, height=8)
        self.tDataEncOut.grid(column=0, row=4, columnspan=2)

        # Decrypt tab
        #   Input datatype display
        #   Input data textfield
        #   Decrypt button
        #   Output datatype display
        #   Output data textfield
        Label(tabDecrypt, text='Encrypted Data').grid(column=0, row=0)
        clickedDataDecIn = StringVar()
        clickedDataDecIn.set("UTF-8")
        dropDataDecIn = OptionMenu(tabDecrypt, clickedDataDecIn, *dataTypeOptions, command=self.dataDecInEncoding).grid(column=1, row=0)
        self.eDataDecIn = scrolledtext.ScrolledText(tabDecrypt, wrap=WORD, width=66, height=8)
        self.eDataDecIn.grid(column=0, row=1, columnspan=2)
        btnDecrypt = Button(tabDecrypt, text='Decrypt', command=self.decrypt).grid(column=0, row=2, columnspan=2)
        Label(tabDecrypt, text='Decrypted data').grid(column=0, row=3)
        clickedDataDecOut = StringVar()
        clickedDataDecOut.set("UTF-8")
        dropDataDecOut = OptionMenu(tabDecrypt, clickedDataDecOut, *dataTypeOptions, command=self.dataDecOutEncoding).grid(column=1, row=3)
        self.tDataDecOut = scrolledtext.ScrolledText(tabDecrypt, wrap=WORD, width=66, height=8)
        self.tDataDecOut.grid(column=0, row=4, columnspan=2)

    '''FUNCTIONS'''
    def confirmKey(self):
        TAG="RlrpEncryptionGUI.confirmKey"
        if DEBUG: print(TAG, "confirm")
        if DEBUG: print(TAG, "sessionKey:", self.sessionKey.get())
        if DEBUG: print(TAG, "privateKey:", self.privateKey.get())
        if DEBUG: print(TAG, "lastKey:", self.lastKey.get())

    def resetLastKey(self):
        TAG="RlrpEncryptionGUI.resetLastKey"

        self.lastKey.set(self.sessionKey.get())

    def encrypt(self):
        TAG="RlrpEncryptionGUI.encrypt"
        if DEBUG: print(TAG, "self.eDataEncIn", bytearray(self.eDataEncIn.get("1.0",'end-1c'),'utf-8').hex())
        if DEBUG: print(TAG, "self.eDataEncIn", self.eDataEncIn.get("1.0",'end-1c'))
        if DEBUG: print(TAG, "lastKey", self.lastKey.get().encode())                       #interpret string as bytearray
        if DEBUG: print(TAG, "privateKey", self.privateKey.get().encode())                 #interpret string as bytearray

        input = encInData(self.eDataEncIn.get("1.0",'end-1c'), self.lastKey.get().encode(), self.privateKey.get().encode())
        RlrpEncrypt()
        output = RlrpEncrypt.encrypt(self, input)
        self.tDataEncOut.delete('1.0', END)
        self.tDataEncOut.insert(INSERT, bytes.fromhex(hex(output.data)[2:]).decode('unicode_escape'))   #hex(output.data)) //TODO align to encoding dropdown
        self.lastKey.set(bytes.fromhex(f'{output.key:x}').decode('utf-8'))                              #hex(output.key))  //TODO align to encoding dropdown

    def decrypt(self):
        TAG="RlrpEncryptionGUI.decrypt"
        if DEBUG: print(TAG, "decrypt")    

    def dataEncInEncoding(self, value):
        TAG="RlrpEncryptionGUI.dataEncInEncoding"
        if DEBUG: print(TAG, "dataEncInEncoding", value)

    def dataEncOutEncoding(self, value):
        TAG="RlrpEncryptionGUI.dataEncOutEncoding"
        if DEBUG: print(TAG, "dataEncOutEncoding", value)

    def dataDecInEncoding(self, value):
        TAG="RlrpEncryptionGUI.dataDecInEncoding"
        if DEBUG: print(TAG, "dataDecInEncoding", value)

    def dataDecOutEncoding(self, value):
        TAG="RlrpEncryptionGUI.dataDecOutEncoding"
        if DEBUG: print(TAG, "dataDecOutEncoding", value)

root = Tk()
rlrpEncryptionGUI = RlrpEncryptionGUI(root)
root.mainloop()