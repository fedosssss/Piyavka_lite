from tkinter import *  
from tkinter import messagebox  
from tkinter import ttk 
from PIL import ImageTk, Image
import os
import os,json,datetime,random,getpass,shutil,sys,re
import time
import __main__
import telebot
from telebot import types
import webbrowser
print(__main__.__file__)#D:\git_projects\piy_lite\PIYAVKA_installer.py
print(os.path.dirname(os.path.realpath(__main__.__file__)))#D:\git_projects\piy_lite

def callback(event):
    webbrowser.open_new(r"https://t.me/BotFather")

def add_to_startup(USER_NAME):
    file_path = os.path.dirname(os.path.realpath(__main__.__file__)) + "\Piyavka_lite.py"
    bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % USER_NAME
    with open(bat_path + '\\' + "System Invoker Utility.bat", "w+") as bat_file:
        bat_file.write(r'''@echo off
start "" %s''' % file_path)


def print_selection():
    global btn
    if var1.get()==1:
        btn = Button(tab2, text="ГОТОВО", command=clicked) 
        btn.place(x=400, y=290)

    if var1.get()==0:
        btn.destroy()

def change_get():
    inlist=["Русский", "English"]
    inlist.remove(comboExample.get())
    comboExample["values"] = [inlist[0]]

def callbackFunc(event):
    global labl
    labl.destroy()
    if comboExample.get().lower()=="english":
        labl = Label(tab1, text='''Requirements:
            1) You have to create your bot in telegram (you will need a bot token to work)
            2) Subsequently, your device will be controlled through this bot
            3) Enter only the correct data, otherwise you will need to reinstall the program
            4)Do not overload the bot: make at least some time interval between sending messages''',bg='white',font="Calibri 12",fg="black")

    elif comboExample.get().lower()=="русский":
        labl = Label(tab1, text='''Требования:
            1) Вы должны создать своего бота в телеграмме(для работы потребуется токен бота)\nБот создаётся с помощью BotFather(https://t.me/BotFather)
            2) Впоследствии через этого бота и будет управляться Ваше устройство
            3) Вводите только верные данные, иначе нужно будет переустановить программу
            4) Не перегружайте бота: делайте хоть какой-то временной промежуток между отправками сообщений''',bg='white',font="Calibri 12",fg="black")

    
    labl.place(x=0,y=0)
        


def clicked():
    global message,window
    
    if message.get()=="":
        messagebox.showinfo('Предупреждение', 'Нельзя оставлять поле "токен" пустым!')           
    else:
        token=message.get()
        txt.delete(0, END)
       
        if os.path.exists(appdata_path_to_json) and os.path.getsize(appdata_path_to_json)>0:#.json существует
            if os.path.exists(appdata_path_to_exe):#.ехе существует и .json существует
                input("exe and json exists")#окно выводв (всё установлено для обновы nIr_upgrader)

            else:#.ехе не существует .json существует
                try:
                    add_to_startup(USER_NAME)
                    input("has done")
                except Exception as a:
                    print(a)
                    input()
                
                    
        else:#.json не существует  
            lb32 = Label(tab2, text="Напишите /start своему боту, чтобы завершить регистрацию!",bg="white",font="Calibri 15",fg="red")  
            lb32.place(x=0,y=170) 
            bot=telebot.TeleBot(str(token))
            @bot.message_handler(commands=["start"])
            def start(message):
                global id_admin
                id_admin=message.chat.id
                if message.from_user.last_name != None: 
                    mess=f'<b>{message.from_user.first_name} <u>{message.from_user.last_name}</u></b>, спасибо за установку нашего продукта! Установщик сейчас закроется, а уведомления начнут приходить уже при след. включении устройства, обязательно ознакомьтесь с функционалом. Если возникли вопросы: https://t.me/botoklepalka '      
                elif message.from_user.last_name == None:
                    mess=f'<b>{message.from_user.first_name} </b>, спасибо за установку нашего продукта! Установщик сейчас закроется, а уведомления начнут приходить уже при след. включении устройства, обязательно ознакомьтесь с функционалом. Если возникли вопросы: https://t.me/botoklepalka'
                else:
                    mess='Спасибо за установку нашего продукта! Установщик сейчас закроется, а уведомления начнут приходить уже при след. включении устройства, обязательно ознакомьтесь с функционалом. Если возникли вопросы: https://t.me/botoklepalka'
                bot.send_message(message.chat.id,mess,parse_mode="html")
                bot.stop_polling()
            bot.polling(none_stop = False)
            person_info=[]
            turn_on=0
            notification_status = True 
            info_list={
                'token': token,
                'id_admin' : id_admin,
                'notification_status': notification_status,
                'turn_on': turn_on
                }
                                
            person_info.append(info_list)
            with open(appdata_path_to_json,"w") as file:
                json.dump(info_list,file,indent=2,ensure_ascii=False)
                
            try:
                add_to_startup(USER_NAME=USER_NAME)

            except Exception:
                print("something went wrong with appdata")
        window.destroy()
