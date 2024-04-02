from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import os
import shutil
import requests
import json




def open_tasks(link, path):
    try:
        a = "1" + 1
        # URL файла PDF, который вы хотите скачать
        url = link + "&print=true&pdf=z&sol=true&num=true&ans=true"

        # Путь и имя файла, под которым он будет сохранён локально
        file_path = path + ".pdf"

        if os.path.exists(file_path):
            print(f"существует {file_path}")
        else:
            # Отправка GET-запроса по указанному URL
            response = requests.get(url, timeout=1)

            flag = True
            while flag:
                # Проверка успешности запроса (код состояния 200)
                if response.status_code == 200:
                    # Открытие файла для записи в бинарном режиме и сохранение содержимого
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                    print("скачан", file_path)
                    flag = False
                else:
                    print("Ошибка", response.status_code)
                    time.sleep(30)
                    flag = False
    except:
        try:
            url = link + "&print=true&sol=true&num=true&ans=true"
            file_path = path

            if os.path.exists(file_path + ".pdf"):
                print(f'существует {file_path + ".pdf"}')
            else:
                from selenium import webdriver
                from selenium.webdriver.chrome.options import Options
                from selenium.webdriver.chrome.service import Service

                chrome_options = Options()

                # Указываем, чтобы Chrome использовал "headless" режим (без GUI).
                # chrome_options.add_argument("--headless")

                # Включаем автоматическую печать в PDF без диалоговых окон
                chrome_options.add_argument("--kiosk-printing")

                # Путь к драйверу Chrome
                chrome_driver_path = '/Users/golubev/PycharmProjects/DipLit/chromedriver'

                # Путь для сохранения PDF
                download_folder = file_path

                # Установка пути сохранения с помощью аргументов командной строки
                chrome_options.add_experimental_option('prefs', {
                    'printing.print_preview_sticky_settings.appState': json.dumps({
                        'recentDestinations': [
                            {
                                'id': 'Save as PDF',
                                'origin': 'local',
                                'account': '',
                            }
                        ],
                        'selectedDestinationId': 'Save as PDF',
                        'version': 2
                    }),
                    'savefile.default_directory': download_folder
                })

                # Указание пути к драйверу и добавление опций
                service = Service(executable_path=chrome_driver_path)
                driver = webdriver.Chrome(service=service, options=chrome_options)

                # Переход на страницу, содержимое которой вы хотите распечатать
                driver.get(url)

                # Выполнение JavaScript для открытия окна печати и автоматического сохранения в PDF
                driver.execute_script('return window.print();')

                # Закрытие браузера
                driver.quit()

                # Путь к папке загрузок
                downloads_folder = '/Users/golubev/Downloads'

                # Путь к папке, куда нужно переместить файл
                destination_folder = path

                url = url.split("//")[1]
                # Имя файла, который нужно переместить
                file_name = f'{url}.pdf'.replace("/", '_').replace("?", '_')
                # print(file_name)
                # Полный путь к файлу в папке загрузок
                source_file = os.path.join(downloads_folder, file_name)

                # math-ege.sdamgia.ru_problem_id=29918&print=true.pdf
                # math-ege.sdamgia.ru_problem_id=29918&print=true.pdf

                # Полный путь к месту назначения файла
                destination_file = os.path.join(destination_folder + ".pdf", "")[:-1]

                # Проверяем, существует ли файл в папке загрузок
                if os.path.exists(source_file):
                    # Перемещаем файл
                    shutil.move(source_file, destination_file)
                    print(f"Файл перемещён в {destination_file}")
                else:
                    print(f"Файл не найден: {source_file}")


        except Exception as ex:
            print("пиздец", ex)


