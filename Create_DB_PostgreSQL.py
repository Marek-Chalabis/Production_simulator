#  -*- coding: utf-8 -*-
#  Program fills and create random DB/tables/records for DB
# creates dummy posts for django website in json file(under specifications)
# creates random users with different pics (using selenium)
# specify parameters for different actions!!!
import Random_generator
import numpy
import math
import datetime
import time
import psycopg2
import csv
import PyPDF2
import requests
import os
import string
import random
import json
import shutil
import urllib.request
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
# fill with correct data to establish connection to server
HOST = 'localhost'
USER = 'postgres'
PASSWORD = 'admin'
PORT = '5432'
NAME_DB = 'production_simulator_db'
# True - NAME_DB will be recreated (DROP and CREATE) False - DB already exists
DB_RESET = True

# ------------------------------CREATE DATABASE--------------------------------
# Fill the DATA
NUMBER_OF_TOOLS = 3000
NUMBER_OF_PROJECTS = 75
NUMBER_OF_EMPLOYEES = 200
BASE_SALARY_PER_HOUR = 20
# leave first variable in LIST_PRODUCER, still you can add others producers
LIST_PRODUCER = ['Unsupported Producer', 'Fanar', 'YG-1', 'GMG', "Ceratizit", 'Guhring']
# LIST_OF_POSITIONS needs to be 4 variable(to add more change class logic Positions), you can change job positions
LIST_OF_POSITIONS = ['Junior - operator', 'Mid - operator', 'Senior - operator', 'specialist - operator']
# name for magazine
MAGAZINE = 'STORAGE'
# SPECIFICATION for db
assert NUMBER_OF_TOOLS > NUMBER_OF_PROJECTS, "NUMBER_OF_PROJECTS should be less then NUMBER_OF_TOOLS"
assert NUMBER_OF_TOOLS > NUMBER_OF_EMPLOYEES, "NUMBER_OF_EMPLOYEES should be less then NUMBER_OF_TOOLS"
assert NUMBER_OF_PROJECTS > 0, 'NUMBER_OF_PROJECTS needs to be more then 0'
assert NUMBER_OF_EMPLOYEES > 0, 'NUMBER_OF_EMPLOYEES needs to be more then 0'

# -------------------------------CREATE DUMMY DATA FOR WEBSITE --------------------------------------------
# number of information (posts) separated to all active users
NUMBER_OF_INFORMATION_posts = 1000
# table name in PostgreSQL for information (posts)
TABLE_NAME_FOR_INFORMATION = 'informations_showinformations'

# -------------------------------ADD USERS--------------------------------------------------
# url for create/update users
URL = 'http://127.0.0.1:8000/'
# number of users to add
NUMBER_OF_USERS_TO_ADD = 20
# name of directory to save profile pics
DIRECTORY = 'profile_pics'
# number of different pics to use for users
NUMBER_OF_PICS = 20
# theme for pics
THEME = 'Cats'
# number of branches in production simulation->users->models->Profile->branch
NUMBER_OF_BRANCHES = 5


