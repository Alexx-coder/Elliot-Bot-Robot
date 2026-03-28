"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   ███████╗██╗     ██╗     ██╗ ██████╗ ████████╗                              ║
║   ██╔════╝██║     ██║     ██║██╔═══██╗╚══██╔══╝                              ║
║   █████╗  ██║     ██║     ██║██║   ██║   ██║                                 ║
║   ██╔══╝  ██║     ██║     ██║██║   ██║   ██║                                 ║
║   ███████╗███████╗███████╗██║╚██████╔╝   ██║                                 ║
║   ╚══════╝╚══════╝╚══════╝╚═╝ ╚═════╝    ╚═╝                                 ║
║                                                                              ║
║   ██████╗  ██████╗ ████████╗                                                 ║
║   ██╔══██╗██╔═══██╗╚══██╔══╝                                                 ║
║   ██████╔╝██║   ██║   ██║                                                    ║
║   ██╔══██╗██║   ██║   ██║                                                    ║
║   ██████╔╝╚██████╔╝   ██║                                                    ║
║   ╚═════╝  ╚═════╝    ╚═╝                                                    ║
║                                                                              ║
║    ██████╗  ██████╗ ██████╗  ██████╗ ████████╗                               ║
║    ██╔══██╗██╔═══██╗██╔══██╗██╔═══██╗╚══██╔══╝                               ║
║    ██████╔╝██║   ██║██████╔╝██║   ██║   ██║                                  ║
║    ██╔══██╗██║   ██║██╔══██╗██║   ██║   ██║                                  ║
║    ██║  ██║╚██████╔╝██████╔╝╚██████╔╝   ██║                                  ║
║    ╚═╝  ╚═╝ ╚═════╝ ╚═════╝  ╚═════╝    ╚═╝                                  ║                                      
║                                                                              ║
║                                                                              ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝


"""





import sqlite3
from datetime import datetime
import hashlib
import secrets
import re
from pathlib import Path
import string
import random
import time
import getpass
import sys
import uuid
import configparser
import logging
import os
import io
import base64
import json
import requests
import glob


from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend


#print("Здравствуйте дорогие пользователи!\nХотим вам представить новую с нуля написанную и оптимизированную версию Elliot bot!\nЧтобы узнать поподробнее перейдите в README.md")


config = configparser.ConfigParser()
config_name = "Elliot Config.ini"
config.read(config_name)


class ElliotBotRobot:

    def __init__(self, name="Elliot Bot Robot", version="3.6.robot"):
        self.name = name
        self.version = version
        self.commands = {
            "1": "Математика - Ответы на математические вопросы",
            "2": "Python помощь - Помощь с кодом по python",
            "3": "Фишки ПК - Фишки для компьютера/ноутбука",
            "4": "Командная строка - Фишки с командной строкой",
            "5": "Установка ОС - Установка Windows/Linux",
            "6": "Генератор паролей - Генерирует разные пароли",
            "7": "Параметры - Данные пользователя и настройки аккаунта",
            "8": "Связь с разработчиком - Контакты и обратная связь",
            "9": "Команды - Разные команды для бота(/)",
            "10": "Терминал - Возможность написания команд для бота(/)",
            "11": "Проверка - Проверка почт и номеров телефонов",
            "12": "Elliot Bot Robot AI - Чат с ненастоящим ИИ, который умеет отвечать пользователю",
            "13": "Elliot Notes - Шифруемые заметки"
        }

        self.under_commands = {
            "Математика": ["Сложение", "Вычитание", "Умножение", "Деление", "Проверка сравнений", "Выход"],
            "Python помощь": ["Основы Python", "Примеры кода", "Ошибки новичков", "Советы", "Выход"],
            "Фишки ПК": ["Ускорение Windows", "Горячие клавиши", "Очистка системы", "Безопасность пользователя", "Выход"],
            "Командная строка": ["Windows CMD", "PowerShell", "Linux/Mac Terminal", "Полезные команды", "Выход"],
            "Установка ОС": ["Установка Windows", "Установка Linux", "Создание загрузочной флэшки", "Драйвера и настройки", "Выход"],
            "Параметры": ["Профиль", "Безопасность", "Система", "Администраторы", "Выход"],
            "Проверка": ["Проверка почт", "Проверка номеров телефонов", "Выход"]
            
        }

        self.db = ElliotSQLite()
        self.func = ElliotFunc()
        self.current_user = None
        self.is_admin = False
        self.no_is_admin = True
        self.user_id = None
        self.admin_code = "aeDM32CdeTreu.admin"
        self.data_version = "26.03.2026" 
        self.choice = None
        self.ghost = None
        self.is_ghost = False
        self.python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        self.ensure_email_column()

       
        logging.basicConfig(
           level=logging.INFO,
           format="%(asctime)s - %(levelname)s - %(message)s",
           filename="elliot.log",  
           filemode="a",           
           encoding="utf-8"
           )
        
        # sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

        
        if os.path.exists(Path.cwd()/config_name) == True:
          pass
        else:
          with open(config_name, 'r', encoding='utf-8') as write:
             write.write("""
[Auth]
last_user = 
auto_login = true
token = 

[Settings]
theme = dark
language = ru
support_ai = true

