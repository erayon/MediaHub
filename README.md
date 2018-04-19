# MediaHub

![Alt text](figx.png?raw=true "Visualization")

# Installation

## First create the Database
```
git clone repository
cd MediaHub/util
python movie_parser.py

```

## Run the server

```
cd MediaHub/hub
python manage.py runserver 8000 
go to "http://127.0.0.1:8000/myapp/home/"
```


# Note
1. Currenly only work on Linux, not yet implemented for Mac and Windows.
2. If server failed to run do : python manage.py migrate then run the server.