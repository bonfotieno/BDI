# Developer: Bonface Otieno; bonnyotieno9@gmail.com
# Botien Driver Installer

# Botien Driver Installer Description
# ===================================
# Botien Driver Installer is a windows OS based software that saves you from that headache of installing device drivers manually
# by automating the whole process fo you. You just have to specify the .inf setup file then the software will do the installation.
# Driver information is also displayed before installation.
# In addition to that it also shows you installed device drivers on the "Available Devices" tab.

"""
Botien Driver Installer License
===============================
Developer: Bonface Otieno; bonnyotieno9@gmail.com
===============================

Except where otherwise noted, all of the documentation and software included in the Botien Driver Installer
package is copyrighted by Bonface Otieno.

Copyright (C) 2021 Bonface Otieno. All rights reserved.

This software is provided "as-is," without any express or implied warranty. In no event shall the
author be held liable for any damages arising from the use of this software.

Permission is granted to anyone to use this software for any purpose, including commercial
applications, and to alter and redistribute it, provided that the following conditions are met:

1. All redistributions of source code files must retain all copyright notices that are currently in
   place, and this list of conditions without modification.

2. All redistributions in binary form must retain all occurrences of the above copyright notice and
   web site addresses that are currently in place (for example, in the About boxes).

3. The origin of this software must not be misrepresented; you must not claim that you wrote the
   original software. If you use this software to distribute a product, an acknowledgment in the
   product documentation would be appreciated but is not required.

4. Modified versions in source or binary form must be plainly marked as such, and must not be
   misrepresented as being the original software.


Bonface Otieno
bonnyotieno9@gmail.com
+254794317784
"""

from tkinter import Tk, filedialog, Frame, Button, Scrollbar, Label, PhotoImage, Canvas, Entry, Message, \
    VERTICAL, ALL, END, IntVar, Radiobutton, messagebox
from subprocess import Popen, PIPE
from os import chdir, getcwd, remove
import shutil
from json import loads
from psutil import process_iter
import xml.etree.ElementTree as ET
from threading import Thread
from webbrowser import open as donateWebPage


class IntegrityCheck(Frame):
    def __init__(self, root):
        self.root = root
        self.root.attributes("-topmost", True)
        self.root.overrideredirect(1)
        self.root.config(bg='#c3c3c3')
        width = 430
        height = 320
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.root.geometry("%dx%d+%d+%d" % (width, height, x, y))
        Frame.__init__(self, self.root, bg='#c3c3c3')
        self.logo = PhotoImage(file="10/logo.png")
        self.logoLabel = Label(self, image=self.logo, bd=0)
        self.label = Label(self, text="If the driver you want to install is not digitally signed, windows10 won't "
                                      "install it.\nChoose one of these options to disable driver integrity check:",
                           justify='left', bg='#c3c3c3')
        self.option = IntVar()
        self.option1 = Radiobutton(self, text="I want to disable driver signature enforcement permanently\n"
                                              "[NOT RECOMMENDED:Some versions of windows doesn't support it]",
                                   font=('Calibri', 10), bg='#c3c3c3', justify='left', var=self.option,
                                   command=self.option1command, value=1)
        self.option2 = Radiobutton(self, text='I want to disable driver signature enforcement Temporarily\n[You will '
                                              'have to do it manually by: Shift+Restart→Troubleshoot→\nAdvanced '
                                              'options→Startup Settings→Restart→Press "7" or "F7"]',
                                   font=('Calibri', 10), justify='left', bg='#c3c3c3', var=self.option,
                                   command=self.option2command, value=2)
        self.option.set(1)
        self.bt1 = Button(self, text="Disable and Restart", padx=15, relief='flat', bd=0,
                          command=self.disable_and_restart,
                          bg='#00a8f3', fg='#ffffff')
        self.bt2 = Button(self, text="I already did that", padx=15, relief='flat', bd=0, command=self.bt2command,
                          bg='#00a8f3', fg='#ffffff')
        self.quit = Button(self, text="Quit", padx=15, relief='flat', bd=0, command=self.quit_command,
                           bg='#00a8f3', fg='#ffffff')
        self.logoLabel.grid(row=0, columnspan=3, pady=(0, 0))
        self.label.grid(row=1, columnspan=3, sticky='w')
        self.option1.grid(row=2, columnspan=3, padx=(20, 0), sticky='w')
        self.option2.grid(row=3, columnspan=3, padx=(20, 0), sticky='w')
        self.bt1.grid(row=4, column=0, sticky='w', padx=(10, 0), pady=(10, 0))
        self.quit.grid(row=4, column=1, sticky='e', padx=(0, 10), pady=(10, 0))
        self.bt2.grid(row=4, column=2, sticky='e', padx=10, pady=(10, 0))

    def option2command(self):
        self.bt1.config(state='disabled', bg='#00a8f3')

    def option1command(self):
        self.bt1.config(state='normal')

    def quit_command(self):
        self.root.destroy()

    def bt2command(self):
        self.destroy()
        Root(app)

    def disable_and_restart(self):
        Popen(
            r'bcdedit.exe /set nointegritychecks on')  # this line runs well after raising the privileges in app.exe.manifest file
        Popen(r'shutdown /r /t 0')


