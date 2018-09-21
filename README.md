# RESTFUL API with Flask

SUTD ISTD Term 6 Networks Exercise
We are to create a RESTFUL API with Flask using 3 verbs and 2 nouns
In my version, I created GET, POST, PUSH, EXIT, NOTE, SIZE

## Getting Started

Run the following
```
$ git clone https://github.com/junqingchang/sei-rest
```

### Installing

Install [Mongodb](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-os-x/)
Install python libraries
```
$ pip3 install Flask
$ pip3 install Flask-PyMongo
```

## Usage

Run the following
```
$ cd sei-rest
$ python3 lab2v2.py
```
Run in another terminal
```
$ sudo mongod
```
Run in another terminal
```
$ curl -X GET localhost:5000
$ curl -X POST -d '{"user":"admin", "pass":"admin"}' -H "Content-Type: application/json" localhost:5000
$ curl -X GET localhost:5000/msgboard/
$ curl -X SIZE localhost:5000/msgboard/
$ curl -X NOTE -d '{"message":"welcome to messageboard"}'  -H "Content-Type: application/json" localhost:5000/msgboard/1
$ curl -X GET localhost:5000/msgboard/1
$ curl -X SIZE localhost:5000/msgboard/
$ curl -X DELETE localhost:5000/msgboard/1
$ curl -X SIZE localhost:5000/msgboard/
$ curl -X NOTE -d "New Message" -H "Content-Type: text/plain" localhost:5000/msgboard/1
$ curl -X GET localhost:5000/msgboard/1
$ curl -X SIZE localhost:5000/msgboard/
$ curl -X DELETE localhost:5000/msgboard/1
$ curl -X EXIT localhost:5000/logoutpage
```

## Built With

* [python3](https://www.python.org/) - Language
* [Flask](http://flask.pocoo.org/)
* [Flask-PyMongo](https://flask-pymongo.readthedocs.io/en/latest/)
* [MongoDB](https://www.mongodb.com/) - Database

## Authors

* **Chang Jun Qing**

## Acknowledgments

* Google our best friend