class CreateTool:
    # Creates tools and insert then into DB

    table_name_tools_info = 'tools'

    def __init__(self, number_of_tools):
        # create specific tool
        if DB_RESET:
            CreateTool.__create_table_tools()

        for i in range(number_of_tools):
            self.producer = random.randint(1, len(LIST_PRODUCER))
            self.material = random.choice(['VHM', 'HSS', 'HSS-E'])
            self.geometry = random.choice(['Square', 'Ball', 'Corner radius'])
            self.diameter = random.choice(list
                                          (x for x in (list(round(i, 2) for i in
                                                            numpy.arange(4, 16, 0.2)))
                                           if int(x) % 2 == 0))  # diameter needs to be even before comma
            self.length = 5 * round((
                                        random.choice(
                                            list(x for x in range(25, 80))))
                                    / 5)  # length must be int and be able to return 0 from length % 51
            self.radius = self.__radius_of_tool()
            self.shank = math.ceil(self.diameter)
            self.compensation = round(random.choice
                                      ((list(x for x in
                                             numpy.arange(0, 0.5, 0.01)))  # compensation cannot be more then 0.5
                                       ), 2)
            self.work_length = self.__work_length_tool()
            self.status = self.__status_of_tool()
            self.date = RandomInformation.give_random_date("1/1/2016")
            self.price = random.choice(list(x for x in numpy.arange(20, 150, 0.5)))
            self.project = random.randint(1, NUMBER_OF_PROJECTS)
            CreateTool.fil_tools(self)
            CreateTool.__show_tool(self, i)

    def __radius_of_tool(self):
        # function returns radius of tool depends of there geometry
        if self.geometry == 'Corner radius':
            return round(random.choice
                         (list(numpy.arange(0.2,
                                            ((self.diameter * 0.8) / 2),
                                            0.2))
                          ), 2)
        elif self.geometry == 'Square':
            return 0
        elif self.geometry == 'Ball':
            return self.diameter / 2

    def __work_length_tool(self):
        # returns working length of tool, difference between work length and length of tool CANNOT be less then 20
        # length of working part CANNOT be less then 5
        temp_work = int(random.choice([1, 2, 3, 5, 7]) * self.diameter)
        while True:
            if temp_work < 5:
                temp_work += 1
            elif ((self.length - temp_work) >= 20) and (temp_work < self.length):
                return temp_work
            else:
                temp_work -= 1

    def __status_of_tool(self):
        # returns status of tool depends of compensation
        if self.compensation < 0.3:
            return "Can be use"
        if 0.3 <= self.compensation <= 0.45:
            return "Needs sharpening"
        if self.compensation > 0.45:
            return 'Utilize the tool'

    def __show_tool(self, i):
        # presents information about tools
        print('Number of tools:{:5}'
              '\tDiameter(fi): {:12}'
              '\tMaterial {:8}'
              '\tGeometry: {:15}'
              '\tProducer: {:8}'
              '\tDate of purchase: {:12}'
              '\tStatus: {:15}'
              '\nTool length: {:8}'
              '\tWorking part length: {:5}'
              '\tTool radius: {:5}'
              '\tShank diameter: {:8}'
              '\tCompensation: {:5}'
              '\tPrice : {:5}'
              '\tproject : {:5}'.format
              (i + 1, self.diameter, self.material, self.geometry,
               self.producer, self.date, self.status, self.length,
               self.work_length, self.radius, self.shank, self.compensation, self.price, self.project))
        print('-' * 150)

    @classmethod
    def __create_table_tools(cls):
        cur.execute('''DROP TABLE IF EXISTS {};'''.format(cls.table_name_tools_info))
        cur.execute('''CREATE TABLE {} (
          tool_id BIGSERIAL NOT NULL PRIMARY KEY,
          geometry varchar(20)  NOT NULL CHECK (geometry = 'Square' OR geometry = 'Ball' OR geometry = 'Corner radius'),
          material varchar(20) NOT NULL CHECK(material = 'VHM' OR material =  'HSS' OR material =  'HSS-E'),
          diameter_mm NUMERIC(5, 2) NOT NULL DEFAULT 0,
          shank_diameter_mm NUMERIC(3, 1) NULL,
          tool_radius_mm NUMERIC(5, 2) NULL CHECK (tool_radius_mm >= 0),
          tool_length_mm NUMERIC(5, 2)  NULL CHECK (tool_length_mm > 0),
          working_part_length_mm NUMERIC(5, 1) NULL CHECK (working_part_length_mm > 0),
          compensation_mm FLOAT  NULL CHECK (compensation_mm >= 0),
          producer_id INT NOT NULL,
          status varchar(20) NOT NULL,
          price NUMERIC(8, 2) NOT NULL CHECK (price > 0),
          date_of_purchase DATE NOT NULL DEFAULT CURRENT_DATE,
          project_id INT NOT NULL
          );
        '''.format(cls.table_name_tools_info))
        con.commit()

    @classmethod
    def fil_tools(cls, self):
        cur.execute('''
        INSERT INTO {}(
        geometry, material, diameter_mm,
        shank_diameter_mm, tool_radius_mm, tool_length_mm,
        working_part_length_mm, compensation_mm, producer_id, status,
        price, date_of_purchase,
        project_id) 
        VALUES (
        '{}', '{}', {},
        {}, {}, {},
        {}, {}, '{}', 
        '{}', {}, '{}',
        {}
        )'''.format(cls.table_name_tools_info,
                    self.geometry, self.material, self.diameter,
                    self.shank, self.radius, self.length,
                    self.work_length, self.compensation, self.producer,
                    self.status, self.price, self.date,
                    self.project))
        con.commit()


