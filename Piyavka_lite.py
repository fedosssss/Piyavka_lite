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
from win32gui import GetWindowText, GetForegroundWindow#active apps
import pyttsx3#воспроизведение текста
import time
import numpy as np
import platform 
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
import ctypes
#def's
def file_opening(nomination):#открытие ярлыков(приложений) из рабочего стола
    os.startfile(r'C:\Users\{name1}\Desktop\{name2}'.format(name1=USER_NAME,name2=str(nomination)))

    
def working_time(start_time):#вывод времени работы пк с начала включения
    end_time = time.monotonic()
    return timedelta(seconds=end_time - start_time)

def text_speaker(text):
    engine=pyttsx3.init()
    engine.say(text)
    engine.runAndWait()   
  

def resurs_monitor():#взятие показаний загрузки ЦП(8 секунд) и загрузки ОП(однократно)
    deadtime=time.monotonic()+8
    cpu_mass=[]
    while time.monotonic()<deadtime:
        cpu_mass.append(psutil.cpu_percent())
    feel=None
    if round(np.mean(cpu_mass))>80:
        feel = "сильная"
    elif round(np.mean(cpu_mass))<80 and round(np.mean(cpu_mass))>30:
        feel = "нормальная"
    else:
        feel = "слабая"
        
        
    vk.messages.send(user_id=profile_id,random_id=get_random_id(),keyboard=static_board.get_keyboard(),message=f'''загрузка цп: {round(np.mean(cpu_mass))}%,
 загрузка памяти: {psutil.virtual_memory()[2]}%.
 нагрузка на систему: {feel}
 ''')

    
def msg_root(event):#вывод текста на экран от пользователя 
    root_text=event.text.lower()
    root=Tk()
    root.title("Текстовое уведомление")
    root.geometry("3000x2500")
    lab=Label(root,text=root_text,font="Arial 16")
    root.call('wm', 'attributes', '.', '-topmost', '1')    
    lab.pack()
    root.mainloop()


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




    
    
def secondary_main(token, id_admin, turn_on):
    print("secondary_main is working")
    bot=telebot.TeleBot(token)
    @bot.message_handler(content_types=['text'])
    def get_text_messages(message):
        if message.text.lower()=="включи уведомления" or message.text.lower()=="включить уведомления":
            try:
                USER_NAME = getpass.getuser()
                redirect="recover.json"
                file_path=os.path.dirname(os.path.realpath(__main__.__file__))
                json_path=f"{file_path}\{redirect}"
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
                bot.send_message(id_admin,"Уведомления были включены. Уже при следующем включении устройства Вы будете уведомлены о включении")
                bot.stop_polling()
                time.sleep(8)
                sys.exit()
            
    bot.polling()


    
