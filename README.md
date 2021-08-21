## Run
    $ cp .env.example .env
    $ pip3 install -r requirements.txt
    $ python3 manage.py makemigrations
    $ python3 manage.py migrate
    $ bash change_base_url.sh <domain_name>
    $ python manage.py set_telegram_webhook -n