class Producers:
    # creates and fills table

    table_producer_name = 'producers'

    def __init__(self):
        if DB_RESET:
            Producers.create_table_producers()

            for producer in LIST_PRODUCER:
                cur.execute('''
                            INSERT INTO {}(
                            producer_name,
                            contact_person,
                            phone_number,
                            email,
                            rabat,
                            delivery_time_days) 
                            VALUES (
                            '{}',
                            '{}',
                            '{}', 
                            '{}',
                            {},
                            '{}'
                            )'''.format(Producers.table_producer_name,
                                        producer,
                                        " ".join(RandomInformation.give_name_and_last_name()),
                                        RandomInformation.give_phone_number(),
                                        RandomInformation.give_email_address(),
                                        random.choice(list(x for x in numpy.arange(5, 50, 0.1))),
                                        Producers.__delivery_time_days()
                                        ))
                con.commit()
            # sets parameters to 0 for unsuported producer
            cur.execute('''UPDATE {} SET
            contact_person = '{}',
            rabat = {},
            delivery_time_days = {} 
            WHERE producer_id  = 1;'''.format(Producers.table_producer_name,
                                             'Foreman',
                                             0,
                                             0))
            con.commit()

    @classmethod
    # create table
    def create_table_producers(cls):
        cur.execute('''DROP TABLE IF EXISTS {};'''.format(cls.table_producer_name))
        cur.execute('''CREATE TABLE {} (
                  producer_id SERIAL NOT NULL PRIMARY KEY,
                  producer_name VARCHAR(30) UNIQUE NOT NULL,
                  contact_person VARCHAR(50) NOT NULL,
                  phone_number VARCHAR(50) NOT NULL,
                  email VARCHAR(50),
                  rabat NUMERIC(4, 2) NOT NULL,
                  delivery_time_days VARCHAR(15) NOT NULL
                  );
                '''.format(cls.table_producer_name))
        con.commit()

    @classmethod
    def __delivery_time_days(cls):
        # creates delivery time
        start = random.randint(1, 5)
        end = start + random.randint(1, 5)
        return str(start) + '-' + str(end)


class Projects:
    # create table and fills it with information

    list_of_projects_names = []
    table_projects_name = 'projects'

    def __init__(self, number_of_projects):

        if DB_RESET:
            Projects.__create_table_projects()

        for i in range(number_of_projects):
            name = RandomInformation.give_random_number_of_words(1).capitalize()
            while name in Projects.list_of_projects_names:
                name = RandomInformation.give_random_number_of_words(1).capitalize()
            self.name = name
            self.time_for_project = random.randint(30, 150)
            self.profit = random.randint(1000, 50000)
            Projects.list_of_projects_names.append(self.name)
            cur.execute('''INSERT INTO {}(
                        project_name,
                        time_for_project_hours,
                        profit)
                        VALUES (
                        '{}',
                        {},
                        {}
                        )'''.format(Projects.table_projects_name,
                                    self.name,
                                    self.time_for_project,
                                    self.profit))
            con.commit()
        cur.execute('''UPDATE {} SET project_name  = '{}', 
        time_for_project_hours = 0, profit=0 WHERE project_id  = 1;'''.format(Projects.table_projects_name, MAGAZINE))
        con.commit()

    @classmethod
    def __create_table_projects(cls):
        # creates a table
        cur.execute('''DROP TABLE IF EXISTS {};'''.format(cls.table_projects_name))
        cur.execute('''CREATE TABLE {} (
                          project_id SERIAL NOT NULL PRIMARY KEY,
                          project_name VARCHAR(30) UNIQUE NOT NULL,
                          time_for_project_hours NUMERIC(8, 2),
                          profit NUMERIC(8, 2) NOT NULL 
                          );
                          '''.format(cls.table_projects_name))
        con.commit()


class Employees:
    # create and fills table

    table_name_emploees = 'employees'

    def __init__(self, number_of_employees):
        if DB_RESET:
            Employees.__create_table_employes()

        for i in range(number_of_employees):
            first_name, last_name = RandomInformation.give_name_and_last_name()
            cur.execute('''INSERT INTO {}(
                        first_name, last_name,
                        email, phone_number,
                        position_id, date_of_employment)
                        VALUES (
                        '{}', '{}',
                        '{}', '{}',
                        {},
                        '{}'
                        )'''.format(Employees.table_name_emploees,
                                    first_name, last_name,
                                    RandomInformation.give_email_address(), RandomInformation.give_phone_number(),
                                    int(
                                        str(random.choices(
                                            population=list(x for x in range(1, len(LIST_OF_POSITIONS) + 1)),
                                            weights=[0.5, 0.3, 0.15, 0.05]
                                        )).replace('[', '').replace(']', "")),
                                    RandomInformation.give_random_date("1/1/1990")))
            con.commit()

    @classmethod
    def __create_table_employes(cls):
        # create table
        cur.execute('''CREATE EXTENSION IF NOT EXISTS "uuid-ossp";''')
        cur.execute('''DROP TABLE IF EXISTS {};'''.format(cls.table_name_emploees))
        cur.execute('''CREATE TABLE {} (
                    uuid_employee uuid DEFAULT uuid_generate_v4() NOT NULL,
                    first_name VARCHAR(30) NOT NULL,
                    last_name VARCHAR(30) NOT NULL,
                    email VARCHAR(50),
                    phone_number VARCHAR(30),
                    position_id SERIAL NOT NULL,
                    date_of_employment DATE NOT NULL           
                    );'''.format(cls.table_name_emploees))
        con.commit()


