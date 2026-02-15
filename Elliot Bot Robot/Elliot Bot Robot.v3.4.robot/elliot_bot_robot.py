import sqlite3
import datetime
import hashlib
import secrets
import re
from pathlib import Path
import string
import random


#print("Здравствуйте дорогие пользователи!\nХотим вам представить новую с нуля написанную и оптимизированную версию Elliot bot!\nЧтобы узнать поподробнее перейдите в README.md")

class ElliotBotRobot:
    def __init__(self, name="Elliot Bot Robot", version="3.4.robot"):
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
            "12": "Elliot Bot Robot AI - Чат с ненастоящим ИИ, который умеет отвечать пользователю"
        }
        self.under_commands = {
            "Математика": ["Сложение", "Вычитание", "Умножение", "Деление", "Проверка сравнений", "Выход"],
            "Python помощь": ["Основы Python", "Примеры кода", "Ошибки новичков", "Советы", "Выход"],
            "Фишки ПК": ["Ускорение Windows", "Горячие клавиши", "Очистка системы", "Безопасность пользователя", "Выход"],
            "Командная строка": ["Windows CMD", "PowerShell", "Linux/Mac Terminal", "Полезные команды", "Выход"],
            "Установка ОС": ["Установка Windows", "Установка Linux", "Создание загрузочной флэшки", "Драйвера и настройки", "Выход"],
            "Проверка": ["Проверка почт", "Проверка номеров телефонов", "Выход"]
        }

        self.db = ElliotSQLite()
        self.func = ElliotFunc()
        self.current_user = None
        self.is_admin = False
        self.user_id = None
        self.admin_code = "aeDM32CdeTreu.admin"
        self.data_version = "15.02.2026" 
        self.choice = None
        #self.Elliot_pw_worst = "Данный пароль не рекомендуется для использования"
        #self.Elliot_pw_middle = "Данный пароль соответствует минимальным требованиям для постоянного использования"
        #self.Elliot_pw_normal = "Данный пароль рекомендуется для постоянного использования"

       

    def show_menu(self):
        print(f"Ты в папке: {Path.cwd()}")
        print("Привет, я Эллиот Бот Робот")
        print("ВХОД / РЕГИСТРАЦИЯ / ВЫХОД")
        print("1 - Вход в аккаунт")
        print("2 - Регистрация")
        print("3 - Выход")

        while True:
            try:
                choice = input("Введите 1-3: ").strip()

                if choice not in ["1", "2", "3"]:
                    raise NotFoundFunctionError(choice)
                
                if choice == "1":
                    success = self.login()
                    return success
                elif choice ==  "2":
                    success = self.registr()
                    return success
                elif choice == "3":
                    print("До свидания!")
                    break

            except NotFoundFunctionError as elliot_bot_robot:
                print(f"Возникла ошибка: {elliot_bot_robot}")
                print("Выберите 1, 2 или 3")

    def login(self):
        print("ВХОД В АККАУНТ")

        for попытка in range(3):
            print(f"Попытка {попытка + 1} из 3")
            
            username = input("Логин: ").strip()
            if not username:
                print("Имя пользователя не может быть пустым")
                continue
                
            password = input("Пароль: ").strip()
            if not password:
                print("Пароль не может быть пустым")
                continue
            


            user_id = self.db.authenticate_user(username, password)
            if user_id:
                self.current_user = username
                self.user_id = user_id

                conn = sqlite3.connect(self.db.db_name)
                cursor = conn.cursor()
                cursor.execute("SELECT is_admin FROM users WHERE username = ?", (username,))
                user_data = cursor.fetchone()
                conn.close()
                

                greeting = self.func.time_user()
                now = datetime.datetime.now()
                if user_data and user_data[0] == 1:
                    self.is_admin = True
                    print(f"{greeting} {username}! Вы вошли как Администратор!")
                else:
                    self.is_admin = False
                    print(f"{greeting} {username}! Вы вошли как Обычный пользователь")

                print(f"\nСегодня {now.day}.{now.month}.{now.year}")
                print(f"Данный день идёт уже {now.hour:02}:{now.minute:02}:{now.second:02}")
                break

            else:
                print("Неверный логин или пароль!")
        
        print("Слишком много неудачных попыток.")
        return False
    
    def registr(self):
        print("РЕГИСТРАЦИЯ")

        while True:
            username = input("Создайте имя пользователю: ").strip()

            if not username:
                print("Имя пользователя не должно быть пустым")
                continue

            if len(username) < 3:
                print("Имя пользователя не должно быть меньше 3 символов")
                continue

            if len(username) > 40:
                print("Имя пользователя не должно быть больше 40 символов")
                continue

            try:
                conn = sqlite3.connect(self.db.db_name)
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
                existing_user = cursor.fetchone()
                conn.close()
            
                if existing_user:
                  print("Пользователь с таким именем уже существует!")
                  print("Попробуйте другое имя:")
                  continue
                break
            except:
            
                break

        while True:
            password = input("Теперь пароль пользователю: ").strip()

            if not password:
                print("Пароль пользователя не должен быть пустым!")
                continue

            if len(password) <= 5:
                print("Пароль короткий надо придерживать как минимум норме Elliot_pw_worst")
                print("О нормах паролей в README.md(Примечания)")
                print("Вам придётся ввести пароль длиной минимум 6 символов")
                continue

            if 6<= len(password) <= 7:
                print(f"Норма вашего пароля: Elliot_pw_worst - {self.func.Elliot_pw_worst}")
                print("О нормах паролей в README.md(Примечания)")

                confirm = input("Вы уверены что хотите использовать данный пароль? (да/нет): ").strip().lower()
                if confirm == "да":
                    break
                else:
                    continue
                    

            elif 8 <= len(password) <= 9:
                print(f"Норма вашего пароля: Elliot_pw_middle - {self.func.Elliot_pw_middle}")
                print("О нормах паролей в README.md(Примечания)")
                break


            elif len(password) >= 10:
                print(f"Норма вашего пароля: Elliot_pw_normal - {self.func.Elliot_pw_normal}")
                print("О нормах паролей в README.md(Примечания)")
                break
            else:
                print("Пароль не соответствует ни одной категории")
                break


        while True:
            confirm_password = input("\nПотвердите свой пароль: ").strip()

            if password != confirm_password:
                print("Пароль не совпадает! Повторите попытку")
                continue
            else:
                break

        print("Специальные возможности")
        is_admin = False
        

        while True:
            code_admin = input("Введите специальный код чтобы получить статус Администратора или Enter: ").strip()

            if code_admin == "": #Enter
                print("Вы зарегестрировались как обычный пользователь")
                break

            if code_admin == self.admin_code:
                print("Специальный код совпал! Поздравляю, вы Администратор!")
                is_admin = True
                break

            else:
                print("Специальный код не совпал!")
                retry =  input("Хотите ввести код заново? (да/нет): ").strip().lower()
                if retry != "да":
                    print("Вы зарегистрированы как обычный пользователь!")
                    break
                

        success = self.db.register_user(username, password, is_admin)
        if success:
            self.current_user = username
            
            # Получаем ID пользователя
            conn = sqlite3.connect(self.db.db_name)
            cursor = conn.cursor()
            cursor.execute("SELECT id, is_admin FROM users WHERE username = ?", (username,))
            user_data = cursor.fetchone()
            conn.close()

            greeting = self.func.time_user()
            now = datetime.datetime.now()
            
            if user_data and user_data[1] == 1:  # Проверяем is_admin
               self.is_admin = True
               print(f"{greeting} {username}! Вы вошли как Администратор!")
            else:
               self.is_admin = False  # Явно устанавливаем False
               print(f"{greeting} {username}! Вы вошли как Обычный пользователь")


            print("Теперь вы есть в Базе Данных Elliot Bot Robot!")
            print(f"Ваше имя пользователя: {username}")
            print(f"Ваш уникальный id: {self.user_id}")

            if self.is_admin:
                print("Статус: Администратор")
                print("Вам доступны привелегия!")
            else:
                print("Статус: Обычный пользователь")
                print("Вам не доступный привелегия!")

            print(f"\nДата регистрации: {datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")

            self.db.authenticate_user(username, password)
            return True
        else:
            print("Ошибка при регистрации!")
            return False
        
    def show_main_menu(self):
        #Главное меню
        print(f"ГЛАВНОЕ МЕНЮ - {self.name}, {self.version}")

        if self.current_user:
            print(f"Текущий пользователь: {self.current_user}")
            
            if self.is_admin:
                print("Статус: Администратор")
                print("Вам доступны привелегия!")
            else:
                print("Статус: Обычный пользователь")
                print("Вам не доступный привелегия!")

        print(f"\nВыберите действие:")
        for key, value in self.commands.items():
            print(f"{key}. {value}")

        
        if self.is_admin:
            print("Функции только для администраторов!")
            print("a1 - В разработке или в плане")

        
        print("Функции связанные с работой аккаунта")
        print("u1 - Выход из аккаунта ")
        print("u2 - Завершить работу")

        
    def handle_main_menu(self):
        #Команды для меню 
        while True:
            try:
                self.show_main_menu()
                choice = input("Выберите пункт меню: ").strip().lower()

                if choice == "u1":
                  print(f"До свидания {self.current_user}! Вы вышли из аккаунта")
                  self.current_user = None
                  self.is_admin = False
                  self.user_id = None
                  return False
            
                elif choice == "u2":
                  print("Бот завершает работу по команде пользователя! До свидания!")
                  return None
            
                elif choice in self.commands:
                  self.handle_commands(choice)
                  input("Нажмите Enter чтобы продолжить: ").strip()
                  continue

                elif choice == "a1" and self.is_admin:
                  print("Приносим извинения! Данная команда в разработке или в плане!")
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
                      input("Нажмите Enter чтобы продолжить: ").strip()
                      continue

                    else:
                       raise NotFoundFunctionError(choice)
                
            except NotFoundFunctionError as elliot_bot_robot:
                print(f"Возникла ошибка: {elliot_bot_robot}")
                print("Введите корректный пункт меню")
                input("Нажмите Enter чтобы продолжить: ")
                continue
            except KeyboardInterrupt:
                print("\nБот остановлен пользователем")
                return None
            except Exception as elliot_bot_robot:
                print(f"\nНеизвестная ошибка: {elliot_bot_robot}")
                input("Нажмите Enter чтобы продолжить: ")
                continue

    def handle_commands(self, choice):
        #Основные функции для бота
        #Можно писать либо название функции либо её номер
        if choice in self.commands:
           command_name_or_number = self.commands[choice].split(" - ")[0]
           print(f"Вы выбрали: {command_name_or_number}")
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
            else:
                raise NotFoundFunctionError(command_name_or_number)
        
        except NotFoundFunctionError as elliot_bot_robot:
           print(f"Возникла ошибка: {elliot_bot_robot}")
           print("Введите корректную функцию для бота")
           input("Нажмите Enter чтобы продолжить: ")
        except KeyboardInterrupt:
           print("\nБот остановлен пользователем")
           return None
        except Exception as elliot_bot_robot:
           print(f"\nНеизвестная ошибка: {elliot_bot_robot}")
           input("Нажмите Enter чтобы продолжить: ")


    def math_menu(self):
        #Математика
        print("\nМАТЕМАТИКА")

        for i, option in enumerate(self.under_commands["Математика"], 1):
            print(f"{i}. {option}")

        while True:
            try:
                choice = input("Выберите подфункцию (1-6):")
                if choice == "6":
                    print("Выхожу из Математики")
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
                            print("Надо ввести число! Попробуйте снова:")

                число_1 = получить_число("Это первое число: ")
                число_2 = получить_число("Это второе число: ")

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
                

                print(f"Результат: {число_1} {знак} {число_2} = {результат}")

                while True:
                    ещё_раз_посчитать = input("Хотите ещё раз посчитаю? (да/нет): ").strip().lower()
                    if ещё_раз_посчитать in ["да", "нет"]:
                        break
                    print("Напиши 'да' или 'нет'")

                if ещё_раз_посчитать == "нет":
                    print("Заканчиваю данную функцию")
                    break

            except NotFoundFunctionError as elliot_bot_robot:
                print(f"Возникла ошибка: {elliot_bot_robot}")
                print("Попробуйте ввести подфункцию (1-5)")
            except MathError as elliot_bot_robot:
                print(f"Возникла ошибка в математических операциях: {elliot_bot_robot}")
            except Exception as elliot_bot_robot:
                print(f"Что-то пошло не так: {elliot_bot_robot}")
        
    def under_math(self):
        while True:
          try:
            выражение = input("Введите выражение сравнения. Формат: x (<, >, =) y: ").strip()
            
            # Разбиваем строку на части
            части = выражение.split()
            if len(части) != 3:
                print("Ошибка формата. Пример: 5 > 3")
                continue

            a_str, оператор, b_str = части

            # Преобразуем в числа
            try:
                a = float(a_str) if '.' in a_str else int(a_str)
                b = float(b_str) if '.' in b_str else int(b_str)
            except ValueError:
                print("Ошибка: введите числа.")
                continue

            # Выполняем сравнение
            if оператор == ">":
                результат = a > b
            elif оператор == "<":
                результат = a < b
            elif оператор in ["=", "=="]:
                результат = a == b
            else:
                print("Неподдерживаемый оператор. Используйте >, < или =.")
                continue

            print("Правда!" if результат else "Ложь!")

            # Спрашиваем, продолжать ли
            while True:
                go = input("Продолжить? (да/нет): ").strip().lower()
                if go in ["да", "нет"]:
                    break
                print("Введите 'да' или 'нет'.")

            if go == "нет":
                print("Выхожу...")
                break

          except Exception as ell:
            print(f"Произошла ошибка: {ell}")
          except MathError:
              print(f"Возникла ошибка: {MathError}")




    def python_help_menu(self):
        #Меню помощи по Python
        print("\nПОМОЩЬ ПО PYTHON")

        while True:
            for i, option in enumerate(self.under_commands["Python помощь"], 1):
                print(f"{i}. {option}")
            
            try:
                выбор = input("\nТвой выбор (1-5): ").strip()

                if выбор == "5":
                    print("Выхожу из функции")
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

                input("\n⏎ Нажмите Enter чтобы продолжить...")

            except NotFoundFunctionError as elliot_bot_robot:
                print(f"Ошибка: {elliot_bot_robot}")
                print("Выбери 1, 2, 3, 4 или 5")

            while True:
                ещё = input("\nЕщё про Python? (да/нет): ").strip().lower()
                if ещё in ["да", "нет"]:
                    break
                print("Напиши 'да' или 'нет'")

            if ещё == "нет":
                print("Выхожу из помощи по Python...")
                break

    def pc_tips_menu(self):
        #Фишки для ПК/Ноутбука
        print("\nФишки для ПК/Ноутбука:")

        while True:
            print("\nЧто вы выберите?")
            for i, option in enumerate(self.under_commands["Фишки ПК"], 1):
                print(f"{i}. {option}")

            try:
                выбор = input("Выберите: 1-5: ").strip()

                if выбор == "5":
                    print("Выхожу из данной функции")
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
                
                input("\n⏎ Нажми Enter чтобы продолжить...")
                
            except NotFoundFunctionError as elliot_bot_robot:
                print(f"Ошибка: {elliot_bot_robot}")
                print("Выбери 1, 2, 3, 4 или 5")
            
            while True:
                ещё = input("\nЕщё советы по компьютеру? (да/нет): ").strip().lower()
                if ещё in ["да", "нет"]:
                    break
                print("Напиши 'да' или 'нет'")
            
            if ещё == "нет":
                print("Заканчиваю компьютерные советы...")
                break

    def command_line_menu(self):
        #Командная строка
        print("\nФишки с командной строкой:")

        while True:
            print("\nЧто интересует?")
            for i, option in enumerate(self.under_commands["Командная строка"], 1):
                print(f"{i}. {option}")
            
            try:
                выбор = input("Твой выбор (1-5): ").strip()
                
                if выбор == "5":
                    print("Выхожу из командной строки...")
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
                
                input("\n⏎ Нажми Enter чтобы продолжить...")
                
            except NotFoundFunctionError as elliot_bot_robot:
                print(f"Ошибка: {elliot_bot_robot}")
                print("Выбери 1, 2, 3, 4 или 5")
            
            while True:
                ещё = input("\nЕщё про командную строку? (да/нет): ").strip().lower()
                if ещё in ["да", "нет"]:
                    break
                print("Напиши 'да' или 'нет'")
            
            if ещё == "нет":
                print("Выхожу из командной строки...")
                break

    def os_installation_menu(self):
        #Установка ОС
        print("\nУстановка windows/linux:")

        while True:
            print("\nЧто нужно?")
            for i, option in enumerate(self.under_commands["Установка ОС"], 1):
                print(f"{i}. {option}")
            
            try:
                выбор = input("Твой выбор (1-5): ").strip()
                
                if выбор == "5":
                    print("Выхожу из установки ОС...")
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
                
                elif выбор == "3":
                    print("\nЗАГРУЗОЧНАЯ ФЛЕШКА:")
                    print("1. Скачай образ ОС (.iso)")
                    print("2. Скачай Rufus (Windows) или balenaEtcher")
                    print("3. Подключи флешку 8+ GB")
                    print("4. В Rufus выбери флешку и образ")
                    print("5. Нажми Start (данные удалятся!)")
                    print("6. Жди 5-30 минут")
                    print("7. Готово!")
                
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
                
                input("\n⏎ Нажми Enter чтобы продолжить...")               
                
            except NotFoundFunctionError as elliot_bot_robot:
                print(f"Ошибка: {elliot_bot_robot}")
                print("Выбери 1, 2, 3, 4 или 5")
            
            while True:
                ещё = input("\nЕщё про установку ОС? (да/нет): ").strip().lower()
                if ещё in ["да", "нет"]:
                    break
                print("Напиши 'да' или 'нет'")
            
            if ещё == "нет":
                print("Выхожу из установки ОС...")
                break

    def password_generator_menu(self):
        #Генератор паролей
        print("\nГенератор паролей")

        def generated_password():
            chars = string.ascii_letters + string.digits 
            password = ''.join(random.choice(chars) for _ in range(10))
            return password
        
        print("Ваш пароль сгенерирован:", generated_password())
        print("Данный сгенерированный пароль соответствует норме Elliot_pw_normal")
        print("О нормах паролей в README.md(Примечания)")

        while True:
            ещё = input("\nСгенерировать пароль ещё раз: (да/нет): ").strip().lower()
            if ещё == "да":
                print("Новый пароль сгенерирован:", generated_password())
                print("Данный сгенерированный пароль соответствует норме Elliot_pw_normal")
                print("О нормах паролей в README.md(Примечания)")
            elif ещё == "нет":
                print("Выхожу из данной функции")
                break
            else:
                print("Введите 'да' или 'нет'")

    def user_settings_menu(self):
        #Параметры пользователя
        print("\nПараметры:")
        print(f"\nЛогин Пользователя: {self.current_user}")
        print(f"ID Пользователя: {self.user_id}")
        print(f"Статус пользователя: {'Администратор' if self.is_admin else 'Пользователь'}")
        print(f"Дата входа: {datetime.datetime.now().strftime('%d.%m.%Y %H:%M')}")
        
        # Получаем полную информацию из базы
        conn = sqlite3.connect(self.db.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT first_seen, last_seen, failed_attempts FROM users WHERE username = ?", (self.current_user,))
        user_data = cursor.fetchone()
        conn.close()
        
        if user_data:
            first_seen, last_seen, failed_attempts = user_data
            print(f"Дата регистрации: {first_seen}")
            print(f"Последний вход: {last_seen}")
            print(f"Неудачных попыток входа: {failed_attempts}")

    def contact_developer(self):
        #Связь с разработчиком
        print("\nСвязь с разработчиком:")
        
        # Шифр почты
        email_parts = [
            "alexx",
            "-coder",
            "@",
            "internet",
            ".ru"
        ]
        email = "".join(email_parts)

        print(f"\nРазработчик: Alexx-coder")
        print(f"Почта: {email}")
        print("GitHub: Alexx-coder или просто alex")
        print("\nПиши на почту только по делу!")


    def commands_list(self):
        #Команды бота
        print("\nКоманды:")
        print("\n/help - помощь с командами")
        print("/version_bot - какая версия у данного бота")
        print("/data_version - дата выхода данной версии")
        print("/time - текущее время")
        print("/data - текущая дата")
        print("/my_account_info - информация аккаунта пользователя")
        print("/addition - узнать, существует ли дополнение к этой версии")
        print("/whoami - кто я?")
        print("/exit_command - выход из функции")

    def terminal_mode(self):
        """Терминал бота"""
        print("\nТерминал:")
        print("\nСписок всех команд из функции 9")
        self.commands_list()
        
        print("\nВведите команды (для выхода используйте /exit_command):")
        
        while True:
            try:
                команда = input("\nВведите нужную вам команду: ").strip()
            
                if команда == "/help":
                  self.commands_list()
                elif команда == "/version_bot":
                  print(f"Версия бота которую используете на данный момент: {self.version}")
                elif команда == "/data_version":
                  print(f"Когда был выход данной версии бота: {self.data_version}")
                elif команда == "/time":
                  time_now = datetime.datetime.now()
                  print(f"Текущее время: {time_now.hour:02}:{time_now.minute:02}:{time_now.second:02}")
                elif команда == "/data":
                  time_now = datetime.datetime.now()
                  print(f"Текущая дата: {time_now.day}.{time_now.month}.{time_now.year}")
                elif команда == "/my_account_info":
                  self.user_settings_menu()
                elif команда == "/addition":
                  print("Не существует дополнений к данной версии!")
                elif команда == "/whoami":
                  print(f"Вы: {self.current_user}")
                  if self.is_admin:
                    print("Статус: Администратор")
                  else:
                    print("Статус: Обычный пользователь")
                elif команда == "/exit_command":
                  print("Выхожу из терминала")
                  break
                else:
                    raise NotFoundFunctionError(команда)
                
            except NotFoundFunctionError as elliot_bot_robot:
                print(f"Возникла ошибка: {elliot_bot_robot}")
                print("Попробуйте ввести команду из списка с помощью вызова /help")

    def check_menu(self):
        """Проверка email и телефонов"""
        print("\nПроверка:")
        
        while True:
            print("\nЧто нужно?")
            for i, option in enumerate(self.under_commands["Проверка"], 1):
                print(f"{i}. {option}")
        
            выбор = input("Твой выбор (1-3): ").strip()
        
            if выбор == "1":
                user_email_check = input("Введите почту для проверки: ")
                
                if ElliotFunc.validate_email(user_email_check): 
                    print("Email корректный")
                else:
                    print("Email некорректный")
            
            elif выбор == "2":
                print("Введите номер телефона для проверки")
                print("Формат: +7-XXX-XXX-XX-XX")
                proverka_number = input('> ')
            
                pattern = re.compile(r"^\+7-\d{3}-\d{3}-\d{2}-\d{2}")
            
                if pattern.match(proverka_number):
                    print("Номер записан правильно!")
                else:
                    print("Номер записан не правильно!")
        
            elif выбор == "3":
                print("Выхожу из функции проверки")
                break
        
            else:
                print("Неверный выбор! Введите 1, 2 или 3")
                continue
    def elliot_bot_robot_ai(self):
        #Не настоящий ИИ, но является чатом 
        #Команды или запросы ограничены
        base_command = {
            "Привет": "Привет, я Эллиот Бот Робот AI!",
            "Как дела?": "Хорошо, а у тебя",
            "Как дела": "Хорошо, а у тебя",
            "У меня хорошо": "Это хорошо, хочешь расскажу о себе?",
            "Расскажи": "Я молодой проект, в котором есть есть некая защита данных (хэшированные пароли и тд), имею базу данных SQLite.\nСоздатель данной программы собирается добавить куча новых фишек, которые сделают данную программу интересней и полезней!",
            "Расскажи о защите данных": "В данной программе есть защита. Есть хэширование паролей, которые отправляются в хэшированном виде в базу данных.\nДанный метод немного уменьшит шанс кражи паролей",
            "Расскажи о базе данных": "В данной программе есть база данных SQLite. В прошлых версиях бота была JSON, но она хуже чем SQLite, потому что она не является базой данных, а просто файлом и ещё SQLite имеет больше возможностей!",
            "Как помочь проекту": "На данный момент только советами и рекомендациями по будущему развитию",
            "Как помочь автору": "На данный момент только советами и рекомендациями по будущему развитию проектов",
            "О разработчике": "Разработчик: Alexx-coder или alex, Почта: alexx-coder@internet.ru",
            "О Elliot Bot Robot AI": "На данный момент, есть только команды заданный разработчиком для чата. Если по подробнее: Нет такого что Пользователь может справшивать что угодно и получать ответ. Да в будущем может будет встроенный AI от OpenAi, Google и тд, поиск в интернет, прогноз погоды и море чего",
            "Пока": "Пока, если захочешь что то спросить заходи сюда!",
            "Пока!": "Пока, если захочешь что то спросить заходи сюда!"
        }

        print("ELLIOT BOT ROBOT AI\n")
        print("Привет, это Бета-версия Elliot Bot Robot AI")

        while True:
            try:
                command_ai = input("Сообщение: ")
                if command_ai in base_command:
                    print("Elliot Bot Robot AI: " + base_command[command_ai])

                    if command_ai == "Пока" or command_ai == "Пока!":
                        break

                else:
                    raise NotFoundCommandAI(command_ai)

            except NotFoundCommandAI as elliot_bot_robot_ai:
                print(f"Elliot Bot Robot AI: {elliot_bot_robot_ai}")

            except KeyboardInterrupt:
                print("Elliot Bot Robot AI: Диалог завершён пользователем! До свидания!")

            except Exception:
                print("Elliot Bot Robot AI: Произошла ошибка. Попробуйте снова")

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
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password_hash TEXT,
            salt TEXT,
            first_seen TIMESTAMP,
            last_seen TIMESTAMP,
            failed_attempts INTEGER DEFAULT 0,
            locked_until TIMESTAMP,
            is_admin INTEGER DEFAULT 0
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
        
        conn.commit()
        conn.close()
        print(f"База данных {self.db_name} с безопасным хэшированием паролей создана")

    def get_or_create_user(self, username):
        # Получить пользователя или создать нового пользователя
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        now = datetime.datetime.now()

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
    
    def register_user(self, username, password, is_admin=False):
        # Безопасная регистрация с безопасным хранением пароля (исправлено название)
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        now = datetime.datetime.now()

        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            print(f"Пользователь {username} уже существует")
            conn.close()
            return False
        
        password_hash, salt = self.hash_password(password)

        cursor.execute("""
        INSERT INTO users (username, password_hash, salt, first_seen, last_seen, is_admin)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (username, password_hash, salt, now, now, 1 if is_admin else 0))
        
        conn.commit()
        conn.close()
        print(f"Пользователь '{username}' зарегистрирован с безопасным хранением пароля")
        return True
    
    def authenticate_user(self, username, password):
        # Безопасная аутентификация пользователя с защитой от брутфорса 
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        now = datetime.datetime.now()

        cursor.execute("""
        SELECT id, password_hash, salt, failed_attempts, locked_until 
        FROM users WHERE username = ?
        """, (username,))

        user = cursor.fetchone()

        if not user:
            print(f"Пользователь '{username}' не найден")
            conn.close()
            return False
        
        user_id, stored_hash, salt, failed_attempts, locked_until = user

        if locked_until:
            # Проверяем, не строковый ли это формат
            if isinstance(locked_until, str):
                lock_time = datetime.datetime.strptime(locked_until, '%Y-%m-%d %H:%M:%S')
            else:
                lock_time = datetime.datetime.fromisoformat(locked_until)
                
            if lock_time > now:
                print(f"Аккаунт заблокирован до {locked_until}")
                conn.close()
                return False
        
        if self.verify_password(password, stored_hash, salt):
            # Успешная аутентификация
            cursor.execute("""
            UPDATE users SET 
                last_seen = ?,
                failed_attempts = 0,
                locked_until = NULL 
            WHERE id = ?
            """, (now, user_id))

            cursor.execute("""
            INSERT INTO security_logs (user_id, action, timestamp, success)
            VALUES (?, ?, ?, ?)
            """, (user_id, "login", now, 1))
            
            conn.commit()
            conn.close()
            print(f"Успешная аутентификация для '{username}'")
            return user_id
        else:
            # Неверный пароль
            failed_attempts = (failed_attempts or 0) + 1
            print(f"Неверный пароль для '{username}' (попытка {failed_attempts})")

            if failed_attempts >= 5:
                lock_until = now + datetime.timedelta(minutes=45)
                cursor.execute("""
                UPDATE users SET 
                    failed_attempts = ?,
                    locked_until = ?
                WHERE id = ?
                """, (failed_attempts, lock_until.strftime('%Y-%m-%d %H:%M:%S'), user_id))
                print(f"Аккаунт заблокирован до {lock_until}")
            else:
                cursor.execute("""
                UPDATE users SET failed_attempts = ? WHERE id = ?
                """, (failed_attempts, user_id))

            cursor.execute("""
            INSERT INTO security_logs (user_id, action, timestamp, success)
            VALUES (?, ?, ?, ?)
            """, (user_id, "failed_login", now, 0))
            
            conn.commit()
            conn.close()
            return False
        



class ElliotBotError(Exception):
    def __init__(self, message="Возникла ошибка"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"[ElliotBot Error] {self.message}"


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



class ElliotFunc():
    def __init__(self):
        # Нормы паролей Elliot_bot 
        self.Elliot_pw_worst = "Данный пароль не рекомендуется для использования"
        self.Elliot_pw_middle = "Данный пароль соответствует минимальным требованиям для постоянного использования"
        self.Elliot_pw_normal = "Данный пароль рекомендуется для постоянного использования"
        
        # Команды для бота
        self.version_bot = "v3.4.robot"
        self.data_version = "13.02.2026"
        
        # Временные переменные
        self.year_now = None
        self.month_now = None
        self.day_now = None
        self.hour_now = None
        self.minute_now = None
        self.second_now = None
        self.greeting = None

    def time(self):
        time_now = datetime.datetime.now()
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
    
# ЗАПУСК БОТА
if __name__ == "__main__":
    try:
        print("Здравствуйте дорогие пользователи!")
        print("Хотим вам представить новую с нуля написанную")
        print("и оптимизированную версию Elliot bot!")
        
        
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
        print("\nElliot Bot Robot завершает работу! До свидания!")
