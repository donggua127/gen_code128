#! /usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import platform

import tkinter.ttk as ttk
import tkinter.font as tkFont
import tkinter as tk

from pystrich.code128 import Code128Encoder
from PIL import Image, ImageFont, ImageDraw,ImageTk
from tkinter import filedialog
from UI.MainFrm import MainFrame

# 根据系统 引用不同的库
if platform.system() == "Windows":
    from serial.tools import list_ports
    import glob
    import os
else:
    import glob
    import os
    import re

logging.basicConfig(level=logging.WARNING,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')

# 结束符（16进制）CR 13(\r - 0x0D); NL(LF) 10(\n - 0x0A)
END_HEX = "0D0A"


class MainCodeTool(MainFrame):
    '''
    main func class
    '''

    def __init__(self, master=None):
        super(MainCodeTool, self).__init__(master)
        self.root = master

        self.serial_receive_count = 0
        self.serial_recieve_data = []
        self.serial_listbox = list()
        self.serial_roadlist = list()
        self.routelist = list()
        
    
    def add_codes(self):
        try:
            code_selected = self.import_listbox.curselection()
            for index in code_selected:
                self.code_listbox.insert("end",self.import_listbox.get(index))
                        
        except Exception as e:
            logging.error(e)

            
    def del_codes(self):
        try:
            code_selected = self.code_listbox.curselection()
            length = len(code_selected)
            for index in range(length):
                self.code_listbox.delete(code_selected[length-index-1])
            
        except Exception as e:
            logging.error(e)
    
    def import_files(self):
        try:
            file_open = filedialog.askopenfile(title='打开单个文件',
            filetypes=[("文本文件", "*.txt"), ('Python源文件', '*.py')], # 只处理的文件类型
            initialdir='./') # 初始目录
            if file_open != None:
                self.import_files_entry.delete(0,tk.END)
                self.import_files_entry.insert(0,file_open.name)
                lines = file_open.readlines()
                for line in lines:
                    line = line.replace("\n","")
                    self.import_listbox.insert("end",line)
                file_open.close()
        except Exception as e:
            logging.error(e)

    def export_files(self):
        try:
            dir_name = filedialog.askdirectory(title='选择图片保存目录',
            initialdir='./') # 初始目录

            if dir_name != '':
                self.export_files_entry.delete(0,tk.END)
                self.export_files_entry.insert(0,dir_name)
        except Exception as e:
            logging.error(e)

    def gen_codes(self):
        global im,imtk,font
        
        self.progressbar["value"] = 0
        if self.code_listbox.size() > 0:
            step = 100/self.code_listbox.size()
        for index in range(self.code_listbox.size()):
            ## RFID转换为CODE128
            line = self.code_listbox.get(index)
            byte_line = bytes.fromhex(line)
            value = self.conv(byte_line).decode()

            ## 生成CODE128图片
            im_height = int(self.setting_height_entry.get())
            encoder=Code128Encoder(value,{'bottom_border':80,'height':im_height})
            filedir = self.export_files_entry.get()
            
            if os.path.exists(filedir) == False:
                os.makedirs(filedir)
                
            filename = filedir+"/{}.png".format(line)
            encoder.save(filename,bar_width=4)
            
            ## 图片中写入RFID值
            im = Image.open(filename)
            width,height=im.size
            draw = ImageDraw.Draw(im)
            draw.text((20,height-100),line,font=font)
            im.save(filename)

            ## 显示缩略图
            canvas_width = int(self.preview_canvas['width'])
            canvas_height = int(self.preview_canvas['height'])
            im.thumbnail((canvas_width,canvas_height))
            imtk = ImageTk.PhotoImage(im)
            self.preview_canvas.create_image(canvas_width/2,canvas_height/2,image=imtk)

            ## 进度条显示
            self.progressbar["value"] += step
            self.root.update()
            
    def conv(self,rfid):
        code128 = bytes()
        code128 += bytes([rfid[0] & 0x7f])
        code128 += bytes([((rfid[1] << 1) | (rfid[0] >> 7)) & 0x7f])
        code128 += bytes([((rfid[2] << 2) | (rfid[1] >> 6)) & 0x7f])
        code128 += bytes([((rfid[3] << 3) | (rfid[2] >> 5)) & 0x7f])
        code128 += bytes([((rfid[4] << 4) | (rfid[3] >> 4)) & 0x7f])
        code128 += bytes([((rfid[5] << 5) | (rfid[4] >> 3)) & 0x7f])
        code128 += bytes([((rfid[6] << 6) | (rfid[5] >> 2)) & 0x7f])
        code128 += bytes([((rfid[7] << 7) | (rfid[6] >> 1)) & 0x7f])
        code128 += bytes([rfid[7] & 0x7f])
        code128 += bytes([((rfid[8] << 1) | (rfid[7] >> 7)) & 0x7f])
        code128 += bytes([((rfid[9] << 2) | (rfid[8] >> 6)) & 0x7f])
        code128 += bytes([((rfid[10] << 3) | (rfid[9] >> 5)) & 0x7f])
        code128 += bytes([((rfid[11] << 4) | (rfid[10] >> 4)) & 0x7f])
        code128 += bytes([(rfid[11] >> 3) & 0x7f])

        sum_value = 0
        for code in code128:
            sum_value += code
        code128 += bytes([sum_value & 0x7f])
        return code128


if __name__ == '__main__':
    '''
    main loop
    '''
    root = tk.Tk()
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.geometry()
    root.title("CODE128生成工具")

    monacofont = tkFont.Font(family="Monaco", size=16)
    root.option_add("*TCombobox*Listbox*background", "#292929")
    root.option_add("*TCombobox*Listbox*foreground", "#FFFFFF")
    root.option_add("*TCombobox*Listbox*font", monacofont)

    root.configure(bg="#292929")
    combostyle = ttk.Style()
    combostyle.theme_use('default')
    combostyle.configure("TCombobox",
                         selectbackground="#292929",
                         fieldbackground="#292929",
                         background="#292929",
                         foreground="#FFFFFF")
    im=''
    imtk=''
    font = ImageFont.truetype("calibri.ttf",size=70)
    app = MainCodeTool(root)
    root.mainloop()