class Position:
    # create and fill table

    table_name_positions = 'positions'

    def __init__(self):
        if DB_RESET:
            Position.__create_table_positions()
            for position in LIST_OF_POSITIONS:
                cur.execute('''INSERT INTO {}(
                            position_name,
                            hourly_rate)
                            VALUES (
                            '{}',
                            {}
                            );'''.format(Position.table_name_positions,
                                         position,
                                         BASE_SALARY_PER_HOUR * (1 + LIST_OF_POSITIONS.index(position) * 0.3)))
                con.commit()

    @classmethod
    def __create_table_positions(cls):
        # create table
        cur.execute('''DROP TABLE IF EXISTS {};'''.format(cls.table_name_positions))
        cur.execute('''CREATE TABLE {} (
                    position_id  SERIAL,
                    position_name VARCHAR(30) NOT NULL UNIQUE,
                    hourly_rate FLOAT NOT NULL           
                    );'''.format(cls.table_name_positions))
        con.commit()


class EmployeesInProject:
    # create and fill table

    table_name_employees_projects = 'employees_in_projects'

    def __init__(self):
        if DB_RESET:
            EmployeesInProject.__create_table_for_employes_in_use()

        list_of_employees = EmployeesInProject.__get_employees()
        list_of_projects_id = list(x for x in range(1, NUMBER_OF_PROJECTS + 1))

        for project in list_of_projects_id:
            if project == 1:
                continue
            list_with_no_duplicate_employees = list_of_employees.copy()
            random.shuffle(list_with_no_duplicate_employees)
            number_of_empolyees_in_projects = random.randint(1, int(NUMBER_OF_EMPLOYEES / 3))

            for y in range(number_of_empolyees_in_projects):
                cur.execute('''INSERT INTO {}(
                               uuid_employee,
                               project_id)
                               VALUES (
                                       '{}',
                                       {}
                                        );'''.format(
                    EmployeesInProject.table_name_employees_projects,
                    list_with_no_duplicate_employees.pop(),
                    project))
                con.commit()

    @classmethod
    def __create_table_for_employes_in_use(cls):
        # create table
        cur.execute('''DROP TABLE IF EXISTS {};'''.format(cls.table_name_employees_projects))
        cur.execute('''CREATE TABLE {} (
                    connection_id  BIGSERIAL NOT NULL PRIMARY KEY,            
                    uuid_employee uuid NOT NULL,
                    project_id SERIAL NOT NULL         
                    );'''.format(cls.table_name_employees_projects))
        con.commit()

    @classmethod
    def __get_employees(cls):
        # return random list of employees
        cur.execute('SELECT uuid_employee FROM employees')
        info = cur.fetchall()
        list_empl = []
        for row in info:
            for x in row:
                list_empl.append(x)
        random.shuffle(list_empl)
        return list_empl


