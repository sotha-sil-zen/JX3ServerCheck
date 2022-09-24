# -*- coding: utf-8 -*-
import requests
import json
import re
def GET(url):
    #get请求
    req = requests.get(url)
    #输出状态码
    return req.status_code ,req.text
    #输出返回内容
    
def len_zh(data):
    temp = re.findall('[^a-zA-Z0-9.]+', data)
    count = 0
    for i in temp:
        count += len(i)
    return(count)

class ServerStatus:
    def __init__(self,zone,server,status):
        self.zone = zone
        self.server = server
        self.status = "开服" if status==1 else "未开服"
    

def get_server_status():
    status_code,rtn_text=GET("https://www.jx3api.com/app/check")
    if status_code!=200:
        return False
    json_text=json.loads(rtn_text)
    server_status=[]
    for i in json_text['data']:
        zone=i["zone"]
        server=i["server"]
        status=i["status"]
        server_status.append(ServerStatus(zone,server,status))
    return server_status

def is_server_open(server_status,server):
    for i in server_status:
        if i.server==server and i.status=="开服":
            return True
    return False


import threading
import time


import tkinter
import tkinter.ttk
import tkinter.messagebox
from win10toast import ToastNotifier
toaster = ToastNotifier()

def check_server_open(server):
    toaster.show_toast("你正在监听该服务器的开服状态：",
           server,
           icon_path='',
           duration=10)
    while True:
        time.sleep(5)
        server_status=get_server_status()
        if server_status==False:
            toaster.show_toast("网络连接",
                   "剑网三开服监控无法获取服务器信息，请检查网络并重启",
                   icon_path='',
                   duration=10)
            return False
        else:
            if is_server_open(server_status,server):
                toaster.show_toast("已开服",
                       str("你监听的剑网三服务器")+server+str("已开服"),
                       icon_path='',duration=10)
                return True


class MyGUI:
    def __init__(self): 
        self.main_window = tkinter.Tk()
        self.main_window.title('剑网三开服监控')
        server_status=get_server_status()
        if server_status==False:
            label=tkinter.Label(self.main_window,text="无法获取服务器信息，请检查网络并重启")
            label.pack(side=tkinter.TOP, padx="0.1i", pady="0.1i")
            combo_val.append(i.server)
        else:

            var = tkinter.StringVar()
            var.set("请选择要监听开服的区服")
            self.combobox = tkinter.ttk.Combobox(self.main_window, textvariable=var,state="readonly")
            combo_val=[]
            for i in range(len(server_status)):
                label=tkinter.Label(self.main_window,text=server_status[i].zone)
                label.grid(row=i,column=0,columnspan=2)
                label=tkinter.Label(self.main_window,text=server_status[i].server)
                label.grid(row=i,column=2,columnspan=2)
                label=tkinter.Label(self.main_window,text=server_status[i].status)
                label.grid(row=i,column=4,columnspan=2)
                combo_val.append(server_status[i].server)
            self.combobox['value']=tuple(combo_val)
            #self.combobox.pack(padx=5, pady=10)
            self.combobox.grid(row=len(server_status),column=1,columnspan=4)
            self.button=tkinter.Button(self.main_window, text="开始监听",command=self.button_callback)
            self.button.grid(row=len(server_status)+1,column=1,columnspan=4)
            self.thread=None
        self.main_window.mainloop()          
    def button_callback(self):
        if self.button['text']=="开始监听":
            select_server=self.combobox.get()
            
            if select_server=="请选择要监听开服的区服":
                tkinter.messagebox.showerror('请选择区服','请选择正确的区服')
                return
            thread = threading.Thread(target = check_server_open,args =(select_server,))
            thread.start()
            
       
# 创建实例MyGUI        
my_gui = MyGUI()
