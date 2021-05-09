# SJSU CMPE 226 Spring2021TEAM5
import mysql.connector
from utils.auth_checker import auth_checker

cnx = mysql.connector.connect(user='root', password='54802336a',
                              host='127.0.0.1',
                              database='cmpe226_project2_online_education')