class RandomInformation:
    # creates random multi - table information

    male_names = []
    female_names = []
    male_last_name = []
    female_last_name = []
    domains = []
    url_names = 'http://postgresql.cba.pl/wp-content/uploads/2016/03/imiona_pl.csv'
    url_last_name = 'http://d.polskatimes.pl/k/r/1/1f/d0/54d365ec8ea5d_z.pdf'
    url_domains = 'https://gist.github.com/tbrianjones/5992856/raw/93213efb652749e226e69884d6c048e595c1280a/' \
                  'free_email_provider_domains.txt'
    list_of_free_tools = []

    @staticmethod
    def give_name_and_last_name():
        # returns name and last name
        gender = random.choice(['M', 'F'])
        last_name = RandomInformation.__give_last_name(gender)
        first_name = Random_generator.Person.first_name(gender)
        return first_name, last_name

    @staticmethod
    def give_phone_number():
        # returns random phone number
        phone_number = []
        for x in range(3):
            part = random.randint(100, 999)
            phone_number.append(str(part))
        phone_number = ''.join(phone_number)
        phone_number = '+48' + phone_number
        return phone_number

    @staticmethod
    def give_email_address():
        # returns full email address
        if len(RandomInformation.domains) == 0:
            RandomInformation.__get_domains()
        return RandomInformation.__random_email_name() + '@' + random.choice(RandomInformation.domains)

    @staticmethod
    def give_free_tool():
        # return free tools
        if len(RandomInformation.list_of_free_tools) == 0:
            cur.execute('SELECT tool_id FROM tools')
            info = cur.fetchall()
            for row in info:
                RandomInformation.list_of_free_tools.append(row[0])
                random.shuffle(RandomInformation.list_of_free_tools)
        if len(RandomInformation.list_of_free_tools) <= NUMBER_OF_TOOLS:
            return RandomInformation.list_of_free_tools.pop()

    @staticmethod
    def give_random_date(start):
        # return random date from xxx to now

        def random_date(start_date, end, prop):
            return str_time_prop(start_date, end, '%d/%m/%Y', prop)

        def str_time_prop(start_date, end, format_date, prop):
            s_time = time.mktime(time.strptime(start_date, format_date))
            e_time = time.mktime(time.strptime(end, format_date))
            p_time = s_time + prop * (e_time - s_time)
            return time.strftime(format_date, time.localtime(p_time))

        date = random_date(start, datetime.date.today().strftime("%d/%m/%Y"), random.random())
        day, month, year = str(date).split(r'/')
        return year + '-' + month + '-' + day

    @staticmethod
    def give_random_number_of_words(number):
        # create random "word" for email address
        expresion = ''
        for i in range(number):
            word_length = random.randint(1, 15)
            letters = string.ascii_lowercase
            word = ''.join(random.choice(letters) for _ in range(word_length))
            expresion += word + ' '
        return expresion[:-1]

    @staticmethod
    def give_password(password_length):
        password = random.choice(string.ascii_lowercase) + \
                   random.choice(string.ascii_uppercase) + \
                   random.choice(string.punctuation) + \
                   random.choice(string.digits)

        while len(password) != password_length:
            password = password + random.choice(
                [random.choice(string.ascii_lowercase), random.choice(string.ascii_uppercase),
                 random.choice(string.punctuation), random.choice(string.digits)])
        shufle = list(password)
        random.shuffle(shufle)
        password = ''.join(shufle)
        return password

    @classmethod
    def __give_last_name(cls, gender):
        # returns random last_name arguments needs to be M - male F - female
        if len(cls.male_last_name or cls.female_last_name) == 0:
            cls.__get_last_names()
        if gender == 'M':
            return random.choice(cls.male_last_name).title()
        elif gender == "F":
            return random.choice(cls.female_last_name).title()
        else:
            print('Give correct argument F or M')

    @classmethod
    def __get_last_names(cls):
        # downloads pdf file, formats it and returns list of last names
        response = requests.get(cls.url_last_name)

        temp_file_name = "last_name.pdf"
        with open(os.path.join(os.getcwd(), temp_file_name), 'wb') as f:
            f.write(response.content)

        with open(temp_file_name, 'rb') as f:
            pdf_reader = PyPDF2.PdfFileReader(f)
            new_list = []
            for page in range(pdf_reader.numPages):
                page_obj = pdf_reader.getPage(page)
                text = page_obj.extractText()
                text = text.split('\n')
                for x in text:
                    if x.isupper():
                        new_list.append(x)
            for last_name in new_list:
                if new_list.index(last_name) % 2 == 0:
                    cls.female_last_name.append(last_name)
                else:
                    cls.male_last_name.append(last_name)
        os.remove(temp_file_name)

    @classmethod
    def __get_domains(cls):
        # downloads domains names from txt file
        response = requests.get(cls.url_domains)
        temp_file_name = "domains.txt"

        with open(os.path.join(os.getcwd(), temp_file_name), 'wb') as f:
            f.write(response.content)
        with open(temp_file_name, 'r') as f:
            for line in f.readlines():
                line = line.replace("\n", '')
                cls.domains.append(line)

        os.remove(temp_file_name)

    @classmethod
    def __random_email_name(cls):
        # create random "word" for email address
        name_length = random.randint(5, 15)
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(name_length))


