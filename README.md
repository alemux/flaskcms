# FlaskCMS - CS50

Hi guys, this is my little FlaskCMS made up for the CS50 Final Project.
With this little CMS, that you can download and modify and use at your disposal, you can:  

  - Manage Pages, creating automatically a nav menu
  - Manage blog Posts
  - Manage Users (Admins, Editors and Bloggers)
  
# Repo

Official Repo URL: https://github.com/alemux/flaskcms

# Database

  - It use a simple (too simple :|) Sqlite: move to MySQL asap

# To Do

  - Pages need to have their own photogallery and attachments list: integrate a multiple upload
  - Database: move to MySQL!
  - Statistics
  - Sharing buttons
  - Some page parts are still fixed in templates: this must be corrected and configured in db


### Installation

If you need to make a clean installation of Flask, I followed these steps:
```sh
$ mkdir project
$ cd project
```
You have to create a VirtualEnvironment:
```sh
$ python3 -m venv venv
```
You will notice a new folder, venv, inside your root project folder.
Now you have to activate this VirtualEnvironment, inside which you have to install all dependencies (pay attention to starting dot).
```sh
$ . venv/bin/activate
```
Now you are inside this virtual env: let's install Flask and all the stuff
```sh
$ pip install Flask
```
Just list all your required modules inside a "requirements.txt"
```sh
$ pip3 install -r requirements.txt
$ pip3 freeze > requirements.txt
```
With freeze we write inside requirements.txt which version of every bundle we need.

If you run "flask", you can understand which commands it waits: 
Don't forget to say to Flask your application name: in my case, is application.py.
```sh
export FLASK_APP=application.py
```

License
----

MIT License: use as you like. Please feel free to contribute as you can! For any information, please write to amussini@gmail.com, I'll be pleased to help as I can.