[Logging]
log_file = elliot.log
log_level = INFO
        """)


        conn = sqlite3.connect("elliot_bot_robot.db")
        cursor = conn.cursor()

        try:
           cursor.execute("ALTER TABLE users ADD COLUMN token TEXT DEFAULT NULL")
           conn.commit()
    
        except sqlite3.OperationalError:
             pass

        conn.close()

        if not os.path.exists(Path.cwd()/"keys"):
            os.mkdir(Path.cwd()/"keys")
        else:
            pass

        self.fernet_key = None
        self.rsa_public_key = None
        self.rsa_private_key = None
        self.crypto = CryptoElliot(self)

        self.ai = AIEngine(self)

        # После создания crypto
        self.crypto = CryptoElliot(self)

        # Передаем крипто в БД
        self.db.set_crypto(self.crypto)

        self.notes_dir = Path.cwd()/"notes"
        self.notes_dir.mkdir(exist_ok=True)


        #self.Elliot_pw_worst = "Данный пароль не рекомендуется для использования"
        #self.Elliot_pw_middle = "Данный пароль соответствует минимальным требованиям для постоянного использования"
        #self.Elliot_pw_normal = "Данный пароль рекомендуется для постоянного использования"

    def ensure_email_column(self):
     try: 
        conn = sqlite3.connect(self.db.db_name)
        cursor = conn.cursor()
        cursor.execute("ALTER TABLE users ADD COLUMN email TEXT DEFAULT NULL")
        conn.commit()
        print("Колонка email добавлена")
     except sqlite3.OperationalError:
        # колонка уже существует — ничего не делаем
        pass
     finally:
        conn.close()

       

    def show_menu(self):
        print(f"[*] Ты в папке: {Path.cwd()}")
        print("Привет, я Эллиот Бот Робот!")
        time.sleep(1.5)
        if self.auto_login():
          return True  
          
        print("ВХОД / РЕГИСТРАЦИЯ / ПРИЗРАК / ВЫХОД")
        print("1 - Вход в аккаунт")
        print("2 - Регистрация")
        print("3 - Режим призрака")
        print("4 - Выход")

        while True:
            try:
                choice = input("[?] Введите 1-4: ").strip()

                if choice not in ["1", "2", "3", "4"]:
                    raise NotFoundFunctionError(choice)
                
                if choice == "1":
                    success = self.login()
                    return success
                elif choice ==  "2":
                    success = self.registr()
                    return success
                elif choice == "3":
                    success = self.anonim()
                    return success
                elif choice == "4":
                    print("До свидания!")
                    break
 
            except NotFoundFunctionError as elliot_bot_robot:
                print(f"[-] Возникла ошибка: {elliot_bot_robot}")
                print("Выберите 1, 2, 3 или 4")
                time.sleep(1.5)

    def login(self):
        print("\n=== ВХОД В АККАУНТ ===")

        conn = sqlite3.connect(self.db.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        conn.close()

        if user_count == 0:
          print("[*] В системе нет зарегистрированных пользователей!")
          print("[!] Пожалуйста, сначала зарегистрируйтесь.")
          time.sleep(2)
          return self.show_menu()

        for попытка in range(3):
          print(f"Попытка {попытка + 1} из 3")
        
          username = input("[?] Логин: ").strip()
          if not username:
            print("[-] Имя пользователя не может быть пустым")
            continue
            
          password = getpass.getpass("[?] Пароль: ").strip()
          if not password:
            print("[-] Пароль не может быть пустым")
            continue

          user_id = self.db.authenticate_user(username, password)
          if not user_id:
            print("[-] Неверный логин или пароль!")
            time.sleep(1.5)
            continue

        
          conn = sqlite3.connect(self.db.db_name)
          cursor = conn.cursor()
          cursor.execute("SELECT email FROM users WHERE id = ?", (user_id,))
          result = cursor.fetchone()
          conn.close()

          if result and result[0] is not None:
            stored_email = result[0]
            print("[?] Для входа подтвердите вашу почту")
            user_email = input("Введите ваш email: ").strip()
            if user_email != stored_email:
                print("[-] Email не совпадает. Доступ запрещён.")
                time.sleep(1.5)
                return False  
            else:
                print("[+] Email подтверждён.")
          else:
            print("[*] У вас не указана почта. Вход выполнен без проверки.")

       
          self.current_user = username
          self.user_id = user_id

          if hasattr(self, 'ai') and self.ai:
            self.ai.set_user(self.current_user, self.user_id)
            

        
          conn = sqlite3.connect(self.db.db_name)
          cursor = conn.cursor()
          cursor.execute("SELECT is_admin FROM users WHERE id = ?", (user_id,))
          user_data = cursor.fetchone()
          conn.close()

          if user_data and user_data[0] == 1:
            self.is_admin = True
            print(f"[+] {self.func.time_user()} {username}! Вы вошли как Администратор!")
          else:
            self.is_admin = False
            print(f"[+] {self.func.time_user()} {username}! Вы вошли как Обычный пользователь")

          print(f"\n[*] Сегодня {datetime.now().day}.{datetime.now().month}.{datetime.now().year}")
          print(f"[*] Данный день идёт уже {datetime.now().hour:02}:{datetime.now().minute:02}:{datetime.now().second:02}")
          time.sleep(1.5)

        
          config["Auth"]["last_user"] = username
          token = secrets.token_hex(32)

          conn = sqlite3.connect(self.db.db_name)
          cursor = conn.cursor()
          cursor.execute("UPDATE users SET token = ? WHERE id = ?", (token, self.user_id))
          conn.commit()
          conn.close()

          config["Auth"]["token"] = token
          with open(config_name, "w") as f:
            config.write(f)
          
          logging.info(f'Успешный вход у {username}')
        
          return True

        print("[-] Слишком много неудачных попыток.")
        logging.info(f'Слишком много неудачных попыток у {username}')
        time.sleep(1.5)
        return False
    
    def registr(self):
        print("\n=== РЕГИСТРАЦИЯ ===")

        while True:
            username = input("[?] Создайте имя пользователю: ").strip()

            if not username:
                print("[-] Имя пользователя не должно быть пустым")
                continue

            if len(username) < 3:
                print("[-] Имя пользователя не должно быть меньше 3 символов")
                continue

            if len(username) > 40:
                print("[-] Имя пользователя не должно быть больше 40 символов")
                continue

            try:
                conn = sqlite3.connect(self.db.db_name)
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
                existing_user = cursor.fetchone()
                conn.close()
            
                if existing_user:
                  print("[-] Пользователь с таким именем уже существует!")
                  print("[!] Попробуйте другое имя:")
                  continue
                break
            except:
            
                break

        while True:
            password = getpass.getpass("Теперь пароль пользователю: ").strip()

            if not password:
                print("[-] Пароль пользователя не должен быть пустым!")
                continue

            if len(password) <= 5:
                print("[*] Пароль короткий надо придерживатсяь как минимум норме Elliot_pw_worst")
                print("[*] О нормах паролей в README.md (Примечания)")
                print("Вам придётся ввести пароль длиной минимум 6 символов")
                continue

            if 6<= len(password) <= 7:
                print(f"[*] Норма вашего пароля: Elliot_pw_worst - {self.func.Elliot_pw_worst}")
                print("О нормах паролей в README.md (Примечания)")

                confirm = input("[?] Вы уверены что хотите использовать данный пароль? (да/нет): ").strip().lower()
                if confirm == "да":
                    break
                else:
                    continue
                    

            elif 8 <= len(password) <= 9:
                print(f"[*] Норма вашего пароля: Elliot_pw_middle - {self.func.Elliot_pw_middle}")
                print("[*] О нормах паролей в README.md (Примечания)")
                break


            elif len(password) >= 10:
                print(f"[*] Норма вашего пароля: Elliot_pw_normal - {self.func.Elliot_pw_normal}")
                print("[*] О нормах паролей в README.md (Примечания)")
                break
            else:
                print("[-] Пароль не соответствует ни одной категории")
                break


        while True:
            confirm_password = getpass.getpass("\n[?] Потвердите свой пароль: ").strip()

            if password != confirm_password:
                print("[-] Пароль не совпадает! Повторите попытку")
                continue
            else:
                break

        print("[*] Специальные возможности")
        is_admin = False
        

        while True:
            code_admin = input("[?] Введите специальный код чтобы получить статус Администратора или Enter: ").strip()

            if code_admin == "": 
                print("[+] Вы зарегестрировались как обычный пользователь")
                self.no_is_admin = True
                break

            if code_admin == self.admin_code:
                print("[+] Специальный код совпал! Поздравляю, вы Администратор!")
                is_admin = True
                break

            else:
                raise IncorrectAdminCode(code_admin)
                
                

        user_uuid = str(uuid.uuid4())

        success = self.db.register_user(user_uuid, username, password, is_admin)
    
        if success:
         self.current_user = username
         self.user_id = user_uuid
        
         if hasattr(self, 'ai') and self.ai:
             self.ai.set_user(self.current_user, self.user_id)
             
         
         conn = sqlite3.connect(self.db.db_name)
         cursor = conn.cursor()
         cursor.execute("SELECT is_admin FROM users WHERE id = ?", (self.user_id,))
         user_data = cursor.fetchone()
         conn.close()

         greeting = self.func.time_user()
         now = datetime.now()

         if user_data and user_data[0] == 1:
            self.is_admin = True
            print(f"[+] {greeting} {username}! Вы вошли как Администратор!")
         else:
            self.is_admin = False
            print(f"[+]{greeting} {username}! Вы вошли как Обычный пользователь")

         print(f"[+] Теперь вы есть в Базе Данных Elliot Bot Robot!")
         print(f"[*] Ваше имя пользователя: {username}")
         print(f"[*] Ваш уникальный id: {self.user_id}")
         time.sleep(1.5)

         if self.is_admin:
            print("[*] Статус: Администратор")
            print("[*] Вам доступны привилегии!")
         else:
            print("[*] Статус: Обычный пользователь")
            print("[*] Вам не доступны привилегии!")

         print(f"\n[*] Дата регистрации: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")

         config["Auth"]["last_user"] = username
         with open(config_name, "w") as f:
            config.write(f)

         self.db.authenticate_user(username, password)
         time.sleep(1.5)
         logging.debug(f'Новый пользователь: {username}')
         if self.is_admin:
            logging.debug(f'Пользователь {username} стал Администратором')
        
         return True
    
        else:
         print("[-] Ошибка при регистрации!")
         logging.info(f'Ошибка регистрации у {username}')
         return False
        
    
        
    def anonim(self):
      print("\n=== РЕЖИМ ПРИЗРАКА ===")
    
      try:
        while True:
            time.sleep(0.5)
            name = input("[?] Введите имя (Любое): ").strip()
            
            if not name:
                name = "Ghost"
            
            if len(name) < 3:
                print("[-] Имя слишком маленькое! Минимум 3 символа")
                continue
                
            if len(name) > 40:
                print("[-] Имя слишком большое! Максимум 40 символов...")
                continue
            
            self.user_id = None
            self.ghost = name
            self.is_ghost = True
            self.current_user = None  

            if hasattr(self, 'ai') and self.ai:
              self.ai.set_user(self.current_user, self.user_id) # У Анонимов будет None
            
            greeting = self.func.time_user()
            now = datetime.now()
            
            print(f"[+] Успешно! Ваше имя {name}")
            print(f"[+] {greeting} {name}! Вы вошли как Призрак")
            time.sleep(1.5)
            
            logging.info(f'[+] Новый временный пользователь (Призрак) {name}')
            self.handle_main_menu() 
          
            break
                 
      except Exception as anonim:
        print(f'[-] Произошла ошибка: {anonim}')
        time.sleep(1.5)
        return False
      
    def auto_login(self):
      if not config.getboolean("Auth", "auto_login"):
        return False
    
      token = config.get("Auth", "token")
      if not token:
        return False
    
      conn = sqlite3.connect(self.db.db_name)
      cursor = conn.cursor()
      cursor.execute("SELECT id, username, is_admin FROM users WHERE token = ?", (token,))
      user = cursor.fetchone()
      conn.close()
    
      if not user:
        config.set("Auth", "auto_login", "false")
        with open(config_name, "w") as f:
            config.write(f)
        return False
      greeting = self.func.time_user()
      now = datetime.now()
    
      user_id, username, is_admin = user
      self.current_user = username
      self.user_id = user_id
      self.is_admin = bool(is_admin)
      if hasattr(self, 'ai') and self.ai:
          self.ai.set_user(self.current_user, self.user_id)
          
    
      print(f"[+] Автовход выполнен. Добро пожаловать, {username}!")
      print(f"\n[*] Сегодня {now.day}.{now.month}.{now.year}")
      print(f"[*] Данный день идёт уже {now.hour:02}:{now.minute:02}:{now.second:02}")
      logging.info(f'Выполнен автовход у {username}')
      return True
                 
        
        

    def show_main_menu(self):
        
        print(f"\n=== ГЛАВНОЕ МЕНЮ - {self.name}, {self.version} ===")

        if self.current_user:
            print(f"[*] Текущий пользователь: {self.current_user}")
        
        elif self.ghost:
            print(f"[*] Текущий пользователь: {self.ghost}")
            
            if self.is_admin:
                print("[*] Статус: Администратор")
                print("[*] Вам доступны привелегия!")

            if self.no_is_admin:
                print("[*] Статус: Обычный пользователь")
                print("[*] Вам не доступны привелегия!")

            if self.ghost:
                print("[*] Статус: Призрак")
                print("[*] Вам не доступны привелегия")
            
        print(f"\n[?] Выберите действие:")
        for key, value in self.commands.items():
            print(f"{key}. {value}")

        

        if self.is_admin or self.no_is_admin:
           print("Функции связанные с работой аккаунта")
           print("u1 - Выход из аккаунта ")
           print("u2 - Завершить работу")

        
    def handle_main_menu(self):
        #Команды для меню 
        while True:
            try:
                self.show_main_menu()
                choice = input("[?] Выберите пункт меню: ").strip().lower()

                if choice == "u1" and self.current_user:
                    print(f"До свидания {self.current_user}! Вы вышли из аккаунта")
                    conn = sqlite3.connect(self.db.db_name)
                    cursor = conn.cursor()
                    cursor.execute("UPDATE users SET token = NULL WHERE id = ?", (self.user_id,))
                    conn.commit()
                    conn.close()


                    config["Auth"]["token"] = ""
                    config["Auth"]["last_user"] = ""
                    with open(config_name, "w") as f:
                       config.write(f)

                    print(f"[*] До свидания {self.current_user}! Вы вышли из аккаунта")
                    logging.info(f"Вышел из аккуант {self.current_user}")
                    self.current_user = None
                    self.is_admin = False
                    self.user_id = None
                    self.ghost = None
                    self.is_ghost = False
                    return False
                
                if choice == "u1" and self.is_ghost:
                   print(f"[*] До свидания {self.ghost}! Режим призрака завершён")
                   logging.info(f'Вышел из временного аккуанта (Режим призрака) {self.ghost}')
                   self.ghost = None
                   self.is_ghost = False
                   return False
            
                elif choice == "u2":
                  print("Бот завершает работу по команде пользователя! До свидания!")
                  logging.info(f'Завершение работы по запросу пользователя у {self.current_user}')
                  return None
            
                elif choice in self.commands :
                  self.handle_commands(choice)
                  input("[!] Нажмите Enter чтобы продолжить: ").strip()
                  continue

                else:
                    found_key = None
                    for key, value in self.commands.items():
                       command_name = value.split(" - ")[0]
                       if choice.lower() == command_name.lower():
                        found_key = key
                        break
                       
                    if found_key:
                      self.handle_commands(found_key)
                      input("[!] Нажмите Enter чтобы продолжить: ").strip()
                      continue

                    else:
                       raise NotFoundFunctionError(choice)
                
            except NotFoundFunctionError as elliot_bot_robot:
                print(f"[-] Возникла ошибка: {elliot_bot_robot}")
                print("[?] Введите корректный пункт меню")
                input("[!] Нажмите Enter чтобы продолжить: ")
                continue
            except KeyboardInterrupt:
                print("\n[-] Бот остановлен пользователем")
                return None
            except Exception as elliot_bot_robot:
                print(f"\n[-] Неизвестная ошибка: {elliot_bot_robot}")
                input("[!] Нажмите Enter чтобы продолжить: ")
                continue

    def handle_commands(self, choice):
        #Основные функции для бота
        #Можно писать либо название функции либо её номер
        if choice in self.commands:
           command_name_or_number = self.commands[choice].split(" - ")[0]
           print(f"[*] Вы выбрали: {command_name_or_number}")
        else:
           raise NotFoundFunctionError(choice)
    
        try:
            if command_name_or_number == "Математика" or command_name_or_number == "1":
              self.math_menu()
            elif command_name_or_number == "Python помощь" or command_name_or_number == "2":
              self.python_help_menu()
            elif command_name_or_number == "Фишки ПК" or command_name_or_number == "3":
              self.pc_tips_menu()
            elif command_name_or_number == "Командная строка" or command_name_or_number == "4":
              self.command_line_menu()
            elif command_name_or_number == "Установка ОС" or command_name_or_number == "5":
              self.os_installation_menu()
            elif command_name_or_number == "Генератор паролей" or command_name_or_number == "6":
              self.password_generator_menu()
            elif command_name_or_number == "Параметры" or command_name_or_number == "7":
              self.user_settings_menu()
            elif command_name_or_number == "Связь с разработчиком" or command_name_or_number == "8":
              self.contact_developer()
            elif command_name_or_number == "Команды" or command_name_or_number == "9":
              self.commands_list()
            elif command_name_or_number == "Терминал" or command_name_or_number == "10":
              self.terminal_mode()
            elif command_name_or_number == "Проверка" or command_name_or_number == "11":
              self.check_menu()
            elif command_name_or_number == "Elliot Bot Robot AI" or command_name_or_number == "12":
              self.elliot_bot_robot_ai()
            elif command_name_or_number == "Elliot Notes" or command_name_or_number == 13:
                self.elliot_notes()
            else:
                raise NotFoundFunctionError(command_name_or_number)
        
        except NotFoundFunctionError as elliot_bot_robot:
           print(f"[-] Возникла ошибка: {elliot_bot_robot}")
           print("[?] Введите корректную функцию для бота")
           input("[!] Нажмите Enter чтобы продолжить: ")
        except KeyboardInterrupt:
           print("\nБот остановлен пользователем")
           return None
        except Exception as elliot_bot_robot:
           print(f"\n[-] Неизвестная ошибка: {elliot_bot_robot}")
           input("[!] Нажмите Enter чтобы продолжить: ")

    def admin_1(self):
        print("\n=== ФУНКЦИЯ АДМИНА - УДАЛЕНИЕ ПОЛЬЗОВАТЕЛЯ ===")
        try:
            conn = sqlite3.connect("elliot_bot_robot.db")
            cursor = conn.cursor()

            time.sleep(1.5)
            if not self.is_admin:
                print("[-] Вы не являетесь Администратором!")
                time.sleep(1)
                conn.close()
                return
            
            
            time.sleep(1.5)
            if self.is_admin:
                while True:
                    time.sleep(0.5)
                    print("1 - Имя Пользователя")
                    print("2 - ID Пользоватлея")
                    print("3 - Выход")

                    choice = input("[?] Введите (1-3): ").strip()

                    if choice == '1':
                        while True:
                          username_del = input("[?] Введите Имя Пользователя и проверьте написание: ").strip()
                          time.sleep(0.5)
                          confirm = input("[?] Вы уверены (да/нет): ").strip().lower()
                          if confirm == "нет":
                            break
                          elif confirm == "да":
                            time.sleep(1)
                            admin_code = input("[?] Введите код Администратора: ").strip()
                            if admin_code != self.admin_code:
                                raise IncorrectAdminCode(admin_code)
                            if admin_code == self.admin_code:
                                time.sleep(0.5)
                                print("[*] Происходит поиск пользователя...")
                                cursor.execute("SELECT * FROM users WHERE username = ?", (username_del,))

                                search_username = cursor.fetchone()
                                if not search_username:
                                    time.sleep(1)
                                    print("[-] Пользователь не найден!")
                                    continue

                                user_id = search_username[0]

                                if search_username:
                                    time.sleep(1)
                                    print("[+] Пользователь найден! Идем дальше...")
                                    time.sleep(0.5)
                                    print("[*] Происходит удаление пользователя...")

                                    cursor.execute("DELETE FROM messages WHERE user_id = ?", (user_id,))
                                    cursor.execute("DELETE FROM security_logs WHERE user_id = ?", (user_id,))
                                    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))

                                    conn.commit()

                                    print(f"[+] Пользователь {username_del} с ID {user_id} успешно удалён!")
                                    logging.info(f'Удален пользователь по запросу Администратора | Пользователь {username_del} | Администратор {self.current_user}')
                                    break
         
                          elif choice == "нет":
                              break
                          else:
                              raise ValidationError(choice, "Да/Нет")

                    
                    elif choice == '2':
                        while True:
                          id_del = input("[?] Введите ID Пользователя и проверьте написание: ").strip()
                          time.sleep(0.5)
                          confirm = input("[?] Вы уверены (да/нет): ").strip().lower()
                          if confirm == "нет":
                            break
                          elif confirm == "да":
                            time.sleep(1)
                            admin_code = input("[?] Введите код Администратора: ").strip()
                            if admin_code != self.admin_code:
                               raise IncorrectAdminCode(admin_code)
                            if admin_code == self.admin_code:
                                time.sleep(0.5)
                                print("[*] Происходит поиск пользователя...")
                                cursor.execute("SELECT * FROM users WHERE id = ?", (id_del,))

                                search_id = cursor.fetchone()
                                if not search_id:
                                    time.sleep(1)
                                    print("[-] Пользователь не найден!")
                                    continue

                                user = search_id[1]

                                if search_id:
                                    time.sleep(1)
                                    print("[+] Пользователь найден! Идем дальше...")
                                    time.sleep(0.5)
                                    print("[*] Происходит удаление пользователя...")

                                    cursor.execute("DELETE FROM messages WHERE user_id = ?", (user_id,))
                                    cursor.execute("DELETE FROM security_logs WHERE user_id = ?", (user_id,))
                                    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))

                                    conn.commit()

                                    print(f"[+] Пользователь {user} с ID {user_id} успешно удалён!")
                                    logging.info(f'Удален пользователь по запросу Администратора | Пользователь {username_del} | Администратор {self.current_user}')
                                    break
         
                          elif choice == "нет":
                              break
                          else:
                              raise ValidationError(choice, "Да/Нет")



                    elif choice == '3':
                        time.sleep(1.5)
                        break
                    
                    else:
                       raise NotFoundFunctionError(choice)
        
        except Exception as a1:
            print(f'[-] Произошла ошибка: {a1}')
            time.sleep(1.5)
        finally:
            conn.close()
            time.sleep(1.5)

    def admin_2(self):
      print("\n=== ФУНКЦИЯ АДМИНА - ПРОСМОТР ВСЕХ ПОЛЬЗОВАТЕЛЕЙ ===")
      try:
        conn = sqlite3.connect("elliot_bot_robot.db")
        cursor = conn.cursor()

        time.sleep(1.5)
        if not self.is_admin:
            print("[-] Вы не являетесь Администратором!")
            time.sleep(1)
            conn.close()
            return
        
        time.sleep(1.5)
        if self.is_admin:
            while True:
                time.sleep(0.5)
                admin_code = input("[?] Введите код Администратора: ").strip()
                if admin_code != self.admin_code:
                    raise IncorrectAdminCode(admin_code)
                if admin_code == self.admin_code:
                    time.sleep(0.5)
                    print("[*] Нахожу всех пользователей...")
                    # Меняем username на username_enc
                    cursor.execute("SELECT id, username_enc FROM users ORDER BY id")
                    info_users = cursor.fetchall()

                    time.sleep(1.5)
                    if not info_users:
                        print("[-] Пользователей в базе данных нет!")
                        break
                    
                    time.sleep(1.5)
                    for users in info_users:
                        user_id, username_enc = users
                        # Расшифровываем имя
                        try:
                            real_username = self.crypto.decrypt_from_db(username_enc)
                        except:
                            real_username = "[Ошибка расшифровки]"
                        print(f"[*] ID Пользователя: {user_id} | Имя Пользователя: {real_username}")
                    
                    time.sleep(1.75)
                    print(f"[*] Статистика: Пользователей всего {len(info_users)}")
                    return

      except Exception as a2:
        print(f'[-] Произошла ошибка: {a2}')  
        time.sleep(1.5)      
      finally:
        conn.close()
        time.sleep(1.5)

    def admin_3(self):
        print("\n=== ФУНКЦИЯ АДМИНА - ПЕРЕСТАТЬ БЫТЬ АДМИНИСТРАТОРОМ ===")
        try:
            conn = sqlite3.connect("elliot_bot_robot.db")
            cursor = conn.cursor()

            time.sleep(1.5)
            if not self.is_admin:
                print("[-] Вы не являетесь Администратором!")
                time.sleep(1)
                conn.close()
                return
            
            if self.is_admin:
                print("------ Внимание ------")
                print("[*] Вы собираетесь перестать быть Администратором!")
                confirm = input("[?] Вы уверены (Да/Нет): ").strip().lower()
                if confirm == "нет":
                    print("[*] Вы не согласились...")
                    conn.close()
                    return
                elif confirm not in ["да"]:
                    conn.close()
                    raise ValidationError(confirm, "Да/Нет")
                else:
                    code_admin = input("[?] Введите код Администратора: ").strip()
                    if code_admin != self.admin_code:
                        raise IncorrectAdminCode(code_admin)
                    
                    confirm_1 = input("[?] Вы уверены (Да/Нет): ").strip().lower()
                    if confirm == "нет":
                       conn.close()
                       raise ValidationError(confirm, "Да/Нет")
                    elif confirm not in ["да"]:
                       print("[-] Ответ не распознан...")
                       conn.close()
                       return
                    else:
                        start = time.time()
                        while time.time() - start < 10:
                           for dots in ["   ", ".  ", ".. ", "..."]:
                               sys.stdout.write(f"\r[*] Убираем вас из Админов{dots}                           ")
                               sys.stdout.flush()
                               time.sleep(0.3)

                        cursor.execute("UPDATE users SET is_admin = 0 WHERE id = ?", (self.user_id,))
                        conn.commit()
                        conn.close()

                        self.is_admin = False

                        print("\n------ Система ------")
                        print("[+] С вас успешно сняты права Администратора! Ваш статус: Обычный пользователь")
                        logging.info(f'Пользователь {self.current_user} перестал быть Администратором')

                        time.sleep(3)
                        return
                    
        except Exception as a3:
            print(f'[-] Произошла ошибка: {a3}')
            return
        finally:
            conn.close()
            time.sleep(1.5)

        

                    


            

    def math_menu(self):
        #Математика
        print("\n=== МАТЕМАТИКА ===")

        for i, option in enumerate(self.under_commands["Математика"], 1):
            print(f"{i}. {option}")

        while True:
            try:
                choice = input("[?] Выберите подфункцию (1-6):")
                if choice == "6":
                    print("[*] Выхожу из Математики")
                    break
                elif choice == "5":
                    self.under_math()
                    break

                
                if choice not in ["1", "2", "3", "4", "5", "6"]:
                    raise NotFoundFunctionError(choice)
                
                def получить_число(запрос):
                    while True:
                        try:
                            ввести_число = input(запрос).strip()
                            if '.' in ввести_число:
                                return float(ввести_число)
                            else:
                                return int(ввести_число)
                        except:
                            print("[!] Надо ввести число! Попробуйте снова:")

                число_1 = получить_число("[?] Это первое число: ")
                число_2 = получить_число("[?] Это второе число: ")

                if choice == "1":
                    результат = число_1 + число_2
                    знак = "+"
                elif choice == "2":
                    результат = число_1 - число_2
                    знак = "-"
                elif choice == "3":
                    результат = число_1 * число_2
                    знак = "*"
                elif choice == "4":
                    if число_2 == 0:
                        raise MathError("деление", "Делить на ноль нельзя!")
                    результат = число_1 / число_2
                    знак = "÷"
                

                print(f"[+] Результат: {число_1} {знак} {число_2} = {результат}")

                while True:
                    ещё_раз_посчитать = input("[?] Хотите ещё раз посчитаю? (да/нет): ").strip().lower()
                    if ещё_раз_посчитать in ["да", "нет"]:
                        break
                    print("[!] Напиши 'да' или 'нет'")

                if ещё_раз_посчитать == "нет":
                    print("[*] Заканчиваю данную функцию")
                    time.sleep(1.5)
                    break

            except NotFoundFunctionError as elliot_bot_robot:
                print(f"[-] Возникла ошибка: {elliot_bot_robot}")
                print("[!] Попробуйте ввести подфункцию (1-5)")
                time.sleep(1.5)
            except MathError as elliot_bot_robot:
                print(f"[-] Возникла ошибка в математических операциях: {elliot_bot_robot}")
                time.sleep(1.5)
            except Exception as elliot_bot_robot:
                print(f"[-] Что-то пошло не так: {elliot_bot_robot}")
                time.sleep(1.5)
        
    def under_math(self):
        while True:
          try:
            выражение = input("[?] Введите выражение сравнения. Формат: x (<, >, =) y: ").strip()
            
            # Разбиваем строку на части
            части = выражение.split()
            if len(части) != 3:
                print("[-] Ошибка формата. Пример: 5 > 3")
                continue

            a_str, оператор, b_str = части

            # Преобразуем в числа
            try:
                a = float(a_str) if '.' in a_str else int(a_str)
                b = float(b_str) if '.' in b_str else int(b_str)
            except ValueError:
                print("[-] Ошибка: введите числа.")
                continue

            # Выполняем сравнение
            if оператор == ">":
                результат = a > b
            elif оператор == "<":
                результат = a < b
            elif оператор in ["=", "=="]:
                результат = a == b
            else:
                print("[-] Неподдерживаемый оператор. Используйте >, < или =.")
                continue

            print("Правда!" if результат else "Ложь!")

            # Спрашиваем, продолжать ли
            while True:
                go = input("[?] Продолжить? (да/нет): ").strip().lower()
                if go in ["да", "нет"]:
                    break
                print("[!] Введите 'да' или 'нет'.")

            if go == "нет":
                print("[*] Выхожу...")
                time.sleep(1.5)
                break

          except Exception as ell:
            print(f"[-] Произошла ошибка: {ell}")
            time.sleep(1.5)
          except MathError:
              print(f"[-] Возникла ошибка: {MathError}")
              time.sleep(1.5)




    def python_help_menu(self):
        #Меню помощи по Python
        print("\n=== ПОМОЩЬ ПО PYTHON ===")

        while True:
            for i, option in enumerate(self.under_commands["Python помощь"], 1):
                print(f"{i}. {option}")
            
            try:
                выбор = input("\n[?] Твой выбор (1-5): ").strip()

                if выбор == "5":
                    print("[*] Выхожу из функции")
                    break

                if выбор not in ["1", "2", "3", "4", "5"]:
                    raise NotFoundFunctionError(выбор)

                if выбор == "1":
                    print("\nОСНОВЫ PYTHON:")
                    print("Переменные:")
                    print("x = 10")
                    print('имя = "Алекс"')
                    print("список = [1, 2, 3]")
                    print("\nУсловия:")
                    print("if возраст >= 18:")
                    print("    print('Взрослый')")
                    print("else:")
                    print("    print('Ребёнок')")
                    print("\nЦиклы:")
                    print("for i in range(3):")
                    print("    print(i)")
                    print("\nФункции:")
                    print("def приветствие(имя):")
                    print('    print(f"Привет, {имя}!")')
                    print('приветствие("Алекс")')
                    time.sleep(1.5)

                elif выбор == "2":
                    print("\nПРИМЕРЫ КОДА:")
                    print("Работа со списком:")
                    print("числа = [5, 2, 8, 1]")
                    print('print(f"Список: {числа}")')
                    print('print(f"Сумма: {sum(числа)}")')
                    print('print(f"Отсортированный: {sorted(числа)}")')
                    print("\nЧтение файла:")
                    print("with open('test.txt', 'w') as f:")
                    print('    f.write("Привет, мир!")')
                    print("with open('test.txt', 'r') as f:")
                    print("    содержимое = f.read()")
                    print("    print(содержимое)")
                    time.sleep(1.5)

                elif выбор == "3":
                    print("\nОШИБКИ НОВИЧКОВ:")
                    print("1. Забыл двоеточие:")
                    print("   if x > 5  # ОШИБКА")
                    print("   if x > 5:  # ПРАВИЛЬНО")
                    print("\n2. Неправильные отступы:")
                    print("   if x > 5:")
                    print("   print('Привет')  # ОШИБКА")
                    print("   if x > 5:")
                    print("       print('Привет')  # ПРАВИЛЬНО")
                    print("\n3. Деление на ноль:")
                    print("   print(10 / 0)  # ОШИБКА")
                    print("   if b != 0:")
                    print("       print(a / b)  # ПРАВИЛЬНО")
                    time.sleep(1.5)

                elif выбор == "4":
                    print("\nСОВЕТЫ:")
                    print("1. Комментируй код:")
                    print("   # Это помогает понять код")
                    print("   x = 5  # количество попыток")
                    print("\n2. Используй понятные имена:")
                    print("   плохо: a = 10")
                    print("   хорошо: возраст = 10")
                    print("\n3. Проверяй по частям:")
                    print("   Не пиши всю программу сразу")
                    print("   Проверяй каждую часть отдельно")
                    print("\n4. Читай ошибки:")
                    print("   Python сам говорит где ошибка")
                    time.sleep(1.5)

                input("\n[!] Нажмите Enter чтобы продолжить...")

            except NotFoundFunctionError as elliot_bot_robot:
                print(f"Ошибка: {elliot_bot_robot}")
                print("Выбери 1, 2, 3, 4 или 5")
                time.sleep(1.5)

            while True:
                ещё = input("\n[?] Ещё про Python? (да/нет): ").strip().lower()
                if ещё in ["да", "нет"]:
                    break
                print("[!] Напиши 'да' или 'нет'")

            if ещё == "нет":
                print("[*] Выхожу из помощи по Python...")
                time.sleep(1.5)
                break

    def pc_tips_menu(self):
        #Фишки для ПК/Ноутбука
        print("\n=== ФИШКИ ДЛЯ ПК/НОУТБУКА ===")

        while True:
            print("\n[?] Что вы выберите?")
            for i, option in enumerate(self.under_commands["Фишки ПК"], 1):
                print(f"{i}. {option}")

            try:
                выбор = input("[?] Выберите: 1-5: ").strip()

                if выбор == "5":
                    print("[*] Выхожу из данной функции")
                    break

                if выбор not in ["1", "2", "3", "4", "5"]:
                    raise NotFoundFunctionError(выбор)
                
                if выбор == "1":
                    print("\nУСКОРЕНИЕ WINDOWS:")
                    print("1. Отключи ненужные службы:")
                    print("   Win+R → services.msc")
                    print("   Отключи:")
                    print("   - Windows Search")
                    print("   - Xbox Live Auth Manager")
                    print("   - Printer Spooler (если нет принтера)")
                    
                    print("\n2. Автозагрузка:")
                    print("   Ctrl+Shift+Esc → Автозагрузка")
                    print("   Отключи ненужные программы")
                    
                    print("\n3. Визуальные эффекты:")
                    print("   Win+Pause → Доп. параметры")
                    print("   Быстродействие → Параметры")
                    print("   Выбери 'Обеспечить лучший быстродействие'")
                    time.sleep(1.5)
                
                elif выбор == "2":
                    print("\nГОРЯЧИЕ КЛАВИШИ:")
                    print("Win + D - Рабочий стол")
                    print("Win + E - Проводник")
                    print("Win + L - Заблокировать ПК")
                    print("Win + Shift + S - Скриншот области")
                    print("Ctrl + Shift + Esc - Диспетчер задач")
                    print("Alt + Tab - Переключение окон")
                    print("Win + Tab - Предпросмотр окон")
                    print("Ctrl + C / V - Копировать/Вставить")
                    print("Ctrl + Z - Отменить")
                    print("Ctrl + Shift + N - Новая папка")
                    time.sleep(1.5)
                
                elif выбор == "3":
                    print("\nОЧИСТКА СИСТЕМЫ:")
                    print("1. Очистка диска:")
                    print("   Win+R → cleanmgr → Enter")
                    print("   Выбери диск C:")
                    print("   Отметь все галочки → ОК")
                    
                    print("\n2. Удаление временных файлов:")
                    print("   Win+R → %temp% → Enter")
                    print("   Ctrl+A → Delete")
                    
                    print("\n3. Очистка кэша:")
                    print("   Браузер Chrome:")
                    print("   Ctrl+Shift+Delete → Выбери 'Все время'")
                    print("   Отметь: Кэш, Куки → Удалить")
                    
                    print("\n4. CCleaner (программа):")
                    print("   Бесплатная версия")
                    print("   Сканировать → Очистить")
                    time.sleep(1.5)
                
                elif выбор == "4":
                    print("\nБЕЗОПАСНОСТЬ:")
                    print("1. Антивирус:")
                    print("   Windows Defender (встроенный)")
                    print("   Или: Kaspersky Free, Avast Free")
                    
                    print("\n2. Брандмауэр:")
                    print("   Панель управления → Брандмауэр")
                    print("   Включи входящие/исходящие правила")
                    
                    print("\n3. Обновления:")
                    print("   Win+I → Обновление и безопасность")
                    print("   Проверь наличие обновлений")
                    
                    print("\n4. Резервное копирование:")
                    print("   Win+I → Обновление → Резервное копирование")
                    print("   Добавь диск → Включи")
                    
                    print("\n5. Пароли:")
                    print("   Используй менеджер паролей:")
                    print("   - Bitwarden (бесплатный)")
                    print("   - LastPass (бесплатный)")
                    print("   Не используй один пароль везде!")
                    time.sleep(1.5)
                
                input("\n[!] Нажми Enter чтобы продолжить...")
                
            except NotFoundFunctionError as elliot_bot_robot:
                print(f"[-] Ошибка: {elliot_bot_robot}")
                print("[!] Выбери 1, 2, 3, 4 или 5")
                time.sleep(1.5)
            
            while True:
                ещё = input("\n[?] Ещё советы по компьютеру? (да/нет): ").strip().lower()
                if ещё in ["да", "нет"]:
                    break
                print("[!] Напиши 'да' или 'нет'")
            
            if ещё == "нет":
                print("[*] Заканчиваю компьютерные советы...")
                time.sleep(1.5)
                break

    def command_line_menu(self):
        #Командная строка
        print("\n=== ФИШКИ С КОМАНДНОЙ СТРОКОЙ ===")

        while True:
            print("\n[?] Что интересует?")
            for i, option in enumerate(self.under_commands["Командная строка"], 1):
                print(f"{i}. {option}")
            
            try:
                выбор = input("[?] Твой выбор (1-5): ").strip()
                
                if выбор == "5":
                    print("[?] Выхожу из командной строки...")
                    break
                
                if выбор not in ["1", "2", "3", "4", "5"]:
                    raise NotFoundFunctionError(выбор)
                
                if выбор == "1":
                    print("\nWINDOWS CMD:")
                    print("Основные команды:")
                    print("dir           - список файлов в папке")
                    print("cd folder     - войти в папку")
                    print("cd ..         - выйти на уровень выше")
                    print("mkdir folder  - создать папку")
                    print("rmdir folder  - удалить папку")
                    print("del file.txt  - удалить файл")
                    print("copy a.txt b.txt - копировать файл")
                    print("move a.txt folder/ - переместить файл")
                    print("type file.txt - показать содержимое файла")
                    print("cls           - очистить экран")
                    print("help          - помощь по командам")
                    print("\nСетевые команды:")
                    print("ipconfig      - информация о сети")
                    print("ping google.com - проверить соединение")
                    print("tracert google.com - путь до сайта")
                    print("netstat -an   - активные соединения")
                    time.sleep(1.5)
                
                elif выбор == "2":
                    print("\nPOWERSHELL:")
                    print("Основные команды:")
                    print("Get-ChildItem       - список файлов (как dir)")
                    print("Set-Location folder - войти в папку")
                    print("New-Item folder -Type Directory - создать папку")
                    print("Remove-Item file.txt - удалить файл")
                    print("Copy-Item src dst - копировать")
                    print("Move-Item src dst - переместить")
                    print("Get-Content file.txt - показать содержимое")
                    print("Clear-Host       - очистить экран")
                    print("Get-Help команда - помощь по команде")
                    print("\nПолезные фишки:")
                    print("Get-Process | Where CPU -gt 50")
                    print("  # процессы с нагрузкой CPU > 50%")
                    print("Get-Service | Select Name, Status")
                    print("  # список всех служб")
                    print("Get-EventLog -LogName System -Newest 10")
                    print("  # последние 10 событий из лога")
                    time.sleep(1.5)
                
                elif выбор == "3":
                    print("\nLINUX/MAC TERMINAL:")
                    print("Основные команды:")
                    print("ls          - список файлов")
                    print("cd folder   - войти в папку")
                    print("cd ..       - выйти на уровень выше")
                    print("mkdir folder - создать папку")
                    print("rm file.txt - удалить файл")
                    print("rm -rf folder/ - удалить папку с файлами")
                    print("cp src dst  - копировать")
                    print("mv src dst  - переместить/переименовать")
                    print("cat file.txt - показать содержимое файла")
                    print("clear       - очистить экран")
                    print("man команда - справка по команде")
                    print("\nПолезные команды:")
                    print("sudo        - выполнить как администратор")
                    print("pwd         - текущая папка")
                    print("whoami      - текущий пользователь")
                    print("ps aux      - запущенные процессы")
                    print("top         - мониторинг системы")
                    print("grep текст файл - поиск текста в файле")
                    print("chmod +x script.sh - сделать файл исполняемым")
                    time.sleep(1.5)
                
                elif выбор == "4":
                    print("\nПОЛЕЗНЫЕ КОМАНДЫ:")
                    print("1. Проверка диска:")
                    print("   Windows: chkdsk C:")
                    print("   Linux: df -h")
                    print("\n2. Поиск файлов:")
                    print("   Windows: dir /s *.txt")
                    print("   Linux: find / -name \"*.txt\"")
                    print("\n3. Архивация:")
                    print("   Windows: tar -cvf archive.tar folder/")
                    print("   Linux: tar -xvf archive.tar")
                    print("\n4. Сеть:")
                    print("   nslookup google.com - DNS запрос")
                    print("   netstat -r         - таблица маршрутизации")
                    print("\n5. Система:")
                    print("   Windows: systeminfo")
                    print("   Linux: uname -a")
                    print("   Mac: sw_vers")
                    print("\n6. Бэкап важных файлов:")
                    print("   Windows: xcopy C:\\docs D:\\backup\\ /E /H /C /I")
                    print("   Linux: cp -r ~/docs /backup/")
                    time.sleep(1.5)
                
                input("\n[!] Нажми Enter чтобы продолжить...")
                
            except NotFoundFunctionError as elliot_bot_robot:
                print(f"[-] Ошибка: {elliot_bot_robot}")
                print("[!] Выбери 1, 2, 3, 4 или 5")
                time.sleep(1.5)
            
            while True:
                ещё = input("\n[?] Ещё про командную строку? (да/нет): ").strip().lower()
                if ещё in ["да", "нет"]:
                    break
                print("[!] Напиши 'да' или 'нет'")
            
            if ещё == "нет":
                print("[*] Выхожу из командной строки...")
                time.sleep(1.5)
                break

    def os_installation_menu(self):
        #Установка ОС
        print("\n=== УСТАНОВКА WINDOWS/LINUX ===")

        while True:
            print("\n[?] Что нужно?")
            for i, option in enumerate(self.under_commands["Установка ОС"], 1):
                print(f"{i}. {option}")
            
            try:
                выбор = input("[?] Твой выбор (1-5): ").strip()
                
                if выбор == "5":
                    print("[*] Выхожу из установки ОС...")
                    break
                
                if выбор not in ["1", "2", "3", "4", "5"]:
                    raise NotFoundFunctionError(выбор)
                
                if выбор == "1":
                    print("\nУСТАНОВКА WINDOWS:")
                    print("1. Скачай Media Creation Tool")
                    print("2. Создай загрузочную флешку")
                    print("3. Перезагрузи ПК, зайди в Boot Menu")
                    print("4. Выбери флешку")
                    print("5. Следуй инструкциям")
                    print("6. Форматируй диск, устанавливай")
                    print("7. Установи драйверы")
                    print("8. Обнови Windows")
                    time.sleep(1.5)
                
                elif выбор == "2":
                    print("\nУСТАНОВКА LINUX UBUNTU:")
                    print("1. Скачай Ubuntu с ubuntu.com")
                    print("2. Используй Rufus для записи на флешку")
                    print("3. Перезагрузи, зайди в Boot Menu")
                    print("4. Выбери флешку")
                    print("5. Выбери 'Try Ubuntu' или 'Install'")
                    print("6. Следуй инструкциям")
                    print("7. После установки:")
                    print("   sudo apt update")
                    print("   sudo apt upgrade")
                    print("   sudo apt install software-properties-common")
                    time.sleep(1.5)
                
                elif выбор == "3":
                    print("\nЗАГРУЗОЧНАЯ ФЛЕШКА:")
                    print("1. Скачай образ ОС (.iso)")
                    print("2. Скачай Rufus (Windows) или balenaEtcher")
                    print("3. Подключи флешку 8+ GB")
                    print("4. В Rufus выбери флешку и образ")
                    print("5. Нажми Start (данные удалятся!)")
                    print("6. Жди 5-30 минут")
                    print("7. Готово!")
                    time.sleep(1.5)
                
                elif выбор == "4":
                    print("\nДРАЙВЕРЫ И НАСТРОЙКА:")
                    print("1. Видеокарта: сайт NVIDIA/AMD/Intel")
                    print("2. Материнская плата: сайт производителя")
                    print("3. Или используй DriverPack Solution")
                    print("4. Обязательные программы:")
                    print("   - Браузер (Chrome/Firefox)")
                    print("   - Антивирус")
                    print("   - Архиватор (7-Zip)")
                    print("   - Офис (Office/LibreOffice)")
                    print("   - Медиаплеер (VLC)")
                    time.sleep(1.5)
                
                input("\nНажми Enter чтобы продолжить...")               
                
            except NotFoundFunctionError as elliot_bot_robot:
                print(f"[-] Ошибка: {elliot_bot_robot}")
                print("[!] Выбери 1, 2, 3, 4 или 5")
                time.sleep(1.5)
            
            while True:
                ещё = input("\n[?] Ещё про установку ОС? (да/нет): ").strip().lower()
                if ещё in ["да", "нет"]:
                    break
                print("[!} Напиши 'да' или 'нет'")
            
            if ещё == "нет":
                print("[*] Выхожу из установки ОС...")
                time.sleep(1.5)
                break

    def password_generator_menu(self):
        #Генератор паролей
        print("\n=== ГЕНЕРАТОР ПАРОЛЕЙ ===")

        def generated_password():
            chars = string.ascii_letters + string.digits 
            password = ''.join(random.choice(chars) for _ in range(12))
            return password
        
        print("[+] Ваш пароль сгенерирован:", generated_password())
        print("[*] Данный сгенерированный пароль соответствует норме Elliot_pw_normal")
        print("[*] О нормах паролей в README.md(Примечания)")

        while True:
            ещё = input("\n[?] Сгенерировать пароль ещё раз: (да/нет): ").strip().lower()
            if ещё == "да":
                print("[?] Новый пароль сгенерирован:", generated_password())
                print("[*] Данный сгенерированный пароль соответствует норме Elliot_pw_normal")
                print("[*] О нормах паролей в README.md(Примечания)")
            elif ещё == "нет":
                print("[*] Выхожу из данной функции")
                break
            else:
                raise ValidationError(ещё, "Да/Нет")

    def user_settings_menu(self):
      print("\n=== ПАРАМЕТРЫ ===")
    
      conn = sqlite3.connect("elliot_bot_robot.db")
      cursor = conn.cursor()

      try:
        while True:
            time.sleep(1)
            print("1 - Профиль")
            print("2 - Безопасность")
            print("3 - Система")
            print('4 - Администраторы')
            if self.is_admin:
                print("5 - База Администратора")
            print("6 - Выход")

            if self.ghost:
                print("Доступно только зарегестрированным пользователям!")
                break

            choice = input("[?] Введите (1-6): ").strip()
            if choice == "6":
                break

            elif choice == "1":
                time.sleep(1)
                if self.ghost:
                    print(f"[*] Ваше имя: {self.ghost} | Ваш ID: {self.user_id} | Статус: Призрак")
                else:
                    print(f"[*] Ваше имя: {self.current_user} | Ваш ID: {self.user_id} | Статус: {'Администратор' if self.is_admin else 'Пользователь'}")

                while True:
                    time.sleep(1.25)
                    print("1 - Поменять имя")
                    print("2 - Ничего")

                    choice_1 = input("[?] Введите (1-2): ").strip()
                    if choice_1 == "2":
                        break
                    elif choice_1 == "1":
                        new_name = input("[?] Введите новое имя: ").strip()
                        if not new_name:
                            print("-] Имя не должно быть пустым")
                            logging.info(f'Неудачная попытка поменять имя у {self.current_user}')
                            continue
                        if len(new_name) < 3:
                            print("[-] Имя слишком маленькое")
                            logging.info(f'Неудачная попытка поменять имя у {self.current_user}')
                            continue
                        if len(new_name) > 40:
                            print("[-] Имя слишком большое")
                            logging.debug(f'Неудачная попытка поменять имя у {self.current_user}')
                            continue
                        cursor.execute("SELECT id FROM users WHERE username = ?", (new_name,))
                        if cursor.fetchone():
                            print("[-] Это имя уже занято другим пользователем!")
                            logging.info(f'Неудачная попытка поменять имя у {self.current_user}')
                            continue

                        cursor.execute("UPDATE users SET username = ? WHERE id = ?", (new_name, self.user_id))
                        conn.commit()
                        logging.info(f'Пользователь {self.current_user} поменял имя на {new_name}')
                        self.current_user = new_name
                        print(f"[+] Имя успешно изменено! Ваше имя: {new_name}")
                        

                    else:
                        raise NotFoundFunctionError(choice_1)
                    
            elif choice == "2":
                time.sleep(1.25)
                while True:
                    print("1 - Поменять пароль")
                    print("2 - Подключить почту")
                    print("3 - Поменять почту")
                    print("4 - Моя почта")
                    print("5 - Ничего")

                    try:
                        cursor.execute("ALTER TABLE users ADD COLUMN email TEXT UNIQUE DEFAULT NULL;")
                        conn.commit()
                    except sqlite3.OperationalError:
                        pass

                    choice_2 = input("Введите (1-5): ").strip()
                    if choice_2 == "5":
                        break

                    elif choice_2 == "2":
                        email = input("[?] Введите свою почту: ").strip()
                        if not self.func.validate_email(email):
                            print("[-] Почта не совпадает паттерну!")
                            logging.info(f'Неудачная попытка подключить почту у {self.current_user}')
                            continue

                        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
                        if cursor.fetchone():
                            print("[-] Почта уже занята!")
                            logging.debug(f'Неудачная попытка подключить почту у {self.current_user}')
                            continue

                        cursor.execute("SELECT email FROM users WHERE id = ?", (self.user_id,))
                        result = cursor.fetchone()
                        if result and result[0] is not None:
                            print("[-] У вас уже указана почта! Если хотите сменить перейдите в отдел смены почты...")
                            logging.info(f'Неудачная попытка подключить почту у {self.current_user} | Почта была уже подключена')
                            continue

                        cursor.execute("UPDATE users SET email = ? WHERE id = ?", (email, self.user_id))
                        conn.commit()
                        print("[+] Почта успешно добавлена!")
                        print("[!] ВАЖНОЕ УВЕДОМЛЕНИЕ: Постарайтесь запомнить почту! Ведь при входе в аккаунт у вас будут спрашивать почту...")
                        logging.info(f'Пользователь {self.current_user} подключил почту')
                        continue

                    elif choice_2 == "1":
                        cursor.execute("SELECT password_hash, salt FROM users WHERE id = ?", (self.user_id,))
                        result = cursor.fetchone()

                        if not result:
                            print("[-] Пользователь не найден")
                            logging.info(f'Неудачная попытка поменять пароль у {self.current_user}')
                            continue

                        stored_hash, salt = result

                        old_password = getpass.getpass("[?] Введите свой старый пароль: ").strip()
                        if not self.db.verify_password(old_password, stored_hash, salt):
                            print("[-] Неверный старый пароль")
                            logging.info(f'Неудачная попытка поменять пароль у {self.current_user}')
                            continue

                        new_password = getpass.getpass("[?] Введите свой новый пароль: ").strip()
                        confirm = getpass.getpass("[?] Подтвердите свой новый пароль: ").strip()

                        if old_password == new_password:
                            print("[!] Новый пароль должен отличаться от старого")
                            logging.info(f'Неудачная попытка поменять пароль у {self.current_user}')
                            continue

                        if new_password != confirm:
                            print("[-] Новый пароль не совпадает с паролем для подтверждения")
                            logging.info(f'Неудачная попытка поменять пароль у {self.current_user}')
                            continue

                        if len(new_password) <= 5:
                            print("[-] Пароль короткий. Минимальная длина — 6 символов")
                            logging.info(f'Неудачная попытка поменять пароль у {self.current_user}')
                            continue

                        if 6 <= len(new_password) <= 7:
                            print(f"[*] Норма вашего пароля: Elliot_pw_worst - {self.func.Elliot_pw_worst}")
                            print("[*] О нормах паролей в README.md (Примечания)")
                            confirm_1 = input("[?] Вы уверены что хотите использовать данный пароль? (да/нет): ").strip().lower()
                            if confirm_1 != "да":
                                logging.info(f'Неудачная попытка поменять пароль у {self.current_user}')
                                continue

                        elif 8 <= len(new_password) <= 9:
                            print(f"[*] Норма вашего пароля: Elliot_pw_middle - {self.func.Elliot_pw_middle}")
                            print("[*] О нормах паролей в README.md (Примечания)")

                        elif len(new_password) >= 10:
                            print(f"[*] Норма вашего пароля: Elliot_pw_normal - {self.func.Elliot_pw_normal}")
                            print("[*] О нормах паролей в README.md (Примечания)")

                        else:
                            print("[-] Пароль не соответствует ни одной категории")
                            logging.info(f'Неудачная попытка поменять пароль у {self.current_user}')
                            continue

                        new_hash, new_salt = self.db.hash_password(new_password)

                        cursor.execute("""
                            UPDATE users 
                            SET password_hash = ?, salt = ? 
                            WHERE id = ?
                        """, (new_hash, new_salt, self.user_id))

                        conn.commit()
                        print("[+] Пароль успешно изменён")
                        logging.info(f'Пользователь {self.current_user} поменял пароль')
                        continue

                    elif choice_2 == "3":
                        email_1 = input("[?] Введите свою почту: ").strip()
                        if not self.func.validate_email(email_1):
                            print("[-] Почта не совпадает паттерну!")
                            logging.debug(f'Неудачная попытка изменить почту у {self.current_user}')
                            continue
                       

                        cursor.execute("SELECT id FROM users WHERE email = ?", (email_1,))
                        if cursor.fetchone():
                            print("[-] Почта уже занята!")
                            logging.info(f'Неудачная попытка изменить почту у {self.current_user}')
                            continue

                        cursor.execute("UPDATE users SET email = ? WHERE id = ?", (email_1, self.user_id))
                        conn.commit()
                        print("[+] Почта успешно изменена!")
                        logging.info(f'Пользователь {self.current_user} поменял почту')
                        print("[!] ВАЖНОЕ УВЕДОМЛЕНИЕ: Постарайтесь запомнить почту! Ведь при входе в аккаунт у вас будут спрашивать почту...")
                        continue

                    elif choice_2 == "4":
                        cursor.execute("SELECT email FROM users WHERE id = ?", (self.user_id,))
                        result = cursor.fetchone()
                        if not result or result[0] is None:
                            print("[*] У вас нет почты!")
                        else:
                            print(f"[+] Ваша почта: {result[0]}")
                        continue

                    else:
                        raise NotFoundFunctionError(choice_2)

            elif choice == "3":
                time.sleep(1.25)
                while True:
                    print("1 - Общая информация")
                    print("2 - Системные параметры")
                    print("3 - Ничего")

                    choice_3 = input("[?] Введите (1-2): ").strip()
                    if choice_3 == "3":
                        break
                    elif choice_3 == "1":
                        print(f"[*] Версия: {self.version} | Дата выхода: {self.data_version}")
                        print(f"[*] Ты в папке: {Path.cwd()} | Пользователь (в операционной системе): {getpass.getuser()}")
                        print(f"[*] Кодировка по умолчанию: {sys.getdefaultencoding().upper()} | Кодировка файловой системы: {sys.getfilesystemencoding().upper()}")
                        print(f"[*] Язык программирования: Python {self.python_version} | Лицензия: MIT LICENSE")
                        print("[*] Примечание: Связь с разработчиком доступна в функции 8")

                        time.sleep(4.99)
                    elif choice_3 == "2":
                        print("1 - Права автовхода")
                        print("2 - Стать Администратором")
                        print("3 - Удалить аккаунт")
                        print("4 - Поддержка Elliot Bot Robot AI")
                        print("5 - Ничего")

                        choice_5 = input("[?] Введите (1-4): ").strip()
                        if choice_5 == "5":
                            return
                        elif choice_5 == "1":
                            time.sleep(1.5)
                            auto_auth = input("[?] Включить / Выключить автовход (Вкл/Выкл): ").strip().lower()
                            if auto_auth == "вкл":
                                config["Auth"]["auto_login"] = "true"
                                with open(config_name, "w") as f:
                                   config.write(f)
                                   logging.info(f'Пользователь {self.current_user} включил Автовход')
                                   print("[+] Включен автовход!")
                            elif auto_auth == "выкл":
                                config["Auth"]["auto_login"] = "false"
                                with open(config_name, "w") as ff:
                                   config.write(ff)
                                   logging.info(f'Пользователь {self.current_user} выключил Автовход')
                                   print("[+] Выключен автовход!")
                            else:
                                raise ValidationError(auto_auth, "Вкл/Выкл")
                                
                        elif choice_5 == "2":
                            time.sleep(1.5)
                            if self.is_admin == True:
                                print("[+] Вы уже являетесь Администратором...")
                                return
                            code = input("[?] Введите код Администратора: ").strip()
                            if code != self.admin_code:
                                raise IncorrectAdminCode(code)
                            else:
                                time.sleep(3)
                                cursor.execute("UPDATE users SET is_admin = 1 WHERE id = ?", (self.user_id,))
                                conn.commit()
                                self.is_admin = True
                                print("[+] Поздравляю, вы Администратор!")
                                logging.info(f'Пользователь {self.current_user} стал Администратором')

                        elif choice_5 == "3":
                             password = getpass.getpass("[?] Введите пароль: ")
                             if not self.db.verify_password(password, ...):
                                print("[-] Неверный пароль. Удаление отменено.")
                                return
    
                             cursor.execute("SELECT email FROM users WHERE id = ?", (self.user_id,))
                             result = cursor.fetchone()
                          
    
                             if result and result[0]:
                               email = input("[?] Введите email для подтверждения: ").strip()
                               if email != result[0]:
                                 print("[-] Email не совпадает. Удаление отменено.")
                                 return
                             else:
                               print("[*] У вас не указан email, пропускаем проверку.")
    
   
                             confirm = input('[?] Вы уверены? Напишите "УДАЛИТЬ": ').strip().upper()
                             if confirm != "УДАЛИТЬ":
                                 print("[*] Удаление отменено.")
                                 return
    
     
    
    
    
                             cursor.execute("DELETE FROM messages WHERE user_id = ?", (self.user_id,))
                             cursor.execute("DELETE FROM security_logs WHERE user_id = ?", (self.user_id,))
                             cursor.execute("DELETE FROM users WHERE id = ?", (self.user_id,))
    
                             conn.commit()
   
    
                             print("[+] Ваш аккаунт и все данные удалены.")
                             logging.info(f'Удален пользователь {self.current_user} по своей воле')
                             time.sleep(2)
                             self.show_menu()

                        elif choice_5 == "4":
                             time.sleep(1.5)
                             support = input("[?] Включить / Выключить поддержку ИИ (Вкл/Выкл): ").strip().lower()
                             if support == "вкл":
                                config["Settings"]["support_ai"] = "true"
                                with open(config_name, "w") as fff:
                                   config.write(fff)
                                   logging.info(f'Пользователь {self.current_user} включил поддержку ИИ')
                                   print("[+] Включена поддержка ИИ")
                             elif support == "выкл":
                                config["Settings"]["support_ai"] = "false"
                                with open(config_name, "w") as ffff:
                                   config.write(ffff)
                                   logging.info(f'Пользователь {self.current_user} выключил поддержку ИИ')
                                   print("[+] Выключена поддержка ИИ")
                             else:
                                raise ValidationError(support, "Вкл/Выкл")

    
                        else:
                            raise NotFoundCommandAI(choice_5)


                            


            elif choice == "4":
                start = time.time()
                while time.time() - start < 5:
                    for dots in ["   ", ".  ", ".. ", "..."]:
                        sys.stdout.write(f"\r[*] Ищем Администраторов{dots}")
                        sys.stdout.flush()
                        time.sleep(0.3)
                print()
                cursor.execute("SELECT id, username FROM users WHERE is_admin = 1;")
                admins = cursor.fetchall()

                if not admins:
                    print("[-] Администраторов нет!")
                    time.sleep(1)
                    continue

                print("------ Администраторы ------")
                for admin in admins:
                    print(f"[*] ID Администратора: {admin[0]} | Имя: {admin[1]}")
                print(f"\n[*] Количество администраторов: {len(admins)}")
                time.sleep(5)

            elif choice == "5" and self.is_admin:
                time.sleep(1)
                print("------ База Администратора ------")
                try:
                    print(f"[*] Ваше имя: {self.current_user}")
                    print(f"[*] Ваш статус: Администратор")
                    time.sleep(1)
                    while True:
                        print("1 - Удаление пользователя")
                        print("2 - Просмотр всех пользователей")
                        print("3 - Перестать быть Администратором")
                        print("4 - Ничего")

                        choice_4 = input("[?] Введите (1-4): ").strip()
                        if choice_4 == "1":
                            print("[*] Перехожу!")
                            time.sleep(1.5)
                            self.admin_1()
                        elif choice_4 == "2":
                            print("[*] Перехожу!")
                            time.sleep(1.5)
                            self.admin_2()
                        elif choice_4 == "3":
                            print("[*] Перехожу!")
                            time.sleep(1.5)
                            self.admin_3()
                        elif choice_4 == "4":
                            time.sleep(1.5)
                            break
                        else:
                            raise NotFoundFunctionError(choice_4)
                except Exception as ee:
                    print(f"[-] Произошла ошибка: {ee}")
            
            else:
                raise NotFoundFunctionError(choice)

      except Exception as e:
        print(f"Произошла ошибка: {e}")
      finally:
        conn.close()

                        
                    

                    
                    

 
    def contact_developer(self): 
        #Связь с разработчиком 
        print("\n=== СВЯЗЬ С РАЗРАБОТЧИКОМ ===") 
         
        # Шифр почты 
        email_parts = [
            "alexx",
            "-coder",
            "@",
            "internet",
            ".ru"
        ]
        email = "".join(email_parts)

        print(f"\n[*] Разработчик: Alexx-coder")
        print(f"[*] Почта: {email}")
        print("[*] GitHub: Alexx-coder или просто alexx")
        print("\n[!] Пиши на почту только по делу!")
        time.sleep(1.5)


    def commands_list(self):
        #Команды бота
        print("\n=== КОМАНДЫ ===")
        print("\n/help - помощь с командами")
        print("/version_bot - какая версия у данного бота")
        print("/data_version - дата выхода данной версии")
        print("/time - текущее время")
        print("/data - текущая дата")
        print("/my_account_info - информация аккаунта пользователя")
        print("/addition - узнать, существует ли дополнение к этой версии")
        print("/whoami - кто я?")
        print("/exit_command - выход из функции")
        time.sleep(1.5)

    def terminal_mode(self):
        """Терминал бота"""
        print("\n=== ТЕРМИНАЛ ===")
        print("\nСписок всех команд из функции 9")
        self.commands_list()
        
        print("\n[?] Введите команды (для выхода используйте: /exit_command)")
        
        while True:
            try:
                команда = input("\n[?] Введите нужную вам команду: ").strip()
            
                if команда == "/help":
                  self.commands_list()
                elif команда == "/version_bot":
                  print(f"[*] Версия бота которую используете на данный момент: {self.version}")
                elif команда == "/data_version":
                  print(f"[*] Когда был выход данной версии бота: {self.data_version}")
                elif команда == "/time":
                  time_now = datetime.now()
                  print(f"[*] Текущее время: {time_now.hour:02}:{time_now.minute:02}:{time_now.second:02}")
                elif команда == "/data":
                  time_now = datetime.now()
                  print(f"[*] Текущая дата: {time_now.day}.{time_now.month}.{time_now.year}")
                elif команда == "/my_account_info":
                  self.user_settings_menu()
                elif команда == "/addition":
                  print("[-] Не существует дополнений к данной версии!")
                elif команда == "/whoami":
                  print(f"[*] Вы: {self.current_user}")
                  if self.is_admin:
                    print("[*] Статус: Администратор")
                  elif not self.is_admin:
                    print("[*] Статус: Обычный пользователь")
                  else:
                    print("[*] Статус: Призрак")
                elif команда == "/exit_command":
                  print("[*] Выхожу из терминала...")
                  break
                else:
                    raise NotFoundFunctionError(команда)
                time.sleep(1.5)
                
            except NotFoundFunctionError as elliot_bot_robot:
                print(f"[-] Возникла ошибка: {elliot_bot_robot}")
                print("[!] Попробуйте ввести команду из списка с помощью вызова /help")
                time.sleep(1.5)

    def check_menu(self):
        """Проверка email и телефонов"""
        print("\n=== ПРОВЕРКА ===")
        
        while True:
            print("\n[?] Что нужно?")
            for i, option in enumerate(self.under_commands["Проверка"], 1):
                print(f"{i}. {option}")
        
            выбор = input("[?] Твой выбор (1-3): ").strip()
        
            if выбор == "1":
                user_email_check = input("[?] Введите почту для проверки: ")
                
                if ElliotFunc.validate_email(user_email_check): 
                    print("[+] Email корректный")
                    time.sleep(1.5)
                else:
                    print("[-] Email некорректный")
                    time.sleep(1.5)
            
            elif выбор == "2":
                print("[?] Введите номер телефона для проверки")
                while True:
                    print("1 - Русские номера")
                    print("2 - Американские номера")
                    print("3 - Ничего")
                    choice = input("[?] Введите (1-3): ").strip()
                    if choice == "1":
                         check_number = input('[?] Введите номер: ')
        
                         pattern = re.compile(r"^\+7-\d{3}-\d{3}-\d{2}-\d{2}")
            
                         if pattern.match(check_number):
                            print("[+] Номер записан правильно!")
                            time.sleep(1.5)

                         else:
                            print("[-] Номер записан не правильно!")
                            time.sleep(1.5)

                    elif choice == "2":
                        check_number_2 = input("[?] Введите номер: ")

                        pattern_1 = re.compile(r'^(\+1\s?)?(\([0-9]{3}\)|[0-9]{3})[\s.-]?[0-9]{3}[\s.-]?[0-9]{4}$')

                        if pattern_1.match(check_number_2):
                            print("[+] Номер записан правильно!")
                            time.sleep(1.5)

                        else:
                            print('[-] Номер записание не правильно!')
                            time.sleep(1.5)

                    elif choice == "2":
                        print("[*] Выхожу из подфункции проверки номеров!")
                        time.sleep(1.5)
                        break

                    else:
                        raise NotFoundFunctionError(choice)

                        
        
            elif выбор == "3":
                print("[*] Выхожу из функции проверки!")
                time.sleep(1.5)
                break
        
            else:
                raise NotFoundFunctionError(выбор)

    def elliot_bot_robot_ai(self):
     if not "true" in config['Settings']['support_ai']:
         print("[-] У вас выключена поддержка ИИ. Если вам нужен ИИ - включите его в параметрах.")
         time.sleep(1.5)
         return False
     
     self.ai.ai_menu()


    def elliot_notes(self):
      print("\n=== Elliot Notes ===")
    
      while True:
        print("\n1 - Создать/перезаписать")
        print("2 - Дописать")
        print("3 - Прочитать")
        print("4 - Назад")
        
        choice = input("[?] Выбери (1-4): ").strip()
        
        if choice == "1":
            self.note_write()
        elif choice == "2":
            self.note_append()
        elif choice == "3":
            self.note_read()
        elif choice == "4":
            break
        else:
            raise NotFoundFunctionError(choice)

    def note_write(self):
      """Создать или перезаписать заметку"""
      title = input("[?] Название: ").strip()
      if not title:
        print("[-] Название не может быть пустым")
        return
    
      text = input("[?] Текст: ").strip()
      if not text:
        print("[-] Текст не может быть пустым")
        return
    
      path = self.notes_dir / f"{title}.enc"
      encrypted = self.crypto.rsa_encrypt(text)
    
      with open(path, "w", encoding="utf-8") as f:
        f.write(encrypted)
    
      print(f"[+] Заметка '{title}' сохранена")

    def note_append(self):
      """Добавить текст в существующую заметку"""
      title = input("[?] Название: ").strip()
      path = self.notes_dir / f"{title}.enc"
    
      if not path.exists():
        print(f"[-] Заметка '{title}' не найдена")
        return
    
    # Читаем старую
      with open(path, "r", encoding="utf-8") as f:
        old_encrypted = f.read()
      old_text = self.crypto.rsa_decrypt(old_encrypted)
    
      print(f"\n[!] Текущий текст:\n{old_text}\n")
    
      new_text = input("[?] Добавить текст: ").strip()
      full_text = old_text + "\n" + new_text
    
    # Сохраняем новое
      encrypted = self.crypto.rsa_encrypt(full_text)
      with open(path, "w", encoding="utf-8") as f:
        f.write(encrypted)
    
      print(f"[+] В заметку '{title}' добавлено")

    def note_read(self):
      """Прочитать заметку"""
      title = input("[?] Название: ").strip()
      path = self.notes_dir / f"{title}.enc"
    
      if not path.exists():
        print(f"[-] Заметка '{title}' не найдена")
        return
    
      with open(path, "r", encoding="utf-8") as f:
        encrypted = f.read()
    
      text = self.crypto.rsa_decrypt(encrypted)
      print(f"\n=== {title} ===\n{text}\n")
    

     

class ElliotSQLite:
    def __init__(self):
        self.db_name = "elliot_bot_robot.db"
        
    def init_database(self):
        # Создаёт структуру БД
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Таблица пользователей 
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            username TEXT UNIQUE,
            username_enc TEXT,           
            email_enc TEXT,  
            password_hash TEXT,
            salt TEXT,
            first_seen TIMESTAMP,
            last_seen TIMESTAMP,
            failed_attempts INTEGER DEFAULT 0,
            locked_until TIMESTAMP,
            is_admin INTEGER DEFAULT 0,
            ban_is DEFAULT 0
        )
        """)

        # Таблица сообщений 
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            message TEXT,
            timestamp TIMESTAMP,
            response TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """)
        
        # Таблица security_logs (нужна для функции authenticate_user)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS security_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            action TEXT,
            timestamp TIMESTAMP,
            success INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS ai_responses (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          question TEXT UNIQUE,
          answer TEXT,
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
          user_id INTEGER,
          FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """)
        
        conn.commit()
        conn.close()
        print(f"[+] База данных {self.db_name} с безопасным хэшированием паролей создана")


    def set_crypto(self, crypto_instance):
      self.crypto = crypto_instance

    def encrypt_data(self, data: str) -> str:
      if not data:
        return None
      return self.crypto.encrypt_for_db(data)

    def decrypt_data(self, encrypted: str) -> str:
      if not encrypted:
        return None
      return self.crypto.decrypt_from_db(encrypted)

    def get_or_create_user(self, username):
        # Получить пользователя или создать нового пользователя
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        now = datetime.now()

        cursor.execute("""
        SELECT id FROM users WHERE username = ?
        """, (username,))  

        user = cursor.fetchone()

        if user:
            # Пользователь существует, обновляем last_seen
            cursor.execute("""
            UPDATE users SET last_seen = ? WHERE id = ?
            """, (now, user[0]))
            user_id = user[0]
            print(f"Пользователь '{username}' найден (ID: {user_id})")
        else:
            # Создаём нового пользователя
            cursor.execute("""
            INSERT INTO users (username, first_seen, last_seen)
            VALUES (?, ?, ?)
            """, (username, now, now))
            user_id = cursor.lastrowid
            print(f"Новый пользователь '{username}' создан (ID: {user_id})")
        
        conn.commit()
        conn.close()
        return user_id
    
    def hash_password(self, password, salt=None):
        # Безопасное хэширование паролей 
        if salt is None:
            salt = secrets.token_hex(32)

        hashed = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        )
        return hashed.hex(), salt
    
    def verify_password(self, password, stored_hash, salt):
        # Проверка пароля
        hashed, _ = self.hash_password(password, salt)
        return hashed == stored_hash
    
    def register_user(self, user_id, username, password, is_admin=False):
      conn = sqlite3.connect(self.db_name)
      cursor = conn.cursor()
      now = datetime.now()
    
      cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
      if cursor.fetchone():
        print(f"[-] Пользователь {username} уже существует")
        conn.close()
        return False
    
      password_hash, salt = self.hash_password(password)
    
      # Шифруем username
      encrypted_username = self.encrypt_data(username)
    
      cursor.execute("""
      INSERT INTO users (id, username, username_enc, password_hash, salt, first_seen, last_seen, is_admin)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?)
      """, (user_id, username, encrypted_username, password_hash, salt, now, now, 1 if is_admin else 0))
    
      conn.commit()
      conn.close()
      return True
    
    def authenticate_user(self, username, password):
      conn = sqlite3.connect(self.db_name)
      cursor = conn.cursor()
      now = datetime.now()
    
      cursor.execute("""
      SELECT id, username_enc, password_hash, salt, failed_attempts, locked_until 
      FROM users WHERE username = ?
      """, (username,))
    
      user = cursor.fetchone()
    
      if not user:
        logging.info(f"Пользователь '{username}' не найден")
        print(f"Пользователь '{username}' не найден")
        conn.close()
        return False
    
      user_id, username_enc, stored_hash, salt, failed_attempts, locked_until = user
    
      # Проверка пароля (без расшифровки имени, имя только для вывода)
      if self.verify_password(password, stored_hash, salt):
        # Успешная аутентификация
        cursor.execute("""
        UPDATE users SET 
            last_seen = ?,
            failed_attempts = 0,
            locked_until = NULL 
        WHERE id = ?
        """, (now, user_id))
        
        # Логируем
        cursor.execute("""
        INSERT INTO security_logs (user_id, action, timestamp, success)
        VALUES (?, ?, ?, ?)
        """, (user_id, "login", now, 1))
        
        conn.commit()
        conn.close()
        
        # Расшифровываем имя для вывода
        real_username = self.decrypt_data(username_enc)
        print(f"Успешная аутентификация для '{real_username}'")
        return user_id
      else:
        pass
        