def main(token, id_admin, turn_on):
    print("main is working")
    global power_sleep, power_restart, sound_stat,text_speach, text_window, text_menu, file_path, cam_path, screen_path, photo_handler, screen_image_path, menu_stat, noti_status, power_off
    
    #system variables
    file_path=os.path.dirname(os.path.realpath(__main__.__file__))#link to startup
    cam_path=f"{file_path}\cam.png"
    screen_path=f"{file_path}\screen.png"
    screen_image_path=f"{file_path}\screen_logo.png"
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
    btn1 = KeyboardButton("Звуковое оповещение🔊")
    btn2 = KeyboardButton("Вывод текста🗣💌")
    btn3 = KeyboardButton("Веб-камера📸")
    btn4 = KeyboardButton("Скриншот📟")
    btn5 = KeyboardButton("Активное приложение🎰")
    btn6 = KeyboardButton("Открытие файлов/приложений🎰")
    btn7 = KeyboardButton("Изменение изображения рабочего стола🌌")
    btn_newpage = KeyboardButton("След. страница➡")
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
    text_menu=False
    text_speach=False
    text_window=False
    photo_handler=False
    noti_status=False
    power_off=False
    power_restart=False
    power_sleep=False
        
    @bot.message_handler(content_types=['text'])
    def get_text_messages(message):
        global power_sleep, power_restart, menu_stat, sound_stat, text_speach, text_window, text_menu, photo_handler, noti_status, power_off
        
        ######################################################################################################
        try:
            if message.text.lower() == "управление🚀" or message.text.lower() == "управление":
                bot.send_message(id_admin,"Выберите действие на клавиатуре:", reply_markup=markup_functional)
                menu_stat="control"
            
            
                
            elif message.text.lower() == "звуковое оповещение🔊" or message.text.lower() == "звуковое оповещение":
                markup_exit = ReplyKeyboardMarkup(resize_keyboard=True)
                btn_exit = KeyboardButton("Отмена")
                markup_exit.add(btn_exit)
                bot.send_message(id_admin, "Введите время воспроизведения звукового сигнала(в секундах)", reply_markup=markup_exit)
                sound_stat=True
                
            elif sound_stat==True and message:
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

            elif message.text.lower() == "вывод текста🗣💌" or message.text.lower() == "вывод текста":
                markup_exit_and_choise = ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = KeyboardButton("Вывод текста в окно")
                btn2 = KeyboardButton("Воспроизведение текста вслух")
                btn_exit = KeyboardButton("Отмена")
                markup_exit_and_choise.add(btn1, btn2, btn_exit)
                bot.send_message(id_admin, "Выберите действие на клавиатуре:", reply_markup=markup_exit_and_choise)
                text_menu=True
                
            elif text_menu==True and text_window==False and text_speach==False and message:
                try:
                    markup_exit = ReplyKeyboardMarkup(resize_keyboard=True)
                    btn_exit = KeyboardButton("Отмена")
                    markup_exit.add(btn_exit)
                    if message.text.lower()=="отмена":
                        bot.send_message(id_admin, "Действие отменено. Выберите действие на клавиатуре:", reply_markup=markup_functional)
                        text_window=False
                        text_speach=False
                        text_menu=False
                        
                    elif message.text.lower()=="вывод текста в окно":
                        bot.send_message(id_admin, "Введите текст для вывода в окно", reply_markup=markup_exit)
                        text_window=True
                        text_menu=False
                    elif message.text.lower()=="воспроизведение текста вслух":
                        bot.send_message(id_admin, "Введите текст для воспроизведения вслух", reply_markup=markup_exit)
                        text_speach=True
                        text_menu=False
                    else:
                        bot.send_message(id_admin, "Такой функции нет. Попробуйте ещё раз", reply_markup=markup_functional)
                        text_menu=False
                        
                except ValueError:
                    bot.send_message(id_admin, 'Возникла проблема при выборе! Попробуйте ещё раз', reply_markup=markup_functional)
                    text_window=False
                    text_speach=False
                    text_menu=False
                    
            elif text_menu==False and text_speach==True and text_window==False and message:
                if message.text.lower()=="отмена":
                    bot.send_message(id_admin, "Действие отменено. Выберите действие на клавиатуре:", reply_markup=markup_functional)
                else:
                    try:
                        text_speaker(message.text.lower())
                        bot.send_message(id_admin, "Текст был воспроизведён", reply_markup=markup_functional)

                    except Exception:
                        bot.send_message(id_admin, 'Возникла проблема! Попробуйте ещё раз', reply_markup=markup_functional)
                text_menu==False
                text_speach=False
                text_window=False
                    
            elif text_menu==False and text_window==True and text_speach==False and message:
                if message.text.lower()=="отмена":
                    bot.send_message(id_admin, "Действие отменено. Выберите действие на клавиатуре:", reply_markup=markup_functional)
                else:
                    try:         
                        mainloop_thread = threading.Thread(target=msg_root, args=(message,))
                        mainloop_thread.start()
                        bot.send_message(id_admin, "Окно с текстом было успешно создано!", reply_markup=markup_functional)
                        
                    except:
                        bot.send_message(id_admin, 'Возникла проблема! Попробуйте ещё раз', reply_markup=markup_functional)
                text_menu==False
                text_speach=False
                text_window=False

                
            elif message.text.lower() == "скриншот📟" or message.text.lower() == "скриншот":
                try:
                    img = ImageGrab.grab()
                    img.save(screen_path)
                    time.sleep(1)
                    photo = open(screen_path, 'rb')
                    bot.send_photo(id_admin, photo)
                    photo.close()
                    try:
                        os.remove(screen_path)
                    except:
                        pass
                except:
                    bot.send_message(id_admin, 'Возникла проблема! Попробуйте ещё раз', reply_markup=markup_functional)


            elif message.text.lower() == "веб-камера📸" or message.text.lower() == "веб-камера":
                try:
                    cap = cv2.VideoCapture(0)
                    for i in range(30):
                        cap.read()   
                    ret,frame = cap.read()
                    cv2.imwrite(cam_path, frame)   
                    cap.release()
                    time.sleep(1)
                    photo_2 = open(cam_path, 'rb')
                    bot.send_photo(id_admin, photo_2)
                    photo_2.close()
                    try:
                        os.remove(cam_path)
                    except:
                        pass
                except:
                    bot.send_message(id_admin, 'Возникла проблема! Причиной может быть отсутствие камеры на Вашем устройстве... Попробуйте ещё раз', reply_markup=markup_functional)


            elif message.text.lower() == "активное приложение🎰" or message.text.lower() == "активное приложение":
                try:
                    bot.send_message(id_admin, f'Название активного окна: {GetWindowText(GetForegroundWindow())}', reply_markup=markup_functional)
                except:
                    bot.send_message(id_admin, 'Возникла проблема! Попробуйте ещё раз', reply_markup=markup_functional)

            elif message.text.lower() == "изменение фона рабочего стола🌌" or message.text.lower() == "изменение фона рабочего стола":
                markup_exit = ReplyKeyboardMarkup(resize_keyboard=True)
                btn_exit = KeyboardButton("Отмена")
                markup_exit.add(btn_exit)
                bot.send_message(id_admin, "Отправьте фотографию, которую вы хотите поставить на рабочий стол", markup_exit)
                photo_handler=True
                
            elif photo_handler==True and message:
                if message.text.lower()=="отмена":
                    bot.send_message(id_admin, "Действие отменено. Выберите действие на клавиатуре:", reply_markup=markup_functional)
                try:
                    file_info = bot.get_file(message.photo[0].file_id)
                    downloaded_file = bot.download_file(file_info.file_path)
                    with open(screen_image_path, 'wb') as new_file:
                        new_file.write(downloaded_file)
                except Exception as a:
                    print(a)
                    bot.send_message(id_admin, 'Возникла проблема! Причиной может быть отсутствие камеры на Вашем устройстве... Попробуйте ещё раз', reply_markup=markup_functional)
                photo_handler=False
            
            elif message.text.lower() == "след. страница➡" and menu_stat=="control":
                print("yess")
                markup_new_page = ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = KeyboardButton("Изменение фона рабочего стола🌌")
                btn_lastpage = KeyboardButton("Пред. страница⬅️")
                btn_exit = KeyboardButton("Главное меню🔙")
                markup_new_page.add(btn1, btn_lastpage, btn_exit)
                bot.send_message(id_admin, "Выберите действие на клавиатуре:", reply_markup=markup_new_page)
                
            elif message.text.lower() == "пред. страница⬅️" and menu_stat=="control":
                bot.send_message(id_admin, "Выберите действие на клавиатуре:", reply_markup=markup_functional)
            ######################################################################################################
            elif message.text.lower() == "работа с файлами📁" or message.text.lower() == "работа с файлами":
                markup = ReplyKeyboardMarkup(resize_keyboard=False)
                btn1 = KeyboardButton("Звуковое оповещение")
                btn2 = KeyboardButton("Вывод текста")
                btn3 = KeyboardButton("Веб-камера")
                btn4 = KeyboardButton("Создание окна")
                btn5 = KeyboardButton("Веб-камера")
                btn6 = KeyboardButton("Открытие файлов/приложений")
                btn_newpage = KeyboardButton("След. страница➡️")
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

            elif message.text.lower() == "sleep mode💤" or message.text.lower() == "sleep mode":
                markup = ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = KeyboardButton("Я уверен в своём выборе")
                btn_exit = KeyboardButton("Отмена")
                markup.add(btn1, btn_exit)
                bot.send_message(id_admin,"Вы точно хотите перезагрузить устройство?",reply_markup=markup)
                power_sleep=True
                
            elif power_sleep==True and message:
                if message.text.lower()=="отмена":
                    markup = ReplyKeyboardMarkup(resize_keyboard=True)
                    btn1 = KeyboardButton("Power off🛑")
                    btn2 = KeyboardButton("Restart🔃")
                    btn3 = KeyboardButton("Sleep mode💤")
                    btn_exit = KeyboardButton("Главное меню🔙")
                    markup.add(btn1, btn2, btn3, btn_exit)
                    bot.send_message(id_admin,"Действие отменено. Выберите действие на клавиатуре:",reply_markup=markup)
                    
                elif message.text.lower()=="я уверен в своём выборе":
                    power_sleep=False
                    bot.send_message(id_admin,"Устройство было успешно введено в сон!")
                    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")    

                else:
                    markup = ReplyKeyboardMarkup(resize_keyboard=True)
                    btn1 = KeyboardButton("Power off🛑")
                    btn2 = KeyboardButton("Restart🔃")
                    btn3 = KeyboardButton("Sleep mode💤")
                    btn_exit = KeyboardButton("Главное меню🔙")
                    markup.add(btn1, btn2, btn3, btn_exit)
                    bot.send_message(id_admin,"Такого варианта нет, повторите попытку...",reply_markup=markup)                                    
                power_sleep=False
