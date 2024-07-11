# main.py
from flask import Flask
from routes import app
from functions import create_table

if __name__ == '__main__':
    create_table()
    app.run(debug=True)