##############################################        
USER_NAME = getpass.getuser()
redirect="recover.json"
main_code='WinIR.exe'
appdata_m=r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % USER_NAME#link to startup
appdata_path_to_json=f"{os.path.dirname(os.path.realpath(__main__.__file__))}\{redirect}"
appdata_path_to_exe=f"{appdata_m}\{main_code}"
##############################################
window = Tk()
window['bg']="white"
window.title("PIYAVKA_Lite")
window.geometry(f'800x{window.maxsize()[1]//2}')
window.resizable(False,False)

tab_control = ttk.Notebook(window)  
tab1 = ttk.Frame(tab_control)

tab2 = ttk.Frame(tab_control)  
tab_control.add(tab1, text='Требования')  
tab_control.add(tab2, text='Регистрация')
tab_control.pack(expand=1, fill='both')


style = ttk.Style()

style.theme_create( "main", parent="default", settings={
        "TNotebook": {"configure": {"background": "white" } },
        "TNotebook.Tab": {
            "configure": {"padding": [5, 1], "background": "white"},
            "map":       {"background": [("selected","#FF0000")],
                          "expand": [("selected", [1, 1, 1, 0])] } } } )

style.theme_use("main")



lbl = Label(tab1, text=None,bg="white")  
lbl.place(x=0,y=0,width=800,height=800)
lbl = Label(tab2, text=None,bg="white")  
lbl.place(x=0,y=0,width=800,height=800)
try:
    img = ImageTk.PhotoImage(Image.open("a1.png"))
    panel = Label(tab2, image = img)
    panel.place(x=0,y=0)
except Exception:
    pass
var1 = IntVar()
c1=Checkbutton(tab2, text='Я согласен с правилами сообщества',variable=var1, onvalue=1, offvalue=0, command=print_selection,bg="white")
c1.place(x=0,y=230)
labl = Label(tab1, text='''Требования:
            1) Вы должны создать своего бота в телеграмме(для работы потребуется токен бота)
            2) Впоследствии через этого бота и будет управляться Ваше устройство
            3) Вводите только верные данные, иначе нужно будет переустановить программу
            4) Не перегружайте бота: делайте хоть какой-то временной промежуток между отправками сообщений''',bg='white',font="Calibri 12",fg="black")
labl.place(x=0,y=0)
label_link = Label(tab1, text="Помощь: Как создать своего бота?", fg="blue", cursor="hand2")
label_link.pack()
label_link.bind("<Button-1>", callback)
label_link.place(x=0,y=350)
comboExample = ttk.Combobox(tab1, 
                            values=[
                                    "Русский", 
                                    "English"],
                            postcommand=change_get,state="readonly")
comboExample.place(x=150,y=window.maxsize()[1]//2-50)
comboExample.current(0)
comboExample.bind("<<ComboboxSelected>>", callbackFunc)

lb2 = Label(tab2, text="Токен Вашего личного бота:",bg="white",font="Calibri 15",fg="black")  
lb2.place(x=0,y=170)


message=StringVar()
txt = Entry(tab2,width=10,textvariable=message)  
txt.place(x=280,y=180,width=398)

window.mainloop()