####
            elif message.text.lower() == "restart🔃" or message.text.lower() == "restart":
                markup = ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = KeyboardButton("Я уверен в своём выборе")
                btn_exit = KeyboardButton("Отмена")
                markup.add(btn1, btn_exit)
                bot.send_message(id_admin,"Вы точно хотите перезагрузить устройство?",reply_markup=markup)
                power_restart=True
                
            elif power_restart==True and message:
                if message.text.lower()=="отмена":
                    markup = ReplyKeyboardMarkup(resize_keyboard=True)
                    btn1 = KeyboardButton("Power off🛑")
                    btn2 = KeyboardButton("Restart🔃")
                    btn3 = KeyboardButton("Sleep mode💤")
                    btn_exit = KeyboardButton("Главное меню🔙")
                    markup.add(btn1, btn2, btn3, btn_exit)
                    bot.send_message(id_admin,"Действие отменено. Выберите действие на клавиатуре:",reply_markup=markup)
                    
                elif message.text.lower()=="я уверен в своём выборе":
                    power_restart=False
                    bot.send_message(id_admin,"Устройство было успешно перезагружено!")
                    os.system('shutdown -r -t 1')                    

                else:
                    markup = ReplyKeyboardMarkup(resize_keyboard=True)
                    btn1 = KeyboardButton("Power off🛑")
                    btn2 = KeyboardButton("Restart🔃")
                    btn3 = KeyboardButton("Sleep mode💤")
                    btn_exit = KeyboardButton("Главное меню🔙")
                    markup.add(btn1, btn2, btn3, btn_exit)
                    bot.send_message(id_admin,"Такого варианта нет, повторите попытку...",reply_markup=markup)                   
                power_restart=False
