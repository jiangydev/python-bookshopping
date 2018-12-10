#!/usr/bin/python3
# -*- coding: utf-8 -*-
import mysql.connector
from mysql.connector import errorcode


def close_db(cursor, cnx):
    cursor.close()
    cnx.close()


def open_db():
    config = {
        'user': 'root',
        'password': 'toor',
        'host': '127.0.0.1',
        'database': 'pythontest',
        'raise_on_warnings': True
    }
    try:
        return mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
