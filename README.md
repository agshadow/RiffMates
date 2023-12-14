Create Virtual Environment

> python -m venv ./venv
> activate the environment
> (Linux)
> source venv/bin/activate
> or (windows)
> ./venv/Scripts/activate

clone the repository
git clone <repository URL>

install django
(venv) python -m pip instal django

Note if theres is a requirements.txt, install requirements.txt
pip install -r requirements.txt

To generate the requirements.txt
Pip freeze > requirements.txt

run the server
(venv) python manage.py runserver

to migrate database:
python manage.py makemigrations bands
python manage.py migrate

up to page 178 7.2.3
