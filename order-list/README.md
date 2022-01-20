# How to run project on local

    !We run this project on Ubuntu 20.04 LTS. If you are using windows you should use windows versions

    First, you need to clone project codes

    $ git clone https://github.com/umutBayraktar/order-processes.git

    Go to the project base directory

    $ cd order-processes
    $ cd order-list

    Create virtual environment. (We user python version 3.8 in this project)
    $ virtualenv -p python3.8 env-list

    Activate environment

    $ source env-list/bin/activate

    Install dependencies

    $ pip install -r requirements.txt

    Go to the project directory

    $ cd orderlist

    Edit .env file for your environment values

    Create database

    $ python manage.py migrate
    
    Run django project

    $ python manage.py runserver

# How to run project on docker

    First, you need to clone project codes
    
    $ git clone https://github.com/umutBayraktar/order-processes.git

    Go to the project directory

    $ cd order-processes
    $ cd order-list

    Edit .env file for your environment values (.env file in order-processes/order-list/orderlist/)
    Go to the .env file directory and open it with nano. Change and save it with your environment values

    $ cd orderlist
    $ nano .env

    Turn to the dockerfile path

    $ cd ..

    Create Docker image
    
    ! If you don't have docker please install docker on your machine, first

    Then, build image with command below

    $ docker build -t orderlist:1.0 .

    ! In this project we have 3 subprojects. The first one accept order and add it to queue, the seconde one consumes queu and write it to database and this third one (this one) read date from database and represents an API.

    The second one and this project should use the same database. I used sqlite in this project. So you need the bind your common database path to your docker image


    $ docker run -it -p 8000:8000 --mount type=bind,source="$(pwd)"/db.sqlite3,target=/code/orderlist/db.sqlite3 orderlist:1.0

    Also this project reads some constanst from .env file. If you want to change it you need to change this file and build and run again. Also you can bing environment variables with run command or you can use better tools like compose or k8s

