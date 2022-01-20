# How to run project on local

    !We run this project on Ubuntu 20.04 LTS. If you are using windows you should use windows versions

    First, you need to clone project codes

    $ git clone https://github.com/umutBayraktar/order-processes.git

    Go to the project base directory

    $ cd order-processes
    $ cd order-accept

    Create virtual environment. (We user python version 3.8 in this project)
    $ virtualenv -p python3.8 env

    Activate environment

    $ source env/bin/activate

    Install dependencies

    $ pip install -r requirements.txt

    Go to the project directory

    $ cd order_accept

    Edit .env file for your environment values

    Run django project

    $ python manage.py runserver

# How to run project on Docker

    First, you need to clone project codes
    
    $ git clone https://github.com/umutBayraktar/order-processes.git

    Go to the project directory

    $ cd order-processes
    $ cd order-accept

    Edit .env file for your environment values (.env file in order-processes/order-accept/order_accept/)
    Go to the .env file directory and open it with nano. Change and save it with your environment values

    $ cd order_accept
    $ nano .env

    Turn to the dockerfile path

    $ cd ..
    Create Docker image
    
    ! If you don't have docker please install docker on your machine, first

    Then, build image with command below

    $ docker build -t orderaccept:1.0 .


    $ docker run -it -p 8000:8000 orderaccept:1.0