class CreateUsers:
    # PLEASE DONT USE THIS ON HEROKU
    # creates users and updates thiers profile

    list_of_img_paths = []
    username_list = []
    password_list = []

    def __init__(self, number_of_users):
        CreateUsers.__download_img_for_users()
        CreateUsers.__update_profile(number_of_users)
        CreateUsers.__save_users()
        keep = input('Do you want to keep pics? Write "yes" to save')
        if keep.lower() != 'yes':
            shutil.rmtree(DIRECTORY)
            print('Folder was removed ')
        print(f'\n  {number_of_users} - New users have been created and updated')

    @classmethod
    def __download_img_for_users(cls):
        # creates folder if not exists and saves there img
        if os.path.exists(DIRECTORY) is False:
            os.mkdir(DIRECTORY)

        options = Options()
        options.headless = True
        browser = webdriver.Chrome(options=options)
        # website with free images
        browser.get('https://all-free-download.com/')

        browser.find_element_by_id('q_photos').send_keys(THEME)
        browser.find_element_by_xpath('/html/body/div[1]/div/nav[2]/ul/li[2]/form/div/div/div/button/i') \
            .click()
        try:
            for num_pics in range(1, NUMBER_OF_PICS + 1):
                src = browser.find_element_by_xpath(
                    f'/html/body/div[1]/div/div/div[2]/div/div/div[{num_pics}]/a[1]/img') \
                    .get_attribute('src')
                urllib.request.urlretrieve(src, os.path.join(DIRECTORY, f"{num_pics}.jpg"))
        except:
            print(f'There are no more pics at the first page, you downloaded {num_pics} pics with theme - {THEME}')
        browser.close()

        for r, d, f in os.walk(DIRECTORY):
            for files in f:
                if files.endswith('.jpg'):
                    cls.list_of_img_paths.append((os.path.join(os.getcwd(), os.path.join(r, files))))

    @classmethod
    def __update_profile(cls, number_of_users):
        # updates profile if already exists
        browser = Chrome()
        # url to project
        browser.get(URL)
        for i in range(number_of_users):
            # register
            time.sleep(2)
            browser.find_element_by_link_text('Register').click()

            time.sleep(2)
            user = RandomInformation.give_random_number_of_words(1)
            while user in CreateUsers.username_list:
                user = RandomInformation.give_random_number_of_words(1)
            cls.username_list.append(user)
            browser.find_element_by_id('id_username').send_keys(user)

            password = RandomInformation.give_password(9)
            cls.password_list.append(password)
            browser.find_element_by_id('id_password1').send_keys(password)
            browser.find_element_by_id('id_password2').send_keys(password)

            browser.find_element_by_id('id_email').send_keys(RandomInformation.give_email_address())

            first_name, last_name = RandomInformation.give_name_and_last_name()
            browser.find_element_by_id('id_first_name').send_keys(first_name)
            browser.find_element_by_id('id_last_name').send_keys(last_name)
            browser.find_element_by_id('submit-id-submit').click()
            time.sleep(2)
            # log in
            browser.find_element_by_link_text('Login').click()

            time.sleep(2)
            browser.find_element_by_xpath('/html/body/div/div/form/fieldset/div[1]/div/input').send_keys(user)
            browser.find_element_by_id('id_password').send_keys(password)
            browser.find_element_by_xpath('/html/body/div/div/form/div[1]/button[1]').click()

            # go to profile to change branch and profile img
            time.sleep(2)
            browser.find_element_by_xpath('/html/body/nav/div/ul[2]/li[2]/a/img').click()
            browser.find_element_by_xpath('/html/body/nav/div/ul[2]/li[2]/div/a[1]').click()
            browser.find_element_by_id('id_branch').click()
            browser.find_element_by_xpath(f'/html/body/div/div[2]/form/fieldset/div[1]/div/select/option['
                                          f'{random.randint(1, NUMBER_OF_BRANCHES)}]').click()
            browser.find_element_by_id("id_image").send_keys(random.choice(CreateUsers.list_of_img_paths))
            browser.find_element_by_xpath('/html/body/div/div[2]/form/button').click()

            # log out
            time.sleep(2)
            browser.find_element_by_xpath('/html/body/nav/div/ul[2]/li[2]/a/img').click()
            browser.find_element_by_xpath('/html/body/nav/div/ul[2]/li[2]/div/a[2]').click()
        browser.close()

    @classmethod
    def __save_users(cls):
        # saves users informations(username, password)
        with open('users_informations.txt', 'w') as f:
            f.write('USERNAME   :   PASSWORD\n')
            for i in range(len(cls.username_list)):
                f.write(str(i) + '  ' + str(cls.username_list[i]) + '   :   ' +
                        (cls.password_list[i]) + '\n')
            print(f"\nFile with logins and passwords for users was created at:"
                  f"\n{os.getcwd()}")