class Root(object):
    contentFrame = None  # static variable to be accessed in Dashboard class

    def __init__(self, root):
        Thread(target=AvailableDevices.scan).start()
        width = 700
        height = 550
        self.root = root
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.root.attributes("-topmost", False)
        self.root.geometry("%dx%d+%d+%d" % (width, height, x, y))
        self.root.config(bg='#fafafa')
        self.root.overrideredirect(0)
        self.root.resizable(0, 0)
        self.root.iconbitmap(r'10\logo.ico')
        self.root.title('BDInstaller - Botien Softwares')
        contentFrame = Frame(self.root, bg='#fafafa')
        self.dashboard = Dashboard(self.root)
        self.dashboard.pack(side='left', fill='y')
        contentFrame.pack(side='left', fill='both')
        self.dashboard.homeCallback()


class Dashboard(Frame):
    def __init__(self, root):
        self.root = root
        self.content = None
        Frame.__init__(self, self.root, bg='#c3c3c3')
        self.logo = PhotoImage(file="10/logo.png")
        self.logolabel = Label(self, image=self.logo, bd=0)
        self.logolabel.grid(row=0, column=0, pady=(0, 0))
        self.canvas = Canvas(self, width=164, height=200, bg='#c3c3c3', highlightthickness=0)
        self.canvas.grid(row=1, column=0)
        self.canvas.create_line(0, 0, 164, 0, fill='#dce1ff')
        self.home = Button(self, text="Home", padx=55, pady=5, command=self.homeCallback, font=('Calibri', 14),
                           relief='flat', bd=0, bg='#c3c3c3', fg='#f9faff')
        self.canvas.create_window(81, 23, window=self.home)
        self.canvas.create_line(0, 45, 164, 45, fill='#dce1ff')
        self.available = Button(self, text="Available Devices", padx=12, pady=5, command=self.availableCallback,
                                font=('Calibri', 14), relief='flat', bd=0, bg='#c3c3c3', fg='#f9faff')
        self.canvas.create_window(81, 68, window=self.available)
        self.canvas.create_line(0, 90, 164, 90, fill='#dce1ff')
        self.donate = Button(self, text="Donate", command=self.donateCallback, padx=50, pady=5, font=('Calibri', 14),
                             relief='flat', bd=0, bg='#c3c3c3', fg='#f9faff')
        self.canvas.create_window(81, 113, window=self.donate)
        self.canvas.create_line(0, 135, 164, 135, fill='#dce1ff')

    def homeCallback(self):
        self.home.config(bg='#cfc3fe', state='disabled')
        if currentContent == 'available':
            self.available.config(bg='#c3c3c3', state='normal')
            self.content.destroy()
        elif currentContent == 'donate':
            self.donate.config(bg='#c3c3c3', state='normal')
            self.content.destroy()
        else:
            pass
        self.content = Home(Root.contentFrame)
        self.content.pack()

    def availableCallback(self):
        self.available.config(bg='#cfc3fe', state='disabled')
        if currentContent == 'home':
            self.home.config(bg='#c3c3c3', state='normal')
            self.content.destroy()
        elif currentContent == 'donate':
            self.donate.config(bg='#c3c3c3', state='normal')
            self.content.destroy()
        else:
            pass
        self.content = AvailableDevices(Root.contentFrame)
        self.content.pack()

    def donateCallback(self):
        self.donate.config(bg='#cfc3fe', state='disabled')
        if currentContent == 'home':
            self.home.config(bg='#c3c3c3', state='normal')
            self.content.destroy()
        elif currentContent == 'available':
            self.available.config(bg='#c3c3c3', state='normal')
            self.content.destroy()
        else:
            pass
        self.content = Donate(Root.contentFrame)
        self.content.pack()


