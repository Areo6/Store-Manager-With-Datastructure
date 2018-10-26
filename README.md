[![Build Status](https://travis-ci.com/Eubule/Store-Manager-With-Datastructure.svg?branch=master)](https://travis-ci.com/Eubule/Store-Manager-With-Datastructure)
[![Coverage Status](https://coveralls.io/repos/github/Eubule/Store-Manager-With-Datastructure/badge.svg?branch=master)](https://coveralls.io/github/Eubule/Store-Manager-With-Datastructure?branch=master)
[![Maintainability](https://api.codeclimate.com/v1/badges/5741cbf4174da77be5bd/maintainability)](https://codeclimate.com/github/Eubule/Store-Manager-With-Datastructure/maintainability)
[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/64a4c747d49e3cc8bc71)

# Store-Manager-With-Datastructure
Store Manager is a web application that helps store owners manage sales and product inventory  records

## Link to Store Manager on Github Pages

[Store Manager](https://eubule.github.io/Strore-Manager/)

## Link to Store-Manage-Using-Datatucture App on Heroku

[Store-Manage-Using-Datatucture](https://store-manager-malaba.herokuapp.com/api/v1/products)

## Routes captured by Store Manager

 REQUEST | ROUTE | FUNCTIONALITY
 ------- | ----- | -------------
 **POST** | /api/v1/products | Admin creates a new product
 **POST** | /api/v1/Sales | Attendant creates new sale records
 **GET** | /api/v1/products | Fetches all products
 **GET** | /api/v1/products/< productId> | Fetches a specific product
 **GET** | /api/v1/sales | Admin fetches all sale records
 **GET** | /api/v1/sales/< productId> | Fetches a specific sale record

 ## BUIlT WITH

 * Flask
 * Python

 ## HOW TO RUN THE APPLICATION

 ### SETING UP THE ENVIRONMENT
 
 1. Clone this repository to your local PC

    **` git clone https://github.com/Eubule/Store-Manager-With-Datastructure.git `** [here](https://github.com/Eubule/Store-Manager-With-Datastructure/)


 2. Create a virtual environment to run application specific dependencies

    **`$ virtualenv venv`**  To create a virtual environment separate from your system

    **`$ source venv/bin/activate`**   To activate you virtual environment

    **`$ pip install flask`**   To install the flask framework that will be used throughout

    **`$ pip freeze > requirements.txt`**   To install requirements useful when hosting the app on a remote server


### RUN THE APP

 1. To run the app

    **` python app.py `**

 2. To run tests

    **`  python -m pytest --cov app/ `**


## AUTHOR

_Malaba MASHAURI Eric_