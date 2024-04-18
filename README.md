# How to install and configure?

You should have python 3.11 or higher installed on your machine.

1) Initialize a virtual environment with the following command:
```bash
python -m venv venv
```

2) Activate the virtual environment

3) Install the dependencies with the following command:
```bash
pip install -r requirements.txt
```

4) Create a .env file in the root of the project with the following content:
```bash
SECRET_KEY=django-insecure-3$0s7naz^y-$yjwx)jjj#dzt0%butv7)rnffz67#_0)lnsgwc@
DB_NAME=heartUp  # Replace this with the name of your database
DB_USER=postgres # Replace this with the user of your database
DB_PASSWORD=12345 # Replace this with the password of your database
DB_HOST=localhost # Replace this with the host of your database
DB_PORT=5432 # Replace this with the port of your database

API_HEART_BEAT_URL=https://hawk-model-dingo.ngrok-free.app/predict_audio
API_UCL_URL=https://a0c9-178-91-253-107.ngrok-free.app/predict
API_ECG_URL=https://3709-178-91-253-107.ngrok-free.app/upload
```
For the database I use PostgreSQL, so you should have it installed and configured on your machine.
Create new database there named heartUp and replace the values of DB_USER, DB_PASSWORD, DB_HOST and DB_PORT with your own values.

5) Run the following command to apply the migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

6) Run the following command to create a superuser:
```bash
python manage.py createsuperuser
```

7) Run the following command to start the server:
```bash
python manage.py runserver
```

8) Access the admin page at http://localhost:8000/admin and login with the superuser credentials created in step 6.
