#! /usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter.ttk as ttk
import tkinter.font as tkFont
import tkinter as tk
from PIL import Image,ImageTk

try:
    from UI import PyTkinter as pytk
except:
    import PyTkinter as pytk

g_font = ('Monaco', 12)

class MainFrame(object):
    '''
    Serial窗体
    '''

    def __init__(self, master=None):
        '''
        初始化
        '''
        self.root = master
        self.create_frame()

    def create_frame(self):
        '''
        创建窗体
        '''
        self.frm = pytk.PyFrame(self.root)
        self.frm.pack(fill="both", expand=1)

        self.import_listbox = pytk.PyListbox(self.frm,font=g_font,selectmode='extended',width=30)
        self.import_listbox.grid(column=0,row=0,rowspan=2,sticky=tk.N+tk.S,padx=5,pady=5)
        #self.import_listbox.insert(0,'text')

        self.add_btn = pytk.PyButton(self.frm,font=g_font,text='>>',command=self.add_codes)
        self.add_btn.grid(column=1,row=0,sticky=tk.S,padx=5,pady=5)

        self.del_btn = pytk.PyButton(self.frm,font=g_font,text='<<',command=self.del_codes)
        self.del_btn.grid(column=1,row=1,sticky=tk.N,padx=5,pady=5)


        self.code_listbox = pytk.PyListbox(self.frm,font=g_font,selectmode='extended',width=30,fg="red")
        self.code_listbox.grid(column=2,row=0,rowspan=2,sticky=tk.N+tk.S,padx=5,pady=5)

        self.preview_canvas = pytk.PyCanvas(self.frm,width=200,height=200)
        self.preview_canvas.grid(column=3,row=0,rowspan=2,padx=5,pady=5)

        self.gen_codes_btn = pytk.PyButton(self.frm,text='生成CODE128',command=self.gen_codes)
        self.gen_codes_btn.grid(column=2,row=2,padx=5,pady=5,sticky=tk.N+tk.S+tk.E+tk.W)

        self.frm_file = pytk.PyLabelFrame(self.frm)
        self.frm_file.grid(column=0,row=2,columnspan=2,padx=5,pady=5,sticky=tk.N+tk.S+tk.E+tk.W)
        self.create_frm_file()

        self.frm_setting = pytk.PyLabelFrame(self.frm)
        self.frm_setting.grid(column=3,row=2,padx=5,pady=5,sticky=tk.N+tk.S+tk.E+tk.W)
        self.create_frm_setting()

        self.progressbar = ttk.Progressbar(self.frm,value=0)
        self.progressbar.grid(column=0,row=3,columnspan=4,padx=5,pady=5,sticky=tk.N+tk.S+tk.E+tk.W)
    def create_frm_file(self):
        self.import_files_entry = pytk.PyEntry(self.frm_file,font=g_font)
        self.import_files_entry.grid(column=0,row=0,padx=5,pady=5)
        self.import_files_btn = pytk.PyButton(self.frm_file,font=g_font,text='导入文件',command=self.import_files)
        self.import_files_btn.grid(column=1,row=0,padx=5,pady=5)

        self.export_files_entry = pytk.PyEntry(self.frm_file,font=g_font)
        self.export_files_entry.grid(column=0,row=1,padx=5,pady=5)
        self.export_files_entry.insert(0,'./image')
        self.export_files_btn = pytk.PyButton(self.frm_file,font=g_font,text='导出目录',command=self.export_files)
        self.export_files_btn.grid(column=1,row=1,sticky=tk.N,padx=5,pady=5)
        pass

    def create_frm_setting(self):
        self.setting_width_label = pytk.PyLabel(self.frm_setting,font=g_font,text="宽度:")
        self.setting_width_label.grid(column=0,row=0,padx=5,pady=5)
        self.setting_width_label = pytk.PyLabel(self.frm_setting,font=g_font,width=5,text="880")
        self.setting_width_label.grid(column=1,row=0,padx=5,pady=5)

        self.setting_height_label = pytk.PyLabel(self.frm_setting,font=g_font,text="高度:")
        self.setting_height_label.grid(column=0,row=1,padx=5,pady=5)
        self.setting_height_entry = pytk.PyEntry(self.frm_setting,font=g_font,width=5)
        self.setting_height_entry.grid(column=1,row=1,padx=5,pady=5)
        self.setting_height_entry.insert(0, '1000')
        pass
        
    def add_codes(self):
        pass

    def del_codes(self):
        pass

    def import_files(self):
        pass

    def export_files(self):
        pass

    def gen_codes(self):
        pass


if __name__ == '__main__':
    '''
    main loop
    '''
    root = tk.Tk()
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.geometry()

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

    app = MainFrame(root)
    app.frm.pack(fill="both", expand=1)
    '''
    测试预览窗口
    '''
            
    im = Image.open('../IMAGE/test.png')
    canvas_width = int(app.preview_canvas['width'])
    print(canvas_width)
    canvas_height = int(app.preview_canvas['height'])
    print(canvas_height)
    im.thumbnail((canvas_width,canvas_height))
    imtk = ImageTk.PhotoImage(im)
    app.preview_canvas.create_image(canvas_width/2,canvas_height/2,image=imtk)
    root.mainloop()
