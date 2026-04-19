import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret!'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://phpmyadmin:ridhotri123@localhost/absensi'
    SQLALCHEMY_TRACK_MODIFICATIONS = False