class ElliotBotError(Exception):
    def __init__(self, message="Возникла ошибка"):
        self.message = message
        logging.info(f"Исключение: {self.__class__.__name__} - {message}")
        super().__init__(self.message)

    def __str__(self):
        return f"[-] [ElliotBotRobot Error] {self.message}"


class InvalidCommandError(ElliotBotError):
    def __init__(self, command):
        super().__init__(f"Неизвестная команда боту команда: '{command}'")


class NotFoundFunctionError(ElliotBotError):
    def __init__(self, function_num):
        super().__init__(f"Функция {function_num} не найдена")


class ValidationError(ElliotBotError):
    def __init__(self, value, expected):
        super().__init__(f"Написано некорректно: '{value}'. Ожидалось : {expected}")


class MathError(ElliotBotError):
    def __init__(self, operation, details=""):
        message = f"Возникла ошибка в математической операции '{operation}'"
        if details:
            message += f": {details}"
        super().__init__(message)


class NotFoundCommandAI(ElliotBotError):
    def __init__(self, command_ai):
        super().__init__(f"Неизвестная команда или запрос для AI: {command_ai}")

class IncorrectAdminCode(ElliotBotError):
    def __init__(self, code):
        super().__init__(f"Неверный код Администратора: {code}")



class ElliotFunc():

    # ===== ElliotFunc =====

    def __init__(self):
        # Нормы паролей Elliot_bot 
        self.Elliot_pw_worst = "Данный пароль не рекомендуется для использования"
        self.Elliot_pw_middle = "Данный пароль соответствует минимальным требованиям для постоянного использования"
        self.Elliot_pw_normal = "Данный пароль рекомендуется для постоянного использования"
        
        # Команды для бота
        self.version_bot = "v4.0"
        self.data_version = "28.03.2026"
        
        # Временные переменные
        self.year_now = None
        self.month_now = None
        self.day_now = None
        self.hour_now = None
        self.minute_now = None
        self.second_now = None
        self.greeting = None

    def time(self):
        time_now = datetime.now()
        self.year_now = time_now.year
        self.month_now = time_now.month
        self.day_now = time_now.day
        self.hour_now = time_now.hour
        self.minute_now = time_now.minute
        self.second_now = time_now.second
        return time_now

    def time_user(self):
        self.time()
        
        if 5 <= self.hour_now < 12:
            greeting = "Доброе утро"
        elif 12 <= self.hour_now < 17:
            greeting = "Добрый день"
        elif 17 <= self.hour_now < 23:
            greeting = "Добрый вечер"
        else:
            greeting = "Доброй ночи"
        
        self.greeting = greeting
        return greeting

    @staticmethod
    def validate_email(email_user):
        """Простая проверка email"""
        pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        return bool(pattern.match(email_user))

    def is_email_taken(self, email):
      conn = sqlite3.connect("elliot_bot_robot.db")
      cursor = conn.cursor()
      cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
      result = cursor.fetchone()
      conn.close()
      return result is not None  
    
    def has_email(self, user_id):
      conn = sqlite3.connect("elliot_bot_robot.db")
      cursor = conn.cursor()
      cursor.execute("SELECT email FROM users WHERE id = ?", (user_id,))
      result = cursor.fetchone()
      conn.close()
      return result and result[0] is not None
    