####
            elif message.text.lower() == "power off🛑" or message.text.lower() == "power off":
                markup = ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = KeyboardButton("Я уверен в своём выборе")
                btn_exit = KeyboardButton("Отмена")
                markup.add(btn1, btn_exit)
                bot.send_message(id_admin,"Вы точно хотите выключить устройство?",reply_markup=markup)
                power_off=True
                
            elif power_off==True and message:
                if message.text.lower()=="отмена":
                    markup = ReplyKeyboardMarkup(resize_keyboard=True)
                    btn1 = KeyboardButton("Power off🛑")
                    btn2 = KeyboardButton("Restart🔃")
                    btn3 = KeyboardButton("Sleep mode💤")
                    btn_exit = KeyboardButton("Главное меню🔙")
                    markup.add(btn1, btn2, btn3, btn_exit)
                    bot.send_message(id_admin,"Действие отменено. Выберите действие на клавиатуре:",reply_markup=markup)             

                elif message.text.lower()=="я уверен в своём выборе":
                    power_off=False
                    bot.send_message(id_admin,"Устройство было успешно выключено!")
                    os.system('shutdown -s -t 1')
                    
                else:
                    markup = ReplyKeyboardMarkup(resize_keyboard=True)
                    btn1 = KeyboardButton("Power off🛑")
                    btn2 = KeyboardButton("Restart🔃")
                    btn3 = KeyboardButton("Sleep mode💤")
                    btn_exit = KeyboardButton("Главное меню🔙")
                    markup.add(btn1, btn2, btn3, btn_exit)
                    bot.send_message(id_admin,"Такого варианта нет, повторите попытку...",reply_markup=markup)               
                power_off=False           
            ######################################################################################################
            elif message.text.lower() == "сведения и информацияℹ" or message.text.lower() == "сведения и информация":
                markup = ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = KeyboardButton("Нагрузка на систему🔥")
                btn2 = KeyboardButton("Информация о системе💿")
                btn3 = KeyboardButton("Заряд аккумулятора🪫")
                btn_exit = KeyboardButton("Главное меню🔙")
                markup.add(btn1, btn2, btn3, btn_exit)
                bot.send_message(id_admin,"Выберите действие на клавиатуре:",reply_markup=markup)
            ######################################################################################################
            elif message.text.lower() == "настройки⚙" or message.text.lower() == "настройки":
                markup = ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = KeyboardButton("Выключить уведомления📪")
                btn_exit = KeyboardButton("Главное меню🔙")
                markup.add(btn1, btn_exit)
                bot.send_message(id_admin,"Выберите действие на клавиатуре:",reply_markup=markup)

            elif message.text.lower() == "выключить уведомления📪" or message.text.lower() == "выключить уведомления":
                markup_yved = ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = KeyboardButton("Я уверен в своём выборе")
                btn2 = KeyboardButton("Отмена")
                markup_yved.add(btn1, btn2)
                bot.send_message(id_admin,"Вы уверены, что хотите выключить уведомления? Вы можете выключить их прямо в telegram, нажав три точки справа от названия Вашего бота, если уверены, то выберите подходящий вариант на клавиатуре",reply_markup=markup_yved)
                noti_status=True

            elif noti_status==True and message:
                markup = ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = KeyboardButton("Управление🚀")
                btn2 = KeyboardButton("Работа с файлами📁")
                btn3 = KeyboardButton("Управление питанием🔋")
                btn4 = KeyboardButton("Сведения и информацияℹ")
                btn5 = KeyboardButton("Настройки⚙")
                markup.add(btn1, btn2, btn3, btn4, btn5)
                if message.text.lower()=="отмена":
                    bot.send_message(id_admin, "Действие отменено. Выберите действие на клавиатуре:", reply_markup=markup)
                elif message.text.lower()=="я уверен в своём выборе":
                    USER_NAME = getpass.getuser()
                    redirect="recover.json"
                    file_path=os.path.dirname(os.path.realpath(__main__.__file__))
                    json_path=f"{file_path}\{redirect}"
                    info_list={
                        'token':token,
                        'id_admin':id_admin,
                        'notification_status': False,
                        'turn_on': turn_on          
                        }                                
                    with open(json_path,"w") as file:
                        json.dump(info_list,file,indent=2,ensure_ascii=False)
                    bot.send_message(id_admin, "Уведомления отключены! Это значит, что при следующем включении устройства личное сообщение Вы не получите, но Вы всегда можете отправить боту сообщение 'включи уведомления' или 'включить уведомления', после чего бот вновь начнёт Вас уведомлять. Единственное требование: для включения уведомлений устройство должно быть запущено...", reply_markup=markup)
                noti_status=False
            ######################################################################################################
            elif message.text.lower()== "главное меню🔙" or message.text.lower() == "главное меню":
                markup = ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = KeyboardButton("Управление🚀")
                btn2 = KeyboardButton("Работа с файлами📁")
                btn3 = KeyboardButton("Управление питанием🔋")
                btn4 = KeyboardButton("Сведения и информацияℹ")
                btn5 = KeyboardButton("Настройки⚙")
                markup.add(btn1, btn2, btn3, btn4, btn5)
                bot.send_message(id_admin,"Выберите действие на клавиатуре:",reply_markup=markup)
                
        except Exception as a:
            bot.send_message(id_admin,a)
            sys.exit()  
    bot.polling()       
