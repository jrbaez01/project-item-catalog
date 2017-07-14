# Project: Item Catalog
With this project I learned to develop an application that provides a list of items within a variety of categories. Also I learned how to implement a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items.

## Dependencies
In order to be able to run the project you will need to have installed:
 - Python 2.7
 - Virtualenv: https://virtualenv.pypa.io/en/stable/installation/

## How to run
1. Install virtualenv if you have not. ```$ [sudo] pip install virtualenv```
2. Clone the source code in your local envarioment
3. Enter to the code directory and create a virtual envarioment. ```virtualenv venv```
4. Activate the virtual envatioment. ```$ . venv/bin/activate```
5. Execute the bash instructions on the installdev file: ```$ . installdev```
6. Now you should be ready to run the server: ```$ flask run```

Open the app on http://localhost:5000/

A JSON endpoint is located at http://localhost:5000/catalog.json
