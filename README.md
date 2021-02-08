1. Все конфигурационные настройки настройки лежат 
в файле .env с переименовать файл ENV/backend/.env_example в .env
   прописать свои настройки для баз данных и smtp сервера
   также для дебага можно включить доп функционал(после включения не забываем про collectstatic и миграции):
    - Silk 
    - DJANGO DEBUG SQL, 
    - DJANGO ADMIN
    - DJANGO DEBUG TOOLBAR
    
2. Для запуска и тестирования преложения сделан файл 
Makefile можно запускать как на linux так и на windows платформах 
   для windows нужно дополнительно установить либу http://getgnuwin32.sourceforge.net/
   для удобства запуска можно оустановить плагин для pycharm https://plugins.jetbrains.com/plugin/9333-makefile-language
   - создаем виртуальное окружение python 3.7
   - прописываем environments в ENV/backend/.env (база, почта)
   - pip install -r  backend/requirements/develop.txt
   - запуск make migrate (или по старинке через manage.py backend/core/manage.py)
   - запуск python backend\core\manage.py my_runserver
     или make run
   - тесты make test
   - провекра кода линтером make code-check
    