class Donate(Frame):
    def __init__(self, root):
        global currentContent
        currentContent = 'donate'
        self.root = root
        Frame.__init__(self, self.root, bg='#fafafa')
        self.label = Label(self, wraplength=400,
                           text="One of the best ways to keep free softwares rocking is through donations."
                                " Kindly donate to support us. Thank you.", font=('Calibri', 15), bg='#fafafa',
                           fg='#00a8f3')
        self.button = PhotoImage(file="10/button.png")
        self.QRCode = PhotoImage(file="10/link.png")
        self.donateButton = Label(self, bg='#fafafa', image=self.button, bd=0)
        self.donateButton.bind('<Button-1>', lambda dummy=0: self.donate())
        self.QRLabel = Label(self, bg='#fafafa', image=self.QRCode, bd=0)
        self.label.grid(row=0, pady=(40, 0))
        self.donateButton.grid(row=1)
        self.QRLabel.grid(row=2, pady=(40, 0))

    def donate(self):
        donateWebPage('https://www.paypal.com/donate?hosted_button_id=N22AG78LDBTCG')


class AvailableDevices(Frame):
    def __init__(self, root):
        global currentContent
        currentContent = 'available'
        self.root = root
        Frame.__init__(self, self.root, bg='#fafafa')
        self.availablelogo = PhotoImage(file='10/available.png')
        self.availablelabel = Label(self, image=self.availablelogo, bd=0)
        self.label = Label(self, text='Available Devices In Your\nComputer', font=('Calibri', 26), bg='#fafafa',
                           fg='#50e5ff')
        self.rescan = Button(self, text="Rescan", command=self.rescan_callback, relief='flat', bd=0,
                             bg='#50e5ff', fg='#ffffff')
        self.Frame = Frame(self, bg='#f0f0f0')
        self.scrollbar = Scrollbar(self.Frame, background='#f0f0f0', relief='flat', orient=VERTICAL)
        self.canvas = Canvas(self.Frame, yscrollcommand=self.scrollbar.set, highlightthickness=0, width=520, height=350,
                             bg='#f0f0f0')
        self.canvas.pack(side='left')
        self.scrollbar.pack(side='right', fill='y')
        self.scrollbar.configure(command=self.canvas.yview)
        self.driverquery()

        self.availablelabel.grid(row=0, column=0, pady=(5, 5), padx=(20, 0), sticky='w')
        self.label.grid(row=0, column=1, sticky='w', padx=(0, 40))
        self.Frame.grid(row=1, columnspan=2)
        self.rescan.grid(row=2, column=1, sticky='e', pady=(30, 0), padx=(0, 50))

    def driverquery(self):
        global devicesAreScanned
        if devicesAreScanned is True:
            self.displaydevices()
        else:
            self.scan()
            self.displaydevices()

    def displaydevices(self):
        XBASE, YBASEkey, YBASEvalue, DISTANCE = 30, 15, 30, 45
        i = 0
        for key in devices:
            self.canvas.create_text((XBASE, YBASEkey + i * DISTANCE), anchor='w', text=key, fill='#7a7a7a',
                                    font=('Calibri', 13))
            self.canvas.create_text((XBASE, YBASEvalue + i * DISTANCE), anchor='w', text=devices[key],
                                    font=('Calibri', 12), fill='#9d9d9d')
            self.canvas.create_line(0, 45 + i * DISTANCE, 520, 45 + i * DISTANCE, fill='#e4e4e4')
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            i += 1
        self.canvas.create_text((XBASE, YBASEkey + i * DISTANCE), anchor='w',
                                text='Kindly Note:',
                                fill='#313ce0', font=('Calibri', 13))
        self.canvas.create_text((XBASE, 40 + i * DISTANCE), anchor='w',
                                text="If a device you are looking for is not in this list;\nPlug in the device or "
                                     "install it's driver and then hit 'Rescan'.",
                                font=('Calibri', 12), fill='#7a7a7a')
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def rescan_callback(self):
        global devicesAreScanned
        self.rescan.config(state='disabled')
        devicesAreScanned = False
        self.canvas.delete(ALL)
        self.driverquery()
        self.rescan.config(state='normal')

    @staticmethod
    def scan():
        global devices
        global devicesAreScanned
        output = (Popen(r'driverquery.exe /fo list', stdout=PIPE, shell=True).stdout.read()).decode('utf-8')
        # <===============creating a json object to hold the devices name from driver query output===============>
        output_list = output.split('\r')
        firstline = 1
        secondline = 2
        string = '{"Ignore'
        # <===================this loop extracts only the first and second line of each block====================>
        while firstline <= len(output_list) and secondline <= len(output_list):
            string = string + output_list[firstline]
            string = string + output_list[secondline]
            firstline += 5
            secondline += 5
        # <========================creating the dictionary now========================>
        string = string.replace('Module Name:       ', '", "')
        string = string.replace('Display Name:      ', '": "')
        string = string.replace('\n', '')
        string = string.replace('"Ignore",', '')
        string = string + '"}'
        devices = loads(string)
        devicesAreScanned = True


