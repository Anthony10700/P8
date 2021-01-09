## About Project 8
- This deposit concerns project number 8 of openclassrooms you will find below the instructions for the installation the necessary information
- URL HEROKU https://purbeurre-at.herokuapp.com/purbeurre/index.html

## For installation
#### In your terminal : 
* Create a python environment : 
    * `$ pip install virtualenv `
    * `$ virtualenv -p python3 venv` 
    * `$ activate venv` 
* Clone this repository on the same folder with venv
* Install the requirements :
    * `$ pip install -r requirements.txt`
    * install https://www.postgresql.org/ on your os
        * Make data base :
            *   'NAME': 'nutella_platform'
            *   'USER': 'postgres'
            *   'PASSWORD': 'YOUR_PASSWORD' EDIT PASSWORD in nutella_platform\settings.py 145
            *   'HOST': '127.0.0.1'
            *   'PORT': '5432'
* In your terminal go to the root of the repository, then enter :
    * `$ activate venv` 
    * `$ python manage.py migrate`
    * `$ python manage.py import_product 5`
    * `$ python manage.py runserver`

* Go to  http://127.0.0.1:8000/

## Functionality
* You can search for products that are related to the previously imported categories (purbeurre\url_import_openfood.txt)
    * For exemple
        * https://fr.openfoodfacts.org/categorie/boissons-a-la-canneberge.json = boisson
* You can save them and search for substitutes, but you will need to create an account first.

## Example
