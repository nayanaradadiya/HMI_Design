#!/usr/bin/python3
import os
from sys import getsizeof
from pympler.asizeof import asizeof
from os import path
import tkinter
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from PIL import Image, ImageTk,ImageOps
import PIL
from time import perf_counter
import collections
import fnmatch
import time
import shutil
import serial
import struct
from binascii import hexlify
import threading
from threading import Timer
from wifi import *
from wifi import Cell,Scheme
import sqlite3
# from gpiozero import LED
from resources.modules.constant import *

# Touch_led=LED(23)
# Comm_led=LED(24)

# Here, we are creating our class, Window, and inheriting from the Frame
# class. Frame is a class from the tkinter module.
class Window(Frame):

    # Define settings upon initialization. Here you can specify
    def __init__(self, master=None):

        # Parameters that you want to send through the Frame class.
        Frame.__init__(self, master)

        # reference to the master widget, which is the tk window
        self.master = master

        #with that, we want to then run init_window, which doesn't yet exist
        self.init_window()
        # self.master.attributes()

    #Creation of init_window
    def init_window(self):
        # changing the title of our master widget
        self.master.title("Tarasvat Industrial Electronics")
        # Define directory for access images
        self.script_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
        self.resource_dir = os.path.join(self.script_dir,'resources/')
        self.test_dir = os.path.join(self.resource_dir,'test/')
        self.setting_dir = os.path.join(self.resource_dir,'setting/')
        self.hook_setting_dir = os.path.join(self.setting_dir,'hook/')
        self.design_setting_dir = os.path.join(self.setting_dir,'design/')
        self.harness_setting_dir = os.path.join(self.setting_dir,'harness/')
        self.setup_setting_dir = os.path.join(self.setting_dir,'setup/')
        self.files_dir = os.path.join(self.resource_dir,'files/')
        self.view_png_img = os.path.join(self.files_dir,'view_png.png')
        self.images_dir = os.path.join(self.resource_dir,'images/')
        self.pendrive_dir = '/media/pi'

        ### Start Global variables

        # Window width and height settings
        self.winWidth = 1024
        self.winHeight = 600
        self.menuHeight = 80
        self.frameHeight = self.winHeight - self.menuHeight
        self.thread_flg = 0

        # Predefine arrays
        self.topMenu = ['Info','Files','USB','Test','Settings','Reports','Wifi']
        self.keypad = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'C', '0', 'OK']
        self.harnessArr = [('Harness 1',1), ('Harness 2',2),('Harness 4',4)]
        self.selectDesignArr = [('Invert Design',0), ('Reverse Card',1)]
        self.weftSelectorArr = [
                            ('Weft Selector Disable',0),
                            ('Weft Selector Enable',1),
                            ('Weft Selector Enable with Sensor',2)]
        self.pickFindArr = [
                            ('Pick Find Disable',0),
                            ('Pick Find Enable-Forward Machine',1),
                            ('Pick Find Enable-Forward/Reverse Machine',2)]
        self.sensorPatternArr = [
                            ('Sensor Setup 1',1),
                            ('Sensor Setup 2',2),
                            ('Sensor Setup 3',3)]

        self.hooksArr = [
            'H0064 R02 C04',
            'H0048 R03 C02','H0072 R03 C03','H0096 R03 C04','H0144 R03 C06','H0192 R03 C08',
            'H0096 R04 C03','H0064 R04 C02','H0128 R04 C04','H0192 R04 C06','H0320 R04 C10',
            'H0160 R05 C04','H0240 R05 C06','H0320 R05 C08',
            'H0384 R06 C08','H0480 R05 C10',
            'H0448 R07 C08',
            'H0384 R08 C06','H0448 R08 C07','H0512 R08 C08','H0640 R08 C10','H0768 R08 C12','H0960 R08 C15',
            'H0480 R10 C06','H0640 R10 C08','H0800 R10 C10','H0960 R10 C12',
            'H0480 R12 C05','H0672 R12 C07','H0768 R12 C08','H0864 R12 C09','H0960 R12 C10','H1056 R12 C11',
            'H1152 R12 C12','H1248 R12 C13','H1344 R12 C14','H1440 R12 C15','H1536 R12 C16',

            'H0672 R14 C06','H0896 R14 C08','H1008 R14 C09','H1120 R14 C10','H1232 R14 C11','H1344 R12 C15',
            'H1456 R14 C13','H1568 R14 C14','H1680 R14 C15','H1792 R14 C16','H1904 R14 C17','H2016 R14 C18',
            'H2128 R14 C19','H2240 R14 C20','H2352 R14 C21','H2464 R14 C22','H2576 R14 C23','H2688 R14 C24',

            'H0640 R16 C05','H0896 R16 C07','H1024 R16 C08','H1152 R16 C09','H1280 R16 C10','H1408 R16 C11',
            'H1536 R16 C12','H1792 R16 C14','H1920 R16 C15','H2048 R16 C16','H2176 R16 C17','H2304 R16 C18',
            'H2432 R16 C19','H2688 R16 C21','H3072 R16 C24','H4992 R16 C39','H5376 R16 C42',

            'H4032 R24 C21','H5376 R24 C21'
            ]

        self.setting_menu = ['General','Design','Harness','Production','Features','Sensor Setup','Number of Hooks']

        self.report_menu = ['Shift Manage']

        ## Start Predefine variables
        # Info tab's variable
        self.DesignName = StringVar()
        self.Pick_txt =IntVar()
        self.Pick_txt_tmp = StringVar()
        self.PickBar = StringVar()
        self.Repeat_txt =StringVar()
        self.Rpm_txt =StringVar()
        self.Meter_txt=StringVar()
        self.Efficiency_txt =StringVar()
        self.Bundle_txt =StringVar()
        self.Sensor1_txt=StringVar()
        self.Sensor2_txt=StringVar()
        self.copyBar = StringVar()
        self.copy_text = StringVar()

        # Setting tab's variable
        self.settingDesign = 0
        self.harness = 1
        self.selectDesign = [1,0]
        self.diameter = StringVar()
        self.SetDiameter = 0
        self.curr_pick = 0
        self.curr_rpm = 0
        self.no_of_hook = StringVar()
        self.password_str = StringVar()
        self.network_name = StringVar()
        self.letter_up = False
        self.shiftSetting = []
        self.deUnChkSetting = []
        self.deChkSetting = []
        self.hrOnSetting = []
        self.hrOffSetting = []
        self.wfOnSetting = []
        self.wfOffSetting = []
        self.pfOnSetting = []
        self.pfOffSetting = []
        self.snOnSetting = []
        self.snOffSetting = []
        self.nfhookSetting = []

        # Files' related variables
        self.keyboard_keys = [
            ('1','2','3','4','5','6','7','8','9','0','_','-','+','='),
            ('a','b','c','d','e','f','g','h','i','k','l','m','n','o'),
            ('p','q','r','s','t','u','v','w','x','y','z','\\','/','*'),
            ('Backspace','Enter','!','@','#','$','%','&','(',')')
        ]
        # self.keyboard_keys_all = [
        #     ('~','!','@','#','$','%','^','&','*','(',')','-','_','+'),
        #     ('1','2','3','4','5','6','7','8','9','0','=','{','}','|'),
        #     ('a','b','c','d','e','f','g','h','i','k','l','m','n','o'),
        #     ('p','q','r','s','t','u','v','w','x','y','z','[',']','?'),
        #     ('Caps Lock','Backspace','Enter','.','<','>',',',':')
        # ]
        self.keyboard_keys_all = [
            ('~','!','@','#','$','%','^','&','*','(',')','-','_','<x'),
            ('1','2','3','4','5','6','7','8','9','0','=','{','}','+'),
            ('Q','W','E','R','T','Y','U','I','O','P','[',']','<','>'),
            ('A','S','D','F','G','H','J','K','L',':','"',';','\'','?'),
            ('Z','X','C','V','B','N','M',',','/','.','|','Caps')
        ]
             
        self.search_file_str = StringVar()
        self.active_search = StringVar()
        self.fileRowsOri = []
        self.fileRows = []
        self.FileChked = []
        self.FileChkLblAll = []
        self.FileUnChkLblAll = []

        #usb section
        self.search_file_str_usb = StringVar()
        self.totalfilefound = StringVar()
        self.usb_files = []
        self.usbThreadId = None
        self.usb_last_dir = []
        self.usb_last_final_dir = ''

        self.Namelenth = 0
        #Image related variables
        self.rotate_left = 0
        self.rotate_right = 0
        self.rotate_state = 0
        self.flip_state = ''

        #Testing tab varaible
        self.Test_pick = StringVar()
        self.Test_Sensor1 = StringVar()
        self.Test_Sensor2 = StringVar()
        self.test_start = False

        # setting tab variable
        self.setting_cmd = 0
        #Serial data init
        self.ser = serial.Serial(
                port='/dev/ttyS0',
                # baudrate = 168269,
                baudrate = 336538,
                # baudrate =38400 ,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=0
        )
        self.Recivedata = []

        ## End Predefine variables with default values

        ### End Global variables

        ### Start Global image define
        self.minus_icon = PhotoImage(file=os.path.join(self.images_dir, 'cminus.png'))
        self.plus_icon = PhotoImage(file=os.path.join(self.images_dir, 'cplus.png'))
        self.calc_icon = PhotoImage(file=os.path.join(self.images_dir, 'ccalc.png'))
        self.reset_icon = PhotoImage(file=os.path.join(self.images_dir, 'creset.png'))
        self.view_icon = PhotoImage(file=os.path.join(self.images_dir, 'view_icon.png'))
        self.hide_icon = PhotoImage(file=os.path.join(self.images_dir, 'hide.png'))
        self.search_icon = PhotoImage(file=os.path.join(self.images_dir, 'search.png'))
        self.del_icon = PhotoImage(file=os.path.join(self.images_dir, 'fdel.png'))
        self.copy_icon = PhotoImage(file=os.path.join(self.images_dir, 'copyicon.png'))
        self.unchkall_icon = PhotoImage(file=os.path.join(self.images_dir, 'unchk_all.png'))
        self.chkall_icon = PhotoImage(file=os.path.join(self.images_dir, 'chk_all.png'))
        self.unchk_icon = PhotoImage(file=os.path.join(self.images_dir, 'unchkicon.png'))
        self.chk_icon = PhotoImage(file=os.path.join(self.images_dir, 'chkicon.png'))
        self.roff_icon = PhotoImage(file=os.path.join(self.images_dir, 'radiooff.png'))
        self.ron_icon = PhotoImage(file=os.path.join(self.images_dir, 'radioon.png'))
        self.close_icon = PhotoImage(file=os.path.join(self.images_dir, 'crossicon.png'))
        self.zoomin_icon = PhotoImage(file=os.path.join(self.images_dir, 'zoomin.png'))
        self.zoomout_icon = PhotoImage(file=os.path.join(self.images_dir, 'zoomout.png'))
        self.rleft_icon = PhotoImage(file=os.path.join(self.images_dir, 'rotate_left.png'))
        self.rright_icon = PhotoImage(file=os.path.join(self.images_dir, 'rotate_right.png'))
        self.fleftright_icon = PhotoImage(file=os.path.join(self.images_dir, 'flip_left_right.png'))
        self.ftopbottom_icon = PhotoImage(file=os.path.join(self.images_dir, 'flip_top_bottom.png'))
        self.save_icon = PhotoImage(file=os.path.join(self.images_dir, 'save.png'))
        self.file_icon = PhotoImage(file=os.path.join(self.images_dir, 'file_icon.png'))
        self.folder_icon = PhotoImage(file=os.path.join(self.images_dir, 'folder_icon.png'))
        self.wifi_icon = PhotoImage(file=os.path.join(self.images_dir, 'wifi.png'))
        self.tick_icon = PhotoImage(file=os.path.join(self.images_dir, 'tick.png'))
        self.wifi_off_icon = PhotoImage(file=os.path.join(self.images_dir, 'wifi_off.png'))
        ### End Global image define


        # Define tab wise global frames
        # self.master = Frame(self.master, width=self.winWidth, height=self.frameHeight) #Body frame
        self.topFrame = Frame(self.master, width=self.winWidth, height=self.menuHeight) #Store menu
        self.InfoFrame = Frame(self.master, width=self.winWidth, height=self.frameHeight) #Info frame
        self.FileFrame = Frame(self.master, width=self.winWidth, height=self.frameHeight) #Files frame
        self.USBFrame = Frame(self.master, width=self.winWidth, height=self.frameHeight) #USB frame
        self.TestFrame = Frame(self.master, width=self.winWidth, height=self.frameHeight) #Test frame
        self.ReportFrame = Frame(self.master, width=self.winWidth, height=self.frameHeight) #Report frame
        self.SettingFrame = Frame(self.master, width=self.winWidth, height=self.frameHeight) #Setting frame
        self.POPFrame = Frame(self.master, width=self.winWidth, height=self.winHeight) #Pop frame
        self.popupCanvas = Canvas(self.master, width=self.winWidth, height=self.winHeight, background="#FFFFFF",bd=0,highlightthickness = 0)
        self.passwordFrame = Frame(self.master, width=self.winWidth, height=self.frameHeight) #Setting frame
        self.WifiFrame = Frame(self.master, width=self.winWidth, height=self.frameHeight) #Setting frame
        self.msgFrame = Frame(self.master, width=self.winWidth, height=self.frameHeight) #Setting frame
        self.initCanvas = Canvas(self.master, width=self.winWidth, height=self.winHeight, background="#FFFFFF",bd=0,highlightthickness = 0)
        self.ErrorFrame =Frame(self.master, width=self.winWidth, height=self.menuHeight)
        ##tab wise frame init
        #View Frame
        self.viewFrame = Frame(self.master,width=self.winWidth,height=self.winHeight)
        #Test Frame
        self.TestFrameImgCanvas = Canvas(self.TestFrame, width=(self.winWidth - 45), height=((self.frameHeight/1.5) - 40), bd=1, relief='solid')
        self.TestFrameImgCanvas.grid(row=0,column=0)
        self.TestFrameOPCanvas = Canvas(self.TestFrame, width=(self.winWidth - 45), height=(self.frameHeight/2), relief='solid', background='#FFFFFF',bd=0,highlightthickness = 0)
        self.TestFrameOPCanvas.grid_forget()

        #Global Style for objects
        estyle = ttk.Style()
        estyle.element_create("plain.field",'from','clam')
        estyle.layout('EntryStyle.TEntry',
                        [('Entry.plain.field',{'children':[(
                            'Entry.background',{'children':[(
                                'Entry.padding', {'children':[(
                                    'Entry.textarea', {'sticky': 'news'})],
                                'sticky':'news'})],
                            'sticky':'news'})],
                        'border':'2', 'sticky':'news'})])

        ttk.Style().configure('Vertical.TScrollbar', background='#9B9C9B',width=50,hight=500,troughcolor='#6A6A69')
        ttk.Style().configure('Horizontal.TScrollbar', background='#9B9C9B',width=50,troughcolor='#6A6A69')
        ttk.Style().map('TScrollbar', background=[('active','#9B9C9B')])
        ttk.Style().configure('transparent.TButton', foreground='#000000', background='#FFFFFF', font="Verdana 13", relief=SOLID)
        ttk.Style().map('transparent.TButton', background=[('active','#738780'),('selected','#738780')], foreground=[('active','#000'),('selected','#000')])
        ttk.Style().configure('selected.TButton', foreground='#000000', background='#738780', font="Verdana 13", relief=SOLID)
        ttk.Style().map('selected.TButton', background=[('active','#738780'),('selected','#738780')], foreground=[('active','#000'),('selected','#000')])
        ttk.Style().configure('bgray.TButton', foreground='#FFFFFF', background='#586273', font="Verdana 13", relief=RAISED)
        ttk.Style().map('bgray.TButton', background=[('active','#9096A2')], foreground=[('active','#000')])
        estyle.configure('EntryStyle.TEntry',padding=14, background="#526C87",relief="solid",fieldbackground="#EEEEEE")
        ttk.Style().map('TEntry', fieldbackground=[('disabled','#738780')], foreground=[('disabled','#000000')])
        ttk.Style().configure('head.TLabel',font="Verdana 10 bold", foreground="#12355B")
        ttk.Style().configure('infoRect.TLabel', padding=10, background="#526C87",font="Verdana 25",width="20", anchor="center", foreground="#FFF")
        ttk.Style().configure('red.Horizontal.TProgressbar',thickness=50, toughcolor="#FFFFFF", bordercolor="#FFFFFF", lightcolor="#FFFFFF", darkcolor="#FFFFFF", foreground="red", background="#12355B")
        ttk.Style().configure('tableTH.TLabel', relief="solid", padding=(10,5), background="#A3A3A3",font="Verdana 16 bold")
        ttk.Style().configure('tableTD.TLabel',relief="solid", padding=10, background="#FFFFFF",font="Verdana 14")
        ttk.Style().configure('tableTDD.TLabel',relief="solid", padding=10, background="#FFFFFF",font="Verdana 14 bold",foreground='#12355B')
        ttk.Style().configure('plain.TLabel', padding=10, font="Verdana 14")
        ttk.Style().configure('file.TLabel', foreground='#000', font="Verdana 18")
        ttk.Style().configure('fileRes.TLabel', foreground='#526C87', font="Verdana 18")
        ttk.Style().configure('file.TButton', foreground='#000', background='#A37B3C', font="Verdana 10", padding=(0,0), relief="RAISED",width=8)
        ttk.Style().map('file.TButton', background=[('active','#5D4723')], foreground=[('active','#FFF')])
        ttk.Style().configure('message.TButton', foreground='#000', background="#526C87", font="Verdana 25", padding=(0,10), relief="RAISED",width=8)
        ttk.Style().map('message.TButton', background=[('active','#12355B')], foreground=[('active','#FFF')])
        ttk.Style().configure('setting.TButton', foreground='#000', background='#A37B3C', font="Verdana 14", padding=5, relief="RAISED")
        ttk.Style().map('setting.TButton', background=[('active','#5D4723')], foreground=[('active','#FFF')])
        ttk.Style().configure('lgkeypad.TButton', foreground='#000', background='#526C87', font="Verdana 35", padding=5, width=3, relief=RAISED)
        ttk.Style().map('lgkeypad.TButton', background=[('active','#12355B')], foreground=[('active','#FFF')])
        ttk.Style().configure('lgkeyboard.TButton', foreground='#000', background='#526C87', font="Verdana 20 bold", padding=(8,10), relief=RAISED)
        ttk.Style().map('lgkeyboard.TButton', background=[('active','#12355B')], foreground=[('active','#FFF')])
        ttk.Style().configure('keypad.TButton', foreground='#000', background='#526C87', font="Verdana 20", padding=5, width=3, relief="RAISED")
        ttk.Style().map('keypad.TButton', background=[('active','#12355B')], foreground=[('active','#FFF')])
        ttk.Style().configure('red.TLabel', foreground='red', background='#FFFFFF', font="Verdana 15 bold", padding=10)
        ttk.Style().configure('lblHead.TLabel', foreground='#000000', background='#FFFFFF', font="Verdana 13", padding=10)
        ttk.Style().configure('lblBody.TLabel', foreground='#55625A', background='#FFFFFF', font="Verdana 13", padding=10)
        ttk.Style().configure('test.TButton', foreground='#000', background='red', font="Verdana 14", padding=5, relief="RAISED")
        ttk.Style().map('test.TButton', background=[('active','dark red')], foreground=[('active','#FFF')])

        # self.master.configure(background='white')
        self.gen_loader()

        self.initCanvas = Canvas(self.master, width=self.winWidth, height=self.winHeight, background="#FFFFFF",bd=0,highlightthickness = 0)
        self.initCanvas.grid(row=0,column=0,sticky='news')

        logo_img = PhotoImage(file=os.path.join(self.images_dir, 'logo.png'))
        lbl = Label(self.initCanvas,image=logo_img, background='#FFFFFF')
        lbl.image = logo_img
        lbl.place(x=200,y=0)

        # self.Info_ReadSerial()
        # self.master.after(50, self.Info_ReadSerial)
        # Call header once all things loading
        r = Timer(3.0, self.header_section)
        r.start()

    def ask_messagebox(self,text,tab):
        # self.master.withdraw()
        top =Toplevel(self.master)
        top.title("ask")
        top.geometry("1024x600+0+0")

        top.wm_attributes("-type","splash")
        top.overrideredirect(True)
        # top.deiconify()
        msg=Message(top,text=text, foreground='#526C87',font="Verdana 40 ",width=1024,anchor='center')
        msg.place(x=512,y=300,anchor = CENTER)
        button1=Button(top,text="Yes",
                    width=10,
                    style='message.TButton',
                    command=lambda child=top,txt='yes',tabname=tab: self.closeChildWin_ask(child,txt,tabname))
        button1.place(x=400,y=500,anchor=CENTER)
        button2=Button(top,text="No",
                    width=10,
                    style='message.TButton',
                    command=lambda child=top,txt='No',tabname=tab: self.closeChildWin_ask(child,txt,tabname))
        button2.place(x=660,y=500,anchor=CENTER)

    def closeChildWin_ask(self, child,btn_text,tabname):
        if btn_text == 'yes':
            # print(btn_text)
            # print(tabname)
            if tabname == 'info':
                self.ser.write(MAIN_ADD)
                self.ser.write(RESET_PROD)
                self.ser.write(EOD)
            if tabname == 'Delete':
                #Delete all files
                for f in range(len(self.FileChked)):
                    fpath = os.path.join(self.files_dir,self.FileChked[f])
                    if os.path.exists(fpath):
                        os.remove(fpath)
                self.clear_files('files',True)
            if tabname == 'Copy':
                print("Copy repeate")
                self.copyfcnt = self.copyfcnt + 1
                self.fcImg.save(self.cpyimg)
        child.destroy()
        self.master.deiconify()
    def messagebox(self,title,text):
        # self.master.withdraw()
        top =Toplevel(self.master)
        # top =Toplevel()
        time.sleep(.1)
        top.geometry("1024x600+0+0")
        # if self.thread_flg == 1:
        #     self.thread_flg=0
        #     top.overrideredirect(False)
        # else:
        top.wm_attributes("-type","splash")
        time.sleep(.1)
        top.overrideredirect(True)
        # top.deiconify()

        msg=Message(top,text=text, foreground='#526C87',font="Verdana 40 ",width=1024,anchor='center')
        # msg.grid(row=0,column=0,padx=(5,0),pady=(100,0),sticky='news')
        msg.place(x=512,y=300,anchor = CENTER)
        button=Button(top,text="OK",
                width=10,
                style='message.TButton',
                # padding=10,
                command=lambda child=top: self.closeChildWin(child))
        # button.grid(row=1,column=0,padx=(5,0),pady=(20,0),sticky='news')
        button.place(x=512,y=500,anchor=CENTER)
        # top.deiconify()
        # top.maxsize()
        # msg=Message(top,text=text, foreground='#526C87',font="Verdana 40",padx=100,pady=60,relief=RAISED)
        # msg.pack(side="top",fill="both",expand=True)

        # button=Button(top,text="ok",command=lambda child=top: self.closeChildWin(child))
        # button.pack(side="bottom",fill="both",expand=True)
        # top.attributes(disabled=True)

        # top.wm_attributes("-type","splash")

    def closeChildWin(self, child):
        print("child call")
        child.destroy()
        self.master.deiconify()
        return

    # Header section
    # Top menu #info, #Files, #USB, #Test, #Setting, #Report
    def header_section(self):
        self.initCanvas.grid_forget()
        self.topFrame.grid(row=0,sticky='nw')
        # self.master.grid(row=1,sticky='nw')
        ## Tabbing design
        # Background color of whole wrap menu
        ttk.Style().configure('menu.TNotebook', background='#526C87',borderwidth=0)
        # Style for individual tab
        ttk.Style().configure('menu.TNotebook.Tab', background='#526C87',padding=(9,15),font="Verdana 20", anchor="center", width=7)
        # Map active or selected tab design
        ttk.Style().map("menu.TNotebook.Tab", background=[("selected","#12355B")],foreground=[("selected","#FFFFFF")])

        # Configure Tabbing frame
        self.tabControls = ttk.Notebook(self.topFrame, width=self.winWidth, style='menu.TNotebook')
        self.tabControls.grid(row=0,column=1)

        # Bind click event of each tab
        self.tabControls.bind('<<NotebookTabChanged>>', self.on_tab_selected)

        #Generate individual tabs
        for t in range(len(self.topMenu)):
            if self.topMenu[t] == 'Info':
                self.info_tab = Frame(self.tabControls)
                self.tabControls.add(self.info_tab, text=self.topMenu[t], compound=TOP)
            elif self.topMenu[t] == 'Wifi':
                self.wifi_tab = Frame(self.tabControls)
                self.tabControls.add(self.wifi_tab, text=self.topMenu[t],image=self.wifi_off_icon, compound=LEFT)
            else:
                tab = Frame(self.tabControls)
                self.tabControls.add(tab, text=self.topMenu[t], compound=TOP)

    # Tab click event callback function
    # Get section releated to Tab
    def on_tab_selected(self,event):
        selected_tab = event.widget.select()
        tab_text = event.widget.tab(selected_tab, 'text')

        if tab_text == 'Info':

            print("info start")
            self.stop_test_pattern()
            self.reset_variable()
            self.Req_fileName()
            self.infoThreadId= self.master.after(50, self.Info_ReadSerial)
            self.info_section()
            self.InfoFrame.grid(row=1, sticky='nsew', padx=20, pady=20)
            # self.Stop_INFO()
        elif tab_text == 'Files':
            self.master.after_cancel(self.infoThreadId)
            if self.curr_rpm == 0:
                self.Stop_INFO()
                self.master.after_cancel(self.infoThreadId)
                self.stop_test_pattern()
                self.reset_variable()
                self.reset_frame(self.FileFrame)
                self.fileRowsOri = self.fileRows = []
                self.fileRowsOri = self.fileRows = self.files_feed(self.files_dir)
                self.files_section()
                self.FileFrame.grid(row=1, sticky='nsew', padx=20, pady=20)
            else:
                self.tabControls.select(self.tab1)
                self.messagebox("error","Machine is in running mode. Access denied.")
                # self.messagebox('Warning','Machine is in running mode. Access denied.')
        elif tab_text == 'USB':
            # self.Stop_INFO()
            if self.curr_rpm == 0:
                self.Stop_INFO()
                self.infoThreadId= self.master.after(50, self.Info_ReadSerial)
                self.stop_test_pattern()
                self.reset_variable()
                self.reset_frame(self.USBFrame)
                self.usb_section(True)
                # self.usbThreadId= self.master.after(10, self.usb_section(True))
                self.USBFrame.grid(row=1, sticky='nsew', padx=20, pady=20)
            else:
                self.tabControls.select(self.tab1)
                # messagebox.showwarning('Warning','Machine is in running mode. Access denied.')
                self.messagebox('Warning','Machine is in running mode. Access denied.')
        elif tab_text == 'Test':
            if self.curr_rpm == 0:
                self.Stop_INFO()
                self.reset_variable()
                self.test_section()
                self.TestFrame.grid(row=1, sticky='nsew', padx=20, pady=20)
            else:
                self.tabControls.select(self.tab1)
                self.messagebox('Warning','Machine is in running mode. Access denied.')
        elif tab_text == 'Settings':
            if self.curr_rpm == 0:
                self.Stop_INFO()
                self.stop_test_pattern()
                self.reset_variable()
                self.reset_frame(self.SettingFrame)
                self.SettingFrame.grid(row=1, sticky='nsew')
                self.SettingFrameLeft = Frame(self.SettingFrame,height=self.frameHeight)
                self.SettingFrameLeft.grid(row=0,column=0,sticky='nw')
                self.SettingFrameRight = Frame(self.SettingFrame)
                self.SettingFrameRight.grid(row=0,column=1,sticky='nw',padx=20,pady=20)
                self.vertical_tab_menu(self.SettingFrameLeft,self.setting_menu)
            else:
                self.tabControls.select(self.tab1)
                self.messagebox('Warning','Machine is in running mode. Access denied.')

        elif tab_text == 'Reports':
            if self.curr_rpm == 0:
                self.reset_variable()
                self.reset_frame(self.ReportFrame)
                self.ReportFrame.grid(row=1, sticky='nsew')

                self.ReportFrameLeft = Frame(self.ReportFrame,height=self.frameHeight)
                self.ReportFrameLeft.grid(row=0,column=0,sticky='nw')
                self.ReportFrameRight = Frame(self.ReportFrame)
                self.ReportFrameRight.grid(row=0,column=1,sticky='nw',padx=20,pady=20)

                self.vertical_tab_menu(self.ReportFrameLeft,self.report_menu)

            else:
                self.tabControls.select(self.info_tab)
                self.messagebox('Warning','Machine is in running mode. Access denied.')

        elif tab_text == 'Wifi':
            if self.curr_rpm == 0:
                self.reset_variable()
                self.reset_frame(self.WifiFrame)
                self.WifiFrame.grid(row=1, sticky='nsew', padx=20, pady=20)
                self.get_wifi_list()
                self.wifi_section()
            else:
                self.tabControls.select(self.info_tab)
                self.messagebox('Warning','Machine is in running mode. Access denied.')


     # Vertical tabbing menu

    # Vertical tabbing menu
    def vertical_tab_menu(self,pframe, menu_arr):
        ttk.Style().configure('lefttab.TNotebook', background='#526C87',borderwidth=0,tabposition='wn')
        # Style for individual tab
        ttk.Style().configure('lefttab.TNotebook.Tab', background='#526C87',padding=(10,15),font="Verdana 17", anchor="center", width=15)
        # Map active or selected tab design
        ttk.Style().map("lefttab.TNotebook.Tab", background=[("selected","#12355B")],foreground=[("selected","#FFFFFF")])
        # Configure Tabbing frame
        self.leftTabCnt = ttk.Notebook(pframe, style='lefttab.TNotebook',height=self.winHeight)
        self.leftTabCnt.grid(row=0,column=0,sticky='nw')

        for t in range(len(menu_arr)):
            tab = Frame(self.leftTabCnt)
            self.leftTabCnt.add(tab, text=menu_arr[t])

        # Bind click event of each tab
        self.leftTabCnt.bind('<<NotebookTabChanged>>', self.on_lefttab_selected)

    # Left tab menu click event
    # Get section releated to Tab
    def on_lefttab_selected(self,event):
        selected_tab = event.widget.select()
        tab_text = event.widget.tab(selected_tab, 'text')

        if tab_text == 'General':
            self.reset_frame(self.SettingFrameRight)
            self.general_setting_section()
        elif tab_text == 'Design':
            self.setting_cmd = SET_DESIGN_SET
            self.reset_frame(self.SettingFrameRight)
            self.design_setting_section()
            self.get_controller_setting(GET_SETTINGS)

        elif tab_text == 'Harness':
            self.setting_cmd = SET_HARNES_SET
            self.reset_frame(self.SettingFrameRight)
            self.harness_setting_section()
            self.get_controller_setting(GET_SETTINGS)

        elif tab_text == 'Production':
            self.setting_cmd = SET_ROLL_DIA
            self.reset_frame(self.SettingFrameRight)
            self.production_setting_section()
            self.get_controller_setting(GET_SETTINGS)

        elif tab_text == 'Features':
            self.setting_cmd = SET_WEFT_SLCT
            self.reset_frame(self.SettingFrameRight)
            self.feature_setting_section()
            self.get_controller_setting(GET_SETTINGS)
    
        elif tab_text == 'Sensor Setup':
            self.setting_cmd = SET_SENSR_SETUP
            self.reset_frame(self.SettingFrameRight)
            self.sensor_setting_section()
            self.get_controller_setting(GET_SETTINGS)

        elif tab_text == 'Number of Hooks':
            self.setting_cmd = SET_NUMBER_HOOK
            self.reset_frame(self.SettingFrameRight)
            self.nofHooks_setting_section()
            self.get_controller_setting(GET_SETTINGS)

        elif tab_text == 'Shift Manage':
            self.setting_cmd = SET_DESIGN_SET
            self.reset_frame(self.ReportFrameRight)
            self.shift_report_section()
        return


    #Destroy frames' child before going to that tab
    #pframe = parent frame name whose child will be destroy
    def reset_frame(self,pframe):
        for child in pframe.winfo_children():
            child.destroy()

    #Reset all variable before going into any tabs
    def reset_variable(self):
        # Hide all frame before display anyone frame
        self.InfoFrame.grid_forget()
        self.FileFrame.grid_forget()
        self.USBFrame.grid_forget()
        self.TestFrame.grid_forget()
        self.TestFrameOPCanvas.grid_forget()
        self.SettingFrame.grid_forget()
        self.WifiFrame.grid_forget()
        self.passwordFrame.grid_forget()
        self.msgFrame.grid_forget()
        self.POPFrame.grid_forget()
        self.popupCanvas.grid_forget()
        self.viewFrame.grid_forget()
        self.ReportFrame.grid_forget()
       
        #Reset few variables
        self.lblCol = []
        self.lblROffCol = []
        self.lblROnCol = []
        self.lblChkCol = []
        self.lblUnChkCol = []
        self.FileChked = []
        self.FileChkLblAll = []
        self.FileUnChkLblAll = []

        self.shiftSetting = []
        self.deUnChkSetting = []
        self.deChkSetting = []
        self.hrOnSetting = []
        self.hrOffSetting = []
        self.wfOnSetting = []
        self.wfOffSetting = []
        self.pfOnSetting = []
        self.pfOffSetting = []
        self.snOnSetting = []
        self.snOffSetting = []
        self.nfhookSetting = []

        self.setting_cmd ='N'
        #read data from controller and display in display

        #Remove png file if exists
        self.remove_sample_png()

    #remove sample png files which generate while viewing and we had convert bmp into png
    def remove_sample_png(self):
        if os.path.exists(self.view_png_img):
            os.remove(self.view_png_img)

    #Serial communication with controller
    def Info_ReadSerial(self):
        # print('a')
        while True:
            if self.Test_flg == 2:
                self.Test_flg =0
                self.test_start = 0
                print("communication error,info")
                self.messagebox("Error","Communication error")
                print('break info')

            Read_Data  = self.ser.read()
            # print(Read_Data)
            if len(Read_Data) == 0:
                # print(len(Read_Data))
                break
            if len(Read_Data) !=0:
                self.Recivedata.append(Read_Data)
                # print(Read_Data)
                if len(self.Recivedata) > 25 :
                    self.Recivedata = []
                    self.ser.flushInput()
                if (len(self.Recivedata) > 1 and self.Recivedata[len(self.Recivedata)-1] != EOD):
                    continue

                # print(Recivedata)    
                # if val.find(DISPLAY_ADD) != -1 and val.find(EOD) != -1 and val.find(FILE_NAME) != -1 :
                if len(self.Recivedata)>5 and self.Recivedata[0] == DISPLAY_ADD and self.Recivedata[1]==FILE_NAME:
                    print('file name')
                    print('lenth',self.Recivedata[2] )
                    self.Namelenth = self.bytes_to_int(self.Recivedata[2],0)
                    # print(self.Recivedata)
                    self.Recivedata =  self.Recivedata[3:self.Namelenth+3]
                    printStr =b''.join(self.Recivedata)
                    printStr.decode("utf-8")

                    self.DesignName.set(printStr)
                    self.Recivedata = []
                    self.Test_flg = 1

                if len(self.Recivedata)== 4 and self.Recivedata[0] == DISPLAY_ADD and self.Recivedata[len(self.Recivedata)-1] == EOD and self.Recivedata[1] == ERR:
                    print("error")
                    # print(self.Recivedata[2])
                    self.Recivedata[2]=self.bytes_to_int(self.Recivedata[2],0)
                    # print(self.Recivedata[2])
                    if self.Recivedata[2] == CARD_NOT_DETECT:
                        print(self.Recivedata[2])
                        self.messagebox('Error','CARD NOT DETECT')
                    if self.Recivedata[2] ==CARD_INIT_FAIL:
                        print(self.Recivedata[2])
                        self.messagebox('Error','CARD INITIALIZE FAIL')
                    if self.Recivedata[2] ==FAT32_NOT_FOUND :
                    # if self.Recivedata[2] == 0x02 :
                        print(self.Recivedata[2])
                        self.messagebox('Error','FAT32 NOT FOUND')
                    if self.Recivedata[2] == ERROR_IN_CLUSTER :
                        print(self.Recivedata[2])
                        self.messagebox('Error','ERROR IN CLUSTER')
                    if self.Recivedata[2] == DSGN_NOT_FOUND :
                        print(self.Recivedata[2])
                        self.messagebox('Error','DESIGN NOT FOUND')
                    if self.Recivedata[2] == DSGN_INVALID :
                        print(self.Recivedata[2])
                        self.messagebox('Error','DESIGN INVALID')
                    if self.Recivedata[2] == EEPROM_ERR :
                        print(self.Recivedata[2])
                        self.messagebox('Error','EEPROM ERROR')
                    if self.Recivedata[2] == BPS_ERR :
                        print(self.Recivedata[2])
                        self.messagebox('Error','Format memory card')
                    if self.Recivedata[2] == SPC_ERR :
                        print(self.Recivedata[2])
                        self.messagebox('Error','Format memory card')
                    self.Recivedata = []

                # if val.find(DISPLAY_ADD) != -1 and val.find(EOD) != -1 and val.find(HOOK_SETTING) != -1:

                if len(self.Recivedata) == 16 and self.Recivedata[0] == DISPLAY_ADD and self.Recivedata[len(self.Recivedata)-1] == EOD and self.Recivedata[1] == HOOK_SETTING:
                    printStr ="".join([str(elem) for elem in self.Recivedata])
                    printStr = (printStr.replace('\'',''))
                    printStr = (printStr.replace('b',''))
                    printStr = (printStr.replace('~',''))
                    self.Bundle_txt.set(printStr[2:])
                    self.Recivedata = []

                if len(self.Recivedata) == 21 and self.Recivedata[0] == DISPLAY_ADD and self.Recivedata[len(self.Recivedata)-1] == EOD and self.Recivedata[1] == CURRENT_STATUS:
                    CurrentPick = self.bytes_to_int(self.Recivedata[3],0)
                    CurrentPick = self.bytes_to_int(self.Recivedata[2],CurrentPick)
                    self.curr_pick = CurrentPick

                    TotalPick = self.bytes_to_int(self.Recivedata[5],0)
                    TotalPick = self.bytes_to_int(self.Recivedata[4],TotalPick)
                    self.Pick_txt.set(str(CurrentPick)+'/'+str(TotalPick))

                    Repeat = self.bytes_to_int(self.Recivedata[7],0)
                    Repeat = self.bytes_to_int(self.Recivedata[6],Repeat)
                    self.Repeat_txt.set(str(Repeat)+" Repeat")

                    Rpm = self.bytes_to_int(self.Recivedata[9],0)
                    Rpm = self.bytes_to_int(self.Recivedata[8],Rpm)
                    self.curr_rpm = Rpm
                    self.Rpm_txt.set(str(Rpm)+" RPM")

                    Efficiency = self.bytes_to_int(self.Recivedata[11],0)
                    Efficiency = self.bytes_to_int(self.Recivedata[10],Efficiency)
                    self.Efficiency_txt.set(str(Efficiency)+" %Efficiency")

                    Meter = self.Recivedata[12]+self.Recivedata[13]+self.Recivedata[14]+self.Recivedata[15]
                    Meter_S = struct.unpack("f", Meter)
                    ch_meter = str(Meter_S).replace(',','').replace('(','').replace(')','').split('.')
                    if len(ch_meter) > 1:
                        m1 = ch_meter[0]
                        m2 = ch_meter[1][0:1]
                        Meter = m1 + '.' + m2
                    else:
                        Meter = ch_meter
                    self.curr_meter = Meter

                    TotalMeter = self.bytes_to_int(self.Recivedata[19],0)
                    TotalMeter = self.bytes_to_int(self.Recivedata[18],TotalMeter)
                    self.Meter_txt.set(str(Meter)+'/'+str(TotalMeter)+" Meter")

                    Bundle = self.bytes_to_int(self.Recivedata[17],0)
                    Bundle = self.bytes_to_int(self.Recivedata[16],Bundle)
                    # self.Bundle_txt.set(str(Bundle)+" Hook")
                    # self.Bundle_txt.set(str(192)+" Hook")

                    PickValue = 0
                    if TotalPick > 0:
                        PickValue= CurrentPick*100 / TotalPick
                    self.PickBar.set(PickValue)
                    self.Recivedata = []

                elif len(self.Recivedata) == 5 and self.Recivedata[0] == DISPLAY_ADD and self.Recivedata[len(self.Recivedata)-1] == EOD and self.Recivedata[1] == SENSR_STATUS:
                    print("sensr")
                    if self.bytes_to_int(self.Recivedata[2],0) == 0x01:
                        self.circleCanvas.itemconfig(self.Sensor1, fill='green')
                    else :
                        self.circleCanvas.itemconfig(self.Sensor1, fill='gray')

                    if self.bytes_to_int(self.Recivedata[3],0) == 0x01:
                        self.circleCanvas.itemconfig(self.Sensor2, fill='green')
                    else :
                        self.circleCanvas.itemconfig(self.Sensor2, fill='gray')
                    self.Recivedata = []
                # elif self.Recivedata.find(DISPLAY_ADD) != -1 and self.Recivedata.find(TEST_PICK) != -1 and self.Recivedata.find(EOD) != -1:
                elif len(self.Recivedata) == 7 and self.Recivedata[0] == DISPLAY_ADD and self.Recivedata[len(self.Recivedata)-1] == EOD and self.Recivedata[1] == TEST_PICK:
                    # self.Test_pick.set(int(hexlify(self.Recivedata[3:4]), 16))
                    # print(int(self.Recivedata[3],10))
                    Test_pick=self.bytes_to_int(self.Recivedata[3],0)

                    self.TestPick.config(text=Test_pick)
                    #set sensor op
                    if self.bytes_to_int(self.Recivedata[4],0) == 0x01:
                        self.TestLEDC.itemconfig(self.TestSensor1, fill='green')
                    else :
                        self.TestLEDC.itemconfig(self.TestSensor1, fill='gray')

                    if self.bytes_to_int(self.Recivedata[5],0) == 0x01:
                        self.TestLEDC.itemconfig(self.TestSensor2, fill='green')
                    else :
                        self.TestLEDC.itemconfig(self.TestSensor2, fill='gray')
                    self.Recivedata = []
                # elif(self.Recivedata.find(DISPLAY_ADD) != -1)and(self.Recivedata.find(SET_STATUS)!=-1)and(self.Recivedata.find(EOD)!=-1):
                #len ==15 bytes
                elif  len(self.Recivedata) == 15 and (self.Recivedata[0] == DISPLAY_ADD)and(self.Recivedata[1] == SET_STATUS)and(self.Recivedata[len(self.Recivedata)-1] == EOD):

                    self.Status_timer.cancel()
                    self.Test_flg = 1

                    print("compare data")
                    print(self.Recivedata)

                    if self.setting_cmd == SET_DESIGN_SET :
                        # print("self.setting_cmd",self.setting_cmd)
                        self.settingDesign = self.bytes_to_int(self.Recivedata[2])

                        #Reset all selection from setting image
                        # print("lblcol",len(self.lblCol))
                        if len(self.lblCol) > 0:
                            for l in range(len(self.lblCol)):
                                self.lblCol[l].config(relief=RAISED)
                                self.lblCol[l].config(background='#526C87')

                        #Set selecton to click image
                            self.lblCol[self.settingDesign].config(relief=SUNKEN)
                            self.lblCol[self.settingDesign].config(background='#12355B')

                        self.selectDesign[0] = self.bytes_to_int(self.Recivedata[3])
                        self.selectDesign[1] = self.bytes_to_int(self.Recivedata[4])
                        
                        # self.selectDesignArr[0][1]=self.selectDesign[0]
                        # self.selectDesignArr[1][1]=self.selectDesign[1]

                        print(self.selectDesign[0])
                        print(self.selectDesign[1])
                        if self.selectDesign[0] == 1:
                            #Set checkbox checked based on click
                            self.lblChkCol[0].grid(row=3,column=0, sticky="EW",pady=20)
                            #Hide uncheck checkbox
                            self.lblUnChkCol[0].grid_forget()
                        else:
                            # Show uncheck checkbox and hide checked checkbox
                            self.lblUnChkCol[0].grid(row=3,column=0, sticky="EW",pady=20)
                            self.lblChkCol[0].grid_forget()

                        if self.selectDesign[1] == 1:
                            #Set checkbox checked based on click
                            self.lblChkCol[1].grid(row=3,column=1, sticky="EW",pady=20)
                            #Hide uncheck checkbox
                            self.lblUnChkCol[1].grid_forget()
                        else:
                            # Show uncheck checkbox and hide checked checkbox
                            self.lblUnChkCol[1].grid(row=3,column=1, sticky="EW",pady=20)
                            self.lblChkCol[1].grid_forget()

                    # # set harness from controller
                    if self.setting_cmd == SET_HARNES_SET :
                        print("self.setting_cmd",self.setting_cmd)

                        self.harness = self.bytes_to_int(self.Recivedata[5])
                        print("harness=",self.harness)
                        if self.harness == 1:
                            self.harness = 0
                        elif self.harness == 2:
                            self.harness = 1
                        else:
                            self.harness = 2
                        #Hide all checked radio
                        print("len(self.hrOnSetting)",len(self.hrOnSetting))
                        if len(self.hrOnSetting) > 0:
                            for on in range(len(self.hrOnSetting)):
                                self.hrOnSetting[on].grid_forget()

                        #Display all uncheck radio
                        if len(self.hrOffSetting) > 0:
                            for on in range(len(self.hrOffSetting)):
                                self.hrOffSetting[on].grid(row=on+1,column=0, sticky="EW",pady=5)

                        # set checked to click radio
                        self.hrOnSetting[self.harness].grid(row=self.harness+1,column=0, sticky="EW",pady=5)

                    if self.setting_cmd == SET_ROLL_DIA :
                        print("self.setting_cmd",self.setting_cmd)
                        # self.diameter = int(hexlify(self.Recivedata[6:8]), 16)
                        # self.SetDiameter = int(hexlify(self.Recivedata[6:7]), 16)
                        dia = self.bytes_to_int(self.Recivedata[6])
                        self.SetDiameter = dia
                        self.diameter.set(self.SetDiameter)
                        self.Recivedata = []
                        print(self.settingDesign)
                        print(self.harness)
                        print(self.selectDesign)
                        print(self.SetDiameter)

                    if self.setting_cmd == SET_WEFT_SLCT :
                        self.Weft_selection = self.bytes_to_int(self.Recivedata[7])
                        print("weft",self.Weft_selection)
                        if len(self.wfOnSetting) > 0:
                            for on in range(len(self.wfOnSetting)):
                                self.wfOnSetting[on].grid_forget()

                        #Display all uncheck radio
                        if len(self.wfOffSetting) > 0:
                            for on in range(len(self.wfOffSetting)):
                                self.wfOffSetting[on].grid(row=on+1,column=0, sticky="EW",pady=5)

                        # set checked to click radio
                        self.wfOnSetting[self.Weft_selection].grid(row=self.Weft_selection+1,column=0, sticky="EW")
                        self.Pick_find = self.bytes_to_int(self.Recivedata[8])
    
                        print("self.setting_cmd",self.setting_cmd)

                        if len(self.pfOnSetting) > 0:
                            for on in range(len(self.pfOnSetting)):
                                self.pfOnSetting[on].grid_forget()

                        #Display all uncheck radio
                        if len(self.pfOffSetting) > 0:
                            for on in range(len(self.pfOffSetting)):
                                self.pfOffSetting[on].grid(row=on+1,column=0, sticky="EW",pady=5)

                        # set checked to click radio
                        self.pfOnSetting[self.Pick_find].grid(row=self.Pick_find+1,column=0, sticky="EW")
                        

                    if self.setting_cmd == SET_SENSR_SETUP :
                        print("self.sensor setting",self.setting_cmd)
                        self.sensor_setup = self.bytes_to_int(self.Recivedata[9])
                        print("self.sensor_setup",self.sensor_setup)
                        print("on",len(self.snOnSetting))
                        print("off",len(self.snOffSetting))
                        if len(self.snOnSetting) > 0:
                            for on in range(len(self.snOnSetting)):
                                self.snOnSetting[on].grid_forget()

                        #Display all uncheck radio
                        if len(self.snOffSetting) > 0:
                            for on in range(len(self.snOffSetting)):
                                self.snOffSetting[on].grid(row=on+1,column=0, sticky="EW",pady=5)
                                       
                        self.snOnSetting[self.sensor_setup-1].grid(row=self.sensor_setup,column=0, sticky="EW") 
                                            
                    if self.setting_cmd == SET_NUMBER_HOOK :
                        hook="H0064 R02 C04"
                        
                        self.totalhook = self.bytes_to_int(self.Recivedata[11],0)
                        self.totalhook = self.bytes_to_int(self.Recivedata[10],self.totalhook)
                        # print(self.totalhook*8)
                        self.hookrow = self.bytes_to_int(self.Recivedata[12])
                        self.hookclm = self.bytes_to_int(self.Recivedata[13])

                        str1='{0:04d}'.format( self.totalhook*8)                     
                        str3='{0:02d}'.format(self.hookrow)
                        str4='{0:02d}'.format(self.hookclm)
   
                        hook='H'+str1+' R'+str3+' C'+str4
                        print(hook)

                        self.nf_hook.config(text='Selected hook: "'+ hook +'"')#,image=self.close_small_icon,compound=RIGHT
                        self.nf_hook.bind('<Button-1>',lambda e:self.reset_hook())
                        #If already data exists then first clear it
                        if self.no_of_hook.get() != '':
                            index = self.match_with_array(self.hooksArr,self.no_of_hook.get())
                            self.nfhookSetting[index].config(style='transparent.TButton')
                        #Set new data
                        self.no_of_hook.set(hook)
                        index = self.match_with_array(self.hooksArr,hook)
                        self.nfhookSetting[index].config(style='selected.TButton')    
                
                    self.Recivedata = []

        self.infoThreadId=self.master.after(50, self.Info_ReadSerial)

    # Info section design
    # Get Running machine's status like filename, meter, rpm, led, bundles, etc
    # you may set meter and production from here, too.
    def info_section(self):
        #info left frame
        self.InfoFrameL = Frame(self.InfoFrame, width=self.winWidth/2, height=self.frameHeight)
        self.InfoFrameL.grid(row=0,column=0,sticky='news')
        #info right frame
        self.InfoFrameR = Frame(self.InfoFrame, width=self.winWidth/2, height=self.frameHeight)
        self.InfoFrameR.grid(row=0,column=1,sticky='news')

        #info keypad frame
        self.InfoFramek = Frame(self.InfoFrame, width=self.winWidth/2, height=self.frameHeight)
        self.InfoFramek.grid_forget()

        #Current running file name display
        self.info_fname = Label(self.InfoFrameL,textvariable=self.DesignName, style='infoRect.TLabel',wraplength=400)
        self.info_fname.grid(row=0,column=0, padx=20, pady=20, ipady=10)

        ## Display current pick
        prolbl = Label(self.InfoFrameL, text="", style='infoRect.TLabel')
        prolbl.grid(row=1,column=0, padx=20, pady=20, ipady=10)

        #display pick decrease button
        self.mbtn = Label(prolbl, image=self.minus_icon,background='#526C87')
        self.mbtn.image = self.minus_icon
        self.mbtn.place(x=15,y=17)
        self.mbtn.bind("<Button>", lambda e:self.pick_update(False))

        #display pick by progress
        pro = Progressbar(prolbl, style='red.Horizontal.TProgressbar', orient = HORIZONTAL, length=200, mode='determinate',variable=self.PickBar)
        pro.place(x=85,y=15)

        #display pick value
        barlbl =  Label(prolbl,textvariable=self.Pick_txt, font="Verdana 20", foreground="#FFFFFF", background="#12355B")
        barlbl.place(x=185,y=45,anchor = CENTER)
        # barlbl.place(anchor = CENTER)

        #display pick increase button
        self.pbtn = Label(prolbl, image=self.plus_icon,background='#526C87')
        self.pbtn.image = self.plus_icon
        self.pbtn.place(x=310,y=17)
        self.pbtn.bind("<Button>", lambda e:self.pick_update(True))

        #display pick calculator button
        self.cbtn = Label(prolbl, image=self.calc_icon,background='#526C87')
        self.cbtn.image = self.calc_icon
        self.cbtn.place(x=375,y=17)

        #Bind keypad
        self.InfoFramekT = Canvas(self.InfoFramek,width=self.winWidth/2,bd=0,highlightthickness=0)
        self.InfoFramekT.grid(row=0,column=0,sticky='news')
        self.InfoFramekB = Canvas(self.InfoFramek,width=self.winWidth/2,bd=0,highlightthickness=0)
        self.InfoFramekB.grid(row=1,column=0,sticky='news',pady=35)
        self.cbtn.bind("<Button-1>", lambda e, pframe=self.InfoFramek,tab='info',st='lgkeypad.TButton':self.gen_keypad(pframe,tab,st))

        #Pick textbox value enter by calculator

        self.mEntryInfo = Entry(self.InfoFramekT, textvariable=self.Pick_txt_tmp, style='EntryStyle.TEntry',font="Verdana 30", width=12)
        self.mEntryInfo.grid(row=0,column=0, sticky="nw", padx=5)

        #Hide keypad window
        self.closeInfokeypad = Label(self.InfoFramekT,image=self.close_icon)
        self.closeInfokeypad.image = self.close_icon
        self.closeInfokeypad.bind("<Button-1>",lambda e:self.close_keypad())
        self.closeInfokeypad.grid(row=0,column=1, sticky="nw", padx=10, pady=20)

        #RPM Section
        rpmlbl = Label(self.InfoFrameL, textvariable=self.Rpm_txt, style='infoRect.TLabel')
        rpmlbl.grid(row=2,column=0, padx=20, pady=20, ipady=10)

        #Meter section
        meterlbl = Label(self.InfoFrameL, textvariable=self.Meter_txt, style='infoRect.TLabel')
        meterlbl.grid(row=3,column=0, padx=20, pady=20, ipady=10)
        #display reset button
        self.rbtn = Label(meterlbl, image=self.reset_icon,background='#526C87')
        self.rbtn.image = self.reset_icon
        self.rbtn.place(x=375,y=17)
        self.rbtn.bind("<Button>", lambda e:self.meter_reset())

        ## Right Section
        #LED section
        self.circleCanvas = Canvas(self.InfoFrameR, width=444, height=80, relief=RAISED, background="#526C87",bd=0,highlightthickness = 0)
        self.circleCanvas.grid(row=0,column=0, padx=20, pady=20)
        self.Sensor1=self.create_circle(170,40,25,self.circleCanvas, 'gray')
        self.Sensor2=self.create_circle(270,40,25,self.circleCanvas, 'gray')

        #Repeat Section
        repeatlbl = Label(self.InfoFrameR,textvariable=self.Repeat_txt, style='infoRect.TLabel')
        repeatlbl.grid(row=1,column=0, padx=20, pady=20, ipady=10)


        #Efficency section
        efflbl = Label(self.InfoFrameR, textvariable=self.Efficiency_txt, style='infoRect.TLabel')
        efflbl.grid(row=2,column=0, padx=20, pady=20, ipady=10)

        #Bundle section
        bundlelbl = Label(self.InfoFrameR,textvariable=self.Bundle_txt, style='infoRect.TLabel')
        bundlelbl.grid(row=3,column=0, padx=20, pady=20, ipady=10)

        # self.master.after(250, self.Info_ReadSerial)

    #Close keypad window
    def close_keypad(self):
        self.InfoFramek.grid_forget()
        self.Pick_txt_tmp.set('')
        self.InfoFrameR.grid(row=0,column=1,sticky='news')
        self.cbtn.config(state=NORMAL)

    #Genearte circle
    def create_circle(self, x, y, r, cname, colorname, outlinec = ''):
        x0 = x - r
        y0 = y - r
        x1 = x + r
        y1 = y + r
        return cname.create_oval(x0, y0, x1, y1, fill=colorname, outline=outlinec)

    #Stop info tab reading data
    def Stop_INFO(self):
        self.ser.write(MAIN_ADD)
        self.ser.write(INFO_STOP)
        self.ser.write(EOD)

    #Update pick on info section
    def pick_update(self,is_add):
        if is_add:
            self.ser.write(MAIN_ADD)
            self.ser.write(PICK_UP)
            self.ser.write(EOD)
            # self.Pick_txt.set(self.Pick_txt.get() + 1)
            # if self.Pick_txt.get() > 0:
            #     self.mbtn.config(state=NORMAL)
        else:
            self.ser.write(MAIN_ADD)
            self.ser.write(PICK_DOWN)
            self.ser.write(EOD)
            # if self.Pick_txt.get() <= 0:
            #     self.messagebox('Warning', 'You can not set pick less than 0')
            # else:
            #     self.Pick_txt.set(self.Pick_txt.get() - 1)
            #     if self.Pick_txt.get() <= 0:
            #         self.mbtn.config(state=DISABLED)

    #Reset Meter production
    def meter_reset(self):
        # conMsg = messagebox.askquestion('Reset meter', 'Are you sure you want to\nReset meter?')
        conMsg =self.ask_messagebox( 'Are you sure you want to\nReset meter?','info')
        print("ASK msg box out")
        # conMsg=self.input_str
        # print("conMsg",self.input_str)
        # if conMsg == 'yes':
        #     print(conMsg)
        #     self.ser.write(MAIN_ADD)
        #     self.ser.write(RESET_PROD)
        #     self.ser.write(EOD)
        # self.master.overrideredirect(False)
    # Files Section
    # Get List of files from resources/files folder
    # View Single File, Delete multiple files
    # Display selected single file beside table
    # Display design name + Enter meter by keypad and send to controller
    def files_section(self):
        if len(self.fileRowsOri) > 0:
            self.FileFrameLeft = Frame(self.FileFrame, width=self.winWidth/2,height=self.frameHeight)
            self.FileFrameLeft.grid(row=0,column=0, pady=(0,10), sticky='nw')

            #Start Action button frame
            self.FileFrameAction = Frame(self.FileFrameLeft, width=self.winWidth/2,height=self.menuHeight)
            self.FileFrameAction.grid(row=0,column=0, pady=(0,10), sticky='nw')

            self.FileFrameDesign = Frame(self.FileFrame, width=self.winWidth/2,height=self.frameHeight-80)
            self.FileFrameDesign.grid_forget()

            #Search bar section
            self.searchEntry = Entry(self.FileFrameAction, textvariable=self.search_file_str, style='EntryStyle.TEntry',font="Verdana 15", width=16)
            self.searchEntry.grid(row=0,column=0, sticky="news")
            #Search button for search file
            self.searchBtn = Button(self.FileFrameAction,
                    text='Find',
                    image=self.search_icon,
                    style='file.TButton',
                    compound=TOP,
                    # padding=10,
                    state=DISABLED,
                    command= lambda :self.search_files('files'))
            # self.searchBtn.image = self.search_icon
            self.searchBtn.grid(row=0,column=1, sticky="news",padx=1)

            self.searchEntry.bind('<FocusIn>',lambda e:self.fin_searchbar('files'))
            self.searchEntry.bind('<Button-1>',lambda e:self.fin_searchbar('files'))
            self.searchEntry.bind('<KeyRelease>',lambda e:self.autosearch_files('files'))

            #Close searchbar
            self.fcloseBtn = Label(self.FileFrameAction,
                    image=self.close_icon)
            self.fcloseBtn.image = self.close_icon
            self.fcloseBtn.grid_forget()
            self.fcloseBtn.bind('<Button>', lambda e: self.fout_searchbar('files',True))

            #View button for view image
            self.fviewBtn = Button(self.FileFrameAction,
                    text='View',
                    image=self.view_icon,
                    style='file.TButton',
                    compound=TOP,
                    # padding=10,
                    command= lambda tab='files': self.view_file(tab))
            # self.fviewBtn.image = self.view_icon
            self.fviewBtn.grid(row=0,column=2, padx=10)

            #Del button for delete multiple image
            self.fdelBtn = Button(self.FileFrameAction,
                    text='Delete',
                    image=self.del_icon,
                    style='file.TButton',
                    compound=TOP,
                    # padding=10,
                    command=self.delete_file)
            self.fdelBtn.image = self.del_icon
            self.fdelBtn.grid(row=0,column=3)

            Label(self.FileFrameAction, textvariable=self.totalfilefound, style='file.TButton',font="Verdana 15").grid(row=0,column=4,padx=10, sticky="news")
            self.filesfound = Label(self.FileFrameAction, text='', style='lblBody.TLabel')

            #Start Scrollbar section of Table
            self.FileFrameTable = Frame(self.FileFrameLeft, width=self.winWidth/2,height=self.frameHeight-80)
            self.FileFrameTable.grid(row=2,column=0, sticky='nw')

            #files collect
            tCols = ['Name','DateTime']

            #Parameter
            #1:Frame outer
            #2:rows
            #3:columns
            #4:Required checkbox
            self.gen_table(self.FileFrameTable,self.fileRows,tCols,'files',True)
            #End Scrollbar section of Table

            #Active search section
            self.activeSearch = Frame(self.FileFrameLeft, width=self.winWidth/2)
            self.activeSearch.grid_forget()

            lbl = Label(self.activeSearch,textvariable=self.active_search,style='fileRes.TLabel',font="Verdana 14 bold",wraplength=400)
            lbl.grid(row=0,column=0,sticky='nw')

            btn = Button(self.activeSearch,text='Clear',command=lambda :self.clear_files('files',True), style='bgray.TButton')
            btn.grid(row=0,column=1,sticky='nw',padx=10,pady=(0,5))

            ##Start Design Selected image section for send on controller
            self.FileFrameDesignlbl = Frame(self.FileFrameDesign)
            self.FileFrameDesignlbl.grid(row=0,column=0,padx=(15,5),pady=(0,5), sticky='news')
            #Display selected File name
            dlbl = Label(self.FileFrameDesignlbl, text='Design',style='file.TLabel')
            dlbl.grid(row=0,column=0, sticky="nw")
            self.designName = Label(self.FileFrameDesignlbl, text='',style='fileRes.TLabel', wraplength=self.winWidth/2.5)
            self.designName.grid(row=1,column=0, sticky="nw")

            #Enter Meter
            self.FileFrameDesignM = Frame(self.FileFrameDesign)
            self.FileFrameDesignM.grid(row=1,column=0,padx=(15,5),pady=(0,5), sticky='news')

            self.pick = StringVar()
            mlbl = Label(self.FileFrameDesignM, text='Meter',style='file.TLabel', padding=0)
            mlbl.grid(row=0,column=1, sticky="nw", padx=5, pady=15)
            self.mEntryFile = Entry(self.FileFrameDesignM, textvariable=self.pick, style='EntryStyle.TEntry',font="Verdana 15", width=10)
            self.mEntryFile.grid(row=0,column=0, sticky="nw")

            #Start Meter keypad
            self.FileFrameDesignKpad = Frame(self.FileFrameDesign, width=200,height=200)
            self.FileFrameDesignKpad.grid(row=2,column=0, sticky='news', padx=10)
            self.gen_keypad(self.FileFrameDesignKpad,'files','lgkeypad.TButton')
            #End Meter keypad
            #End Design Selected image section for send on controller


            #Call full keypad
            self.gen_search_area(self.FileFrame,'files')
            #End search file section
        else:
            self.reset_frame(self.FileFrame)
            loaderLbl = Label(self.FileFrame,
                    text='Please copy files from PenDrive to see list of files.',
                    style='fileRes.TLabel',
                    font='Verdana 25',
                    anchor="center", width=40)
            loaderLbl.grid(row=0,column=0,padx=(30,0),pady=(200,0),sticky='news')

    #Calling search area
    def gen_search_area(self,pframe,tab):
        #Call full keypad
        self.searchArea = Frame(pframe,width=self.winWidth)
        self.searchArea.grid_forget()

        self.searchAreaResCanvas = Canvas(self.searchArea,width=self.winWidth,height=150,bd=0,highlightthickness=0)
        self.searchAreaResCanvas.grid(row=0,column=0,sticky='news')

        self.gen_full_keypad(self.searchArea,tab)

    #Get files data from files directory
    def files_feed(self,dir,is_path=False,match=''):
        rows = []
        # print("filesfeed")
        for r, dirs, fnames in os.walk(dir):
            # print("\ndir",dir,r)
            # for fname in fnmatch.filter(fnames, '*.bmp'):
            for fname in fnames:
                if fname.lower().endswith('.bmp'):
                    if is_path:
                        if match != '':
                            # print('1')
                            if fname.find(match) is not -1:
                                print('*')
                                rows.append((fname,
                                            r,
                                            time.ctime(os.path.getmtime(os.path.join(r, fname)))))
                        else:
                            # print('2')
                            rows.append((fname,
                                            r,
                                            time.ctime(os.path.getmtime(os.path.join(r, fname)))))
                    else:
                        if match != '':
                            # print('3')
                            if fname.find(match) is not -1:
                                # print('*')
                                rows.append((fname,
                                            time.ctime(os.path.getmtime(os.path.join(r, fname)))))
                        else:
                            # print('4')
                            rows.append((fname,
                                        time.ctime(os.path.getmtime(os.path.join(r, fname)))))

        # print(rows)
        return rows

    #Genrate table with vertical
    #pframe = parent frame
    #rows_coll = number of rows error
    #col_coll = number of column array
    #is_chkbox = if user needs checkbox in table
    def gen_table(self,pframe,rows_coll,col_coll=[],tab='',is_chkbox=False):
        self.FileChked = []
        self.FileUnChkLblAll = []
        self.FileChkLblAll = []
        #Remove old childs of table
        for child in pframe.winfo_children():
            child.destroy()

        canvas = Canvas(pframe, background="#FFFFFF",bd=0,highlightthickness = 0)
        canvas.grid(row=0,column=0, sticky='news')

        vsb =  Scrollbar(pframe, orient='vertical', command=canvas.yview, style='Vertical.TScrollbar')
        vsb.grid(row=0,rowspan=7,column=1, sticky='ns')
        canvas.configure(yscrollcommand=vsb.set)

        innFrame = Frame(pframe)
        canvas.create_window((0,0), window=innFrame, anchor='nw')
        dw = 931
        dh=380
        if tab == 'files': dw = 546

        #if checkbox allowed and column exists then display
        if len(col_coll) > 0 and is_chkbox:
            #Start Check all and uncheckall checkbox design
            self.unchkAlllbl = {}
            self.unchkAlllbl = Label(innFrame, image=self.unchkall_icon,style='tableTH.TLabel')
            self.unchkAlllbl.image = self.unchkall_icon
            self.unchkAlllbl.grid(row=0,column=0, sticky="nsew")

            self.chkAlllbl = {}
            self.chkAlllbl = Label(innFrame, image=self.chkall_icon,style='tableTH.TLabel')
            self.chkAlllbl.image = self.chkall_icon
            self.chkAlllbl.grid_forget()

            self.unchkAlllbl.bind("<Button-1>", lambda e, unclbl = self.unchkAlllbl, clbl = self.chkAlllbl, chked = True, row = 0, col = 0: self.chk_all_file(unclbl,clbl,chked,row,col,tab))
            self.chkAlllbl.bind("<Button>", lambda e, unclbl = self.unchkAlllbl, clbl = self.chkAlllbl, chked = False, row = 0, col = 0: self.chk_all_file(clbl,unclbl,chked,row,col,tab))
            #End Check all and uncheckall checkbox design

        #if column allowed
        if len(col_coll) > 0:
            for c in range(len(col_coll)):
                clbl = Label(innFrame, text=col_coll[c],style='tableTH.TLabel')
                clbl.grid(row=0, column=c+1, sticky="nsew")

        #if data found
        self.totalfilefound.set(str(len(rows_coll))+" items")
        if len(rows_coll) > 0:
            print("file found",len(rows_coll))

            for r in range(len(rows_coll)):
                if is_chkbox:
                    fname = rows_coll[r][0]
                    if tab == 'usb':
                        fname = rows_coll[r]
                        # print("fname",fname)
                    #Start Un Checlbox Design
                    unchklbl = {}
                    unchklbl = Label(innFrame, text='', image=self.unchk_icon,style='tableTD.TLabel',compound=LEFT)
                    unchklbl.image = self.unchk_icon
                    unchklbl.grid(row=r+1,column=0, sticky="nsew")
                    unchklbl.bind("<Button>", lambda e, index = r, fname = fname , chked = True, row = r+1, col = 0: self.chk_single_file(index,fname,chked,row,col,tab))
                    self.FileUnChkLblAll.append(unchklbl)
                    #End Un Checlbox Design

                    #Start Checlbox Design
                    chklbl = {}
                    chklbl = Label(innFrame, text='', image=self.chk_icon,style='tableTD.TLabel',compound=LEFT)
                    chklbl.image = self.chk_icon
                    chklbl.bind("<Button-1>", lambda e, index = r, fname = fname, chked = False, row = r+1, col = 0: self.chk_single_file(index,fname,chked,row,col, tab))
                    self.FileChkLblAll.append(chklbl)
                    chklbl.grid_forget()
                    #Start Checlbox Design

                if len(col_coll) > 0:
                    #Start Display other rows and cols
                    for c in range(len(col_coll)):
                        if tab == 'files':
                            w = 15
                            wl = 180
                            if c == 1:
                                w = 22
                                wl = 260
                        elif tab == 'usb':
                            w = 23
                            wl = 280
                            if c == 1:
                                w = 18
                                wl = 200
                            if c == 2:
                                w = 22
                                wl = 260

                        #Set style
                        st = 'tableTD.TLabel'
                        if tab == 'usb' and c == 0 and os.path.isdir(os.path.join(rows_coll[r][1],rows_coll[r][0])):
                            st = 'tableTDD.TLabel'

                        #Update lable name
                        tname = rows_coll[r][c]
                        # print("tname",tname)
                        if tab == 'usb' and c == 1:
                            tname = rows_coll[r][c].replace(self.pendrive_dir,'')

                        rlbl = Label(innFrame, text=tname,style=st, width=w,wraplength=wl)
                        if tab == 'usb' and c == 0 and os.path.isfile(os.path.join(rows_coll[r][1],rows_coll[r][0])):
                            rlbl.config(image=self.file_icon)
                            rlbl.config(compound=LEFT)
                            rlbl.image = self.file_icon

                        rlbl.grid(row=r+1, column=c+1, sticky="nsew")

                        #Set bind event if directory found
                        if tab == 'usb' and c == 0 and os.path.isdir(os.path.join(rows_coll[r][1],rows_coll[r][0])):
                            rlbl.config(image=self.folder_icon)
                            rlbl.config(compound=LEFT)
                            rlbl.image = self.folder_icon
                            # if len(os.path.join(rows_coll[r][1],rows_coll[r][0]))<100:
                            rlbl.bind('<Button-1>', lambda e, dname=(os.path.join(rows_coll[r][1],rows_coll[r][0])):self.jump_to_folder(dname))

                    #End Display other rows and cols
                else:
                    #Start Display other rows
                    w = 20
                    wl = 250
                    rlbl = Label(innFrame, text=rows_coll[r],style='tableTD.TLabel', width=w,wraplength=wl)
                    rlbl.grid(row=r+1, column=0, sticky="nsew")
                    #End Display other rows

        else:

            dh=90
            rlbl = Label(innFrame, text="No more records are found.",style='tableTD.TLabel',width=76)

            rlbl.grid(row=1, column=0, columnspan=len(col_coll)+1, sticky="nsew")

        innFrame.update_idletasks()
        bbox = canvas.bbox('all')
        print("dw=",dw)
        print("dh=",dh)
        canvas.config(scrollregion=bbox, width=dw, height=dh)
        return

    def jump_to_last_dir(self):
        last = ''
        root_path = ''
        print(self.usb_last_dir)
        self.usb_last_dir = self.usb_last_dir[:-1]
        if len(self.usb_last_dir) > 0: last = self.usb_last_dir[-1]

        print("last=",self.usb_last_final_dir)
        if len(self.usb_last_dir) == 0 and self.usb_last_final_dir != '':
            print("comes=",len(os.listdir(self.pendrive_dir)))
            for root in os.listdir(self.pendrive_dir):
                test_path = ''
                test_path = os.path.join(self.pendrive_dir,root)
                print(test_path)
                if os.access(test_path,os.R_OK) and os.access(test_path,os.W_OK) and os.access(test_path,os.X_OK):
                    root_path = os.path.join(self.pendrive_dir,root)
                    if self.usb_last_final_dir.find(root_path) == -1: root_path = ''
                else:
                    continue


            last = root_path


        if len(self.usb_last_dir) > 0 or last != '':
            self.jump_to_folder(last,False)
            if len(self.usb_last_dir) == 0 and self.usb_last_final_dir != '':
                self.back_usb_btn.place(x=-100,y=-100)
        else:
            self.USBFrameTable.grid_forget()
            time.sleep(1)
            self.usb_section(True)
        return

    def jump_to_folder(self, dname, is_forward=True):

        match = ''
        nmatch = self.search_file_str_usb.get()
        self.usb_files = self.dis_subdir(dname,match)
        # print(type(self.usb_files))
        # print("lenth of files=",len(self.usb_files))
        # print("sizeof arrey",getsizeof(self.usb_files,set()))
        # print("sizeof arrey",asizeof(self.usb_files))
        if sum(map(len,self.usb_files))< 600 :
        # if asizeof(self.usb_files) > 0:
            self.USBFrameTable.grid_forget()
            self.reset_frame(self.USBFrameTable)
            self.usb_files = []

            if len(nmatch) > 0:
                match = nmatch
            self.usb_files = self.dis_subdir(dname,match)
            #files collect
            tCols = ['Name','Folder','DateTime']

            print("Dname",dname)
            print("match",match)

            #Parameter
            #1:Frame outer
            #2:rows
            #3:columns
            #4:Required checkbox
            print("type=",type(self.usb_files))

            print("self.usb_files=",self.usb_files)
            self.gen_table(self.USBFrameTable,self.usb_files,tCols,'usb',True)

            self.USBFrameTable.grid(row=2,column=0, sticky='nw')

            # store last directory name
            if is_forward:
                self.usb_last_dir.append(dname)

            self.back_usb_btn.place(x=860,y=30)
            #End Scrollbar section of Table
            return
        else :
            self.messagebox('Error','Folder name is too long.')

    #focus into searchbar
    def fin_searchbar(self,tab):
        self.searchEntry.config(width=62)
        self.fviewBtn.grid_forget()
        self.fcloseBtn.grid(row=0,column=2, sticky="news",padx=(40,20))
        self.searchArea.grid(row=1,column=0,sticky='news')
        self.activeSearch.grid_forget()
        if tab == 'usb':
            self.USBFrameTable.grid_forget()
            self.fcopyBtn.grid_forget()
            self.back_usb_btn.place(x=-100,y=-100)
            if len(self.usb_last_dir) > 0:
                self.usb_last_final_dir = self.usb_last_dir[-1]

        elif tab == 'files':
            self.FileFrameTable.grid_forget()
            self.FileFrameDesign.grid_forget()
            self.fdelBtn.grid_forget()

        #Remove all children of search result section
        self.reset_frame(self.searchAreaResCanvas)
        return

    #focus out searchbar
    def fout_searchbar(self,tab,is_base=False):
        self.search_file_str.set('')
        if is_base and tab == 'usb':
            self.search_file_str_usb.set('')
            self.searchEntry.config(width=24)
        else:
            self.searchEntry.config(width=16)
        self.searchBtn.config(state=DISABLED)
        self.fviewBtn.grid(row=0,column=2,padx=10)
        self.fcloseBtn.grid_forget()
        self.searchArea.grid_forget()
        if tab == 'usb':
            self.USBFrameTable.grid(row=2,column=0, sticky='nw')
            self.fcopyBtn.grid(row=0,column=3)
            if len(self.usb_last_dir) > 0:
                self.back_usb_btn.place(x=860,y=30)
            self.usb_last_final_dir = ''
        elif tab == 'files':
            self.fdelBtn.grid(row=0,column=3)
            self.FileFrameTable.grid(row=2,column=0, sticky='nw')

        self.master.focus()
        return

    #Search files
    def search_files(self,tab):

        print("serch file")
        if tab == 'usb':
            dlen = len(self.usbRows)
        elif tab == 'files':
            dlen = len(self.fileRows)
        print("find files")
        #Clear section before update new data
        self.clear_files(tab)
        self.activeSearch.grid(row=1,column=0, sticky='nw')
        self.active_search.set('Search: "'+self.search_file_str.get()+'"('+str(dlen)+')')
        self.search_file_str.set('')
        if self.usb_last_final_dir != '':
            last_path = self.usb_last_final_dir

            self.usb_last_dir = []
            root_path = ''
            for root in os.listdir(self.pendrive_dir):
                test_path = ''
                test_path = os.path.join(self.pendrive_dir,root)
                print("root_path=",test_path)
                if os.access(test_path,os.R_OK) and os.access(test_path,os.W_OK) and os.access(test_path,os.X_OK):
                    root_path = os.path.join(self.pendrive_dir,root)
                    if last_path.find(root_path) == -1: root_path = ''
                else:
                    continue

            last_path = last_path.replace(root_path,'').split('/')
            print(last_path)

            if len(last_path) > 0:
                for l in range(len(last_path)):
                    if last_path[l] != '':
                        p = root_path+'/'+last_path[l]
                        self.usb_last_dir.append(p)
                        root_path = p

            if len(self.usb_last_dir) > 0:
                self.back_usb_btn.place(x=860,y=30)
        return

    #Clear main file section
    #based = if it is full resh and wants to get files
    #from directory then set True otherwise False
    def clear_files(self,tab,based=False):
        if tab == 'files':
            self.reset_frame(self.FileFrame)
        elif tab == 'usb':
            self.reset_frame(self.USBFrame)

        #Get fresh files from directory
        if based:
            if tab == 'files':
                self.fileRowsOri = self.fileRows = self.files_feed(self.files_dir)
                self.search_file_str.set('')

        time.sleep(1)
        #Update file section
        self.FileChked = []
        self.FileUnChkLblAll = []
        self.FileChkLblAll = []
        if tab == 'files':
            self.files_section()
        elif tab == 'usb':
            if based:
                self.usb_section(True)
                self.search_file_str.set('')
            else:
                self.usb_section()

        self.active_search.set('')
        return

    #Auto search files
    def autosearch_files(self,tab):
        fileRowsTemp = []
        fileOriTemp = []
        print("auto serch file")
        #if search text exists then search icon open
        if len(self.search_file_str.get()) > 0:
            self.searchBtn.config(state=NORMAL)
        else:
            self.searchBtn.config(state=DISABLED)

        self.search_file_str_usb.set(self.search_file_str.get())

        #Loop files array
        dir = ''
        if tab == 'files':
            fileOriTemp = self.fileRowsOri
        elif tab == 'usb':
            if len(self.usb_last_dir) > 0:
                dir = self.usb_last_dir[-1]
            fileOriTemp = self.usbRowsOri

        if len(fileOriTemp) > 0 and len(self.search_file_str.get()) > 0:
            for f in range(len(fileOriTemp)):
                if dir != '' and fileOriTemp[f][1].find(dir) == -1:
                   continue
                find_word=self.search_file_str.get()
                if find_word.lower() in fileOriTemp[f][0].lower():
                # if  self.search_file_str.get().lower in fileOriTemp[f][0].lower():
                    fileRowsTemp.append(fileOriTemp[f])

            #if search result got then disaply files in listbox
            if len(fileRowsTemp) > 0:
                Lb1 = Listbox(self.searchAreaResCanvas,bd=0,width=63,height=5,selectbackground = '#12355B', highlightthickness = 0, font="Verdana 16",relief=GROOVE, selectmode=SINGLE)
                scrollbar = Scrollbar(self.searchAreaResCanvas, orient=VERTICAL)
                Lb1.config(yscrollcommand=scrollbar.set)
                scrollbar.config(command=Lb1.yview)
                #insert into listbox
                for l in range(len(fileRowsTemp)):
                    Lb1.insert(END, fileRowsTemp[l][0])
                    if tab == 'usb':
                        Lb1.insert(END, fileRowsTemp[l][1].replace(self.pendrive_dir,''))
                    Lb1.insert(END, '')

                Lb1.bind("<<ListboxSelect>>",lambda e:self.select_single_file(e,tab))
                Lb1.grid(row=0,column=0,sticky='nw',pady=(0,15))
                scrollbar.grid(row=0,column=1, sticky='ns')

        else:
            #if no data in search then remove elements from frame
            self.reset_frame(self.searchAreaResCanvas)
            self.messagebox('Warning','Nomore files are available in system.')

        if tab == 'usb':
            print("usb")
            self.usb_files = []
            self.usbRows = []
            self.usbRows = fileRowsTemp
            if len(fileRowsTemp) > 0:
                if self.usb_last_final_dir != '':
                    self.usb_files = self.dis_subdir(self.usb_last_final_dir,self.search_file_str.get())
                else:
                    #Get root structure
                    for root in os.listdir(self.pendrive_dir):
                        root_path = os.path.join(self.pendrive_dir,root)
                        if os.access(root_path,os.R_OK) and os.access(root_path,os.W_OK) and os.access(root_path,os.X_OK):
                            self.usb_files = self.usb_files + self.dis_subdir(root_path,self.search_file_str.get())

        elif tab == 'files':
            self.fileRows = []
            self.fileRows = fileRowsTemp
        return

    #Get single file on select list box item
    #event= click of single file clicked
    def select_single_file(self,event,tab):
        var = event.widget.curselection()[0]
        path_index = 0

        #Clear blank list item click
        if tab == 'files':
            if var%2 != 0:
                event.widget.select_clear(var)
                event.widget.select_set(var-1)
        elif tab == 'usb':
            if var == 0 or var%3 == 0:
                path_index = int(var) + 1
            elif (var+1)%3 == 0:
                path_index = int(var) - 1
                event.widget.select_clear(var)
                event.widget.select_set(var-2)
            else:
                path_index = int(var)
                event.widget.select_clear(var)
                event.widget.select_set(var-1)

        w = event.widget
        index = int(w.curselection()[0])
        value = w.get(index)

        fileOriTemp = []
        fileRowTemp = []
        if tab == 'files':
            fileOriTemp = self.fileRowsOri
        elif tab == 'usb':
            fname = value
            path = w.get(path_index)
            r = self.pendrive_dir+path
            fileRowTemp.append((fname,r,time.ctime(os.path.getmtime(os.path.join(r, fname)))))


        if len(fileOriTemp) > 0:
            for f in range(len(fileOriTemp)):
                if fileOriTemp[f][0].find(value) is not -1:
                    fileRowTemp.append(fileOriTemp[f])

        if len(fileRowTemp) > 0:

            if tab == 'usb':
                #Get root structure
                dtxt = fileRowTemp[0]
                self.usb_files = []
                self.usb_files = fileRowTemp
            else:
                dtxt = fileRowTemp[0][0]
                self.fileRows = fileRowTemp
            #Clear main file section before update new data
            self.clear_files(tab)
            self.chk_single_file(0,dtxt,True,1,0,tab)
            self.activeSearch.grid(row=1,column=0, sticky='nw')
            self.active_search.set('Search: "'+fileRowTemp[0][0]+'"')
            self.search_file_str.set('')
            self.usb_last_dir = []
        return

    #Generate full keypad
    #pframe = parent frame
    # def gen_full_keypad(self, pframe, tab):
    #     self.keypadCanvas = Canvas(pframe,width=self.winWidth,height=200,bd=0,highlightthickness = 0)
    #     self.keypadCanvas.grid(row=1,column=0,sticky='ews',ipadx=10,ipady=10,pady=2)

    #     r = 0
    #     for key_bunch in self.keyboard_keys:
    #         keypadFrame = Frame(self.keypadCanvas,width=self.winWidth)
    #         keypadFrame.grid(row=r,column=0,sticky='news')
    #         r += 1
    #         c = 0
    #         for k in key_bunch:
    #             k=k.capitalize()
    #             if len(k)<=3:
    #                 keypadBtn = Button(keypadFrame, text=k, width=2, style='lgkeyboard.TButton',command=lambda q=k.lower(): self.keyboard_event(q,tab))
    #             else:
    #                 keypadBtn = Button(keypadFrame, text=k.center(5,' '), style='lgkeyboard.TButton',command=lambda q=k.lower(): self.keyboard_event(q,tab))
    #             # if " " in k:
    #             #     keypadBtn['state']='disable'

    #             # keypadBtn['command']=lambda q=k.lower(): self.keyboard_event(q)
    #             keypadBtn.grid(row=0,column=c,sticky='news',padx=5,pady=5)
    #             c += 1
    #     return
    
    def gen_full_keypad(self, pframe,tab,kboard='std'):
        self.keypadCanvas = Canvas(pframe,width=self.winWidth,height=200,bd=0,highlightthickness = 0)
        self.keypadCanvas.grid(row=1,column=0,sticky='ews',ipadx=10,ipady=10,pady=2)

        r = 0
        if kboard == 'full':
            keyarr = self.keyboard_keys_all
        else:
            keyarr = self.keyboard_keys    
        for key_bunch in keyarr:
            keypadFrame = Frame(self.keypadCanvas,width=self.winWidth)
            keypadFrame.grid(row=r,column=0,sticky='news')
            r += 1
            c = 0 
            for k in key_bunch:
                k=k.capitalize()
                if len(k)<=3:
                    keypadBtn = Button(keypadFrame, text=k, width=2, style='lgkeyboard.TButton',command=lambda q=k.lower(): self.keyboard_event(q,tab))
                else:
                    keypadBtn = Button(keypadFrame, text=k.center(5,' '), style='lgkeyboard.TButton',command=lambda q=k.lower(): self.keyboard_event(q,tab))
                # if " " in k:
                #     keypadBtn['state']='disable'
                
                # keypadBtn['command']=lambda q=k.lower(): self.keyboard_event(q)
                keypadBtn.grid(row=0,column=c,sticky='news',padx=5,pady=5)
                c += 1
        return
    

    #Keyboard event handling	
    #key = keyboard key name
    # def keyboard_event(self,key,tab):
    #     str_data = self.search_file_str.get()
    #     if key == 'enter':
    #         self.search_files(tab)
    #     elif key == '<x':
    #         str_data = str_data[:-1]
    #         self.search_file_str.set(str_data)
    #         self.autosearch_files(tab)
    #     else:
    #         str_data += key
    #         self.search_file_str.set(str_data)
    #         self.autosearch_files(tab)
    #     return

    def keyboard_event(self,key,tab):
        print(key)
        if tab == 'setting' or tab == 'wifi':
            str_data = self.password_str.get()
        else:
            str_data = self.search_file_str.get()

        if key == 'enter':
            if tab == 'setting' or tab == 'wifi':
                self.check_password(tab,'wifi')
            else:    
                self.search_files(tab)
        elif key == 'caps':   
            if self.letter_up:
                self.capsLbl.config(text='Capsloack: OFF')
                self.letter_up = False
            else:
                self.capsLbl.config(text='Capsloack: ON')
                self.letter_up = True    
        elif key == '<x':    
            str_data = str_data[:-1]
            if tab == 'setting' or tab == 'wifi':
                self.password_str.set(str_data)    
            else:    
                self.search_file_str.set(str_data)    
                self.autosearch_files(tab)
        else:    
            if self.letter_up:
                str_data += key.upper()
            else:    
                str_data += key

            if tab == 'setting' or tab == 'wifi':
                self.password_str.set(str_data)    
            else:    
                self.search_file_str.set(str_data)    
                self.autosearch_files(tab)
        return
    
    #Send file to HMI
    def Send_Bmp_fileToMcu(self):
        # print('b')
        CopyTimestart=perf_counter()
        if len(self.FileChked) > 0 :
        #Display loader while copy files
            # messagebox.OK('OK','File copied')
            self.Msgstring = ''
            self.Read_line = []
            # self.is_animate = True
            # self.call_loader('Copying file to system....',True,'files')

            filepath = os.path.join(self.files_dir,self.FileChked[0])
            # print(filepath)
            filedata = open(filepath,"rb")
            data = bytearray(filedata.read())
            filedata.close()
            fileName=os.path.basename(filepath)
            fileNameLenth= len(fileName)
            Namelenth=tuple( struct.pack("!I",len(fileName)) )
            print(fileName)
            print(Namelenth[3:])
            print(len(fileName))
            Meters = self.pick.get()
            print(Meters)
            Meters_int = int(Meters)
            Meter_arry=( struct.pack("<H",Meters_int) )         #send data lenth of packet
            print('meters',Meter_arry)
            Datalenth = len(data)
            print(Datalenth)
            Filesize=tuple( struct.pack("!I",len(data)) ) #conver string to byte arr
            print(Filesize)
            Sentdata=0

            DataFlg=0
            if  Datalenth > 16384 :
                SendDatalenth = 16384
            else :
                SendDatalenth= Datalenth

            self.Test_flg = 0
            print(Datalenth)
            self.ser.write(MAIN_ADD)            #send start byte
            self.ser.write(FILE_INQ)            #send conformation command
            self.ser.write(Namelenth[3:])         #file name lenth 1 byte
            self.ser.write(fileName.encode('utf-8'))      #first 8 char of file name
            self.ser.write(Meter_arry[0:2])         #send meters for production
            self.ser.write(data[18:20])    # send width of file
            self.ser.write(data[22:24])    # send hight of file
            self.ser.write(Filesize)             #send file data size
            self.ser.write(EOD)            # send end byte of file
            count=0
            # Test_timer = threading.Timer(5.0, self.Check_test_responce)
            # Test_timer.start()

            while count < 20000:             # wait for Mcu confirmation
                Read_Data  = self.ser.read()

                if len(Read_Data) !=0:
                    self.Read_line.append(Read_Data)
                    print("Read_Data=",Read_Data)

                if len(self.Read_line) > 10 :
                    self.Read_line = []
                    self.ser.flushInput()
                # if len(self.Red_line) > 3 :
                    # print(Read_line)

                # val = self.ser.readline()
                # if len(val)>0:
                    # print(val)
                # time.sleep(0.10)
                # print(count)
                count += 1

                if len(self.Read_line) == 3 and (self.Read_line[0] == DISPLAY_ADD)and(self.Read_line[1] == COPY_FILE)and(self.Read_line[len(self.Read_line)-1] == EOD):
                    self.Read_line = []
                    self.ser.flushInput()
                    DataFlg=1
                    print("file copy start")
                    count=0
                    break
                elif len(self.Read_line) == 3 and (self.Read_line[0] == DISPLAY_ADD)and(self.Read_line[1] == ERR_CPY)and(self.Read_line[len(self.Read_line)-1] == EOD):
                    DataFlg=0
                    self.Read_line = []
                    self.ser.flushInput()
                    print("data repeat")
                    break
                elif len(self.Read_line) == 3 and (self.Read_line[0] == DISPLAY_ADD)and(self.Read_line[1] == MAIN_INVLD)and(self.Read_line[len(self.Read_line)-1] == EOD):
                    self.sendbmptimer.cancel()
                    self.Read_line = []
                    self.ser.flushInput()
                    DataFlg=3
                    self.Msgstring='INVALID file'
                    count=0
                    break
                elif len(self.Read_line)== 4 and self.Read_line[0] == DISPLAY_ADD and self.Read_line[len(self.Read_line)-1] == EOD and self.Read_line[1] == ERR:
                    self.sendbmptimer.cancel()
                    if self.Read_line[2] == CARD_NOT_DETECT:
                        self.Msgstring='CARD NOT DETECT'
                    if self.Read_line[2] ==CARD_INIT_FAIL:
                        self.Msgstring='CARD INITIALIZE FAIL'
                    if self.Read_line[2] ==FAT32_NOT_FOUND :
                        self.Msgstring='FAT32 NOT FOUND'
                    if self.Read_line[2] == ERROR_IN_CLUSTER :
                        self.Msgstring='ERROR IN CLUSTER'
                    if self.Read_line[2] == DSGN_NOT_FOUND :
                        self.Msgstring='DESIGN NOT FOUND'
                    if self.Read_line[2] == DSGN_INVALID :
                        self.Msgstring='DESIGN INVALID'
                    self.Read_line = []
                    self.ser.flushInput()
                    count=0
                    break
                if self.Test_flg == 2:
                    break

                # time.sleep(1)

            if DataFlg == 0:
                self.sendbmptimer.cancel()
                self.Msgstring='Communication error'

            if DataFlg == 1:
                while True:
                    if Datalenth-Sentdata < SendDatalenth :
                        SendDatalenth= Datalenth-Sentdata
                        print("send data lenth=",SendDatalenth)
                    if DataFlg==1 :
                        # data send command
                        DataFlg=0
                        # time.sleep(.500)
                        print("New data")
                        print("sent data =",SendDatalenth)
                        self.ser.write(MAIN_ADD)
                        self.ser.write(FLE_DTA)
                        ii=tuple( struct.pack("!I",SendDatalenth) )         #send data lenth of packet
                        # print('size of data=',ii[2:])
                        self.ser.write(ii[2:])
                        self.ser.write(data[Sentdata:Sentdata+SendDatalenth])
                        self.ser.write(EOD)                             #end of data
                        count=0
                        self.Read_line = []
                        while count < 50000:      # wait for Mcu confirmation
                            # print(count)
                            # time.sleep(1)
                            count += 1
                            # val = self.ser.readline()
                            Read_Data  = self.ser.read()
                            # print(Read_Data)

                            if len(Read_Data) !=0:
                                self.Read_line.append(Read_Data)
                                print(Read_Data)
                            if len(self.Read_line) > 10 :
                                self.Read_line = []
                                self.ser.flushInput()

                            if  len(self.Read_line) > 2 and self.Read_line[0] == DISPLAY_ADD and self.Read_line[1] == CURRENT_STATUS:
                                self.Read_line = []
                                self.ser.flushInput()
                                print("data garbage")
                            if len(self.Read_line) == 3 and (self.Read_line[0] == DISPLAY_ADD)and(self.Read_line[1] == FTCH_MRE)and(self.Read_line[len(self.Read_line)-1] == EOD):
                            # if val.find(DISPLAY_ADD) != -1 and val.find(EOD) != -1 and val.find(FTCH_MRE) != -1:
                                DataFlg=1
                                Sentdata+=SendDatalenth
                                # PickValue= CurrentPick*100 / TotalPick
                                # print(str(round(Sentdata*100 / Datalenth)))
                                self.copyBar.set(str(round(Sentdata*100 / Datalenth)))
                                self.copy_text.set(str(round(Sentdata*100 / Datalenth))+"%")
                                self.Read_line = []
                                self.ser.flushInput()
                                print("send next data")
                                break
                            elif len(self.Read_line) == 3 and (self.Read_line[0] == DISPLAY_ADD)and(self.Read_line[1] == ERR_CPY)and(self.Read_line[len(self.Read_line)-1] == EOD):
                            # elif val.find(DISPLAY_ADD) != -1 and val.find(EOD) != -1 and val.find(ERR_CPY) != -1:
                                DataFlg=1
                                self.Read_line = []
                                self.ser.flushInput()
                                print("data repeat")
                                break

                            elif len(self.Read_line) == 3 and (self.Read_line[0] == DISPLAY_ADD)and(self.Read_line[1] == CLS_FLE)and(self.Read_line[len(self.Read_line)-1] == EOD):
                            # elif val.find(DISPLAY_ADD) != -1 and val.find(EOD) != -1 and val.find(CLS_FLE) != -1:
                                DataFlg=0
                                Sentdata+=SendDatalenth
                                self.copyBar.set(str(round(Sentdata*100 / Datalenth)))
                                self.copy_text.set(str(round(Sentdata*100 / Datalenth))+"%")
                                self.Read_line = []
                                self.ser.flushInput()

                                CopyTimestop=perf_counter()
                                Total_time=str(round(CopyTimestart-CopyTimestop))
                                Total_time=Total_time[1:]

                                if Total_time=='':
                                    Total_time = '1'

                                self.Msgstring='File copied copytime '+str(Total_time)+' sec'
                                print("file copied")
                                break

                            elif len(self.Read_line)== 4 and self.Read_line[0] == DISPLAY_ADD and self.Read_line[len(self.Read_line)-1] == EOD and self.Read_line[1] == ERR:
                                self.sendbmptimer.cancel()

                                if self.Read_line[2] == CARD_NOT_DETECT:
                                    self.Msgstring='CARD NOT DETECT'
                                if self.Read_line[2] ==CARD_INIT_FAIL:
                                    self.Msgstring='CARD INITIALIZE FAIL'
                                if self.Read_line[2] ==FAT32_NOT_FOUND :
                                    self.Msgstring='FAT32 NOT FOUND'
                                if self.Read_line[2] == ERROR_IN_CLUSTER :
                                    self.Msgstring='ERROR IN CLUSTER'
                                if self.Read_line[2] == DSGN_NOT_FOUND :
                                    self.Msgstring='DESIGN NOT FOUND'
                                if self.Read_line[2] == DSGN_INVALID :
                                    self.Msgstring='DESIGN INVALID'
                                self.Read_line = []
                                self.ser.flushInput()
                    if DataFlg == 0 and Sentdata < Datalenth :
                        print("Communication error")
                        self.sendbmptimer.cancel()
                        self.Msgstring='Communication error'
                        break
                    elif DataFlg == 0 :
                        DataFlg=0
                        break
            #Hide loader once files are copied
            self.is_animate = False
            self.call_loader('',True)
            self.sendbmptimer.cancel()

            self.messagebox('Warning',self.Msgstring)


    # View selected file
    def view_file(self, tab):
        #reset variables
        self.rotate_left = 0
        self.rotate_right = 0

        #check how many files selected
        if len(self.FileChked) == 0:
            self.messagebox('Warning','Please select checkbox to view image.')
        elif len(self.FileChked) == 1:
            if tab == 'usb':
                self.view_img_path = os.path.join(self.FileChked[0][1],self.FileChked[0][0])
                print(self.view_img_path)
                if os.path.isdir(self.view_img_path):
                    self.messagebox('Warning','Please select only bmp image to view.')
                    return

            elif tab == 'files':
                self.view_img_path = os.path.join(self.files_dir,self.FileChked[0])

            self.viewFrame.grid(row=0,column=0, sticky='news')

            #Frame for file view
            self.viewCanvasActionFrame = Canvas(self.viewFrame, width=self.winWidth,height=50,background="#FFFFFF",bd=0,highlightthickness = 0)
            self.viewCanvasActionFrame.grid(row=0,column=0, sticky='news')


            if tab == 'files':
                #Rotate Left Button
                rleftBtn = Label(self.viewCanvasActionFrame,
                        background="#FFFFFF",
                        image=self.rleft_icon)
                rleftBtn.image = self.rleft_icon
                rleftBtn.place(x=350,y=10)
                rleftBtn.bind('<Button>', lambda e, process='rotate left': self.image_process(process))

                #Flip top Bottom
                ftbBtn = Label(self.viewCanvasActionFrame,
                        background="#FFFFFF",
                        image=self.ftopbottom_icon)
                ftbBtn.image = self.ftopbottom_icon
                ftbBtn.place(x=400,y=10)
                ftbBtn.bind('<Button>', lambda e, process='flip top bottom': self.image_process(process))

            #Increase Button
            self.zoominBtn = Label(self.viewCanvasActionFrame,
                    background="#FFFFFF",
                    image=self.zoomin_icon)
            self.zoominBtn.image = self.zoomin_icon
            self.zoominBtn.place(x=450,y=10)
            self.zoominBtn.bind('<Button>', lambda e, process='zoom in':self.image_process(process))

            #Decrease Button
            self.zoomoutBtn = Label(self.viewCanvasActionFrame,
                    background="#FFFFFF",
                    image=self.zoomout_icon)
            self.zoomoutBtn.image = self.zoomout_icon
            self.zoomoutBtn.place(x=500,y=10)
            self.zoomoutBtn.bind('<Button>', lambda e, process='zoom out':self.image_process(process))

            if tab == 'files':
                #Flip top Bottom
                flrBtn = Label(self.viewCanvasActionFrame,
                        background="#FFFFFF",
                        image=self.fleftright_icon)
                flrBtn.image = self.fleftright_icon
                flrBtn.place(x=550,y=10)
                ftbBtn.bind('<Button>', lambda e, process='flip left right': self.image_process(process))

                #Rotate Left Button
                rrightBtn = Label(self.viewCanvasActionFrame,
                        background="#FFFFFF",
                        image=self.rright_icon)
                rrightBtn.image = self.rright_icon
                rrightBtn.place(x=600,y=10)
                rrightBtn.bind('<Button>', lambda e, process='rotate right': self.image_process(process))

                #Save image changes
                self.saveBtn = Label(self.viewCanvasActionFrame,
                        background="#FFFFFF",
                        state=DISABLED,
                        image=self.save_icon)
                self.saveBtn.image = self.save_icon
                self.saveBtn.place(x=930,y=10)
                self.saveBtn.bind('<Button>', lambda e, process='save': self.image_process(process))


            #Close window
            closeBtn = Label(self.viewCanvasActionFrame,
                    background="#FFFFFF",
                    image=self.close_icon)
            closeBtn.image = self.close_icon
            closeBtn.place(x=980,y=10)
            closeBtn.bind('<Button>', lambda e: self.close_dialog())

            #check file's mode is bitmap or not
            chkImg = Image.open(self.view_img_path)

            if chkImg.mode != '1':
                #if not bitmap then convert it
                # chkImg = chkImg.convert('1')
                # thresh = 200
                # fn = lambda x : 255 if x > thresh else 0

                # chkImg = chkImg.convert('L').point(fn,mode='1')
                print("convert image")
                # chkImg = chkImg.convert(mode='1',palette=Image.ADAPTIVE,colors=1)

                #Save to same location to access further
                # chkImg.save(self.view_img_path)

            #Make one copy for original to perform process on it
            self.oriImg = Image.open(self.view_img_path)
            #Make other variale to view after process in cnavas
            # self.oriViewImg = Image.open(self.view_img_path)
            self.oriImg.save(self.view_png_img)
            self.oriViewImg = Image.open(self.view_png_img)

            # Add scrollbar to view image in one frame
            self.viewCanvasFrame = Frame(self.viewFrame, width=self.winWidth-40,height=self.winHeight-70)
            self.viewCanvasFrame.grid(row=1,column=0,sticky='news',padx=(0,20),pady=(0,30))

            #Create canvas
            self.viewCanvasFrameC = Canvas(self.viewCanvasFrame, width=self.winWidth-55,height=self.winHeight-105, background="#FFFFFF")
            self.viewCanvasFrameC.grid(row=0,column=0, sticky='news')

            #Create Vertical scroll
            self.viewCanvasFrameVSB =  Scrollbar(self.viewCanvasFrame, orient='vertical',command=self.viewCanvasFrameC.yview,style='Vertical.TScrollbar')
            self.viewCanvasFrameVSB.grid(row=0,column=1, sticky='ns')

            #Create horizontal scroll
            self.viewCanvasFrameHSB =  Scrollbar(self.viewCanvasFrame, orient='horizontal',command=self.viewCanvasFrameC.xview,style='Horizontal.TScrollbar')
            self.viewCanvasFrameHSB.grid(row=1,column=0, sticky='ew')

            #Set scroll with canvas
            self.viewCanvasFrameC.configure(yscrollcommand=self.viewCanvasFrameVSB.set)
            self.viewCanvasFrameC.configure(xscrollcommand=self.viewCanvasFrameHSB.set)

            #Init images
            self.scale= 1.0
            self.bitimg = None
            self.bitimg_id = None

            self.viewCanvasFrameInn = Frame(self.viewCanvasFrame)
            self.viewwin = self.viewCanvasFrameC.create_window((0,0), window=self.viewCanvasFrameInn, anchor='nw')

            #Draw image in canvas
            self.redraw_canvas_img()
        else:
            self.messagebox('Warning','Please select only one checkbox to view image.')

    #image process
    #Rotate left, Rotate right, Flip top bottom, Flip left right, Zoomin, Zoom out,save changes
    def image_process(self, action):
        if action == 'rotate left':
            #Enable save button
            self.saveBtn.config(state=NORMAL)

            self.rotate_left += 1
            if self.rotate_left == 1:
                self.oriViewImg = self.oriImg.rotate(90,PIL.Image.NEAREST,expand=1)
                self.rotate_state = 90
            elif self.rotate_left == 2:
                self.oriViewImg = self.oriImg.rotate(180,PIL.Image.NEAREST,expand=1)
                self.rotate_state = 180
            elif self.rotate_left == 3:
                self.oriViewImg = self.oriImg.rotate(270,PIL.Image.NEAREST,expand=1)
                self.rotate_state = 270
            elif self.rotate_left == 4:
                self.oriViewImg = self.oriImg.rotate(360,PIL.Image.NEAREST,expand=1)
                self.rotate_state = 360
                self.rotate_left = 0

        elif action == 'rotate right':
            #Enable save button
            self.saveBtn.config(state=NORMAL)

            self.rotate_right += 1
            if self.rotate_right == 1:
                self.oriViewImg = self.oriImg.rotate(-90,PIL.Image.NEAREST,expand=1)
                self.rotate_state = -90
            elif self.rotate_right == 2:
                self.oriViewImg = self.oriImg.rotate(-180,PIL.Image.NEAREST,expand=1)
                self.rotate_state = -180
            elif self.rotate_right == 3:
                self.oriViewImg = self.oriImg.rotate(-270,PIL.Image.NEAREST,expand=1)
                self.rotate_state = -270
            elif self.rotate_right == 4:
                self.oriViewImg = self.oriImg.rotate(-360,PIL.Image.NEAREST,expand=1)
                self.rotate_state = -360
                self.rotate_right = 0

        elif action == 'flip left right':
            #Enable save button
            self.saveBtn.config(state=NORMAL)

            self.oriViewImg = self.oriImg.transpose(Image.FLIP_LEFT_RIGHT)
            self.flip_state = 'left-right'

        elif action == 'flip top bottom':
            #Enable save button
            self.saveBtn.config(state=NORMAL)

            self.oriViewImg = self.oriImg.transpose(Image.FLIP_TOP_BOTTOM)
            self.flip_state = 'top-bottom'

        elif action == 'zoom in':
            #Increase by 1.2
            self.scale *= 1.2

            #Get size of image
            iw, ih = self.oriViewImg.size
            #if scaled image width grator than 1050
            #then reduce scale by 1.2 and diable zoomin button
            if iw * self.scale > 1050 :
                self.scale = self.scale / 1.2
                self.zoominBtn.config(state=DISABLED)
            else:
                #if zoomout button disable then enable it
                if self.zoomoutBtn.cget('state') == 'disabled':
                    self.zoomoutBtn.config(state=NORMAL)

        elif action == 'zoom out':
            #Decrease by 1.2
            self.scale = self.scale / 1.2

            #Get size of image
            iw, ih = self.oriViewImg.size
            #if scaled image width less than 30
            #then increase scale by 1.2 and diable zoomout button
            if iw * self.scale < 30 :
                self.scale *= 1.2
                self.zoomoutBtn.config(state=DISABLED)
            else:
                #if zoomin button disable then enable it
                if self.zoominBtn.cget('state') == 'disabled':
                    self.zoominBtn.config(state=NORMAL)

        elif action == 'save':
            if self.saveBtn.cget('state') != 'disabled':
                self.saveBtn.config(state=DISABLED)
                tempImg = None

                if self.rotate_state != 0:
                    tempImg = self.oriImg.rotate(self.rotate_state,PIL.Image.NEAREST,expand=1)
                    tempImg.save(self.view_img_path)
                    tempImg = None
                    self.rotate_state = 0

                if self.flip_state == 'top-bottom':
                    tempImg = self.oriImg.transpose(Image.FLIP_TOP_BOTTOM)
                    tempImg.save(self.view_img_path)
                    tempImg = None
                    self.flip_state = ''
                elif self.flip_state == 'left-right':
                    tempImg = self.oriImg.transpose(Image.FLIP_LEFT_RIGHT)
                    tempImg.save(self.view_img_path)
                    tempImg = None
                    self.flip_state = ''

        #Call Draw image function
        self.redraw_canvas_img()

    #Draw Images
    def redraw_canvas_img(self):
        if self.bitimg_id:
            self.bitimg_id.destroy()

        #Get size or process image
        iw, ih = self.oriViewImg.size
        if iw > 1000 and self.scale == 1.0: self.scale = 0.4
        #Update size with modify scale
        size = int(iw * self.scale), int(ih * self.scale)

        #Get bitmapimage
        # self.bitimg = ImageTk.BitmapImage(self.oriViewImg.resize(size))
        self.oriViewImg.resize(size).save(self.view_png_img)
        self.bitimg = PhotoImage(file=self.view_png_img)

        self.bitimg_id = Label(self.viewCanvasFrameInn, image=self.bitimg, background='#FFF')
        self.bitimg_id.image = self.bitimg
        self.bitimg_id.grid(row=0,column=0)

        self.viewCanvasFrameInn.update_idletasks()

        bbox = self.viewCanvasFrameC.bbox('all')
        self.viewCanvasFrameC.config(scrollregion=bbox)

    #Close view image popup
    def close_dialog(self):
        self.remove_sample_png()
        self.viewFrame.grid_forget()

    #Delete multiple files
    def delete_file(self):
        if len(self.FileChked) > 0:
            self.ask_messagebox('Are you sure you want to\nDelete file(s)?','Delete')
            # conMsg = messagebox.askquestion('Delete Files', 'Are you sure you want to\nDelete file(s)?')
            # if conMsg == 'yes':
            #     #Delete all files
            #     for f in range(len(self.FileChked)):
            #         fpath = os.path.join(self.files_dir,self.FileChked[f])
            #         if os.path.exists(fpath):
            #             os.remove(fpath)

            #     self.clear_files('files',True)

    #Click single checkbox to get design details
    #index = get checkbox index
    #fname = clicked checkbox file name
    #checked = True or False
    #r = row, c = column, tab = tab name
    def chk_single_file(self, index, fname,checked, r, c, tab):
        print(fname)
        #last checkbox status checked or unchecked
        oldlbl = {}
        #new checkbox status checked or unchecked
        newlbl = {}
        if checked:
            oldlbl = self.FileUnChkLblAll[index]
            newlbl = self.FileChkLblAll[index]
            #Store checked checkbox file name
            self.FileChked.append(fname)
        else:
            newlbl = self.FileUnChkLblAll[index]
            oldlbl = self.FileChkLblAll[index]
            #remove uncheck checkbox file name
            self.FileChked.remove(fname)


        if len(self.FileChked) == 1:
            #if only one file checked then display file details
            if tab == 'files':
                self.FileFrameDesign.grid(row=0,column=1, sticky='ne')
                self.mEntryFile.focus()
                self.pick.set('')
                self.designName.config(text=self.FileChked[0])
                #Enable button for view
        else:
            #if multiple file selected then do not show design section
            if tab=='files':
                self.FileFrameDesign.grid_forget()
                self.designName.config(text='')

        #Hide old checkbox
        oldlbl.grid_forget()
        #View new checkbox
        newlbl.grid(row=r,column=c, sticky="nsew")

    #Check all file or uncheck all
    #oldlbl = last checkbox status
    #newlbl = current checkbox status
    # checked = True or False
    #r = row, c = column, tab = tab name
    def chk_all_file(self, oldlbl, newlbl,checked, r, c, tab):
        if checked:
            #Display all checkd checkbox and saved in array with all checked value
            if len(self.FileChkLblAll) > 0:
                for f in range(len(self.FileChkLblAll)):
                    if tab == 'files':
                        self.FileChked.append(self.fileRows[f][0])
                        self.FileUnChkLblAll[f].grid_forget()
                        self.FileChkLblAll[f].grid(row=f+1,column=c, sticky="nsew")
                    elif tab == 'usb':
                        if os.path.isfile(os.path.join(self.usb_files[f][1],self.usb_files[f][0])):
                            self.FileChked.append(self.usb_files[f])
                            self.FileUnChkLblAll[f].grid_forget()
                            self.FileChkLblAll[f].grid(row=f+1,column=c, sticky="nsew")
        else:
            #Display all unchecked checkbox and empty array of file
            self.FileChked = []
            if len(self.FileUnChkLblAll) > 0:
                for f in range(len(self.FileUnChkLblAll)):
                    self.FileChkLblAll[f].grid_forget()
                    self.FileUnChkLblAll[f].grid(row=f+1,column=c, sticky="nsew")

        #Hide old checkbox
        oldlbl.grid_forget()
        #View new checkbox
        newlbl.grid(row=r,column=c, sticky="nsew")

    #fnd total number of mathced file to show that folder
    def match_files_count(self,dir,match):
        total = 0
        for r, dirs, fnames in os.walk(dir):
            files = fnmatch.filter(fnames, '*.bmp')
            if match != '':
                files = fnmatch.filter(files, '*'+match+'*')

            total = len(files)
        return total

    #Display folder and files both on screen based on define directory
    def dis_subdir(self,dir,match='',onlyfiles=False):
        rows = []
        # print("sub directory")
        for root in os.listdir(dir):
            root_path = os.path.join(dir,root)

            #  and self.match_files_count(root_path,match) > 0
            if os.path.isdir(root_path) and not onlyfiles:
                # print("get dir")
                rows.append((root,
                                dir,
                                time.ctime(os.path.getmtime(os.path.join(dir, root)))))
            elif os.path.isfile(root_path) and root_path.lower().endswith('.bmp') :
                # print("usb=",self.usb_last_final_dir)
                if self.usb_last_final_dir != '' and self.usb_last_final_dir.find(dir) is not -1 and self.usb_last_final_dir != dir:
                    continue

                # print("root_path=",root_path)
                # print("match=",match)
                if match != '':
                    if root.find(match) is not -1:
                        rows.append((root,
                                        dir,
                                        time.ctime(os.path.getmtime(os.path.join(dir, root)))))
                else:
                    rows.append((root,
                                dir,
                                time.ctime(os.path.getmtime(os.path.join(dir, root)))))

        return rows

    # USB section
    # Fetch all files from all attach pendrive and display in table
    # Copy all files to internal memory
    # View single file in popup
    def usb_section(self,is_base=False):
        #If pendrive attach then do everything
        print("usb start")
        if len(os.listdir(self.pendrive_dir)) > 0:
            self.reset_frame(self.USBFrame)
            #Hide thread
            if self.usbThreadId:
                self.master.after_cancel(self.usbThreadId)

            if is_base:
                self.usb_last_final_dir = ''
                self.usb_last_dir = []
                self.search_file_str_usb.set('')
                #Fetch all files from pendrive for search utility
                self.usbRows = []
                self.usbRowsOri = []
                self.usb_files = []

                self.usbRowsOri = self.usbRows = self.files_feed(self.pendrive_dir,True)
                #Get root structure
                for root in os.listdir(self.pendrive_dir):
                    root_path = os.path.join(self.pendrive_dir,root)
                    if os.access(root_path,os.R_OK) and os.access(root_path,os.W_OK) and os.access(root_path,os.X_OK):
                        self.usb_files = self.usb_files + self.dis_subdir(root_path)
            #Action button Frame
            self.USBFrameAction = Frame(self.USBFrame, width=self.winWidth,height=self.menuHeight)
            self.USBFrameAction.grid(row=0,column=0, pady=(0,10), sticky='nw')
            #Search bar section
            self.searchEntry = Entry(self.USBFrameAction, textvariable=self.search_file_str, style='EntryStyle.TEntry',font="Verdana 15", width=24)
            self.searchEntry.grid(row=0,column=0, sticky="news")
            #Search button for search file
            self.searchBtn = Button(self.USBFrameAction,
                    text="Find",
                    image=self.search_icon,
                    compound=TOP,
                    style='file.TButton',
                    # padding=10,
                    state=DISABLED,
                    command= lambda :self.search_files('usb'))
            self.searchBtn.grid(row=0,column=1, sticky="news",padx=1)

            self.searchEntry.bind('<FocusIn>',lambda e:self.fin_searchbar('usb'))
            self.searchEntry.bind('<Button-1>',lambda e:self.fin_searchbar('usb'))
            self.searchEntry.bind('<KeyRelease>',lambda e:self.autosearch_files('usb'))

            #Close searchbar
            self.fcloseBtn = Label(self.USBFrameAction,
                    image=self.close_icon)
            self.fcloseBtn.image = self.close_icon
            self.fcloseBtn.grid_forget()
            self.fcloseBtn.bind('<Button>', lambda e: self.fout_searchbar('usb',True))
            #View button for view image
            self.fviewBtn = Button(self.USBFrameAction,
                    text='View',
                    image=self.view_icon,compound=TOP,
                    style='file.TButton',
                    command= lambda tab='usb': self.view_file(tab))
            self.fviewBtn.grid(row=0,column=2, padx=10)


            # Copy muliple files to store in internal memory
            self.fcopyBtn = Button(self.USBFrameAction,
                    text="Copy",
                    image=self.copy_icon,compound=TOP,
                    style='file.TButton',
                    command=lambda :self.copy_files())
            self.fcopyBtn.grid(row=0,column=3)

            # self.filesfound = Label(self.USBFrameAction,textvariable=self.DesignName, style='infoRect.TLabel',wraplength=400)
            # self.filesfound.grid(row=0,column=4)

            Label(self.USBFrameAction, textvariable=self.totalfilefound, style='file.TButton',font="Verdana 15").grid(row=0,column=4,padx=10, sticky="news")
            self.filesfound = Label(self.USBFrameAction, text='', style='lblBody.TLabel')

            self.back_usb_btn = Button(self.USBFrame,text='Back',command=lambda :self.jump_to_last_dir(), style='bgray.TButton')
            self.back_usb_btn.place(x=-100,y=-100)
            #Scrollbar section of Table
            self.USBFrameTable = Frame(self.USBFrame, width=self.winWidth-20,height=self.frameHeight - 100)
            self.USBFrameTable.grid(row=2,column=0, sticky='nw')

            #files collect
            tCols = ['Name','Folder','DateTime']

            #Parameter
            #1:Frame outer
            #2:rows

            #3:columns
            #4:Required checkbox
            self.gen_table(self.USBFrameTable,self.usb_files,tCols,'usb',True)
            #End Scrollbar section of Table
            #Active search section
            self.activeSearch = Frame(self.USBFrame, width=self.winWidth/2)
            self.activeSearch.grid_forget()

            lbl = Label(self.activeSearch,textvariable=self.active_search,style='fileRes.TLabel',font="Verdana 14 bold",wraplength=400)
            lbl.grid(row=0,column=0,sticky='nw')

            btn = Button(self.activeSearch,text='Clear',command=lambda :self.clear_files('usb',True), style='bgray.TButton')
            btn.grid(row=0,column=1,sticky='nw',padx=10,pady=(0,5))

            #Search area
            self.gen_search_area(self.USBFrame,'usb')

        else:
            # self.reset_frame(self.USBFrame)
            loaderLbl = Label(self.USBFrame,
                    text='Please attach PenDrive to get\nimages to copy in internal memory.',
                    style='fileRes.TLabel',
                    font='Verdana 25',
                    anchor="center")
            loaderLbl.place(x=200,y=150)
            # self.usbThreadId= self.master.after(1000, self.usb_section(True))


    #Copy multiple files
    def copy_files(self):
        self.copyfcnt = 0
        #Check if files array is not empty
        if len(self.FileChked) > 0:
            #Display loader while copy files
            self.is_animate = True
            self.call_loader('Copying files....',True)
            # print(self.FileChked)
            for f in range(len(self.FileChked)):
                #Full path of copying file
                fcname = os.path.join(self.FileChked[f][1],self.FileChked[f][0])
                files = []
                # print("fcname",fcname)
                if os.path.isdir(fcname):
                    # print("dir sec")
                    # files = self.files_feed(fcname,True,self.search_file_str_usb.get())
                    files = self.dis_subdir(fcname,self.search_file_str_usb.get(),True)
                    # print(files)
                else:
                    # files[0] = fcname
                    files.append(self.FileChked[f])
                if len(files) > 0:
                    for f in range(len(files)):
                        file = os.path.join(files[f][1],files[f][0])
                        # print("file=",file)
                        self.fcImg = Image.open(file)

                        #Check file is monochrome or not
                        is_mono = self.chk_monochrome(file)
                        #if not mnochrome file found then translate in monochrome
                        if is_mono != 1:
                  #1 Will be convert into monochrome file
                            print("convert img monochrom")
                            thresh = 200
                            fn = lambda x : 255 if x > thresh else 0
                            self.fcImg = self.fcImg.convert('L').point(fn,mode='1')

                            # self.fcImg = self.fcImg.convert('L')
                            # self.fcImg = self.fcImg.convert('1')
                            # self.fcImg = self.fcImg.convert(mode='P',colors=1)
                            # self.fcImg.save(file)
                            self.cpyimg= os.path.join(self.files_dir,files[f][0])
                            if path.exists(os.path.join(self.files_dir,files[f][0])):
                                # tkmsg =self.ask_messagebox('Are you sure, you want to replace '+ files[f][0] +' file?','Copy')
                                tkmsg = messagebox.askquestion('File with same name found', 'Are you sure, you want to replace '+ files[f][0] +' file?')
                                if tkmsg == 'yes':
                                    self.copyfcnt = self.copyfcnt + 1
                                    self.fcImg.save(self.cpyimg)
                            else:
                                self.copyfcnt = self.copyfcnt + 1
                                self.fcImg.save(self.cpyimg)
                        else:
                            #Check file is dulpcate or not
                            if path.exists(os.path.join(self.files_dir,files[f][0])):
                                # tkmsg =self.ask_messagebox('Are you sure, you want to replace '+ files[f][0] +' file?','Copy')
                                tkmsg = messagebox.askquestion('File with same name found', 'Are you sure, you want to replace '+ files[f][0] +' file?')
                                if tkmsg == 'yes':
                                    self.copyfcnt = self.copyfcnt + 1
                                    self.copy_single_file(file,self.files_dir)
                            else:
                                self.copyfcnt = self.copyfcnt + 1
                                self.copy_single_file(file,self.files_dir)

        #Hide loader once files are copied
        self.is_animate = False
        self.call_loader('',True)

        #Display message once all files are copied
        print("total file copied")
        if self.copyfcnt > 0:
            self.messagebox('Information','System has been copied '+ str(self.copyfcnt) +' files')

        #Display all unchecked checkbox once copied successfully
        self.FileChked = []
        if len(self.FileUnChkLblAll) > 0:
            for f in range(len(self.FileUnChkLblAll)):
                self.FileChkLblAll[f].grid_forget()
                self.FileUnChkLblAll[f].grid(row=f+1,column=0, sticky="nsew")

    #Check file is monochrome or not and send status
    def chk_monochrome(self,fullFile):
        #Read file and check 28th elelment which indicate monochrome status
        #if 1 then monochrome otherwise not
        f = open(fullFile,"rb")
        data = bytearray(f.read())
        return data[28]

    #Copy single file from source to destination
    def copy_single_file(self, source, destination):
            shutil.copy(source,destination)

    #Generate popup window
    def gen_loader(self):
        #Generate Popup canvas
        self.popupCanvas.grid_forget()

        #Load gif image
        self.gifImg = []
        img = os.path.join(self.images_dir,'loader.gif')
        #Generate sequence of loader to animate it
        for f in range(0,20):
            pic = PhotoImage(file=img, format="gif - {}".format(f))
            #Store all frame of gif in array
            self.gifImg.append(pic)

        #Create image in canvas with init frame and store in variable
        # self.loaderCImg = self.popupCanvas.create_image(500,200,image=self.gifImg[0])
        #By default false animate option
        self.is_animate = False

    #Call loader function to perform animate gif image
    #lbl = Text of label
    #is_lbl = if lable is print or not
    #counter = sequence of image
    def call_loader(self,lbl,is_lbl,tab=''):
        #Print label is true
        # print('c')
        if is_lbl:
            self.reset_frame(self.popupCanvas)
            loaderLbl = Label(self.popupCanvas,
                    text=lbl,
                    background="#FFFFFF",
                    style='fileRes.TLabel',
                    anchor='center',font='Verdana 20 bold',wraplength=400)
            if tab == 'files':
                loaderLbl.grid(row=0,column=0,padx=200,pady=(300,5))
                pro = Progressbar(self.popupCanvas, style='red.Horizontal.TProgressbar', orient = HORIZONTAL, length=824, mode='determinate',variable=self.copyBar)
                pro.grid(row=1,column=0,padx=100,pady=(0,200))
                Copylbl = Label(pro,textvariable=self.copy_text, font="Verdana 20", foreground="#FFFFFF", background="#12355B")
                Copylbl.place(x=350,y=10)
            else:
                loaderLbl.grid(row=0,column=0,padx=200,pady=(300,300))
                # Copylbl.grid(row=1,column=0,padx=300,pady=(0,150))
        #If user wants to stop animation of gif
        if not self.is_animate:
            self.popupCanvas.grid_forget()
        else:
            #Set image sequence frame based on counter
            # self.popupCanvas.itemconfig(self.loaderCImg,image=self.gifImg[counter])
            #Show popup
            self.popupCanvas.grid(row=0,column=0,sticky="news")
            #Recursively call loader function with updated counter
            # self.master.after(500, lambda: self.call_loader(lbl,False,(counter+1) % len(self.gifImg)))


    # Test section
    # Sample test file top select
    # Get Current pick from controller for selected file
    def test_section(self):
        ## Design frame to display testing image display section
        #row and column position of image
        ypos = 10
        xpos = 10
        #Counted width and height
        cw = 0
        ch = 0
        counter = 0
        #Get all testing images from test directory
        for r, dirs, fnames in os.walk(self.test_dir):
            #Sort testing image ascending order
            fnames.sort()
            for fname in fnames:
                testlbl = {}
                testimg = {}
                counter += 1
                #Get image size
                testimg = Image.open(os.path.join(r,fname))
                w, h = testimg.size
                #Set minimum of image width
                if w < 45:  w = 45

                #Display image
                timg = PhotoImage(file=os.path.join(r,fname))

                #Count new row
                if cw > 0:
                    #Every x position will be image width and 20 space
                    xpos += cw + 20
                    #if x position and current image width is greator than boundry width
                    #then reset x position and increase y position
                    if (xpos + w) > (self.winWidth - 45):
                        xpos = 10
                        ypos += ch + 50
                        #reset counted height if new row detected
                        ch = 0

                testlbl = Label(self.TestFrameImgCanvas, text=os.path.splitext(fname)[0], image=timg,compound=BOTTOM, borderwidth=2 ,relief=RAISED, padding=5)
                testlbl.image = timg
                testlbl.place(x=xpos,y=ypos)

                #Set current width to counted width
                cw = w
                #Check signal image size is differnet that's why
                #calculate width of next image x position
                if os.path.splitext(fname)[0] == 'CHECK SIGNAL': cw += 20
                #Get always highest height counted height
                if ch < h: ch = h

                #Bind image click event
                testlbl.bind("<Button-1>", lambda e, fname = os.path.splitext(fname)[0],val=counter, lbl=testlbl: self.run_test_img(fname,val,lbl))
                #Store all image lable in array to further process
                self.lblCol.append(testlbl)

        ## Output section
        #Output label
        Label(self.TestFrameOPCanvas, text='Output', style='red.TLabel').grid(row=0,column=0, sticky='news')

        #Get design from controller response
        Label(self.TestFrameOPCanvas, text='Design:', style='lblHead.TLabel').grid(row=1,column=0, sticky='news')
        self.TestDesign = Label(self.TestFrameOPCanvas, text='', style='lblBody.TLabel')
        self.TestDesign.grid(row=1,column=1, sticky='news')

        #Get pick value from controller response
        Label(self.TestFrameOPCanvas, text='Pick:', style='lblHead.TLabel').grid(row=1,column=2, sticky='news')
        self.TestPick = Label(self.TestFrameOPCanvas, text='', style='lblBody.TLabel')
        self.TestPick.grid(row=1,column=3, sticky='news')

        #Get Sensor Output from controller response
        Label(self.TestFrameOPCanvas, text='Sensor OP:', style='lblHead.TLabel').grid(row=1,column=4, sticky='news')
        self.TestLEDC = Canvas(self.TestFrameOPCanvas, width=300,height=50, background='#FFFFFF',bd=0,highlightthickness = 0)
        self.TestLEDC.grid(row=1,column=5, sticky='news')
        self.TestSensor1=self.create_circle(50,25,25,self.TestLEDC, 'gray')
        self.TestSensor2=self.create_circle(110,25,25,self.TestLEDC, 'gray')

        #Stop test pattern
        Button(self.TestFrameOPCanvas, text='STOP', style='test.TButton', command=self.stop_test_pattern).grid(row=1,column=6)
    def Check_test_responce(self):
        print("test ok")
        print(self.Test_flg)
        # self.Test_timer.cancel()
        if self.Test_flg == 0:
            self.Test_flg = 2
            print("communication eorortkrktg")
            print("communication error")
            # messagebox.showerror('Error',"communication error")
            # self.messagebox("Error","Communication error")

        # print("test ok")
    #Stop test pattern
    def stop_test_pattern(self):
        if self.test_start:
            self.ser.write(MAIN_ADD)
            self.ser.write(TEST_PTTRN_STP)
            self.ser.write(EOD)
            self.Test_flg = 0
            # Wait for 5 second
            Test_timer = threading.Timer(5.0, self.Check_test_responce)
            Test_timer.start()
            count = 0
            # while count < 100:      # wait for Mcu confirmation
            while True:
                val = self.ser.readline()
                count += 1
                print("read data=",val)
                # self.TestFrameOPCanvas.grid(row=1,column=0, pady=10, ipady=10, sticky='news')
                # Reset all test image selection view
                if len(self.lblCol) > 0:
                    for l in range(len(self.lblCol)):
                        self.lblCol[l].config(relief=RAISED)
                if val.find(DISPLAY_ADD) != -1 and val.find(TEST_PTTRN_STP) != -1 and val.find(EOD) != -1:
                    print("read data lenth=",len(val))
                    count=0
                    self.test_start = 0
                    self.Test_flg = 1
                    Test_timer.cancel()
                    self.TestFrameOPCanvas.grid_forget()
                    self.TestDesign.config(text='')
                    self.TestPick.config(text='')
                    self.TestLEDC.itemconfig(self.TestSensor1, fill='gray')
                    self.TestLEDC.itemconfig(self.TestSensor2, fill='gray')
                    break
                if  self.Test_flg == 2:
                    self.Test_flg = 0
                    print("communication error")
                    Test_timer.cancel()
                    self.messagebox("Error","Communication error")
                    break


    #Send test image to controller and get response from controller
    def run_test_img(self, fname,fval, lbl):

        self.Test_flg = 0
        print("send test bmp",fval)
        self.ser.write(MAIN_ADD)
        self.ser.write(TEST_PTRN)
        # self.ser.write(fname.encode('utf-8'))
        self.ser.write(bytes([fval]))
        self.ser.write(EOD)
        Test_timer = threading.Timer(2.0, self.Check_test_responce)
        Test_timer.start()
        # Display Output canvas
        count = 0
        # wait for Mcu confirmation
        while True:
            # count += 1
            val = self.ser.readline()
            # print("read data=",val)
            # print('self.Test_flg=',self.Test_flg,count)
            if val.find(DISPLAY_ADD) != -1 and val.find(TEST_PICK) != -1 and val.find(EOD) != -1:
                self.Test_flg = 1
                self.test_start = 1
                Test_timer.cancel()
                print("read data lenth=",len(val))
                count=0
                if len(val) >= 7:
                    self.TestFrameOPCanvas.grid(row=1,column=0, pady=10, ipady=10, sticky='news')
                    # Reset all test image selection view
                    if len(self.lblCol) > 0:
                        for l in range(len(self.lblCol)):
                            self.lblCol[l].config(relief=RAISED)

                    # Set selected test image name to output Design label
                    self.TestDesign.config(text=fname)
                    # Set selected option to click test image
                    lbl.config(relief=SUNKEN)

                    # Set pick value
                    self.Test_pick.set(val[3])
                    self.TestPick.config(text=val[3])

                    #set sensor op
                    # if int(hexlify(val[4]),16) == 0x01:
                    if val[4] == 0x01:
                        self.TestLEDC.itemconfig(self.TestSensor1, fill='green')
                    else :
                        self.TestLEDC.itemconfig(self.TestSensor1, fill='gray')

                    # if int(hexlify(val[5]),16) == 0x01:
                    if val[4] == 0x01:
                        self.TestLEDC.itemconfig(self.TestSensor2, fill='green')
                    else :
                        self.TestLEDC.itemconfig(self.TestSensor2, fill='gray')
                break
            if  self.Test_flg == 2:
                self.Test_flg =0
                self.test_start = 0
                Test_timer.cancel()
                print("communication error,time over")
                self.messagebox("Error","Communication error")
                break

    # Setting section
    # Select machine design setting
    # Select harness
    # Select design type
    # Get diameter [You may change diameter by roll diameter button]
    # def setting_section(self):
    #     #Get all settings from controller
    #     # self.get_controller_setting(GET_SETTINGS)
    #     #Get all setting design from setting directory
    #     col = 0
    #     for r, dirs, fnames in os.walk(self.setting_dir):
    #         #sort setting image ascending order
    #         fnames.sort()
    #         for fname in fnames:
    #             settinglbl = {}
    #             settingimg = {}
    #             #Get setting image
    #             settingimg = PhotoImage(file=os.path.join(r,fname))

    #             #Set image in label
    #             settinglbl = Label(self.SettingFrameT, image=settingimg,borderwidth=1, padding=5)
    #             settinglbl.image = settingimg
    #             settinglbl.grid(row=0,column=col,sticky='news',pady=10,padx=10)

    #             #Bind click event of image
    #             settinglbl.bind("<Button-1>", lambda e, fname = col, lbl=settinglbl: self.setting_img_up(fname,lbl))
    #             #Store setting label in array
    #             self.lblCol.append(settinglbl)
    #             print("self.lblCol",self.lblCol)
    #             #Set default setting image selected
    #             # if col == self.settingDesign:
    #             #     settinglbl.config(relief=SUNKEN)
    #             #     settinglbl.config(background='#12355B')
    #             # else:
    #             settinglbl.config(relief=RAISED)
    #             settinglbl.config(background='#ffffff')

    #             col += 1

    #     # Harness settings
    #     hr = 0
    #     for h in range(len(self.harnessArr)):

    #         radiooff = {}
    #         radiooff = Label(self.SettingFrameBL, text=self.harnessArr[h], image=self.roff_icon,style='plain.TLabel',compound=LEFT)
    #         radiooff.image = self.roff_icon
    #         radiooff.bind("<Button>", lambda e, chked = True, row = h, col = 0, fname=hr, index=h: self.get_harness(index,fname,chked,row,col))
    #         self.lblROffCol.append(radiooff)

    #         radioon = {}
    #         radioon = Label(self.SettingFrameBL, text=self.harnessArr[h], image=self.ron_icon,style='plain.TLabel',compound=LEFT)
    #         radioon.image = self.ron_icon
    #         radioon.bind("<Button-1>", lambda e, chked = False, row = h, col = 0, fname=hr, index=h: self.get_harness(index,fname,chked,row,col))
    #         self.lblROnCol.append(radioon)

    #         #set Default value

    #         radiooff.grid(row=h,column=0, sticky="EW",pady=5)
    #         radioon.grid_forget()
    #         hr += 1

    #     # Design settings
    #     for h in range(len(self.selectDesignArr)):
    #         unchk = {}
    #         unchk = Label(self.SettingFrameBL, text=self.selectDesignArr[h], image=self.unchk_icon,style='plain.TLabel',compound=LEFT)
    #         unchk.image = self.unchk_icon
    #         unchk.bind("<Button>", lambda e, chked = True, row = 3, col = h, fname=1, index=h: self.get_select_design(index,fname,chked,row,col))
    #         self.lblUnChkCol.append(unchk)

    #         chk = {}
    #         chk = Label(self.SettingFrameBL, text=self.selectDesignArr[h], image=self.chk_icon,style='plain.TLabel',compound=LEFT)
    #         chk.image = self.chk_icon
    #         chk.bind("<Button-1>", lambda e, chked = False, row = 3, col = h, fname=0, index=h: self.get_select_design(index,fname,chked,row,col))
    #         self.lblChkCol.append(chk)

    #         #set Default value
    #         # if self.selectDesign[h] == 1:
    #         #     chk.grid(row=1,column=h, sticky="EW",pady=20)
    #         #     unchk.grid_forget()
    #         # else:
    #         unchk.grid(row=3,column=h, sticky="EW",pady=20)
    #         chk.grid_forget()
    #     version_widget =  Label(self.SettingFrameBL,text="Version 1.2",borderwidth=1, padding=5)
    #     version_widget.grid(row=4,column=0,sticky='news',pady=10,padx=10)
    #     #diameter settings
    #     self.diameter_widget = Entry(self.SettingFrameBRT, text=self.diameter, state='disabled', width=5,style='EntryStyle.TEntry',font='Verdana 15 bold')
    #     self.diameter_widget.grid(row=0,column=0, sticky="ew", padx=3, pady=5)

    #     btn = Button(self.SettingFrameBRT, text='Roll Diameter', style='setting.TButton', command=self.change_diameter)
    #     btn.grid(row=0, column=1,sticky='EW', pady=5, padx=10)

    #     #Generate keypad canvas
    #     self.gen_keypad(self.SettingFrameBRB,'setting')
    #     #End Meter keypad

    def wifi_section(self):
        #Heading of wifi
        lblwifi = Label(self.WifiFrame, text='Network setting', style='head.TLabel',width=82)
        lblwifi.grid(row=0,column=0,columnspan=4,sticky='nw',pady=(0,20))

        btn = Button(self.WifiFrame,text='Refresh',command=lambda :self.get_wifi_list(True), style='bgray.TButton')
        btn.place(x=610,y=1)

        self.design_wifi_section()
        return

    # Geenral setting section
    # Wifi connection
    # SHIFT selection
    def general_setting_section(self):
        # SHIFT settings
        self.shiftSettingFrame = Frame(self.SettingFrameRight)
        self.shiftSettingFrame.grid(row=0,column=0,sticky='news',pady=(20,0))

        #Heading of design
        lbl = Label(self.shiftSettingFrame, text='Select SHIFT', style='head.TLabel')
        lbl.grid(row=0,column=0,columnspan=4,sticky='nw')

        # shiftArr = self.db_section('shift')
        # for h in range(len(shiftArr)):
        #     btn = {}
        #     btn = Button(self.shiftSettingFrame,text=shiftArr[h],style='transparent.TButton')
        #     # ,command=lambda data=self.hooksArr[h]:self.getHook(data)
        #     btn.grid(row=1,column=h,sticky='nw',padx=5,pady=5)
        #     self.shiftSetting.append(btn)
        return

    #Get all wifi list
    def get_wifi_list(self,is_reset=False):
        if is_reset:
            if len(self.wifi_list)>0: 
                self.reset_frame(self.wifiFrameList)

        wifilist = []
        # print(os.popen('sudo iw dev wlan0 scan | grep SSID').read())
        cells= list(Cell.all('wlan0'))
        stopwords=["Cell(ssid=",")"]
        self.wifi_list=[]
        Connected_id=os.popen('iwgetid').read()
        strlen=len(Connected_id)-2
        Connected_id = Connected_id[17:strlen]
        print("Connected=",Connected_id )
        if Connected_id == '':
            self.tabControls.add(self.wifi_tab, text=self.topMenu[6],image=self.wifi_off_icon, compound=LEFT) 
        i=0
        for item in list(cells):
            str1=str(cells[i])
            strlen=len(str1)-1
            self.wifi_list.append((str1[10:strlen],0))
            if str(self.wifi_list[i][0]) == Connected_id:
                self.wifi_list[i]=list(self.wifi_list[i])
                self.wifi_list[i][1]=1
                self.wifi_list[i]=tuple(self.wifi_list[i])
                self.tabControls.add(self.wifi_tab, text=self.topMenu[6],image=self.wifi_icon, compound=LEFT)
            i=i+1

        print(self.wifi_list)
        if is_reset:
            self.design_wifi_section()
        return

    # Design wifi section
    def design_wifi_section(self):
        #Wifi section
        if len(self.wifi_list) > 0:
            self.wifiFrameList = Frame(self.WifiFrame)
            self.wifiFrameList.grid(row=1,column=0, sticky='news')

            r = 0
            for w in range(len(self.wifi_list)):
                lblname = Label(self.wifiFrameList,text=self.wifi_list[w][0],width=15,font="Verdana 13 bold")
                lblname.grid(row=r,column=0,sticky='news',ipadx=2,pady=5)

                txt_con = ''
                if self.wifi_list[w][1] == 1:
                    txt_con = 'connected'

                lblst = Label(self.wifiFrameList,text=txt_con,width=10,font="Verdana 13")
                lblst.grid(row=r,column=1,sticky='news',ipadx=2,pady=5)

                if self.wifi_list[w][1] == 1:
                    btn = Button(self.wifiFrameList,text='Disconnect',width=10, style='bgray.TButton',command=lambda net=self.wifi_list[w][0]:self.connect_network(net))
                    btn.grid(row=r,column=2,sticky='news',ipadx=2,pady=5,padx=(0,10))
                else:
                    btn = Button(self.wifiFrameList,text='Connect',width=10, style='bgray.TButton',command=lambda net=self.wifi_list[w][0]:self.connect_network(net,True))
                    btn.grid(row=r,column=2,sticky='news',ipadx=2,pady=5,padx=(0,10))
                r += 1
                #Separator
                sep = Separator(self.wifiFrameList, orient=HORIZONTAL)
                sep.grid(row=r,column=0,columnspan=4,sticky='news')

                r += 1
        return

    #Connect to network

    def connect_network(self,net_name,go_connect=False):
        self.network_name.set(net_name)
        if go_connect:
            self.letter_up = False
            self.WifiFrame.grid_forget()
            self.password_section('wifi')
        else:
            # print("disconnect")
            self.Disconnect_network()
        return

    def Disconnect_network(self): 
        print("disconnect")
        with open('/etc/wpa_supplicant/wpa_supplicant.conf','r') as f:
            message = f.readlines()
            index=0
            for item in message:
                print(item)
                if item == "network={\n":                 
                    print ("index=",index)
                    if message[index+4] != "\tdisabled=1\n" :
                        message.insert(index+4,"\tdisabled=1\n")
                        print("Remove disabled")
                index=index+1

            # if Saved_ssid==0:
            #     message.extend(wifiname)

            print(message) 
            print("write")
            os.system("sudo chmod 777 /etc/wpa_supplicant/wpa_supplicant.conf")
            with open('/etc/wpa_supplicant/wpa_supplicant.conf','w') as new_f:
                for item in message:
                    print(item)
                    new_f.write("%s"%item)
            f.close()

            # os.system("sudo wpa_cli -i wlan0 reconfigure")
            responce = os.popen('sudo wpa_cli -i wlan0 reconfigure').read()
            if (responce.find('OK') != -1):
                print("disconnected")  
                self.tabControls.add(self.wifi_tab, text=self.topMenu[6],image=self.wifi_off_icon, compound=LEFT)   
                i=0
                for item in self.wifi_list:
                    self.wifi_list[i]=list(self.wifi_list[i])
                    self.wifi_list[i][1]=0
                    self.wifi_list[i]=tuple(self.wifi_list[i])
                    i=i+1
                self.reset_frame(self.wifiFrameList)
                self.design_wifi_section()    

            print(responce)
            time.sleep(2)

    #Common message section
    def message_section(self,msg):
        self.msgFrame.grid(row=1, sticky='nsew',padx=20,pady=20)
        self.msgLbl = Label(self.msgFrame,
                text=msg,
                style='fileRes.TLabel',
                font='Verdana 25',
                anchor="center", width=40)
        self.msgLbl.grid(row=0,column=0,padx=(30,0),pady=(200,0),sticky='news')
        return

    # Common Password section
    def password_section(self,tab):
        self.passwordFrame.grid(row=1, sticky='nsew',padx=20,pady=20)

        lbl = Label(self.passwordFrame, text='Please enter password', style='head.TLabel')
        lbl.grid(row=0,column=0,columnspan=2,sticky='nw',pady=(0,10))

        self.passEntry = Entry(self.passwordFrame,show='*' , textvariable=self.password_str, style='EntryStyle.TEntry',font="Verdana 15", width=50)
        self.passEntry.grid(row=1,column=0, sticky="news")

        #show password button
        self.showPass = Button(self.passwordFrame,
                image=self.view_icon,
                style='file.TButton',
                padding=10,
                command= lambda :self.pass_format(False))
        self.showPass.image = self.view_icon
        self.showPass.grid_forget()

        #hide password button
        self.hidePass = Button(self.passwordFrame,
                image=self.hide_icon,
                style='file.TButton',
                padding=10,
                command= lambda :self.pass_format(True))
        self.hidePass.image = self.hide_icon
        self.hidePass.grid(row=1,column=1, sticky="news",padx=5)

        #Ok button like enter
        okBtn = Button(self.passwordFrame,
                image=self.tick_icon,
                style='file.TButton',
                padding=10,
                command= lambda :self.check_password(tab))
        okBtn.image = self.tick_icon
        okBtn.grid(row=1,column=2, sticky="news",padx=1)

        #Close searchbar
        fcloseBtn = Label(self.passwordFrame,
                image=self.close_icon)
        fcloseBtn.image = self.close_icon
        fcloseBtn.grid(row=1,column=3, sticky="news",padx=(40,20))
        fcloseBtn.bind('<Button>', lambda e: self.close_pass_sec(tab))

        #capslock status
        self.capsLbl = Label(self.passwordFrame,
                text='Capslock: OFF',
                style='fileRes.TLabel',
                font='Verdana 13 bold',
                anchor="ne")
        self.capsLbl.grid(row=2,column=0,columnspan=4,padx=20,pady=10,sticky='news')

        self.passwordKeyFrame = Frame(self.passwordFrame)
        self.passwordKeyFrame.grid(row=3,column=0,columnspan=5,sticky='news')
        self.gen_full_keypad(self.passwordKeyFrame,tab,'full')
        # self.gen_full_keypad(self.passwordKeyFrame,tab)
        return

    # set password format
    def pass_format(self,is_show=False):
        if is_show:
            self.passEntry.config(show='')
            self.hidePass.grid_forget()
            self.showPass.grid(row=1,column=1, sticky="news",padx=5)
        else:
            self.passEntry.config(show='*')
            self.showPass.grid_forget()
            self.hidePass.grid(row=1,column=1, sticky="news",padx=5)
        return

    # Close password section
    def close_pass_sec(self,tab):
        if tab == 'wifi':
            self.WifiFrame.grid(row=1, sticky='nsew', padx=20, pady=20)
            self.passwordFrame.grid_forget()
            self.msgFrame.grid_forget()
            self.password_str.set('')
            self.network_name.set('')
            # self.get_wifi_list(True)
        return

    #Set password to network
    def check_password(self,tab):
        if self.password_str.get() == '':
            messagebox.showerror('Error',"No Password has been entered.")
        else:
            # self.passwordFrame.grid_forget()
            self.password_str.get()
            if tab == 'wifi':
                # self.messagebox('warnnng','Please do not change the tab and wait \nwhile we are connecting...')

                # print("setup password",self.password_str.get())
                # print("ssid",self.network_name.get())
                wifiname=[]
                wifiname.append("\nnetwork={\n")
                wifiname.append("\tssid=\""+self.network_name.get()+"\"\n")
                wifiname.append("\tpsk=\""+self.password_str.get()+"\"\n")
                wifiname.append("\tkey_mgmt=WPA-PSK\n")
                wifiname.append("}\n")

                print(wifiname)
                with open('/etc/wpa_supplicant/wpa_supplicant.conf','r') as f:
                    message = f.readlines()

                index=0
                for item in message:
                    print(item)
                    if item == "network={\n":
                        print ("index=",index)
                        if message[index+4] != "\tdisabled=1\n" :
                            message.insert(index+4,"\tdisabled=1\n")
                            print("Remove disabled")
                    index=index+1

                Saved_ssid=0
                index=0
                for item in message:
                    # print(item)
                    if item == wifiname[1]:
                        Saved_ssid=1
                        # print ("saved")
                        # print ("index=",index)
                        if message[index+3] == "\tdisabled=1\n" :
                            message.pop(index+1)
                            message.insert(index+1,wifiname[2])
                            message.pop(index+3)
                            # print("Remove disabled")
                    index=index+1

                # print(set(wifiname).issubset(set(message)))

                print(message)
                # if Saved_ssid==1:
                #     os.system("sudo wpa_cli -i wlan0 reconfigure")
                #     time.sleep(5)
                if Saved_ssid==0:
                    # os.chmod('/etc/wpa_supplicant/',0o777)
                    message.extend(wifiname)
                print("write")
                os.system("sudo chmod 777 /etc/wpa_supplicant/wpa_supplicant.conf")
                with open('/etc/wpa_supplicant/wpa_supplicant.conf','w') as new_f:
                    for item in message:
                        print(item)
                        new_f.write("%s"%item)
                f.close()
                # time.sleep(2)       
                # responce = os.system("sudo wpa_cli -i wlan0 reconfigure")
                responce = os.popen('sudo wpa_cli -i wlan0 reconfigure').read()
                print("responce",responce)
             
                if (responce.find("OK") != -1):
                    print("connected")  
                    self.tabControls.add(self.wifi_tab, text=self.topMenu[6],image=self.wifi_icon, compound=LEFT)   
                    self.close_pass_sec(tab)

                    i=0
                    print(self.wifi_list)
                    for item in self.wifi_list:
                        # if self.wifi_list[0] == wifiname[1] :
                        print(str(self.wifi_list[i][0]))
                        print(wifiname[1])
                        if wifiname[1].find(str(self.wifi_list[i][0])) != -1 :   
                            self.wifi_list[i]=list(self.wifi_list[i])
                            self.wifi_list[i][1]=1
                        else:
                            self.wifi_list[i]=list(self.wifi_list[i])
                            self.wifi_list[i][1]=0
                        self.wifi_list[i]=tuple(self.wifi_list[i])    
                        i=i+1
                    print(self.wifi_list)    
                    self.reset_frame(self.wifiFrameList)
                    self.design_wifi_section()    

                elif (responce.find("FAIL") != -1):
                    self.messagebox('warnnig','Password not match. \nPlease enter correct password')

                # print(responce)


        return

    # Design Setting section
    # Select hook image
    # Select design
    def design_setting_section(self):
        #Hook design section
        self.hookSettingFrame = Frame(self.SettingFrameRight)
        self.hookSettingFrame.grid(row=0,column=0,sticky='news',pady=(0,20))

        #Heading of hook
        lbl = Label(self.hookSettingFrame, text='First number of Hook', style='head.TLabel')
        lbl.grid(row=0,column=0,columnspan=4,sticky='nw')

        #Hook design loop from setting/hook
        col = 0
        self.lblCol = []
        self.lblChkCol = []
        self.lblUnChkCol = []
        # self.lblCol=[]   # clear array
        for r, dirs, fnames in os.walk(self.hook_setting_dir):
            #sort setting image ascending order
            fnames.sort()
            for fname in fnames:
                settinglbl = {}
                settingimg = {}
                #Get setting image
                settingimg = PhotoImage(file=os.path.join(r,fname))

                #Set image in label
                settinglbl = Label(self.hookSettingFrame, image=settingimg,borderwidth=1, padding=5)
                settinglbl.image = settingimg
                settinglbl.grid(row=1,column=col,sticky='news',pady=10,padx=10)

                #Bind click event of image
                settinglbl.bind("<Button-1>", lambda e, fname = col, lbl=settinglbl: self.setting_img_up(fname,lbl))

                settinglbl.config(relief=RAISED)
                settinglbl.config(background='#ffffff')

                self.lblCol.append(settinglbl)
                print("self.lblCol",len(self.lblCol) )
                col += 1

        #Separator
        sep = Separator(self.SettingFrameRight, orient=HORIZONTAL)
        sep.grid(row=1,column=0,sticky='news')

        # Design settings
        self.designSettingFrame = Frame(self.SettingFrameRight)
        self.designSettingFrame.grid(row=3,column=0,sticky='news',pady=(20,0))

        #Heading of design
        lbl = Label(self.designSettingFrame, text='Design of Machine', style='head.TLabel')
        lbl.grid(row=0,column=0,columnspan=4,sticky='nw')
     
        #Data of design
        for h in range(len(self.selectDesignArr)):
            unchk = {}
            unchk = Label(self.designSettingFrame, text=self.selectDesignArr[h][0], image=self.unchk_icon,style='plain.TLabel',compound=LEFT)
            unchk.image = self.unchk_icon
            unchk.bind("<Button>", lambda e, chked = True, row = 3, col = h, fname=1, index=h: self.get_select_design(index,fname,chked,row,col))
            self.lblUnChkCol.append(unchk)

            chk = {}
            chk = Label(self.designSettingFrame, text=self.selectDesignArr[h][0], image=self.chk_icon,style='plain.TLabel',compound=LEFT)
            chk.image = self.chk_icon
            chk.bind("<Button-1>", lambda e, chked = False, row = 3, col = h, fname=0, index=h: self.get_select_design(index,fname,chked,row,col))
            self.lblChkCol.append(chk)

            unchk.grid(row=1,column=h, sticky="nw")
            chk.grid_forget()

    # Harness setting section
    # Select harness
    def harness_setting_section(self):
        #Harness design section
        self.harnessSettingFrame = Frame(self.SettingFrameRight)
        self.harnessSettingFrame.grid(row=0,column=0,sticky='news',pady=(0,20))

        #Heading of harness
        lbl = Label(self.harnessSettingFrame, text='Harness selection', style='head.TLabel')
        lbl.grid(row=0,column=0,columnspan=4,sticky='nw')
        self.hrOnSetting = []
        self.hrOffSetting = []
        # Harness settings
        for h in range(len(self.harnessArr)):

            #Radio section
            radiooff = {}
            radiooff = Label(self.harnessSettingFrame, image=self.roff_icon,style='plain.TLabel')
            radiooff.image = self.roff_icon
            radiooff.bind("<Button>", lambda e, chked = True, row = h, col = 0, fname=self.harnessArr[h][1], index=h: self.get_harness(index,fname,chked,row,col))
            self.hrOffSetting.append(radiooff)

            radioon = {}
            radioon = Label(self.harnessSettingFrame, image=self.ron_icon,style='plain.TLabel')
            radioon.image = self.ron_icon
            radioon.bind("<Button-1>", lambda e, chked = False, row = h, col = 0, fname=self.harnessArr[h][1], index=h: self.get_harness(index,fname,chked,row,col))
            self.hrOnSetting.append(radioon)

            radiooff.grid(row=h+1,column=0, sticky="nw",pady=35)
            radioon.grid_forget()

            #data section
            hr_image = PhotoImage(file=os.path.join(self.harness_setting_dir, (self.harnessArr[h][0].replace(' ',''))+'.png'))
            lbl = Label(self.harnessSettingFrame, text=self.harnessArr[h][0], image=hr_image,style='plain.TLabel',compound=RIGHT)
            lbl.image = hr_image
            lbl.grid(row=h+1,column=1, sticky="nw",pady=5)
        return

    # Production setting section
    # Set diameter
    def production_setting_section(self):
        #Prodction section
        self.proSettingFrame = Frame(self.SettingFrameRight)
        self.proSettingFrame.grid(row=0,column=0,sticky='news',pady=(0,20))

        #Heading of hook
        lbl = Label(self.proSettingFrame, text='Change Diameter for production', style='head.TLabel')
        lbl.grid(row=0,column=0,columnspan=2,sticky='nw')

        #diameter settings
        self.diameter_widget = Entry(self.proSettingFrame, text=self.diameter, state='disabled', width=5,style='EntryStyle.TEntry',font='Verdana 15 bold')
        self.diameter_widget.grid(row=1,column=0, sticky="ew", pady=5)

        btn = Button(self.proSettingFrame, text='Roll Diameter', style='setting.TButton', command=self.change_diameter)
        btn.grid(row=1, column=1,sticky='EW', pady=5, padx=10)

        #Generate keypad canvas
        self.settingKeypad = Frame(self.proSettingFrame)
        self.settingKeypad.grid_forget()

        self.gen_keypad(self.settingKeypad,'setting','lgkeypad.TButton')
        #End Meter keypad
        return

    # Feature setting section
    def feature_setting_section(self):
        #Weft design section
        self.wfOffSetting=[]
        self.wfOnSetting=[]
        self.pfOffSetting=[]
        self.pfOnSetting=[]        
        self.weftSettingFrame = Frame(self.SettingFrameRight)
        self.weftSettingFrame.grid(row=0,column=0,sticky='news',pady=(0,20))

        #Heading of weft
        lbl = Label(self.weftSettingFrame, text='Weft Selector', style='head.TLabel')
        lbl.grid(row=0,column=0,columnspan=4,sticky='nw')

        # Weft selector settings
        for h in range(len(self.weftSelectorArr)):
            #Radio section
            radiooff = {}
            radiooff = Label(self.weftSettingFrame, text=self.weftSelectorArr[h][0], image=self.roff_icon,style='plain.TLabel',compound=LEFT)
            radiooff.image = self.roff_icon
            radiooff.bind("<Button>", lambda e, chked = True, row = h, col = 0, fname=self.weftSelectorArr[h][1], index=h: self.get_weftselection(index,fname,chked,row,col))
            self.wfOffSetting.append(radiooff)

            radioon = {}
            radioon = Label(self.weftSettingFrame, text=self.weftSelectorArr[h][0], image=self.ron_icon,style='plain.TLabel',compound=LEFT)
            radioon.image = self.ron_icon
            radioon.bind("<Button-1>", lambda e, chked = False, row = h, col = 0, fname=self.weftSelectorArr[h][1], index=h: self.get_weftselection(index,fname,chked,row,col))
            self.wfOnSetting.append(radioon)

            radiooff.grid(row=h+1,column=0, sticky="nw",pady=5)
            radioon.grid_forget()

        #Separator
        sep = Separator(self.SettingFrameRight, orient=HORIZONTAL)
        sep.grid(row=1,column=0,sticky='news')

        #Pick find design section
        self.pfSettingFrame = Frame(self.SettingFrameRight)
        self.pfSettingFrame.grid(row=2,column=0,sticky='news',pady=(20,0))

        #Heading of weft
        lbl = Label(self.pfSettingFrame, text='Pick Find Section', style='head.TLabel')
        lbl.grid(row=0,column=0,columnspan=4,sticky='nw')

        # Weft selector settings
        for h in range(len(self.pickFindArr)):
            #Radio section
            radiooff = {}
            radiooff = Label(self.pfSettingFrame, text=self.pickFindArr[h][0], image=self.roff_icon,style='plain.TLabel',compound=LEFT)
            radiooff.image = self.roff_icon
            radiooff.bind("<Button>", lambda e, chked = True, row = h, col = 0, fname=self.pickFindArr[h][1], index=h: self.get_pickselection(index,fname,chked,row,col))
            self.pfOffSetting.append(radiooff)

            radioon = {}
            radioon = Label(self.pfSettingFrame, text=self.pickFindArr[h][0], image=self.ron_icon,style='plain.TLabel',compound=LEFT)
            radioon.image = self.ron_icon
            radioon.bind("<Button-1>", lambda e, chked = False, row = h, col = 0, fname=self.pickFindArr[h][1], index=h: self.get_pickselection(index,fname,chked,row,col))
            self.pfOnSetting.append(radioon)

            radiooff.grid(row=h+1,column=0, sticky="nw",pady=5)
            radioon.grid_forget()
        return

    # Sensor setup setting
    def sensor_setting_section(self):
        #Sensor setup design section
        self.snOnSetting = []
        self.snOffSetting = []
        self.snSettingFrame = Frame(self.SettingFrameRight)
        self.snSettingFrame.grid(row=0,column=0,sticky='news',pady=(0,20))

        #Heading of sensor
        lbl = Label(self.snSettingFrame, text='Sensor Setup Selection', style='head.TLabel')
        lbl.grid(row=0,column=0,columnspan=4,sticky='nw')

        # sensor selector settings
        for h in range(len(self.sensorPatternArr)):
            #Radio section
            radiooff = {}
            radiooff = Label(self.snSettingFrame, text=self.sensorPatternArr[h][0], image=self.roff_icon,style='plain.TLabel',compound=LEFT)
            radiooff.image = self.roff_icon
            radiooff.bind("<Button>", lambda e, chked = True, row = h, col = 0, fname=self.sensorPatternArr[h][1], index=h: self.get_sensorselection(index,fname,chked,row,col))
            self.snOffSetting.append(radiooff)

            radioon = {}
            radioon = Label(self.snSettingFrame, text=self.sensorPatternArr[h][0], image=self.ron_icon,style='plain.TLabel',compound=LEFT)
            radioon.image = self.ron_icon
            radioon.bind("<Button-1>", lambda e, chked = False, row = h, col = 0, fname=self.sensorPatternArr[h][1], index=h: self.get_sensorselection(index,fname,chked,row,col))
            self.snOnSetting.append(radioon)

            radiooff.grid(row=h+1,column=0, sticky="nw",pady=5)
            radioon.grid_forget()

        return

    #Select number of hooks
    def nofHooks_setting_section(self):
        #Sensor setup design section
        self.nfhookSetting = []
        self.nfhooksSettingFrame = Frame(self.SettingFrameRight)
        self.nfhooksSettingFrame.grid(row=0,column=0,sticky='news',pady=(0,20))

        #Heading of hook
        self.nf_hook = Label(self.nfhooksSettingFrame, text='Select only one hook', style='head.TLabel')
        self.nf_hook.grid(row=0,column=0,columnspan=10,sticky='nw')

        # hook selector settings
        self.hooksFrame = Frame(self.nfhooksSettingFrame)
        self.hooksFrame.grid(row=1,column=0,sticky='nw',pady=(10,0))

        self.hookcanvas = Canvas(self.hooksFrame, background="#FFFFFF",bd=0,highlightthickness = 0)
        self.hookcanvas.grid(row=0,column=0, sticky='news')

        self.hook_vsb =  Scrollbar(self.hooksFrame, orient='vertical', command=self.hookcanvas.yview, style='Vertical.TScrollbar')
        self.hook_vsb.grid(row=0,column=1, sticky='ns')

        self.hookcanvas.configure(yscrollcommand=self.hook_vsb.set)

        self.hookinnFrame = Frame(self.hooksFrame)
        self.hookcanvas.create_window((0,0), window=self.hookinnFrame, anchor='nw')

        c = 0
        r = 0
        for h in range(len(self.hooksArr)):
            if c > 0 and c%4 == 0:
                c = 0
                r+=1

            btn = {}
            btn = Button(self.hookinnFrame,text=self.hooksArr[h],style='transparent.TButton',command=lambda data=self.hooksArr[h]:self.getHook(data))
            btn.grid(row=r+1,column=c,sticky='nw',padx=5,pady=5)
            self.nfhookSetting.append(btn)
            c+=1


        self.hookinnFrame.update_idletasks()
        row_count = 40
        col_count = 4
        if len(self.hooksArr) < row_count: row_count = len(self.hooksArr)
        bbox = self.hookcanvas.bbox('all')
        cw, ch = bbox[2]-bbox[1], bbox[3]-bbox[1]

        dw, dh = int((cw/col_count) * col_count), int((ch/len(self.hooksArr)) * row_count)
        self.hookcanvas.config(scrollregion=bbox, width=dw, height=dh)

        return


    # Manage shift report
    # You can add new shift and delete and update it
    def shift_report_section(self):
        return

    #Travrse array and find index
    def match_with_array(self,arr,match):
        index = 0
        if len(arr) > 0 and match != '':
            for a in range(len(arr)):
                if arr[a].find(match) is not -1:
                    index = a
                    break
        return index

    #G et selected hook
    def getHook(self, hook):

        print(hook)
        self.hooknum = [0x00,0x40]
        self.hookrow = 0x02
        self.hookclm = 0x04
        self.totalhook = int(hook[1:5])/8
        print(self.totalhook)
        self.hooknum=( struct.pack("<H",int(self.totalhook)) )
        # self.hooknum[0]= int(hook[1:3])
        # self.hooknum[1]=int(hook[3:5])
        self.hookrow = int(hook[7:9])
        self.hookclm =int(hook[11:])

        print(self.hooknum[0])
        print(self.hooknum[1])
        print(self.hookrow)
        print(self.hookclm)
        # self.nf_hook.config(text='Selected hook: "'+ hook +'"')#,image=self.close_small_icon,compound=RIGHT
        # self.nf_hook.bind('<Button-1>',lambda e:self.reset_hook())
        # #If already data exists then first clear it
        # if self.no_of_hook.get() != '':
        #     index = self.match_with_array(self.hooksArr,self.no_of_hook.get())
        #     self.nfhookSetting[index].config(style='transparent.TButton')

        # #Set new data
        # self.no_of_hook.set(hook)
        # index = self.match_with_array(self.hooksArr,hook)
        # self.nfhookSetting[index].config(style='selected.TButton')
        self.get_controller_setting(SET_NUMBER_HOOK)
        return

    def reset_hook(self):
        self.nf_hook.config(text='Select only one hook',image='')
        self.nf_hook.unbind('<Button-1>')
        index = self.match_with_array(self.hooksArr,self.no_of_hook.get())
        self.nfhookSetting[index].config(style='transparent.TButton')
        self.no_of_hook.set('')
        return


    #Get all setting data from controller
    #init indicate you are getting data from controller if its true
    #otherwise first system will send changed setting then get updated setting from controller.
    #that updated settingt we will set to our system variables
    def get_controller_setting(self,init):
        #if called initially then just get all data from controller
        self.Test_flg = 0
        if init==GET_SETTINGS:
            # self.selectDesign[0] = 1
            # self.selectDesign[1] = 0
            print("get data from controler only")
            self.ser.write(MAIN_ADD)
            self.ser.write(SET_REQ)
            self.ser.write(EOD)
        elif init==SET_DESIGN_SET :
            print("image set")
            self.ser.write(MAIN_ADD)
            self.ser.write(SET_STATUS)
            self.ser.write(bytes([SET_DESIGN_SET]))
            print(self.settingDesign)
            self.ser.write(bytes([self.settingDesign]))
            self.ser.write(EOD)
        elif init==SET_INVERT_DES :
            print("invert designe")
            self.ser.write(MAIN_ADD)
            self.ser.write(SET_STATUS)
            self.ser.write(bytes([SET_INVERT_DES]))
            # self.ser.write(bytes([0x05]))
            self.ser.write(bytes([self.selectDesign[0]]))
            print(self.selectDesign[0])
            self.ser.write(EOD)
        elif init == SET_REVRC_CARD:
            print("Reverce card")
            self.ser.write(MAIN_ADD)
            self.ser.write(SET_STATUS)
            self.ser.write(bytes([SET_REVRC_CARD]))
            self.ser.write(bytes([self.selectDesign[1]]))
            print(self.selectDesign[1])
            self.ser.write(EOD)
        elif init==SET_HARNES_SET:
            print("harness")
            self.ser.write(MAIN_ADD)
            self.ser.write(SET_STATUS)
            self.ser.write(bytes([SET_HARNES_SET]))
            print("self.harness",self.harness)
            self.ser.write(bytes([self.harness]))
            self.ser.write(EOD)
        elif init==SET_ROLL_DIA :
            print("diameter")
            print(self.SetDiameter)
            
            self.ser.write(MAIN_ADD)
            self.ser.write(SET_STATUS)
            self.ser.write(bytes([SET_ROLL_DIA]))
            if self.diameter.get()=='':
                self.SetDiameter=0
            else :
                self.SetDiameter=int(self.diameter.get())
 
            self.ser.write(bytes([self.SetDiameter]))
            self.ser.write(EOD)
        elif init==SET_WEFT_SLCT:
            print("weft select")
            print("self.Weft_selection",self.Weft_selection)
            self.ser.write(MAIN_ADD)
            self.ser.write(SET_STATUS)
            self.ser.write(bytes([SET_WEFT_SLCT]))
            self.ser.write(bytes([self.Weft_selection]))
            self.ser.write(EOD)  
        elif init==SET_PICK_FIND:
            print("pick select")
            print("self.pick_selection",self.Pick_find)
            self.ser.write(MAIN_ADD)
            self.ser.write(SET_STATUS)
            self.ser.write(bytes([SET_PICK_FIND]))
            self.ser.write(bytes([self.Pick_find]))
            self.ser.write(EOD)  

        elif init==SET_SENSR_SETUP:
            print("sensor select")
            print("self.SET_SENSR_SETUP",self.sensor_setup)
            self.ser.write(MAIN_ADD)
            self.ser.write(SET_STATUS)
            self.ser.write(bytes([SET_SENSR_SETUP]))
            self.ser.write(bytes([self.sensor_setup]))
            self.ser.write(EOD)  

        elif init == SET_NUMBER_HOOK:    
            # print("self.SET_SENSR_SETUP",self.sensor_setup)
            self.ser.write(MAIN_ADD)
            self.ser.write(SET_STATUS)
            self.ser.write(bytes([SET_NUMBER_HOOK]))
            self.ser.write(bytes([self.hooknum[0]]))
            self.ser.write(bytes([self.hooknum[1]]))
            self.ser.write(bytes([self.hookrow]))
            self.ser.write(bytes([self.hookclm]))
            self.ser.write(EOD)

        self.Status_timer = threading.Timer(2.0, self.Check_test_responce)
        self.Status_timer.start()

    #Generate keypad design
    #Dyanmic frame name to generate frame for keypad
    #For which tab you are going to design
    def gen_keypad(self,frame, tab,st='keypad.TButton'):
        if tab == 'info':
            state =  str(self.cbtn['state'])
            if state == 'disabled':
                return False

            #Generate Frame for keypad
            frame.grid(row=0,column=1,sticky='news',pady=20, padx=20)
            self.mEntryInfo.focus()
            self.InfoFrameR.grid_forget()
            frame = self.InfoFramekB
            self.cbtn.config(state=DISABLED)
            row = 1
        else:
            row = 0

        col = 0
        for k in range(len(self.keypad)):
            if k % 3 == 0:
                row = row + 1
                col = 0

            kpBtn = Button(frame, text=self.keypad[k],style=st, command= lambda kval=self.keypad[k], pframe=frame: self.up_by_keypad(kval,tab,pframe))
            kpBtn.grid(row=row,column=col, padx=5, pady=5, sticky="nw")
            col = col + 1

    #Select Setting image
    #fname s setting image name without extension
    def setting_img_up(self, fname, lbl):
        #Reset all selection from setting image
        #Set setting image name
        self.settingDesign = fname
        #send to controller for confirmation about new setting
        self.get_controller_setting(SET_DESIGN_SET)

    #Set harness
    #index of current clicked radio
    #fname of click harness label name
    #chked will give True or False to inform about radio status
    def get_harness(self,index,fname,chked,row,col):
        #If checked true then do everything
        if chked:
            #set click radio value
            self.harness = fname
            print("fname",fname)
            print("index",index)
            
            #send to controller for confirmation about new setting
        self.get_controller_setting(SET_HARNES_SET)

    #index of current clicked radio
    #fname of click harness label name
    #chked will give True or False to inform about radio status
    def get_weftselection(self,index,fname,chked,row,col):
        #If checked true then do everything
        if chked:
            #set click radio value
            self.Weft_selection = fname
            print("fname",fname)
            print("index",index)
            
            #send to controller for confirmation about new setting
        self.get_controller_setting(SET_WEFT_SLCT)    
    
    def get_pickselection(self,index,fname,chked,row,col):
        #If checked true then do everything
        if chked:
            #set click radio value
            self.Pick_find = fname
            print("fname",fname)
            print("index",index)            
            #send to controller for confirmation about new setting
        self.get_controller_setting(SET_PICK_FIND)    
    
    def get_sensorselection(self,index,fname,chked,row,col):
        #If checked true then do everything
        if chked:
            #set click radio value
            self.sensor_setup = fname
            print("fname",fname)
            print("index",index)            
            #send to controller for confirmation about new setting
        self.get_controller_setting(SET_SENSR_SETUP)        
    #Set design name
    #index of current click checkbox
    #fname current click of checkbox value
    #chked give True or False value of checkbox
    def get_select_design(self,index,fname,chked,row,col):
        #Update index value based on click design type
        self.selectDesign[index] = fname
        print(fname)
        # print(self.selectDesign)
        #send to controller for confirmation about new setting
        if index == 0:
            self.get_controller_setting(SET_INVERT_DES)
        else:
            self.get_controller_setting(SET_REVRC_CARD)
    #Enable diameter textbox
    def change_diameter(self):
        #enable textbox and set focus
        self.diameter_widget.configure(state=NORMAL)
        self.diameter_widget.focus()
        #Show keypad
        self.settingKeypad.grid(row=2,column=0,columnspan=2,sticky='news')

    #Keypad action event
    #key will be 0 - 9, C or OK
    #tab wise coding
    #pframe of parent frame object
    def up_by_keypad(self, key, tab, pframe):
        if key == 'C':
            if tab == 'files':
                self.pick.set('')
            elif tab == 'setting':
                self.diameter.set('')
            elif tab == 'info':
                self.Pick_txt_tmp.set('')
        elif key == 'OK':

            if tab == 'files':
                if str(self.pick.get()) == "":
                    self.messagebox('Warning','Please Enter meters')
                elif int(self.pick.get())>65535:
                    self.messagebox('Warning','Please Enter less then 65535 meters')
                # if len(self.FileChked) > 0 :
                else :
                    #Display loader while copy files
                    print ("ID",self.infoThreadId)
                    self.master.after_cancel(self.infoThreadId)
                    filepath = os.path.join(self.files_dir,self.FileChked[0])
                    fileName=os.path.basename(filepath)
                    FileNamestr="Copying "+ fileName + " to system"
                    print(FileNamestr)
                    self.is_animate = True
                    self.call_loader(FileNamestr,True,'files')
                    # self.call_loader('Copying file to system....',True,'files')
                    self.copyBar.set(str(0))
                    self.copy_text.set(str(0))
                    self.thread_flg =1
                    self.sendbmptimer =threading.Timer(1,self.Send_Bmp_fileToMcu)
                    self.sendbmptimer.start()
                    # self.Msgstring=""
                    # while(True):
                    #     if self.Msgstring != "":
                    #         self.messagebox('Warning',self.Msgstring)
                    #         break
                    # self.Send_Bmp_fileToMcu()

            elif tab == 'info':
                old = str(self.Pick_txt_tmp.get())

                if str(self.Pick_txt_tmp.get()) == "":
                    self.messagebox('Warning','Please Enter Pick')
                elif int(self.Pick_txt_tmp.get())>65535:
                    self.messagebox('Warning','Please Enter Valid Pick')
                else :
                    self.ser.write(MAIN_ADD)
                    self.ser.write(PICK_NUM)
                    numbyte = int(self.Pick_txt_tmp.get()).to_bytes(2, 'little')
                    self.ser.write(numbyte)
                    # self.ser.write(bytes([int(self.Pick_txt_tmp.get())]))
                    self.ser.write(EOD)
                    self.close_keypad()

            elif tab == 'setting':
                #Check diameter should have some value
                # self.SetDiameter=int(self.diameter.get())
                if str(self.diameter.get()) == '':
                    print("warning")
                    self.messagebox('Warning','Please Enter Diameter')
                elif int(self.diameter.get()) > 255:
                    self.messagebox('Warning','Please Enter Diameter below 255')
                else:
                    pframe.grid_forget()
                    self.diameter_widget.configure(state=DISABLED)
                    print("send to controller1")
                    #send to controller for confirmation about new setting
                    self.get_controller_setting(SET_ROLL_DIA )
        else:
            if tab == 'files':
                old = self.pick.get()
                self.pick.set(old + key)

            elif tab == 'info':
                old = self.Pick_txt_tmp.get()
                self.Pick_txt_tmp.set(old + key)

            elif tab == 'setting':
                old = str(self.diameter.get())
                self.diameter.set(old + key)

    #convert byte to integer
    def bytes_to_int(self, bytes_data, res = 0):
        for b in bytes_data:
                res = (res * 256) + int(b)
        return res


    #Read file name on info tab
    def Req_fileName(self):
        print("file name request")
        self.Test_flg=0
        Test_timer = threading.Timer(3, self.Check_test_responce)
        Test_timer.start()
        self.ser.write(MAIN_ADD)
        self.ser.write(FILE_NAME)
        self.ser.write(EOD)
        self.Recivedata=[]
        self.Namelenth=0


# root window created. Here, that would be the only window, but
# you can later have windows within windows.
root = Tk()

# Set Window width and Height
# root.attributes('-type','dock'
# )
root.geometry("1024x600+0+0")
root.focus_force()
# Window should not be resizable
root.resizable(False, False)

root.grid_rowconfigure(1,weight=1)
root.grid_columnconfigure(0,weight=1)
# root.protocol("WM_DELETE_WINDOW",DISABLED)
root.wm_attributes("-type","splash")
# root.wm_attributes("-fullscreen","true")
# Disable close button of window
# def disable_event():
#     pass
# root.protocol('WM_DELETE_WINDOW',DISABLED)

#Hide top level bar
# root.attributes(DISABLED,True)
# root.overrideredirect(1)

#creation of an instance
app = Window(root)

#mainloop
root.mainloop()