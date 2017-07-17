# Project: Item Catalog
With this project I learned to develop an application that provides a list of items within a variety of categories. Also I learned how to implement a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items.

## Dependencies
In order to be able to run the project you will need to have installed:
 - Python 2.7
 - Virtualenv: https://virtualenv.pypa.io/en/stable/installation/

## Install and Run
1. Install virtualenv if you have not. ```$ [sudo] pip install virtualenv```
2. Clone the source code in your local envarioment
3. Enter to the code directory and create a virtual envarioment. ```virtualenv venv```
4. Activate the virtual envatioment. ```$ . venv/bin/activate```
5. Execute the bash instructions on the installdev file: ```$ . installdev```
6. Now you should be ready to run the server: ```$ flask run```

## Usage
Open the app on http://localhost:5000/

You should be able to see a list of the latest items added as initial data. Also if you are logged you will be able to create new items. To login you will only need a Google account. The first user to login will automaticly become the owner of the preloaded items. 

There are also some api endpoints to get the items data in JSON format.  

- In order to get all categories and their items:
http://localhost:5000/api/v1/catalog

- In order to get only one item with the ID:
http://localhost:5000/api/v1/catalog/item/ITEM_ID