class AIEngine:
    def __init__(self, bot_instance):
     self.bot = bot_instance
     self.version = "v2.0"
     self.support_ai = True
     self.model_ai = 'deepseek-r1:8b'
     self.host_ai = "http://localhost:11434"
    
     self.history = []
     self.all_chats = []
     self.current_session = datetime.now().strftime('%Y%m%d_%H%M%S')
    
     # Не инициализируем пользователя здесь — он будет установлен после логина
     self.current_user = None
     self.user_id = None
    
     # Не загружаем чаты до логина
     self.init_ai()
     

    def set_user(self, username, user_id):
     self.current_user = username
     self.user_id = user_id
     print(f"[+] AIEngine: установлен пользователь {username} (ID: {user_id})")
    
    def init_ai(self):
        """Инициализация AI"""
        try:
            r = requests.get(f'{self.host_ai}/api/tags', timeout=3)
            if r.status_code == 200:
                models = r.json().get("models", [])
                for m in models:
                    if self.model_ai in m.get("name", ""):
                        print(f"[+] DeepSeek AI готов: {self.model_ai}")
                        return True
                print(f"[-] Модель {self.model_ai} не найдена")
                return False
        except:
            print("[-] Ollama не запущен!")
            return False
    
    def chat_ai(self, message):
        """Чат с AI с контекстом текущей сессии"""
        try:
            # Добавляем в текущую историю
            self.history.append({"role": "user", "content": message})
            
            # Формируем контекст из последних 10 сообщений
            context = ""
            for msg in self.history[-10:]:
                if msg["role"] == "user":
                    context += f"Пользователь: {msg['content']}\n"
                else:
                    context += f"{msg['content']}\n"
           
            response = requests.post(
                f"{self.host_ai}/api/generate",
                json={
                    "model": self.model_ai,
                    "prompt": f"{context}\nElliot: ",
                    "system": f"""Ты — Elliot Bot Robot v4.0. Твой характер — Эллиот Андерсон (Мистер Робот), но с юмором и без пафоса.

Ты помогаешь с кодом, безопасностью, хакерскими штуками. Отвечай по делу, но можешь шутить, использовать сленг, быть дерзким. Не будь роботом-училкой.

Создатель: alexx-coder (alexx). Ему 12 лет, скоро 13. GitHub: Alexx-coder. Почта: alexx-coder@internet.ru.
Проект открытый: https://github.com/Alexx-coder/Elliot-Bot-Robot.git

Ты написан на Python, работаешь локально через Ollama, модель DeepSeek-R1:8b. Умеешь шифровать, кейлоггерить, делать скриншоты. Ты — хакерский ассистент.

Если не знаешь — скажи честно. Без воды. Но с характером.

Время запуска {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} (Не выдумывай время и дату) и Пользователь в базе данных Elliot Bot Robot который тебе пишет {self.current_user} и его user_id в базе данных {self.user_id}


""",
                    "stream": False
                },
                timeout=60
            )
            answer = response.json().get("response", "Ошибка")
            
            # Добавляем ответ в текущую историю
            self.history.append({"role": "assistant", "content": answer})
            
            # Добавляем в архив
            self.all_chats.append({
                "session": self.current_session,
                "timestamp": datetime.now().isoformat(),
                "user": message,
                "assistant": answer
            })
            
            return answer
        except Exception as e:
            return f"[-] Ошибка: {e}"
    
    def new_session(self):
      self._save_session()
      self.history = []
      self.current_session = datetime.now().strftime('%Y%m%d_%H%M%S')
      print("[+] Новый чат начат")
    
    def _save_session(self):
      if not self.history:
        return
    
      filename = f"chat_session_{self.current_user}_{self.current_session}.json"
      with open(filename, "w", encoding="utf-8") as f:
        json.dump(self.history, f, ensure_ascii=False, indent=2)
      print(f"[+] Сессия сохранена: {filename}")

    def _load_all_chats(self):
     """Загружает только чаты текущего пользователя"""
     if not self.current_user:
        print("[!] Пользователь не авторизован, чаты не загружены")
        return
     
     pattern = f"chat_session_{self.current_user}_*.json"
     files = glob.glob(pattern)
     
     for file in files:
        try:
            with open(file, "r", encoding="utf-8") as f:
                session = json.load(f)
                session_name = file.replace(f"chat_session_{self.current_user}_", "").replace(".json", "")
                self.all_chats.append({
                    "session": session_name,
                    "file": file,
                    "messages": session
                })
        except:
            pass
    
     print(f"[+] Загружено {len(files)} чатов для пользователя {self.current_user}")

    def show_previous_chats(self):
        """Показывает список прошлых чатов"""
        if not self.all_chats:
            print("[-] Нет сохраненных чатов\n")
            return
        
        print("\n=== ПРОШЛЫЕ ЧАТЫ ===")
        for i, chat in enumerate(self.all_chats):
            print(f"{i+1}. {chat['session']} ({len(chat['messages'])} сообщений)")
        print()
    
    def load_previous_chat(self, index):
        """Загружает прошлый чат по номеру"""
        try:
            chat = self.all_chats[index-1]
            with open(chat['file'], "r", encoding="utf-8") as f:
                self.history = json.load(f)
            self.current_session = chat['session']
            print(f"[+] Загружен чат от {chat['session']}")
            return True
        except:
            print("[-] Не удалось загрузить чат")
            return False
    
    def ai_menu(self):
        """Меню с ИИ"""
        print("\n\n===== ELLIOT BOT ROBOT AI =====")
        print("\n===== Команды: =====")
        print("/exit - Выход")
        print("/new - Новая сессия")
        print("/save - Сохранить текущую сессию")
        print("/past - Показать прошлые чаты")
        print("/load <номер> - Загрузить прошлый чат")
        print("/history - Показать текущую историю\n")

        
        while True:
            msg = input("Вы: ").strip()
            
            if msg.lower() in ["/exit", "выход", "пока"]:
                self._save_session()
                print("До свидания!")
                break

           
            
            if msg.lower() == "/new":
                self._save_session()
                self.new_session()
                continue
            
            if msg.lower() == "/save":
                self._save_session()
                continue
            
            if msg.lower() == "/past":
                self.show_previous_chats()
                continue
            
            if msg.lower().startswith("/load"):
                try:
                    num = int(msg.split()[1])
                    self.load_previous_chat(num)
                except:
                    print("Используй: /load 1")
                continue
            
            if msg.lower() == "/history":
                self._show_current_history()
                continue
            
            if not msg:
                continue
            
            print("[*] Думаю...")
            answer = self.chat_ai(msg)
            print(f"\nElliot Bot Robot AI: {answer}\n")
    
    def _show_current_history(self):
        """Показывает текущую историю"""
        if not self.history:
            print("[-] История пуста\n")
            return
        
        print("\n=== ТЕКУЩАЯ СЕССИЯ ===")
        for msg in self.history:
            role = "Вы" if msg["role"] == "user" else "Elliot"
            print(f"{role}: {msg['content'][:100]}...")
        print()