def open_tasks_by_topic(link, path):
    driver_path = '/Users/golubev/PycharmProjects/DipLit/chromedriver'

    service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service)

    driver.get(link)

    my_cookies = [{'name': 'exampleName', 'value': 'exampleValue'}]

    for cookie in my_cookies:
        driver.add_cookie(cookie)

    #     driver.refresh()

    time.sleep(5)

    # Прокрутите страницу вниз, используя JavaScript
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        for i in range(0, 10):  # Примерное количество шагов
            driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight/{10}*{i});")
            time.sleep(1)

        # Ожидание загрузки страницы
        time.sleep(2)

        # Расчёт новой высоты прокрутки и сравнение со старой высотой
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    elements_tasks = driver.find_elements(By.CLASS_NAME, 'problem_container')

    for element_task in elements_tasks:

        link_likes_id = element_task.get_attribute("id").split("_")[1]
        link_likes = element_task.find_element(By.XPATH, "//a[text()='Все']").get_attribute("href").split("=")[
                         0] + "=" + link_likes_id

        print("\t\t" + element_task.get_attribute("id"), link_likes)
        try:
            os.makedirs(path + "/" + element_task.get_attribute("id"))
        except:
            pass

        try:
            tasks = driver.find_element(By.ID, f'likes_{link_likes_id}_full').find_elements(By.TAG_NAME, "a")

            print("\t\t\t" + link_likes_id, f"https://math-ege.sdamgia.ru/problem?id={link_likes_id}")
            # os.makedirs(path + "/" + element_task.get_attribute("id") + "/" + link_likes_id)

            open_tasks(link=f"https://math-ege.sdamgia.ru/problem?id={link_likes_id}",
                       path=path + "/" + element_task.get_attribute("id") + "/" + link_likes_id)

            for task in tasks:
                print("\t\t\t" + task.get_attribute("href").split('=')[1], task.get_attribute("href"))
                # os.makedirs(path + "/" + element_task.get_attribute("id") + "/" + task.get_attribute("href").split('=')[1])

                open_tasks(link=task.get_attribute("href"), path=path + "/" + element_task.get_attribute("id") + "/" +
                                                                 task.get_attribute("href").split('=')[1])

        except:
            print("\t\t\t" + link_likes_id, f"https://math-ege.sdamgia.ru/problem?id={link_likes_id}")
            # os.makedirs(path + "/" + element_task.get_attribute("id") + "/" + link_likes_id)

            open_tasks(link=f"https://math-ege.sdamgia.ru/problem?id={link_likes_id}",
                       path=path + "/" + element_task.get_attribute("id") + "/" + link_likes_id)

        # open_tasks_by_likes(link=link_likes, path=path + "/" + element_task.get_attribute("id"))

    driver.quit()


driver_path = '/Users/golubev/PycharmProjects/DipLit/chromedriver'

service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=service)

driver.get('https://math-ege.sdamgia.ru/prob-catalog')

my_cookies = [{'name': 'exampleName', 'value': 'exampleValue'}]

for cookie in my_cookies:
    driver.add_cookie(cookie)

# driver.refresh()

time.sleep(5)

# try:
#     shutil.rmtree('data')
# except:
#     pass


element_topic = driver.find_elements(By.CLASS_NAME, 'Theme-title')  # названия тем
element_topic2 = driver.find_elements(By.CLASS_NAME, 'Theme-children')  # под темы тем

for i in range(2, len(element_topic), 2):
    folder_name = "data/" + element_topic[i].text
    try:
        os.makedirs(folder_name)
    except:
        pass

    try:
        print(element_topic[i].text)

        elems = element_topic2[i].find_elements(By.CLASS_NAME, 'Theme-titlenot')  # ссылка с названием под темы
        for elem in elems:
            print("\t", elem.text, elem.get_attribute("href"))
            try:
                os.makedirs(folder_name + "/" + elem.text)
            except:
                pass
            open_tasks_by_topic(link=elem.get_attribute("href"), path=folder_name + "/" + elem.text)
    except:
        print(element_topic[i].text)

        print("\t", element_topic[i].text.split(".")[0], element_topic[i].get_attribute("href"))

        try:
            os.makedirs(folder_name + "/" + element_topic[i].text.split(".")[0])
        except:
            pass

    print()

driver.quit()