class Home(Frame):
    def __init__(self, root):
        global currentContent
        currentContent = "home"
        self.t1 = None
        self.t2 = None
        self.root = root
        Frame.__init__(self, self.root, bg='#fafafa')
        self.text = "Select the inf file for which you want to install the driver:"
        self.label = Label(self, font=('Calibri', 13), bg='#fafafa', fg='#50e5ff', text=self.text)
        self.filepath = Entry(self, bg='#ffffff', highlightthickness=1, text=inf_filename,
                              highlightbackground='#c3c3c3',
                              highlightcolor='#c3c3c3', width=65, relief='flat')
        self.filepath.delete(0, END)
        self.filepath.insert(0, inf_filename)
        self.browse = Button(self, text="Browse", command=self.browse_callback, padx=15, relief='flat', bd=0,
                             bg='#50e5ff', fg='#ffffff')
        self.installLabel = Label(self, text='Waiting for .inf file...', bg='#fafafa', pady=10)
        self.infoLabel = Canvas(self, bg='#fafafa', highlightthickness=0, width=536, height=30)
        self.infoLabel.create_text(75, 15, text='Driver information:', fill='#585858', font=('Calibri', 13))

        self.infoFrame = Frame(self, bg='#f0f0f0')
        self.scrollbar = Scrollbar(self.infoFrame, background='#f0f0f0', relief='flat', orient=VERTICAL)
        self.canvas = Canvas(self.infoFrame, yscrollcommand=self.scrollbar.set, width=515, height=350, bg='#f0f0f0')
        self.canvas.pack(side='left')
        self.scrollbar.pack(side='right', fill='y')
        self.scrollbar.configure(command=self.canvas.yview)
        self.messageinfo = Message(self.infoFrame, padx=30, bg='#f0f0f0', fg='#7a7a7a', text=driver_info, width=500)
        self.canvas.create_window(100, 100, window=self.messageinfo)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        self.install = Button(self, text="Install", state="disabled", padx=17, relief='flat', bd=0, bg='#50e5ff',
                              command=self.install_callback, fg='#ffffff')
        if driver_info != '':
            self.installLabel.config(text="Ready to install")
            self.install.config(state='normal')
        self.label.grid(row=0, column=0, columnspan=2, padx=(6, 0), pady=(6, 0), sticky='w')
        self.filepath.grid(row=1, column=0, padx=(8, 0), sticky='w')
        self.browse.grid(row=1, column=1, padx=(10, 0), sticky='w')
        self.installLabel.grid(row=2, column=0)
        self.infoLabel.grid(row=3, column=0, columnspan=2)
        self.infoFrame.grid(row=4, column=0, columnspan=2)
        self.install.grid(row=5, column=1, pady=(30, 0), padx=(0, 35))

    def browse_callback(self):
        global driver_info, inf_filename
        self.filepath.delete(0, END)
        inf_filename = filedialog.askopenfilename(filetypes=[('Setup information file', '.inf')])
        if inf_filename == '':
            self.messageinfo.config(text='')
        self.filepath.insert(0, inf_filename)
        if self.filepath.get() != '':
            self.installLabel.config(text='Ready to install')
            driver_info = (Popen(r'includes\verify.exe /info "' + self.filepath.get() + '"', stdout=PIPE,
                                 shell=True).stdout.read()).decode('utf-8')
            self.messageinfo.config(text=driver_info)
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            self.install.config(state='normal')

    def install_callback(self):
        global SetupFilePath
        self.installLabel.config(text='Installing Driver...')
        self.install.config(state='disabled')
        SetupFilePath = self.filepath.get()
        # =============================writing setup file path to dpinst.xml==========================================
        tree = ET.parse(r"includes\dpinst.xml")
        root = tree.getroot()
        root[4][0].set('path', ".\\" + SetupFilePath[SetupFilePath.rindex('/') + 1:])
        tree.write(r'includes\dpinst.xml')
        mainWorkingDir = getcwd()
        # =====threads -to make sure 'dpinst.xml' and 'bdi.exe' are copied to driver dir before bdi.exe executes======
        self.t1 = Thread(target=shutil.copy, args=[r"includes\dpinst.xml", SetupFilePath[0:SetupFilePath.rindex('/')]])
        self.t2 = Thread(target=shutil.copy, args=[r"includes\bdi.exe", SetupFilePath[0:SetupFilePath.rindex('/')]])
        try:
            self.t1.start(); self.t2.start()
            self.t1.join(); self.t2.join()  # this ensures all the files are copied before further execution
            chdir(SetupFilePath[0:SetupFilePath.rindex('/')])
            Popen('bdi.exe', shell=True)
            chdir(mainWorkingDir)
        except:
            messagebox.showwarning(title="I/O error", message="An Error Occured!")
        self.installLabel.config(text='Ready to install')
        self.install.config(state='normal')


def kill_app():
    global SetupFilePath
    for proc in process_iter():
        if proc.name() == "bdi.exe":
            proc.kill()
    if SetupFilePath != "":
        try:
            chdir(SetupFilePath[0:SetupFilePath.rindex('/')])
            remove("dpinst.xml")
            remove("bdi.exe")
        except:
            pass
    app.destroy()
    exit()


if __name__ == '__main__':
    SetupFilePath = ""  # variable is global to make it accessible to both home class and kill_app()
    devices = {}
    currentContent = ''
    devicesAreScanned = False  # i keep this this variable global so that it won't be destroyed when 'Frame' is destroyed
    driver_info = ''
    inf_filename = ''
    app = Tk()
    app.protocol('WM_DELETE_WINDOW', kill_app)
    IntegrityCheck(app).pack()
    app.mainloop()