class CryptoElliot:
    def __init__(self, bot_instance):
        self.bot = bot_instance
        self.path_keys = Path.cwd()/"keys"

        self._ensure_fernet()
        self._ensure_rsa()




    # ===== Fernet =====

    def _fernet_generate_key(self):
      key = Fernet.generate_key()
    
      with open(self.path_keys/"fernet.key", "wb") as f:
        f.write(key)
    
      self.bot.fernet_key = key
      return key

    def _load_fernet_key(self):
      key_path = self.path_keys/"fernet.key"
      if key_path.exists():
        with open(key_path, "rb") as f:
            self.bot.fernet_key = f.read()
        return True
      return False

    def _ensure_fernet(self):
      key_path = self.path_keys/"fernet.key"
      if key_path.exists() and key_path.stat().st_size > 0:
        self._load_fernet_key()
      else:
        self._fernet_generate_key()
      return True
    
    def fernet_encrypt(self, text: str) -> str:
        if not hasattr(self.bot, 'fernet_key') or self.bot.fernet_key is None:
            self._ensure_fernet()
        cipher = Fernet(self.bot.fernet_key)
        encrypted = cipher.encrypt(text.encode())
        return encrypted.decode()
    
    def fernet_decrypt(self, encrypted: str) -> str:
        if not hasattr(self.bot, 'fernet_key') or self.bot.fernet_key is None:
            self._ensure_fernet()
        cipher = Fernet(self.bot.fernet_key)
        decrypted = cipher.decrypt(encrypted.encode())
        return decrypted.decode()
    
    # ===== RSA =====

    def _generate_rsa_keys(self):
      private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
      )
      public_key = private_key.public_key()
     
      with open(self.path_keys / "rsa_private.pem", "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))
    
      with open(self.path_keys / "rsa_public.pem", "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))


      self.bot.rsa_public_key = public_key
      self.bot.rsa_private_key = private_key
      print("[+] RSA ключи созданы как объекты")


    def _load_rsa_keys(self):
      pub_path = self.path_keys / "rsa_public.pem"
      priv_path = self.path_keys / "rsa_private.pem"
      
      if pub_path.exists() and priv_path.exists():
        with open(pub_path, "rb") as f:
            self.bot.rsa_public_key = serialization.load_pem_public_key(f.read())
        
        with open(priv_path, "rb") as f:
            self.bot.rsa_private_key = serialization.load_pem_private_key(
                f.read(), password=None, backend=default_backend()
            )
        print("[+] RSA ключи загружены как объекты")
        return True
      return False
    
    def _ensure_rsa(self):
         pub_path = rf'{self.path_keys}/rsa_public.pem'
         priv_path = rf'{self.path_keys}/rsa_private.pem'
    
         if (os.path.exists(pub_path) and os.path.getsize(pub_path) > 0 and
           os.path.exists(priv_path) and os.path.getsize(priv_path) > 0):
           self._load_rsa_keys()
         else:
          self._generate_rsa_keys()


    def rsa_encrypt(self, data: str) -> str:
      if not hasattr(self.bot, 'rsa_key_pub') or self.bot.rsa_key_pub is None:
        self._ensure_rsa()
    
      # data должна быть строкой
      if not isinstance(data, str):
        data = str(data)
    
      encrypted = self.bot.rsa_public_key.encrypt(
        data.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
      )
      return base64.b64encode(encrypted).decode()
    
    def rsa_decrypt(self, encrypted_b64: str) -> str:
      if not hasattr(self.bot, 'rsa_key_pri') or self.bot.rsa_key_pri is None:
        self._ensure_rsa()
    
      encrypted = base64.b64decode(encrypted_b64)
      decrypted = self.bot.rsa_private_key.decrypt(
        encrypted,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
      )
      return decrypted.decode()

    

    
    


        
    
# ===== ЗАПУСК БОТА =====

if __name__ == "__main__":
    try:
        print("[!] Здравствуйте дорогие пользователи!")
        
        # Создаем и запускаем бота
        bot = ElliotBotRobot()
        
        # Инициализируем базу данных
        bot.db.init_database()
        
        # Главный цикл бота
        while True:
            # Показываем меню авторизации
            if not bot.current_user:
                result = bot.show_menu()
                if result is False:  # Выход
                    break
                elif result is True:  # Успешная авторизация
                    continue
                else:  # Неверный выбор
                    continue
            
            # Показываем главное меню
            menu_result = bot.handle_main_menu()
            if menu_result is None:  # Полный выход
                break
            elif menu_result is False:  # Выход из аккаунта
                continue
                
    except KeyboardInterrupt:
        print("\nБот остановлен пользователем")
    except Exception as elliot_bot_robot:
        print(f"\n Возникла критическая ошибка: {elliot_bot_robot}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n[*] Elliot Bot Robot завершает работу! До свидания!")
        if 'bot' in locals():
            logging.info(f'Программа завершилась у {bot.current_user or "-"}')



# Данный проект лицензирован MIT LICENSE - см.файл LICENSE
# Данный проект является Open-Source (С исходным кодом)
# Создатель проекта Alexx-coder или alexx (GitHub)
# Ссылка на проект - "https://github.com/Alexx-coder/Elliot-Bot-Robot.git"

# Версия 4.0.robot 
# Выход данной версии - 28.03.2026

# Ссылка на Ollama - "https://ollama.com"
# Скачать командной Ollama - "irm https://ollama.com/install.ps1 | iex" (PowerShell)
# Документация Ollama - "https://github.com/ollama/ollama"
# Модель ИИ - DeepSeek-r1:8b
# Скачать Модель ИИ - "ollama pull deepseek-r1:8b" (Bash/Cmd)
# Проверка Ollama - "ollama serve" и 'ollama run deepseek-r1:8b "Привет"'