class MeasureTime:
    # class - context menager, measure time for specific action
    def __init__(self, text):
        self.text = text

    def __enter__(self):
        self.__start = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__stop = time.time()
        self.__time_difrence = self.__stop - self.__start
        print(self.text, '{}'.format(round(self.__time_difrence, 2)), 'seconds')


def connect_to_db(host, user, password, port, name_db):
    # create connection to PostgreSQL
    # create new DB NAME_DB
    # CONNECTION NEEDS TO BE CLOSED OUTSIDE

    try:
        if DB_RESET:
            # drops existing and creates new one
            con = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                port=port,
            )
            cur = con.cursor()
            con.set_isolation_level(0)
            cur.execute('DROP DATABASE IF EXISTS {}'.format(name_db))
            con.commit()
            cur.execute('''CREATE DATABASE {}
                        WITH
                        OWNER = postgres
                        ENCODING = 'UTF8'
                        CONNECTION LIMIT = -1;'''.format(name_db))
            con.commit()
            con.close()

        con = psycopg2.connect(
            database=name_db,
            user=user,
            password=password,
            host=host,
            port=port
        )
        con.set_isolation_level(0)
        cur = con.cursor()
        return con, cur
    except:
        print('There is something wrong with connection, check your variable: HOST, USER, PASSWORD, PORT'
              '\n Or your DB_RESET=True and blocks actions')


def populate_db():

    con, cur = connect_to_db(HOST, USER, PASSWORD, PORT, NAME_DB)

    with MeasureTime('Creating tools took:'):
        CreateTool(NUMBER_OF_TOOLS)

    with MeasureTime('Creating rest of DB took:'):
        Producers()
        Projects(NUMBER_OF_PROJECTS)
        Employees(NUMBER_OF_EMPLOYEES)
        Position()
        EmployeesInProject()
        con.close()


def list_of_active_users():
    # returns list of active users

    con, cur = connect_to_db(HOST, USER, PASSWORD, PORT, NAME_DB)

    cur.execute('SELECT id FROM auth_user')
    users = cur.fetchall()
    list_of_active_users = []

    for row in users:
        list_of_active_users.append(row[0])
    return list_of_active_users


def create_json_file():
    # creates json file with data to manualy update into django informations(posts)
    informations = []
    file_name = 'informations.json'
    list_of_users = list_of_active_users()
    for i in range(NUMBER_OF_INFORMATION_posts):
        informations.append({
            'title': RandomInformation.give_random_number_of_words(random.randint(1, 10)),
            'info': RandomInformation.give_random_number_of_words(random.randint(10, 200)),
            'date_posted': RandomInformation.give_random_date('1/1/2013'),
            'user_id': random.choice(list_of_users)
        })

    with open(file_name, 'w') as outfile:
        json.dump(informations, outfile)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print(f'\nFile with json data was created in this location:\n{dir_path}\\{file_name}')


def create_informations_db(number_of_inf):
    # adds informations(posts) to DB thru PostgreSQL
    list_of_users = list_of_active_users()
    con, cur = connect_to_db(HOST, USER, PASSWORD, PORT, NAME_DB)

    for x in range(number_of_inf):
        cur.execute('''INSERT INTO {}
        (title, 
        info,
        date_posted, 
        author_id
        ) VALUES (
        '{}', 
        '{}',
        '{}',
        {}
        );'''.format(TABLE_NAME_FOR_INFORMATION,
                     RandomInformation.give_random_number_of_words(random.randint(1, 10)),
                     RandomInformation.give_random_number_of_words(random.randint(10, 200)),
                     RandomInformation.give_random_date("1/1/2013"),
                     random.choice(list_of_users)))

        con.commit()
    print(f'    {number_of_inf} - Informations was added')


def remove_users_and_informations():
    # remove users and informations
    con, cur = connect_to_db(HOST, USER, PASSWORD, PORT, NAME_DB)
    cur.execute('TRUNCATE informations_showinformations;'
                'DELETE FROM informations_showinformations;'
                'ALTER SEQUENCE informations_showinformations_id_seq RESTART WITH 1;'
                'TRUNCATE auth_user CASCADE;'
                'DELETE FROM auth_user;'
                'ALTER SEQUENCE auth_user_id_seq RESTART WITH 1;')
    con.commit()

    print('Users and informations was removed'
          '\n!!! REMEMBER TO CREATE SUPERUSER IN DJANGO!!!\n'
          'USE THIS COMMAND IN TERMINAL BEFORE YOU DO ANYTHING ELSE'
          '\n"python manage.py createsuperuser"')