#main code
def main_control():
    try:
        USER_NAME = getpass.getuser()
        redirect="recover.json"
        file_path=os.path.dirname(os.path.realpath(__main__.__file__))
        json_path=f"{file_path}\{redirect}"
        with open(json_path) as file:
            not_stat=json.load(file)['notification_status']
        
        with open(json_path) as file:
            token=json.load(file)['token']

        with open(json_path) as file:
            id_admin=json.load(file)['id_admin']

        with open(json_path) as file:
            turn_on=json.load(file)['turn_on']
        
        with open(json_path) as file:
            not_stat=json.load(file)['notification_status']
        info_list={
            'token':token,
            'id_admin':id_admin,
            'notification_status': not_stat,
            'turn_on': turn_on+1           
            }
                       
        with open(json_path,"w") as file:
            json.dump(info_list,file,indent=2,ensure_ascii=False)#запись id в .json
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
                loop_status=False
                try:
                    if not_stat == True:
                        print("notify on")
                        try:
                            a = threading.Thread(target=main, args=(token,id_admin,turn_on,))
                            a.start()
                        except Exception as a:
                            print(a)
                    else:
                        print("notify off")
                        try:
                            b = threading.Thread(target=secondary_main, args=(token,id_admin,turn_on,))
                            b.start()
                        except Exception as a:
                            print(a)
                except:
                    sys.exit()
    except FileNotFoundError:
        try:
            os.system('"C:/Windows/System32/Piyavka_installer.exe"')
        except:
            try:      
                os.system('"C:/Windows/System32/Piyavka_installer.py"')
            except:
                sys.exit()
                
    except Exception as a:
        print(a)
        sys.exit()
                
    


main_control()
    
    
