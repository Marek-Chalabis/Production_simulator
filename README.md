# production_simulator
Project production_simulator is a fully functional Web aplication that allows to manage projects, employees and tools of production, it also allows to add informations(posts) for others.

Project is separeted into three major moduls;
1. Using Python to create a logical DB(PostgreSQL) for project
2. Using Django to display and handle interactions between DB and users
3. Make it live using Heroku+AWS
 
From the beginning the project had assumptions to be made such as:
- DB should be random and logical (imitate real production)
- DB needs to be created autmaiclly and easy to created 
- Django should connect to created DB and get informations from there
- Setup for project should be as easy as posible, with all neceserry instrucitons
- for each of the moduls there will be instrucitons how to run it

To make it work start by:
1. Run this pip install (run as administrator):
	python -m pip install --upgrade pip 
	pip install numpy psycopg2 PyPDF2 requests selenium django django-crispy-forms django-filter django-bootstrap-form django-phonenumber-field phonenumbers  Pillow 
	install Chrome + webdriver (https://www.youtube.com/watch?v=dz59GsdvUF8)
2. Run Create_DB_PostgreSQL and choose 999, follow the instructions

*There are 3 folders in respository:
- Random DB - with created DB (
I encourage you to make your own by: Create_DB_PostgreSQL)
- TEST(localhost) - to set up project on your local sever
- PRODUCTION(AWS+HEROKU) - to deploy project 

!!! If you want to see this project online please let me know(project is offline due to the limits on AWS)!!!
https://productionsimulator.herokuapp.com/
You can login as a superuser:
USERNAME - admin
PASSWORD - admin
or as any user created like:
PRODUCTION(AWS+HEROKU)->users_informations.txt