# ----------------------------------------------PROGRAM-----------------------------------
option = input(f"What you want to do?"
               f"\n1-   Create or populate new DATABASE "
               f"WARNING THIS WILL DELETE EXISTING DATABASE OF THIS NAME '{NAME_DB}'"
               f" if DB_RESET=True (At this moment DB_RESET={DB_RESET})"
               f"\n---------------OPTIONS BELOW ONLY AVAILABLE IF YOU MAKE MIGRATIONS IN DJANGO-------------------"
               f"\n2-   Produce dummy date ({NUMBER_OF_INFORMATION_posts} informations(posts))"
               f"\n3-   Add {NUMBER_OF_USERS_TO_ADD} users"
               f"\n4-   Create {NUMBER_OF_USERS_TO_ADD} new users and {NUMBER_OF_INFORMATION_posts} "
               f"informations(posts)"
               f"\n5-   Remowe all users and informations-posts "
               f"(and restart auto_id for users and informations(posts))\n"
               f""
               f"\n999- Choose, if this is your first run")

if int(option) == 1:
    if DB_RESET:
        warning = input("\nAre you completly sure?\n(write -create- to make new DB)\n")
        if warning.lower() == 'create':
            populate_db()
    else:
       populate_db()

elif int(option) == 2:
    choice = input('\nHow you wanna add informations(posts) to the DB?'
                   '\n1-     Manual thru JSON file'
                   '\n2-     Automatically thru PostgeSQL'
                   '(check if the table name for informations = {})\n'.format(TABLE_NAME_FOR_INFORMATION))
    if int(choice) == 1:
        create_json_file()
    elif int(choice) == 2:
        create_informations_db(NUMBER_OF_INFORMATION_posts)

elif int(option) == 3:
    CreateUsers(NUMBER_OF_USERS_TO_ADD)

elif int(option) == 4:
    CreateUsers(NUMBER_OF_USERS_TO_ADD)
    create_informations_db(NUMBER_OF_INFORMATION_posts)

elif int(option) == 5:
    decision = input("Are you sure you want to remove users and informations(posts)?"
                     "\nWrite 'remove' to continue\n")
    if decision.lower() == 'remove':
        remove_users_and_informations()

elif int(option) == 999:
    print('Check your connections at the top of the file')
    DB_RESET = True

    step = input('write "next" to continue')
    while step.lower() != 'next':
        step = input('write "next" to continue')

    print(f'Now DB of the name: "{NAME_DB}" will be created')

    step = input('write "next" to continue')
    while step.lower() != 'next':
        step = input('write "next" to continue')

    con, cur = connect_to_db(HOST, USER, PASSWORD, PORT, NAME_DB)

    with MeasureTime('Creating tools took:'):
        CreateTool(NUMBER_OF_TOOLS)

    with MeasureTime('Creating rest of DB took:'):
        Producers()
        Projects(NUMBER_OF_PROJECTS)
        Employees(NUMBER_OF_EMPLOYEES)
        Position()
        EmployeesInProject()
        con.close()
    print('\nCreate virtual environment and copy production_simulator(from  folder TEST_localhost) there'
          '\nChange directory to production_simulator'
          '\nMake connection to created DB production_simulator->settings DATABASES'
          '\nRun this commands in terminal'
          '\n1 - python manage.py makemigrations'
          '\n2 - python manage.py migrate erp --fake'
          '\n3 - python manage.py migrate'
          '\n3 - python manage.py createcachetable'
          '\n4 - python manage.py createsuperuser'
          '\n5 - python manage.py runserver\n'
          '\nAfter you finished all the tasks')

    step = input('write "next" to continue')
    while step.lower() != 'next':
        step = input('write "next" to continue')

    print('Now users will be created'
          '\n Dont do anything after you write "next"')

    step = input('write "next" to continue')
    while step.lower() != 'next':
        step = input('write "next" to continue')

    DB_RESET = False
    CreateUsers(NUMBER_OF_USERS_TO_ADD)
    print('Now informations(posts) will be created')

    step = input('write "next" to continue')
    while step.lower() != 'next':
        step = input('write "next" to continue')

    create_informations_db(NUMBER_OF_INFORMATION_posts)

    print(f'\nCongratulations, Go to your website:'
          f'\n{URL}')
